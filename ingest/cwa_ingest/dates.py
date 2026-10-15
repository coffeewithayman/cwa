"""When a talk was given, which is often not when the video went up.

Conference recordings are routinely uploaded months or years later, so the
upload date is only the last resort. In order of trust:

1. a sched.com session page linked from the description (exact session day),
2. a full date written in the description ("Recorded on May 1st, 2020"),
3. yt-dlp's release date (the day a livestream / premiere aired),
4. the upload date, flagged for review when the title names an earlier year
   (e.g. "BSidesSF 2015" uploaded in 2023).

`talk_date` returns (YYYY-MM-DD, note); the note goes into talks.md as a
comment so Ayman can see where the date came from.
"""

from __future__ import annotations

import logging
import re
import urllib.request
from datetime import date, datetime

log = logging.getLogger("cwa_ingest")

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
FULL_DATE_RE = re.compile(rf"\b({MONTHS})\s+(\d{{1,2}})(?:st|nd|rd|th)?,?\s+(\d{{4}})\b", re.I)
SCHED_RE = re.compile(r"https?://[\w-]+\.sched\.com/event/\S+")
YEAR_RE = re.compile(r"\b(?:19|20)\d\d\b")
# "Recorded on May 1st, 2020", "A talk given at City College on May 1, 2019"; a bare date
# elsewhere in a description is usually a news item or a sponsor's event, not the talk
WHEN_RE = re.compile(r"\b(recorded|given|filmed|presented|streamed|aired|taped|held)\b", re.I)


def _ymd(s: str | None) -> date | None:
    try:
        return datetime.strptime(s, "%Y%m%d").date() if s else None
    except ValueError:
        return None


def dates_in(text: str, *, after_when: bool = False) -> list[date]:
    out = []
    for m in FULL_DATE_RE.finditer(text or ""):
        if after_when and not WHEN_RE.search(text[max(0, m.start() - 80):m.start()]):
            continue
        month, day, year = m.groups()
        try:
            out.append(datetime.strptime(f"{month} {day} {year}", "%B %d %Y").date())
        except ValueError:
            continue
    return out


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (cwa-ingest)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def sched_date(url: str) -> date | None:
    """The session day from a sched.com event page ("Monday April 20, 2015 5:00pm")."""
    try:
        html = _fetch(url)
    except OSError as exc:
        log.warning("couldn't read %s: %s", url, exc)
        return None
    found = dates_in(re.sub(r"<[^>]+>", " ", html))
    return found[0] if found else None


def talk_date(info: dict, *, fetch_sched=sched_date) -> tuple[str, str]:
    upload = _ymd(info.get("upload_date"))
    release = _ymd(info.get("release_date"))
    desc = info.get("description") or ""
    latest = release or upload

    for url in SCHED_RE.findall(desc):
        d = fetch_sched(url.rstrip(").,"))
        if d:
            return d.isoformat(), "session date from the sched.com link"

    # a date written in the description, never one after the video was published
    written = [d for d in dates_in(desc, after_when=True) if not latest or d <= latest]
    if written:
        return min(written).isoformat(), "from the video description"

    if release and release != upload:
        return release.isoformat(), "date it aired"
    if not upload:
        return "", ""

    years = [int(y) for y in YEAR_RE.findall(info.get("title") or "")]
    earlier = sorted({y for y in years if y < upload.year})
    if earlier:
        return upload.isoformat(), f"upload date, but the title says {earlier[0]}: set the real talk date"
    return upload.isoformat(), ""
