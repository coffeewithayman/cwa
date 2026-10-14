"""Read and write the Markdown intake files in `intake/`.

The files belong to Ayman: this module only ever touches lines it manages
(status lines, fields it fills in when empty, entries it appends) and leaves
everything else byte-for-byte alone. Every write re-reads the file first, so
edits made in an editor between reads are never clobbered.
"""

from __future__ import annotations

import os
import re
import tempfile
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

MANAGED = "<!-- managed -->"

SPECIAL_SECTIONS = {"inbox", "candidates"}
URL_RE = re.compile(r"https?://\S+")
FIELD_RE = re.compile(r"^- ([a-z_]+):\s?(.*?)\s*$")
COMMENT_RE = re.compile(r"<!--.*?-->")
STRUCK_RE = re.compile(r"^\s*-\s+~~.*~~")

# Field order for new entries; anything else goes before `status`.
FIELD_ORDER = [
    "id", "url", "file", "format", "date", "event", "category", "topics",
    "clip", "ayman_speaker", "status",
]
# Fields the pipeline owns outright (rewritten freely, tagged as managed).
MANAGED_FIELDS = {"id", "status"}


def slugify(text: str, max_len: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(slug) > max_len:
        cut = slug[:max_len + 1].rfind("-")      # end on a whole word
        slug = slug[:cut if cut > max_len // 2 else max_len]
    return slug.rstrip("-") or "talk"


def strip_comment(value: str) -> str:
    return COMMENT_RE.sub("", value).strip()


def today() -> str:
    return date.today().isoformat()


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines() if path.exists() else []


def write_lines(path: Path, lines: list[str]) -> None:
    """Atomic write so a crash or a concurrent reader never sees half a file."""
    text = "\n".join(lines).rstrip("\n") + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

@dataclass
class Section:
    heading: str          # text after "## "
    start: int            # index of the "## " line
    end: int              # exclusive

    @property
    def key(self) -> str:
        return self.heading.strip().lower()


def sections(lines: list[str], level: int = 2) -> list[Section]:
    marker = "#" * level + " "
    out: list[Section] = []
    for i, line in enumerate(lines):
        if line.startswith(marker):
            if out:
                out[-1].end = i
            out.append(Section(line[len(marker):].strip(), i, len(lines)))
    return out


def find_section(lines: list[str], name: str) -> Section | None:
    return next((s for s in sections(lines) if s.key == name.lower()), None)


# ---------------------------------------------------------------------------
# talks.md
# ---------------------------------------------------------------------------

@dataclass
class Entry:
    title: str
    fields: dict[str, str] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)       # open notes only

    @property
    def slug(self) -> str:
        return strip_comment(self.fields.get("id", "")) or slugify(self.title)

    def get(self, key: str) -> str:
        return strip_comment(self.fields.get(key, ""))

    @property
    def topics(self) -> list[str]:
        return [t.strip() for t in self.get("topics").split(",") if t.strip()]


def _entry_from(lines: list[str], sec: Section) -> Entry:
    entry = Entry(title=sec.heading)
    in_notes = False
    for line in lines[sec.start + 1:sec.end]:
        if line.startswith("### "):
            in_notes = line[4:].strip().lower() == "notes"
            continue
        if in_notes:
            if line.lstrip().startswith("- ") and not STRUCK_RE.match(line):
                entry.notes.append(line.strip()[2:])
            continue
        m = FIELD_RE.match(line)
        if m:
            entry.fields[m.group(1)] = m.group(2)
    return entry


def parse_talks(path: Path) -> list[Entry]:
    lines = read_lines(path)
    return [_entry_from(lines, s) for s in sections(lines) if s.key not in SPECIAL_SECTIONS]


def find_entry(lines: list[str], slug: str) -> Section | None:
    for sec in sections(lines):
        if sec.key in SPECIAL_SECTIONS:
            continue
        if _entry_from(lines, sec).slug == slug:
            return sec
    return None


def inbox_items(path: Path) -> list[str]:
    """URLs pasted into the Inbox section (comments and blank lines ignored)."""
    lines = read_lines(path)
    sec = find_section(lines, "inbox")
    if not sec:
        return []
    body = "\n".join(lines[sec.start + 1:sec.end])
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    return URL_RE.findall(body)


def remove_from_inbox(path: Path, url: str) -> None:
    lines = read_lines(path)
    sec = find_section(lines, "inbox")
    if not sec:
        return
    for i in range(sec.start + 1, sec.end):
        if url in lines[i] and not lines[i].lstrip().startswith("<!--"):
            del lines[i]
            break
    write_lines(path, lines)


def _format_field(key: str, value: str) -> str:
    line = f"- {key}: {value}".rstrip()
    return f"{line} {MANAGED}" if key in MANAGED_FIELDS else line


def append_entry(path: Path, title: str, fields: dict[str, str]) -> str:
    """Add a new entry at the end of the file. Returns its (unique) slug."""
    lines = read_lines(path)
    existing = {e.slug for e in parse_talks(path)}
    slug = base = fields.get("id") or slugify(title)
    n = 2
    while slug in existing:
        slug, n = f"{base}-{n}", n + 1
    fields = {**fields, "id": slug}
    ordered = [k for k in FIELD_ORDER if k in fields] + [k for k in fields if k not in FIELD_ORDER]
    block = ["", f"## {title}"] + [_format_field(k, fields[k]) for k in ordered] + ["", "### Notes", ""]
    while lines and not lines[-1].strip():
        lines.pop()
    write_lines(path, lines + block)
    return slug


def set_field(path: Path, slug: str, key: str, value: str, *, only_if_empty: bool = False) -> bool:
    """Set `- key: value` inside an entry. Returns True if the file changed.

    With only_if_empty, a value Ayman already typed is never overwritten.
    """
    lines = read_lines(path)
    sec = find_entry(lines, slug)
    if not sec:
        return False
    insert_at = None
    for i in range(sec.start + 1, sec.end):
        line = lines[i]
        if line.startswith("### "):
            insert_at = insert_at or i
            break
        m = FIELD_RE.match(line)
        if m and m.group(1) == key:
            if only_if_empty and strip_comment(m.group(2)):
                return False
            new = _format_field(key, value)
            # keep any inline help comment Ayman's template carried, e.g. format options
            comments = [c for c in COMMENT_RE.findall(m.group(2)) if c != MANAGED]
            if comments and key not in MANAGED_FIELDS:
                new = f"{new}  {' '.join(comments)}"
            if lines[i] == new:
                return False
            lines[i] = new
            write_lines(path, lines)
            return True
        if m:
            insert_at = i + 1
    if insert_at is None:
        insert_at = sec.start + 1
    # keep `status` last among the fields
    if key != "status" and insert_at > sec.start + 1 and FIELD_RE.match(lines[insert_at - 1] or "") \
            and FIELD_RE.match(lines[insert_at - 1]).group(1) == "status":
        insert_at -= 1
    lines.insert(insert_at, _format_field(key, value))
    write_lines(path, lines)
    return True


def set_status(path: Path, slug: str, status: str) -> bool:
    return set_field(path, slug, "status", status)


def add_note_reply(path: Path, slug: str, note_text: str, reply: str) -> bool:
    """Indent a reply under an open note that couldn't be resolved."""
    lines = read_lines(path)
    sec = find_entry(lines, slug)
    if not sec:
        return False
    for i in range(sec.start, sec.end):
        if lines[i].strip() == f"- {note_text}":
            lines.insert(i + 1, f"  - ↳ {reply} ({today()})")
            write_lines(path, lines)
            return True
    return False


def strike_note(path: Path, note_text: str, done: str) -> bool:
    """Mark an open note as handled: ~~note~~ ✔ what was done, date."""
    lines = read_lines(path)
    for i, line in enumerate(lines):
        indent = line[: len(line) - len(line.lstrip())]
        if line.strip() == f"- {note_text}":
            lines[i] = f"{indent}- ~~{note_text}~~ ✔ {done} {today()}"
            write_lines(path, lines)
            return True
    return False


def open_notes(intake_dir: Path) -> list[tuple[Path, str, str]]:
    """(file, section heading, note) for every open note in every intake file.

    A note is any bullet under a `### Notes` (or `## Notes`) heading that isn't
    struck through.
    """
    out = []
    for path in sorted(intake_dir.glob("*.md")):
        lines = read_lines(path)
        heading, in_notes = "", False
        for line in lines:
            if line.startswith("## "):
                heading = line[3:].strip()
                in_notes = heading.lower() == "notes"
                continue
            if line.startswith("### "):
                in_notes = line[4:].strip().lower() == "notes"
                continue
            if in_notes and line.startswith("- ") and not STRUCK_RE.match(line):
                out.append((path, heading, line[2:].strip()))
    return out


# ---------------------------------------------------------------------------
# vocab.md
# ---------------------------------------------------------------------------

@dataclass
class Vocab:
    terms: list[str]
    corrections: dict[str, str]      # heard (lowercase) -> correct
    rejected: set[str]               # heard phrases Ayman struck out of Suggested


TABLE_ROW_RE = re.compile(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")
SUGGEST_RE = re.compile(r'^- \[( |x|X)\] "(.+?)" → (.+?)(?: \(.*\))?\s*$')
STRUCK_SUGGEST_RE = re.compile(r'^- ~~\[.\] "(.+?)" →')


def _bullets(lines: list[str], sec: Section | None) -> list[str]:
    if not sec:
        return []
    return [strip_comment(l[2:]) for l in lines[sec.start + 1:sec.end]
            if l.startswith("- ") and not STRUCK_RE.match(l) and strip_comment(l[2:])]


def parse_vocab(path: Path) -> Vocab:
    lines = read_lines(path)
    secs = {s.key.split("(")[0].strip(): s for s in sections(lines)}
    terms = _bullets(lines, secs.get("terms"))
    corrections: dict[str, str] = {}
    sec = secs.get("corrections")
    if sec:
        for line in lines[sec.start + 1:sec.end]:
            m = TABLE_ROW_RE.match(line)
            if m and not set(m.group(1)) <= set("-: ") and m.group(1).lower() != "heard":
                corrections[m.group(1).lower()] = m.group(2)
    rejected = set()
    sec = secs.get("suggested")
    if sec:
        for line in lines[sec.start + 1:sec.end]:
            m = STRUCK_SUGGEST_RE.match(line)
            if m:
                rejected.add(m.group(1).lower())
    return Vocab(terms, corrections, rejected)


def apply_vocab_suggestions(path: Path) -> list[tuple[str, str]]:
    """Move ticked suggestions into the Corrections table. Returns what moved."""
    lines = read_lines(path)
    secs = {s.key.split("(")[0].strip(): s for s in sections(lines)}
    sug, corr = secs.get("suggested"), secs.get("corrections")
    if not sug or not corr:
        return []
    accepted, keep = [], []
    for i in range(sug.start + 1, sug.end):
        m = SUGGEST_RE.match(lines[i])
        if m and m.group(1).lower() == "x":
            accepted.append((m.group(2), m.group(3)))
        else:
            keep.append(lines[i])
    if not accepted:
        return []
    # last table row in Corrections
    last_row = max((i for i in range(corr.start, corr.end) if lines[i].startswith("|")), default=corr.start)
    new_rows = [f"| {heard} | {correct} |" for heard, correct in accepted]
    lines = (lines[:last_row + 1] + new_rows + lines[last_row + 1:sug.start + 1]
             + keep + lines[sug.end:])
    write_lines(path, lines)
    return accepted


def add_vocab_suggestions(path: Path, suggestions: list[tuple[str, str, str]]) -> int:
    """Append (heard, correct, why) suggestions not already known/rejected."""
    vocab = parse_vocab(path)
    lines = read_lines(path)
    sec = find_section(lines, "Suggested") or next(
        (s for s in sections(lines) if s.key.startswith("suggested")), None)
    if not sec:
        return 0
    existing = {m.group(2).lower() for l in lines[sec.start:sec.end] if (m := SUGGEST_RE.match(l))}
    new = [f'- [ ] "{h}" → {c} ({why})' for h, c, why in suggestions
           if h.lower() not in vocab.corrections and h.lower() not in vocab.rejected
           and h.lower() not in existing]
    if not new:
        return 0
    end = sec.end
    while end > sec.start + 1 and not lines[end - 1].strip():
        end -= 1
    lines[end:end] = new
    write_lines(path, lines)
    return len(new)


# ---------------------------------------------------------------------------
# taxonomy.md
# ---------------------------------------------------------------------------

def parse_taxonomy(path: Path) -> dict[str, list[str]]:
    lines = read_lines(path)
    secs = {s.key: s for s in sections(lines)}
    return {
        "categories": _bullets(lines, secs.get("categories")),
        "topics": _bullets(lines, secs.get("topics")),
    }


# ---------------------------------------------------------------------------
# speakers.md
# ---------------------------------------------------------------------------

SPEAKER_ID_RE = re.compile(r"<!-- id: (\S+) -->")
SPEAKER_CHOICE_RE = re.compile(r"^- \[(x|X)\] (SPEAKER_\d+|none)\b")


def add_speaker_review(path: Path, slug: str, title: str, reason: str,
                       samples: dict[str, str]) -> None:
    lines = read_lines(path)
    if any(f"<!-- id: {slug} -->" in l for l in lines):
        return
    block = ["", f"## {title}", f"<!-- id: {slug} -->", reason]
    block += [f"- [ ] {spk} — {sample}" for spk, sample in samples.items()]
    block += ["- [ ] none — Ayman isn't in this recording"]
    while lines and not lines[-1].strip():
        lines.pop()
    write_lines(path, lines + block)


def speaker_decisions(path: Path) -> dict[str, str]:
    """slug -> chosen speaker label (or 'none') for open review items that are ticked."""
    lines = read_lines(path)
    out = {}
    for sec in sections(lines):
        if sec.heading.startswith("~~"):
            continue
        body = lines[sec.start + 1:sec.end]
        slug = next((m.group(1) for l in body if (m := SPEAKER_ID_RE.search(l))), None)
        choice = next((m.group(2) for l in body if (m := SPEAKER_CHOICE_RE.match(l))), None)
        if slug and choice:
            out[slug] = choice
    return out


def close_speaker_review(path: Path, slug: str, done: str) -> None:
    lines = read_lines(path)
    for sec in sections(lines):
        if any(f"<!-- id: {slug} -->" in l for l in lines[sec.start:sec.end]) \
                and not sec.heading.startswith("~~"):
            lines[sec.start] = f"## ~~{sec.heading}~~ ✔ {done} {today()}"
            write_lines(path, lines)
            return


# ---------------------------------------------------------------------------
# voiceprint.md
# ---------------------------------------------------------------------------

CLIP_RE = re.compile(r"^- (?P<src>\S+)\s+(?P<start>[\d:]+)\s*[–-]\s*(?P<end>[\d:]+)(?P<rest>.*)$")


def parse_timestamp(ts: str) -> float:
    parts = [float(p) for p in ts.strip().split(":")]
    secs = 0.0
    for p in parts:
        secs = secs * 60 + p
    return secs


def parse_range(rng: str) -> tuple[float, float] | None:
    m = re.match(r"\s*([\d:]+)\s*[–-]\s*([\d:]+)", strip_comment(rng))
    return (parse_timestamp(m.group(1)), parse_timestamp(m.group(2))) if m else None


def voiceprint_clips(path: Path) -> list[tuple[int, str, float, float, bool]]:
    """(line index, source, start s, end s, already enrolled) for each clip line."""
    out = []
    for i, line in enumerate(read_lines(path)):
        m = CLIP_RE.match(line)
        if m:
            out.append((i, m.group("src"), parse_timestamp(m.group("start")),
                        parse_timestamp(m.group("end")), "✅" in m.group("rest")))
    return out


def mark_line(path: Path, index: int, suffix: str) -> None:
    lines = read_lines(path)
    base = re.sub(r"\s*(✅|⚠️).*$", "", lines[index])
    lines[index] = f"{base}  {suffix}"
    write_lines(path, lines)
