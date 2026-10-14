"""Cleanup tiers 0-2: free, rule-based, deterministic.

Tier 0 (vocab hotwords) already happened at transcription time. Here:
  tier 1: vocab corrections table, canonical casing of vocab terms, filler removal
  tier 2: flag words worth a second look (low ASR confidence, rare words,
          disagreement with YouTube captions); tier 3 (Haiku) later fixes only these
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from rapidfuzz import fuzz
from wordfreq import zipf_frequency

from . import config
from .intake_md import Vocab

FILLER_RE = re.compile(r"(?:(?<=^)|(?<=[\s,]))(?:um+|uh+|erm+|uhm+|hmm+|mm+)(?:[,.]?)(?=\s|$)", re.I)
REPEAT_RE = re.compile(r"\b(\w+)(?:\s+\1\b)+", re.I)
SPACES_RE = re.compile(r"\s{2,}")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]+")


def _phrase_pattern(phrase: str) -> re.Pattern:
    """Whole-phrase, case-insensitive; spaces and hyphens are interchangeable."""
    parts = [re.escape(p) for p in re.split(r"[\s\-]+", phrase.strip()) if p]
    return re.compile(r"(?<![\w-])" + r"[\s\-]+".join(parts) + r"(?![\w-])", re.I)


@dataclass
class Fix:
    before: str
    after: str
    count: int


def apply_rules(text: str, vocab: Vocab, tally: dict[tuple[str, str], int]) -> str:
    for heard, correct in vocab.corrections.items():
        text, n = _phrase_pattern(heard).subn(correct, text)
        if n:
            tally[(heard, correct)] = tally.get((heard, correct), 0) + n
    for term in vocab.terms:
        text = _phrase_pattern(term).sub(term, text)
    text = FILLER_RE.sub("", text)
    text = REPEAT_RE.sub(r"\1", text)
    text = re.sub(r"\s+([,.?!])", r"\1", text)
    text = re.sub(r"^[,\s]+", "", text)
    text = SPACES_RE.sub(" ", text).strip()
    return text[:1].upper() + text[1:] if text else text


def _known_words(vocab: Vocab) -> set[str]:
    words = set()
    for t in vocab.terms + list(vocab.corrections.values()):
        words.update(w.lower() for w in WORD_RE.findall(t))
    return words


SUFFIXES = ("ing", "ers", "er", "ed", "es", "s")


def _is_known(word: str, known: set[str]) -> bool:
    """Vocab terms count with common suffixes too: pentest -> pentesting, pentesters."""
    w = word.lower()
    if w in known:
        return True
    return any(w.endswith(suf) and w[: -len(suf)] in known for suf in SUFFIXES)


def _caption_text(captions: list[tuple[float, float, str]], start: float, end: float) -> str:
    return " ".join(t for s, e, t in captions if e > start and s < end)


def clean(transcript: dict, vocab: Vocab, captions: list[tuple[float, float, str]]) -> dict:
    known = _known_words(vocab)
    tally: dict[tuple[str, str], int] = {}
    segments, flags = [], []
    for i, seg in enumerate(transcript.get("segments", [])):
        raw = seg.get("text", "").strip()
        text = apply_rules(raw, vocab, tally)
        if not text:
            continue
        for w in seg.get("words", []):
            word = w.get("word", "").strip(".,?!\"'()")
            if len(word) <= 3 or _is_known(word, known):
                continue
            zipf = zipf_frequency(word.lower(), "en")
            score = w.get("score")
            # Alignment scores are naturally low for common words; only content words count.
            if score is not None and score < config.LOW_CONFIDENCE and zipf < config.COMMON_ZIPF:
                flags.append({"seg": i, "word": word, "start": w.get("start"), "reason": f"low confidence {score:.2f}"})
            elif word.isalpha() and zipf < config.RARE_ZIPF:
                flags.append({"seg": i, "word": word, "start": w.get("start"), "reason": "rare word"})
        if captions:
            cap = _caption_text(captions, seg["start"], seg["end"])
            if cap and len(raw) > 20:
                sim = fuzz.token_set_ratio(raw.lower(), cap.lower())
                if sim < 60:
                    flags.append({"seg": i, "word": None, "start": seg["start"],
                                  "reason": f"differs from YouTube captions ({sim:.0f}%)", "captions": cap})
        segments.append({"i": i, "start": round(seg["start"], 2), "end": round(seg["end"], 2),
                         "speaker": seg.get("speaker"), "text": text, "raw": raw})
    return {
        "segments": segments,
        "flags": flags,
        "fixes": [{"heard": h, "correct": c, "count": n} for (h, c), n in sorted(tally.items())],
    }
