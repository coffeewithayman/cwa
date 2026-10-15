"""Work out which diarized speaker is Ayman.

Two independent signals have to agree before a label is trusted:
  1. voice: ECAPA embedding of each speaker vs. Ayman's enrolled voiceprint
  2. context: a solo recording, or the transcript naming Ayman
Anything short of that goes to intake/speakers.md for Ayman to pick.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np

from . import config

NAME_HINTS = ("ayman", "elsawah", "coffee with ayman")


@dataclass
class SpeakerDecision:
    ayman: str | None                      # diarization label, or None if not present
    status: str                            # "auto" | "override" | "solo" | "review" | "absent"
    reason: str
    scores: dict[str, float] = field(default_factory=dict)
    shares: dict[str, float] = field(default_factory=dict)
    segments: list[int] | None = None      # montage only: Ayman's segment indices


@lru_cache(maxsize=1)
def _encoder():
    from speechbrain.inference.speaker import EncoderClassifier
    return EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir=str(config.INGEST_DIR / ".models" / "ecapa"),
        run_opts={"device": config.DEVICE})


def embed(wav: np.ndarray) -> np.ndarray:
    import torch
    with torch.no_grad():
        emb = _encoder().encode_batch(torch.from_numpy(wav).float().unsqueeze(0).to(config.DEVICE))
    v = emb.squeeze().cpu().numpy()
    return v / np.linalg.norm(v)


def load_wav(path: Path) -> np.ndarray:
    import whisperx
    return whisperx.load_audio(str(path))


def speaker_turns(diarization: list[dict]) -> dict[str, list[tuple[float, float]]]:
    turns: dict[str, list[tuple[float, float]]] = {}
    for d in diarization:
        turns.setdefault(d["speaker"], []).append((d["start"], d["end"]))
    return turns


def speaker_embedding(audio: np.ndarray, turns: list[tuple[float, float]], max_seconds: float = 90) -> np.ndarray | None:
    """Mean embedding over a speaker's longest clean turns (up to max_seconds)."""
    picked, total = [], 0.0
    for s, e in sorted(turns, key=lambda t: t[1] - t[0], reverse=True):
        if e - s < 2.0 or total >= max_seconds:
            break
        picked.append((s, e))
        total += e - s
    if not picked:
        return None
    vecs = [embed(audio[int(s * 16000):int(min(e, s + 20) * 16000)]) for s, e in picked]
    v = np.mean(vecs, axis=0)
    return v / np.linalg.norm(v)


# --- voiceprint store -----------------------------------------------------------

def voiceprint() -> np.ndarray | None:
    vecs = [np.load(p) for p in sorted(config.VOICEPRINT_DIR.glob("*.npy"))]
    if not vecs:
        return None
    v = np.mean(vecs, axis=0)
    return v / np.linalg.norm(v)


def add_to_voiceprint(name: str, vec: np.ndarray) -> None:
    config.VOICEPRINT_DIR.mkdir(parents=True, exist_ok=True)
    np.save(config.VOICEPRINT_DIR / f"{name}.npy", vec)


def voiceprint_version() -> str:
    return ",".join(sorted(p.stem for p in config.VOICEPRINT_DIR.glob("*.npy")))


# --- decision ---------------------------------------------------------------------

def is_own_channel(info: dict) -> bool:
    fields = " ".join(str(info.get(k) or "") for k in ("channel_url", "uploader_url", "uploader_id", "channel")).lower()
    return any(c.lower().lstrip("@") in fields for c in config.OWN_CHANNELS)


def decide(workdir: Path, transcript: dict, override: str | None, info: dict | None = None) -> SpeakerDecision:
    turns = speaker_turns(transcript.get("diarization", []))
    talk_time = {spk: sum(e - s for s, e in t) for spk, t in turns.items()}
    total = sum(talk_time.values()) or 1.0
    shares = {spk: round(t / total, 3) for spk, t in sorted(talk_time.items())}
    main = {spk for spk, share in shares.items() if share >= config.MIN_SPEAKER_SHARE}

    if override:
        if override == "none":
            return SpeakerDecision(None, "absent", "Ayman marked as not in this recording", shares=shares)
        return SpeakerDecision(override, "override", "picked in intake/speakers.md", shares=shares)

    audio = load_wav(workdir / "audio.wav")
    vecs = {spk: speaker_embedding(audio, turns[spk]) for spk in main}
    np.savez(workdir / "speaker_embeddings.npz", **{k: v for k, v in vecs.items() if v is not None})

    vp = voiceprint()
    scores = {spk: round(float(v @ vp), 3) for spk, v in vecs.items() if v is not None and vp is not None}
    text = " ".join(seg.get("text", "") for seg in transcript.get("segments", [])).lower()
    named = any(h in text for h in NAME_HINTS)
    solo = max(shares.values(), default=0) >= config.SOLO_SHARE
    dominant = max(shares, key=shares.get) if shares else None
    own = is_own_channel(info or {})

    if scores:
        ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        best, best_score = ranked[0]
        margin = best_score - (ranked[1][1] if len(ranked) > 1 else 0.0)
        voice_ok = best_score >= config.VOICE_ACCEPT and margin >= config.VOICE_MARGIN
        context_ok = named or (solo and best == dominant) or (own and best == dominant)
        if voice_ok and context_ok:
            why = "name mentioned" if named else "own channel" if own else "solo recording"
            return SpeakerDecision(best, "auto", f"voiceprint {best_score:.2f} + {why}", scores, shares)
        if best_score < config.VOICE_ABSENT and not named and not own:
            return SpeakerDecision(None, "absent", f"no voice matches Ayman (best {best_score:.2f}) and he isn't named",
                                   scores, shares)
        if best_score < config.VOICE_ACCEPT * 0.6 and not named:
            reason = f"no speaker sounds like Ayman (best {best_score:.2f}) and his name isn't mentioned"
        else:
            reason = f"voiceprint unsure ({', '.join(f'{s} {v:.2f}' for s, v in ranked)}); name mentioned: {'yes' if named else 'no'}"
        return SpeakerDecision(None, "review", reason, scores, shares)

    # No voiceprint enrolled yet: only a clear solo recording (or his own channel) is accepted.
    if own and dominant:
        return SpeakerDecision(dominant, "solo", f"own channel, main voice ({shares[dominant]:.0%})", shares=shares)
    if solo and dominant:
        return SpeakerDecision(dominant, "solo", f"solo recording ({shares[dominant]:.0%} one voice), no voiceprint yet",
                               shares=shares)
    return SpeakerDecision(None, "review", "no voiceprint enrolled yet and more than one voice", shares=shares)


MONTAGE = "AYMAN"   # pseudo speaker label for snippets attributed one by one


def montage_segments(workdir: Path, transcript: dict) -> tuple[list[int], dict[int, float]]:
    """Montages cut many people together in seconds-long snippets, which
    diarization can't separate. Score every snippet against the voiceprint
    instead; returns (Ayman's segment indices, all scores)."""
    audio = load_wav(workdir / "audio.wav")
    vp = voiceprint()
    if vp is None:
        return [], {}
    segs = transcript.get("segments", [])
    scores = {}
    for i, seg in enumerate(segs):
        s, e = seg["start"], seg["end"]
        pad = max(0.0, (1.5 - (e - s)) / 2)          # pad very short snippets to ~1.5 s
        clip = audio[int(max(0.0, s - pad) * 16000):int((e + pad) * 16000)]
        if len(clip) >= 8000:
            scores[i] = round(float(embed(clip) @ vp), 3)
    mine = [i for i, v in scores.items() if v >= config.MONTAGE_ACCEPT]
    for i in sorted(mine):                         # extend to directly following lines, same voice
        j = i + 1
        while (j < len(segs) and scores.get(j, -1) >= config.MONTAGE_CONTINUE
               and segs[j].get("speaker") == segs[i].get("speaker") and segs[j]["start"] - segs[j - 1]["end"] < 1.5):
            mine.append(j)
            j += 1
    return sorted(set(mine)), scores


def write_samples(workdir: Path, transcript: dict) -> dict[str, str]:
    """A 10 s clip + quote per speaker so Ayman can pick himself in speakers.md."""
    turns = speaker_turns(transcript.get("diarization", []))
    talk_time = {spk: sum(e - s for s, e in t) for spk, t in turns.items()}
    total = sum(talk_time.values()) or 1.0
    out_dir = workdir / "samples"
    out_dir.mkdir(exist_ok=True)
    samples = {}
    for spk, t in sorted(turns.items()):
        if talk_time[spk] / total < config.MIN_SPEAKER_SHARE:
            continue
        s, e = max(t, key=lambda x: x[1] - x[0])
        start = s + max(0.0, (e - s - 10) / 2)
        clip = out_dir / f"{spk}.wav"
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", f"{start:.2f}", "-t", "10",
                        "-i", str(workdir / "audio.wav"), str(clip)], check=True)
        quote = next((seg["text"].strip() for seg in transcript["segments"]
                      if seg.get("speaker") == spk and len(seg.get("text", "")) > 40), "")
        quote = (quote[:90] + "…") if len(quote) > 90 else quote
        samples[spk] = f"{talk_time[spk] / total:.0%} of talk time — {config.rel(clip)}" + (f' — "{quote}"' if quote else "")
    return samples


def save_decision(workdir: Path, d: SpeakerDecision) -> None:
    (workdir / "speakers.json").write_text(json.dumps(d.__dict__, indent=2))
