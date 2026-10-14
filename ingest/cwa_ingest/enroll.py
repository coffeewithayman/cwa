"""Build Ayman's voiceprint from the clips listed in intake/voiceprint.md."""

from __future__ import annotations

import hashlib
import logging
import tempfile
from pathlib import Path

from . import config, fetch, speakers
from . import intake_md as md

log = logging.getLogger("cwa_ingest")


def _embed_clip(wav_path: Path) -> "speakers.np.ndarray":
    import numpy as np
    audio = speakers.load_wav(wav_path)
    window = 10 * 16000
    vecs = [speakers.embed(audio[i:i + window]) for i in range(0, max(len(audio) - window // 2, 1), window)
            if len(audio[i:i + window]) >= 3 * 16000]
    v = np.mean(vecs, axis=0)
    return v / np.linalg.norm(v)


def enroll() -> int:
    added = 0
    for idx, src, start, end, enrolled in md.voiceprint_clips(config.VOICEPRINT_MD):
        if enrolled:
            continue
        name = "clip-" + hashlib.sha256(f"{src}|{start}|{end}".encode()).hexdigest()[:10]
        try:
            with tempfile.TemporaryDirectory() as tmp:
                work = Path(tmp)
                if src.startswith("http"):
                    fetch.fetch_url(src, work, (start, end))
                else:
                    fetch.fetch_file(config.REPO / src, work, (start, end))
                speakers.add_to_voiceprint(name, _embed_clip(work / "audio.wav"))
            md.mark_line(config.VOICEPRINT_MD, idx, f"✅ enrolled {md.today()}")
            added += 1
        except Exception as exc:  # noqa: BLE001
            log.exception("enroll failed for %s", src)
            md.mark_line(config.VOICEPRINT_MD, idx, f"⚠️ {str(exc).splitlines()[0][:100]}")
    return added
