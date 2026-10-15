"""media/inbox/: drop a recording (or a list of links) in and it gets ingested.

Videos only: audio files are moved to _failed/ untouched.
A recording becomes a talks.md entry and moves to media/library/<slug>.<ext>.
An optional Markdown file with the same name carries its details, e.g.

    # Breaking IN — BSides SF 2024
    - format: talk
    - event: BSides SF
    - date: 2024-04-20
    - topics: careers, mentoring
    - url: https://bsidessf.org/talks/...   (slides or event page)

    ### Notes
    - anything else
"""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
import time
from pathlib import Path

from . import config
from . import intake_md as md

log = logging.getLogger("cwa_ingest")

def is_stable(path: Path) -> bool:
    """True once nothing has written to the file for STABLE_SECONDS.

    Uses ctime, which every write bumps and which copy tools can't backdate
    (unlike mtime with `cp -p`), so a half-copied file is never picked up.
    """
    try:
        return time.time() - path.stat().st_ctime >= config.STABLE_SECONDS
    except FileNotFoundError:
        return False


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _registry() -> dict[str, str]:
    return json.loads(config.REGISTRY.read_text()) if config.REGISTRY.exists() else {}


def _save_registry(reg: dict[str, str]) -> None:
    config.REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    config.REGISTRY.write_text(json.dumps(reg, indent=1))


def parse_sidecar(path: Path) -> tuple[str | None, dict[str, str], list[str]]:
    title, fields, notes, in_notes = None, {}, [], False
    for line in md.read_lines(path):
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("#"):
            in_notes = "notes" in line.lower()
        elif in_notes and line.startswith("- "):
            notes.append(line)
        elif m := md.FIELD_RE.match(line):
            fields[m.group(1)] = m.group(2)
    return title, fields, notes


def pretty_title(stem: str) -> str:
    return stem.replace("_", " ").replace("-", " ").strip().title()


def ingest_recording(path: Path, pending_notes: list[str] | None = None) -> str | None:
    reg = _registry()
    digest = sha256(path)
    if digest in reg:
        log.info("%s is a duplicate of %s; moving to _failed", path.name, reg[digest])
        config.FAILED.mkdir(parents=True, exist_ok=True)
        shutil.move(path, config.FAILED / f"{path.name}.duplicate-of-{reg[digest]}")
        return None

    sidecar = path.with_suffix(".md")
    title, fields, notes = (parse_sidecar(sidecar) if sidecar.exists() else (None, {}, []))
    allowed = {k: v for k, v in fields.items() if k in {"format", "date", "event", "category", "topics", "clip", "url", "ayman_speaker"}}
    entry_fields = {"format": "", "date": "", "event": "", "category": "", "topics": "", **allowed,
                    "file": "", "status": "⏳ queued"}
    slug = md.append_entry(config.TALKS_MD, title or pretty_title(path.stem), entry_fields)

    config.LIBRARY.mkdir(parents=True, exist_ok=True)
    dest = config.LIBRARY / f"{slug}{path.suffix.lower()}"
    shutil.move(path, dest)
    md.set_field(config.TALKS_MD, slug, "file", config.rel(dest))
    if sidecar.exists():
        shutil.move(sidecar, config.LIBRARY / f"{slug}.md")
    if notes:
        _add_notes(slug, notes)
    reg[digest] = slug
    _save_registry(reg)
    log.info("queued %s as %s", path.name, slug)
    return slug


def _add_notes(slug: str, notes: list[str]) -> None:
    lines = md.read_lines(config.TALKS_MD)
    sec = md.find_entry(lines, slug)
    if not sec:
        return
    at = next((i + 1 for i in range(sec.start, sec.end) if lines[i].strip().lower() == "### notes"), sec.end)
    lines[at:at] = notes
    md.write_lines(config.TALKS_MD, lines)


def ingest_link_list(path: Path) -> int:
    from .pipeline import add_url
    urls = md.URL_RE.findall(path.read_text(encoding="utf-8", errors="ignore"))
    added = sum(1 for u in urls if add_url(u))
    dest = config.LIBRARY / "_lists"
    dest.mkdir(parents=True, exist_ok=True)
    shutil.move(path, dest / f"{time.strftime('%Y%m%d-%H%M%S')}-{path.name}")
    log.info("link list %s: %d new of %d", path.name, added, len(urls))
    return added


def process_inbox_files(wait_for_stable: bool = True) -> bool:
    """Handle every finished file in media/inbox. Returns True if any are still copying."""
    if not config.INBOX.exists():
        return False
    still_copying = False
    files = sorted(p for p in config.INBOX.iterdir() if p.is_file() and not p.name.startswith("."))
    stems_with_media = {p.stem for p in files if p.suffix.lower() in config.MEDIA_EXTS}
    for path in files:
        ext = path.suffix.lower()
        if ext in config.AUDIO_EXTS and is_stable(path):
            log.warning("inbox: %s is audio only — the archive is videos only; moved to _failed", path.name)
            config.FAILED.mkdir(parents=True, exist_ok=True)
            shutil.move(path, config.FAILED / f"{path.name}.audio-only")
            continue
        if ext not in config.MEDIA_EXTS and ext not in config.LIST_EXTS:
            continue
        if ext in config.LIST_EXTS and path.stem in stems_with_media:
            continue   # sidecar: handled with its recording
        if wait_for_stable and not is_stable(path):
            still_copying = True
            continue
        try:
            if ext in config.MEDIA_EXTS:
                ingest_recording(path)
            else:
                ingest_link_list(path)
        except Exception as exc:  # noqa: BLE001
            log.error("inbox: %s failed: %s", path.name, exc)
            config.FAILED.mkdir(parents=True, exist_ok=True)
            shutil.move(path, config.FAILED / path.name)
    return still_copying
