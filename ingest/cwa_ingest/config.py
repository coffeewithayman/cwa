"""Paths, settings and secrets shared by the ingest pipeline."""

from __future__ import annotations

import os
from pathlib import Path

INGEST_DIR = Path(__file__).resolve().parent.parent
REPO = INGEST_DIR.parent

INTAKE = REPO / "intake"
TALKS_MD = INTAKE / "talks.md"
VOCAB_MD = INTAKE / "vocab.md"
SPEAKERS_MD = INTAKE / "speakers.md"
TAXONOMY_MD = INTAKE / "taxonomy.md"
VOICEPRINT_MD = INTAKE / "voiceprint.md"

MEDIA = REPO / "media"
INBOX = MEDIA / "inbox"
FAILED = INBOX / "_failed"
LIBRARY = MEDIA / "library"
REGISTRY = LIBRARY / ".registry.json"     # sha256 -> slug, catches re-dropped files

CACHE = INGEST_DIR / "cache"              # per-talk audio, raw transcripts, state (gitignored)
META = INGEST_DIR / "meta"                # per-talk source metadata (committed)
VOICEPRINT_DIR = INGEST_DIR / "voiceprint"

SITE_DATA = REPO / "src" / "data" / "talks.json"
SITE_TRANSCRIPTS = REPO / "src" / "content" / "transcripts"

def _load_dotenv() -> None:
    env = INGEST_DIR / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"'))


_load_dotenv()

MEDIA_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".m4a", ".mp3", ".wav", ".flac"}
LIST_EXTS = {".txt", ".md"}
STABLE_SECONDS = 30                        # a dropped file must stop growing this long

# --- transcription (accuracy over speed) ------------------------------------
DEVICE = os.environ.get("CWA_DEVICE", "cuda")          # "cpu" only for quick tests
# CWA_PROFILE=low-vram is for 6 GB cards (e.g. RTX 3050): int8 weights, batch 1,
# and each model is unloaded before the next stage runs. Measured peak on a
# 99-minute episode: ~3.6 GB (default profile needs ~9 GB). Set it in ingest/.env.
LOW_VRAM = os.environ.get("CWA_PROFILE") == "low-vram"
WHISPER_MODEL = os.environ.get("CWA_WHISPER_MODEL", "large-v3")
COMPUTE_TYPE = os.environ.get("CWA_COMPUTE") or (
    "int8" if DEVICE == "cpu" else "int8_float16" if LOW_VRAM else "float16")
GPU_MIN_FREE_GB = float(os.environ.get("CWA_MIN_FREE_GB") or (4.0 if LOW_VRAM else 8))
# pyannote's shipped config uses batches of 32, which needs ~11 GB of VRAM for
# no speed gain (measured: 4 is as fast and needs <1 GB). Results are identical.
ALIGN_SLICE = int(os.environ.get("CWA_ALIGN_SLICE") or 50)   # segments aligned per call
DIARIZATION_BATCH = int(os.environ.get("CWA_DIAR_BATCH") or 4)
WHISPER_ASR_OPTIONS = {"beam_size": 5, "best_of": 5, "condition_on_previous_text": False}
WHISPER_BATCH_SIZE = int(os.environ.get("CWA_BATCH") or (1 if LOW_VRAM else 8))
DIARIZATION_MODEL = "pyannote/speaker-diarization-community-1"

# --- speaker identification ---------------------------------------------------
# Cosine similarity of ECAPA embeddings to the enrolled voiceprint. Starting
# values; tune them on the first ~10 talks Ayman confirms by hand.
VOICE_ACCEPT = 0.55
VOICE_MARGIN = 0.15
# Recordings from these YouTube channels are Ayman's own: strong "it's him" context.
OWN_CHANNELS = ("@coffeewithayman",)
SOLO_SHARE = 0.85          # one speaker holding this much talk time = solo talk
MIN_SPEAKER_SHARE = 0.03   # ignore diarization crumbs below this share
CONTEXT_SECONDS = 30       # question kept before each of Ayman's answers on panels

# --- summaries (local model via Ollama; no API keys) ---------------------------
OLLAMA_URL = os.environ.get("OLLAMA_HOST_URL", "http://localhost:11434")
SUMMARY_MODEL = os.environ.get("CWA_SUMMARY_MODEL") or ("qwen3:4b" if LOW_VRAM else "qwen3:14b")
SUMMARY_CONTEXT = int(os.environ.get("CWA_SUMMARY_CTX") or (16384 if LOW_VRAM else 32768))

# --- cleanup ------------------------------------------------------------------
LOW_CONFIDENCE = 0.5       # aligned word score below this gets flagged
RARE_ZIPF = 2.0            # wordfreq zipf below this (and not a vocab term) gets flagged
COMMON_ZIPF = 4.5          # words more common than this are never flagged for low confidence




def hf_token() -> str | None:
    """HF_TOKEN from the env / ingest/.env, else the token saved by `hf auth login`."""
    if os.environ.get("HF_TOKEN"):
        return os.environ["HF_TOKEN"]
    from huggingface_hub import get_token
    return get_token()


def rel(path: Path) -> str:
    """Path relative to the repo, for writing into the Markdown files."""
    try:
        return str(path.resolve().relative_to(REPO))
    except ValueError:
        return str(path)
