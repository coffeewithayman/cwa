"""Get metadata, 16 kHz mono audio and (when available) captions for a talk."""

from __future__ import annotations

import json
import logging
import re
import subprocess
from pathlib import Path

import yt_dlp


log = logging.getLogger("cwa_ingest")

YOUTUBE_ID_RE = re.compile(r"(?:youtu\.be/|v=|/shorts/|/live/|/embed/)([\w-]{11})")


def normalize_url(url: str) -> str:
    """Canonical form used to spot the same video pasted twice."""
    m = YOUTUBE_ID_RE.search(url)
    if m:
        return f"https://www.youtube.com/watch?v={m.group(1)}"
    return re.sub(r"[?#].*$", "", url.strip()).rstrip("/")


def probe(url: str) -> dict:
    """Metadata only, no download (used when a URL first lands in the Inbox)."""
    with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True, "noplaylist": True}) as ydl:
        info = ydl.extract_info(url, download=False)
    return ydl.sanitize_info(info)


def is_video(info: dict) -> bool:
    """False for audio-only sources (podcast feeds, Apple Podcasts, audio uploads)."""
    vcodecs = [f.get("vcodec") for f in info.get("formats") or []] + [info.get("vcodec")]
    return any(v and v != "none" for v in vcodecs) and (info.get("duration") or 0) > 0


def _ffmpeg_to_wav(src: Path, dest: Path, clip: tuple[float, float] | None) -> None:
    cmd = ["ffmpeg", "-nostdin", "-y", "-loglevel", "error"]
    if clip:
        cmd += ["-ss", str(clip[0]), "-to", str(clip[1])]
    cmd += ["-i", str(src), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(dest)]
    subprocess.run(cmd, check=True)


# Be gentle with YouTube: a backlog of ~70 videos in a row triggers HTTP 429s.
POLITE = {
    "retries": 10,
    "fragment_retries": 10,
    "extractor_retries": 5,
    "sleep_interval_requests": 1,
    "sleep_interval": 5,
    "max_sleep_interval": 15,
}


def fetch_url(url: str, workdir: Path, clip: tuple[float, float] | None) -> dict:
    """Download best audio, convert to audio.wav, then try for English captions. Returns info dict."""
    workdir.mkdir(parents=True, exist_ok=True)
    opts = {
        "quiet": True,
        "noprogress": True,
        "noplaylist": True,
        "format": "bestaudio/best",
        "outtmpl": str(workdir / "source.%(ext)s"),
        **POLITE,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.sanitize_info(ydl.extract_info(url, download=True))
    source = next(p for p in workdir.glob("source.*") if p.suffix not in {".vtt", ".json"})
    _ffmpeg_to_wav(source, workdir / "audio.wav", clip)
    source.unlink()   # keep only the wav; the original is re-downloadable
    (workdir / "info.json").write_text(json.dumps(_slim(info), indent=2))
    _fetch_captions(url, workdir)
    return info


def _fetch_captions(url: str, workdir: Path) -> None:
    """Captions are only a cross-check for Whisper, so failing to get them is fine."""
    opts = {
        "quiet": True,
        "noprogress": True,
        "noplaylist": True,
        "skip_download": True,
        "outtmpl": str(workdir / "source.%(ext)s"),
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en", "en-US", "en-orig"],
        "subtitlesformat": "vtt",
        **POLITE,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.extract_info(url, download=True)
    except Exception as exc:  # noqa: BLE001
        log.warning("captions unavailable for %s (%s); continuing without the cross-check",
                    url, str(exc).splitlines()[0][:120])


def fetch_file(path: Path, workdir: Path, clip: tuple[float, float] | None) -> dict:
    workdir.mkdir(parents=True, exist_ok=True)
    _ffmpeg_to_wav(path, workdir / "audio.wav", clip)
    info = {"title": path.stem, "duration": _duration(path), "extractor_key": "Local"}
    (workdir / "info.json").write_text(json.dumps(info, indent=2))
    return info


def _duration(path: Path) -> float | None:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def _slim(info: dict) -> dict:
    keys = ["id", "title", "description", "upload_date", "release_date", "duration", "channel", "uploader",
            "channel_url", "webpage_url", "extractor_key", "thumbnail", "chapters"]
    return {k: info.get(k) for k in keys}


# --- captions (cross-check only) --------------------------------------------

TS_RE = re.compile(r"(\d+):(\d\d):(\d\d)\.(\d+) --> (\d+):(\d\d):(\d\d)\.(\d+)")
TAG_RE = re.compile(r"<[^>]+>")


def read_captions(workdir: Path, offset: float = 0.0) -> list[tuple[float, float, str]]:
    """Parse a yt-dlp VTT into (start, end, text), de-duplicating rolling auto-captions."""
    vtt = next(iter(sorted(workdir.glob("source*.vtt"))), None)
    if not vtt:
        return []
    cues, last = [], ""
    for block in vtt.read_text(encoding="utf-8", errors="ignore").split("\n\n"):
        m = TS_RE.search(block)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000 - offset
        end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000 - offset
        lines = [TAG_RE.sub("", l).strip() for l in block.split("\n")[1:]]
        lines = [l for l in lines if l and "-->" not in l and l != last]
        if lines:
            last = lines[-1]
            cues.append((start, end, " ".join(lines)))
    return cues
