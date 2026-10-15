"""Short talk summaries from a local model via Ollama — no API keys anywhere.

The summary is written into the talk's entry in intake/talks.md so Ayman can
edit it; it's only generated while that field is empty. If no Ollama server is
running, one is started for this process (models live in ~/.ollama) and the
model is pulled on first use. Ollama unloads the model when idle, so it shares
the GPU with the transcription models.
"""

from __future__ import annotations

import atexit
import json
import logging
import shutil
import subprocess
import time
import urllib.error
import urllib.request

from . import config

log = logging.getLogger("cwa_ingest")

SYSTEM = """You write the short description shown under a talk in Ayman Elsawah's \
public archive of his talks, panels, interviews and podcast appearances. \
Ayman is a security leader (CISO) and educator.

You get the talk's title, show/event, format, and the transcript of what Ayman \
said (lines marked [context] are other people's questions, for orientation only).

Write 2-3 plain sentences in the third person ("Ayman explains...") covering \
the specific points and advice Ayman himself makes. Be concrete: name the \
topics, examples and recommendations he gives. Don't summarise other speakers, \
don't invent anything that isn't in the transcript, no hype, no marketing \
language, no quotation marks. Reply with the summary text only."""

_server: subprocess.Popen | None = None


def _get(path: str, timeout: float = 2) -> dict:
    with urllib.request.urlopen(config.OLLAMA_URL + path, timeout=timeout) as r:
        return json.loads(r.read())


def _post(path: str, body: dict, timeout: float) -> dict:
    req = urllib.request.Request(config.OLLAMA_URL + path, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def ensure_server() -> None:
    """Use a running Ollama, or start one for the lifetime of this process."""
    global _server
    try:
        _get("/api/version")
        return
    except (urllib.error.URLError, OSError):
        pass
    if not shutil.which("ollama"):
        raise RuntimeError("ollama isn't installed (https://ollama.com/download)")
    log.info("starting ollama serve")
    _server = subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    atexit.register(_server.terminate)
    for _ in range(60):
        time.sleep(0.5)
        try:
            _get("/api/version")
            return
        except (urllib.error.URLError, OSError):
            continue
    raise RuntimeError("ollama serve didn't come up")


def ensure_model() -> None:
    names = {m["name"] for m in _get("/api/tags").get("models", [])}
    if config.SUMMARY_MODEL in names or f"{config.SUMMARY_MODEL}:latest" in names:
        return
    log.info("pulling %s (first use; one-time download)", config.SUMMARY_MODEL)
    _post("/api/pull", {"model": config.SUMMARY_MODEL, "stream": False}, timeout=3600)


def unload_all() -> None:
    """Evict every model Ollama has loaded (it doesn't always honour keep_alive)."""
    try:
        loaded = _get("/api/ps").get("models", [])
    except (urllib.error.URLError, OSError):
        return   # no server, nothing loaded
    for m in loaded:
        try:
            _post("/api/generate", {"model": m["name"], "keep_alive": 0}, timeout=30)
            log.info("unloaded %s from the GPU", m["name"])
        except (urllib.error.URLError, OSError):
            pass


def _transcript_text(data: dict) -> str:
    lines = []
    for turn in data["turns"]:
        text = " ".join(l["text"] for l in turn["lines"])
        lines.append(f"Ayman: {text}" if turn["citable"] else f"[context] {turn['speaker']}: {text}")
    return "\n".join(lines)


def summarize(title: str, event: str, fmt: str, transcript: dict) -> str | None:
    ensure_server()
    ensure_model()
    text = _transcript_text(transcript)
    user = f"Title: {title}\nShow/event: {event or 'unknown'}\nFormat: {fmt or 'unknown'}\n\nTranscript:\n{text}"
    if fmt == "montage":
        user += ("\n\nThis is a street-interview montage: Ayman appears only for a few seconds "
                 "among other people. Write 1-2 short sentences about what he says, nothing more.")
    t = time.time()
    resp = _post("/api/chat", {
        "model": config.SUMMARY_MODEL,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
        "stream": False,
        "think": False,
        "keep_alive": 0,                         # unload right away: the GPU is needed for the next transcription
        "options": {"temperature": 0.3, "num_ctx": config.SUMMARY_CONTEXT},
    }, timeout=900)
    unload_all()
    out = " ".join(resp.get("message", {}).get("content", "").split())
    log.info("summary: %s, %d prompt tokens, %.0fs", config.SUMMARY_MODEL, resp.get("prompt_eval_count", 0), time.time() - t)
    return out or None
