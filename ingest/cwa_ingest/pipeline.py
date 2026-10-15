"""Orchestrates intake -> fetch -> transcribe -> speakers -> clean -> publish.

Each step records a fingerprint of its inputs in ingest/cache/<slug>/state.json.
A step re-runs only when its inputs changed (e.g. Ayman edits `format`, ticks a
vocab suggestion, or picks a speaker), so re-running is always cheap and safe.
"""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
import traceback
from pathlib import Path

from . import clean as clean_mod
from . import config, enrich, fetch, publish, speakers
from . import intake_md as md

log = logging.getLogger("cwa_ingest")


def _fp(*parts) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode()).hexdigest()[:16]


class State:
    def __init__(self, slug: str):
        self.dir = config.CACHE / slug
        self.path = self.dir / "state.json"
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {}

    def fresh(self, step: str, fp: str, *outputs: str) -> bool:
        return self.data.get(step) == fp and all((self.dir / o).exists() for o in outputs)

    def done(self, step: str, fp: str) -> None:
        self.data[step] = fp
        self.save()

    def forget(self, *steps: str) -> None:
        for step in steps:
            self.data.pop(step, None)
        self.save()

    def save(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2))


def status(slug: str, text: str) -> None:
    md.set_status(config.TALKS_MD, slug, text)
    log.info("%s: %s", slug, text)


# --- intake ---------------------------------------------------------------------

def known_urls() -> dict[str, str]:
    return {fetch.normalize_url(e.get("url")): e.slug for e in md.parse_talks(config.TALKS_MD) if e.get("url")}


def add_url(url: str) -> str | None:
    """Create a talks.md entry for a URL (metadata pre-filled). None if already there."""
    if fetch.normalize_url(url) in known_urls():
        return None
    try:
        info = fetch.probe(url)
    except Exception as exc:  # noqa: BLE001 - surface any yt-dlp failure in the file
        return md.append_entry(config.TALKS_MD, url, {"url": url, "status": f"⚠️ error: couldn't read link ({str(exc)[:120]})"})
    date = info.get("upload_date")
    fields = {
        "url": url,
        "format": "",
        "date": f"{date[:4]}-{date[4:6]}-{date[6:]}" if date else "",
        "event": info.get("channel") or info.get("uploader") or "",
        "category": "",
        "topics": "",
        "status": "⏳ queued",
    }
    slug = md.append_entry(config.TALKS_MD, info.get("title") or url, fields)
    config.META.mkdir(parents=True, exist_ok=True)
    (config.META / f"{slug}.json").write_text(json.dumps(fetch._slim(info), indent=2))
    return slug


def process_inbox_urls() -> list[str]:
    added = []
    for url in md.inbox_items(config.TALKS_MD):
        slug = add_url(url)
        md.remove_from_inbox(config.TALKS_MD, url)
        if slug:
            added.append(slug)
    return added


# --- per-talk processing ----------------------------------------------------------

def entry_fp(entry: md.Entry) -> str:
    """Everything Ayman can edit on an entry (status excluded)."""
    return _fp({k: v for k, v in entry.fields.items() if k != "status"})


def process(entry: md.Entry, *, force: bool = False) -> None:
    slug = entry.slug
    st = State(slug)
    if force:
        st.data = {}
    s = entry.get("status")
    if s.startswith("⏭") and not force:
        return
    # A failed talk is retried only after Ayman changes the entry (or --force).
    if s.startswith("⚠️") and not force and st.data.get("error_fp") == entry_fp(entry):
        return
    before = dict(st.data)
    vocab = md.parse_vocab(config.VOCAB_MD)
    clip = md.parse_range(entry.get("clip"))
    source = entry.get("url") if not entry.get("file") else entry.get("file")
    if not source:
        status(slug, "⚠️ error: needs a url or file")
        return

    # 1. fetch
    fp_fetch = _fp(source, clip)
    if not st.fresh("fetch", fp_fetch, "audio.wav", "info.json"):
        status(slug, "⬇️ downloading audio")
        if entry.get("file"):
            info = fetch.fetch_file(config.REPO / entry.get("file"), st.dir, clip)
        else:
            info = fetch.fetch_url(entry.get("url"), st.dir, clip)
        config.META.mkdir(parents=True, exist_ok=True)
        shutil.copy(st.dir / "info.json", config.META / f"{slug}.json")
        st.done("fetch", fp_fetch)

    # 2. transcribe (tier 0: vocab terms bias the decoder)
    fp_tx = _fp(fp_fetch, vocab.terms, config.WHISPER_MODEL, config.WHISPER_ASR_OPTIONS, config.DIARIZATION_MODEL)
    if not st.fresh("transcribe", fp_tx, "whisper.json"):
        status(slug, "🎧 transcribing on GPU")
        from . import transcribe
        transcribe.transcribe(st.dir, vocab.terms)
        st.done("transcribe", fp_tx)
    transcript = json.loads((st.dir / "whisper.json").read_text())

    # 3. which speaker is Ayman
    override = entry.get("ayman_speaker") or None
    fp_spk = _fp(fp_tx, override, speakers.voiceprint_version())
    if not st.fresh("speakers", fp_spk, "speakers.json"):
        status(slug, "👂 identifying speakers")
        info = json.loads((st.dir / "info.json").read_text()) if (st.dir / "info.json").exists() else {}
        decision = speakers.decide(st.dir, transcript, override, info)
        speakers.save_decision(st.dir, decision)
        if decision.status == "override" and decision.ayman:
            _learn_voice(st.dir, slug, decision.ayman)
        st.done("speakers", fp_spk)
    decision = json.loads((st.dir / "speakers.json").read_text())

    if not entry.get("format"):
        guess = publish.guess_format(decision["shares"])
        voices = sum(1 for v in decision["shares"].values() if v >= config.MIN_SPEAKER_SHARE)
        md.set_field(config.TALKS_MD, slug, "format", f"{guess} <!-- guessed from {voices} voice(s); fix if wrong -->")
        entry = next(e for e in md.parse_talks(config.TALKS_MD) if e.slug == slug)

    if decision["status"] == "absent":
        status(slug, f"⏭ skipped: {decision['reason']}")
        publish.compile_catalog(md.parse_talks(config.TALKS_MD))
        return
    if decision["status"] != "review" and s.startswith("👤"):
        # resolved without Ayman (e.g. the voiceprint improved): close the open review item
        md.close_speaker_review(config.SPEAKERS_MD, slug, f"resolved automatically ({decision['reason']})")
    if decision["status"] == "review":
        if not s.startswith("👤"):
            samples = speakers.write_samples(st.dir, transcript)
            md.add_speaker_review(config.SPEAKERS_MD, slug, entry.title, decision["reason"], samples)
            status(slug, "👤 needs speaker review — see intake/speakers.md")
        return

    # 4. cleanup tiers 1-2
    fp_clean = _fp(fp_tx, vocab.terms, vocab.corrections)
    if not st.fresh("clean", fp_clean, "clean.json"):
        status(slug, "🧹 cleaning transcript")
        offset = clip[0] if clip else 0.0
        captions = fetch.read_captions(st.dir, offset=offset)
        cleaned = clean_mod.clean(transcript, vocab, captions)
        (st.dir / "clean.json").write_text(json.dumps(cleaned, indent=1))
        st.done("clean", fp_clean)
    cleaned = json.loads((st.dir / "clean.json").read_text())

    # 5. publish
    fp_pub = _fp(fp_spk, fp_clean, entry.get("format"), clip, decision["ayman"])
    out = config.SITE_TRANSCRIPTS / f"{slug}.json"
    if not st.fresh("publish", fp_pub) or not out.exists():
        data = publish.build_transcript(entry, cleaned, decision["ayman"], clip[0] if clip else 0.0)
        publish.write_transcript(slug, data)
        st.done("publish", fp_pub)
    # 6. summary (local model) — only while the field is empty, so Ayman's edits stick
    if not entry.get("summary"):
        _summarize(entry, json.loads(out.read_text()))

    if st.data == before and s.startswith("✅"):
        return   # nothing changed; leave the status line alone
    turns = json.loads(out.read_text())["turns"]
    n_flags = len(cleaned["flags"])
    how = {"auto": f"speaker auto ({decision['reason']})", "override": "speaker confirmed by Ayman",
           "solo": "solo recording"}.get(decision["status"], decision["status"])
    status(slug, f"✅ ingested {md.today()} · {sum(len(t['lines']) for t in turns)} lines · {how} · {n_flags} flagged")


def _summarize(entry: md.Entry, transcript: dict) -> None:
    if config.LOW_VRAM:
        from . import transcribe
        transcribe.release()   # hand the 6 GB card to the summary model
    try:
        text = enrich.summarize(entry.title, entry.get("event"), entry.get("format"), transcript)
    except Exception as exc:  # noqa: BLE001 - a summary is optional; never fail the talk over it
        log.warning("%s: summary failed: %s", entry.slug, exc)
        return
    if text:
        md.set_field(config.TALKS_MD, entry.slug, "summary", text)
        log.info("%s: summary written", entry.slug)


def _learn_voice(workdir: Path, slug: str, label: str) -> None:
    """A speaker Ayman confirmed becomes part of the voiceprint."""
    import numpy as np
    emb_path = workdir / "speaker_embeddings.npz"
    if not emb_path.exists():
        transcript = json.loads((workdir / "whisper.json").read_text())
        turns = speakers.speaker_turns(transcript["diarization"]).get(label, [])
        vec = speakers.speaker_embedding(speakers.load_wav(workdir / "audio.wav"), turns)
    else:
        embs = np.load(emb_path)
        vec = embs[label] if label in embs.files else None
    if vec is not None:
        speakers.add_to_voiceprint(f"talk-{slug}", vec)


# --- reviews coming back from the Markdown files -------------------------------

def apply_speaker_reviews() -> list[str]:
    changed = []
    for slug, choice in md.speaker_decisions(config.SPEAKERS_MD).items():
        md.set_field(config.TALKS_MD, slug, "ayman_speaker", choice)
        done = "not in recording" if choice == "none" else f"Ayman = {choice}"
        md.close_speaker_review(config.SPEAKERS_MD, slug, done)
        changed.append(slug)
    return changed


def apply_vocab() -> list[tuple[str, str]]:
    return md.apply_vocab_suggestions(config.VOCAB_MD)


# --- one full pass ----------------------------------------------------------------

def run_once(*, only: str | None = None, force: bool = False, reclean: bool = False) -> None:
    for d in (config.CACHE, config.META, config.INBOX, config.FAILED, config.LIBRARY):
        d.mkdir(parents=True, exist_ok=True)
    process_inbox_urls()
    from .inbox import process_inbox_files
    process_inbox_files()
    apply_vocab()
    apply_speaker_reviews()
    for entry in md.parse_talks(config.TALKS_MD):
        if only and entry.slug != only:
            continue
        if reclean and State(entry.slug).path.exists():
            State(entry.slug).forget("clean", "publish")
        try:
            process(entry, force=force)
        except Exception as exc:  # noqa: BLE001 - one bad talk must not stop the queue
            if type(exc).__name__ == "GPUBusy" or "out of memory" in str(exc).lower():
                # After a CUDA OOM the context is unusable; stop and retry on the next pass.
                status(entry.slug, f"⏸ waiting for GPU ({exc}); retries automatically")
                break   # every other talk would hit the same wall; try again next pass
            log.error("%s failed:\n%s", entry.slug, traceback.format_exc())
            status(entry.slug, f"⚠️ error: {str(exc).splitlines()[0][:160] if str(exc) else type(exc).__name__}")
            _fail_local_file(entry)
            fresh = next((e for e in md.parse_talks(config.TALKS_MD) if e.slug == entry.slug), entry)
            st = State(entry.slug)
            st.data["error_fp"] = entry_fp(fresh)
            st.save()
    publish.compile_catalog(md.parse_talks(config.TALKS_MD))


def _fail_local_file(entry: md.Entry) -> None:
    """A local file that can't be processed goes to media/inbox/_failed/."""
    f = entry.get("file")
    if f and (config.REPO / f).exists() and "library" in f:
        config.FAILED.mkdir(parents=True, exist_ok=True)
        dest = config.FAILED / Path(f).name
        shutil.move(config.REPO / f, dest)
        md.set_field(config.TALKS_MD, entry.slug, "file", config.rel(dest))
