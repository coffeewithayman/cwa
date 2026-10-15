"""Apply the scope rule and write what the website reads.

  src/content/transcripts/<slug>.json   one per talk (turns, speakers, timestamps)
  src/data/talks.json                   the catalog behind the /talks table
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from . import config
from .intake_md import Entry, parse_range

SOLO_FORMATS = {"talk", "webinar"}
ONE_ON_ONE_FORMATS = {"interview", "podcast-guest"}


def scope_for(fmt: str, n_speakers: int) -> str:
    """'all' keeps the whole recording; 'ayman' keeps only his turns (+ context)."""
    if fmt in SOLO_FORMATS:
        return "all"
    if fmt in ONE_ON_ONE_FORMATS and n_speakers <= 2:
        return "all"
    return "ayman"


def guess_format(shares: dict[str, float]) -> str:
    main = [s for s in shares.values() if s >= config.MIN_SPEAKER_SHARE]
    if len(main) <= 1 or max(main) >= config.SOLO_SHARE:
        return "talk"
    return "interview" if len(main) == 2 else "panel"


def _turns(segments: list[dict], ayman: str | None) -> list[dict]:
    """Merge consecutive segments by the same speaker into turns."""
    turns: list[dict] = []
    for seg in segments:
        who = "ayman" if seg["speaker"] == ayman else (seg["speaker"] or "unknown")
        if turns and turns[-1]["who"] == who:
            turns[-1]["end"] = seg["end"]
            turns[-1]["lines"].append({"t": seg["start"], "text": seg["text"]})
        else:
            turns.append({"who": who, "start": seg["start"], "end": seg["end"],
                          "lines": [{"t": seg["start"], "text": seg["text"]}]})
    return turns


def _label(who: str, fmt: str, others: list[str]) -> str:
    if who == "ayman":
        return "Ayman"
    if fmt in SOLO_FORMATS:
        return "Audience"
    if fmt in ONE_ON_ONE_FORMATS and len(others) == 1:
        return "Host"
    return f"Speaker {others.index(who) + 2}" if who in others else "Speaker"


def build_transcript(entry: Entry, cleaned: dict, ayman: str | None, offset: float) -> dict:
    fmt = entry.get("format")
    segments = [{**s, "start": s["start"] + offset, "end": s["end"] + offset} for s in cleaned["segments"]]
    turns = _turns(segments, ayman)
    others = sorted({t["who"] for t in turns if t["who"] != "ayman"})
    scope = scope_for(fmt, len(others) + (1 if ayman else 0))

    out = []
    for i, turn in enumerate(turns):
        is_ayman = turn["who"] == "ayman"
        if scope == "all":
            out.append({**turn, "citable": is_ayman or fmt in SOLO_FORMATS, "context": False})
        elif is_ayman:
            prev = turns[i - 1] if i else None
            if prev and prev["who"] != "ayman":
                keep = [l for l in prev["lines"] if l["t"] >= prev["end"] - config.CONTEXT_SECONDS] or prev["lines"][-1:]
                out.append({**prev, "start": keep[0]["t"], "lines": keep, "citable": False, "context": True})
            out.append({**turn, "citable": True, "context": False})
    for t in out:
        t["speaker"] = _label(t.pop("who"), fmt, others)
        t["start"], t["end"] = round(t["start"], 1), round(t["end"], 1)
        for line in t["lines"]:
            line["t"] = round(line["t"], 1)
    return {"slug": entry.slug, "scope": scope, "format": fmt, "turns": out}


def write_transcript(slug: str, data: dict) -> Path:
    config.SITE_TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    path = config.SITE_TRANSCRIPTS / f"{slug}.json"
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    return path


# --- catalog ----------------------------------------------------------------------

PLATFORMS = {"Youtube": "YouTube", "Vimeo": "Vimeo", "Local": "Recording"}


def _date(entry: Entry, info: dict) -> str | None:
    if entry.get("date"):
        return entry.get("date")
    d = info.get("upload_date")
    return datetime.strptime(d, "%Y%m%d").date().isoformat() if d else None


def catalog_item(entry: Entry, info: dict) -> dict:
    clip = parse_range(entry.get("clip"))
    duration = (clip[1] - clip[0]) if clip else info.get("duration")
    url = entry.get("url") or info.get("webpage_url")
    if url and clip and "youtube" in (info.get("extractor_key") or "").lower():
        url = f"{url}{'&' if '?' in url else '?'}t={int(clip[0])}"
    return {
        "slug": entry.slug,
        "title": entry.title,
        "url": url,
        "platform": PLATFORMS.get(info.get("extractor_key") or "", info.get("extractor_key") or "Web"),
        "date": _date(entry, info),
        "duration": round(duration) if duration else None,
        "format": entry.get("format") or None,
        "event": entry.get("event") or info.get("channel") or info.get("uploader"),
        "category": entry.get("category") or None,
        "topics": entry.topics,
        "thumbnail": info.get("thumbnail"),
        "summary": entry.get("summary") or None,
        "hasTranscript": (config.SITE_TRANSCRIPTS / f"{entry.slug}.json").exists(),
    }


def compile_catalog(entries: list[Entry]) -> int:
    items = []
    for e in entries:
        status = e.get("status")
        info_path = config.META / f"{e.slug}.json"
        # Only talks that finished and were confirmed to feature Ayman go on the site;
        # queued or unverified candidates (e.g. ESW episodes) stay off it.
        if not status.startswith("✅") or not info_path.exists():
            continue
        items.append(catalog_item(e, json.loads(info_path.read_text())))
    items.sort(key=lambda x: x["date"] or "", reverse=True)
    config.SITE_DATA.parent.mkdir(parents=True, exist_ok=True)
    config.SITE_DATA.write_text(json.dumps(items, indent=1, ensure_ascii=False) + "\n")
    return len(items)
