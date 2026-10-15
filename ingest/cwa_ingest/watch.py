"""Long-running watcher: media/inbox/ and intake/*.md trigger a pipeline pass.

Runs as a systemd user service (see ingest/systemd/). One worker thread does
all the processing, so the GPU only ever has one talk on it.
"""

from __future__ import annotations

import logging
import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from . import config, pipeline

log = logging.getLogger("cwa_ingest")

DEBOUNCE = 3.0          # let editors finish saving
RESCAN = 60.0           # periodic pass catches anything the events missed


class _Trigger(FileSystemEventHandler):
    def __init__(self, wake: threading.Event):
        self.wake = wake

    def on_any_event(self, event):
        path = str(getattr(event, "dest_path", "") or event.src_path)
        name = path.rsplit("/", 1)[-1]
        if name.startswith(".") or "/_failed" in path or path.endswith("~"):
            return
        # Our own writes to intake/*.md also fire events; the next pass is a cheap no-op.
        self.wake.set()


def _notify(summary: str) -> None:
    import shutil
    import subprocess
    if shutil.which("notify-send"):
        subprocess.run(["notify-send", "Talks ingest", summary], check=False)


def watch() -> None:
    for d in (config.INBOX, config.INTAKE):
        d.mkdir(parents=True, exist_ok=True)
    wake = threading.Event()
    observer = Observer()
    observer.schedule(_Trigger(wake), str(config.INBOX), recursive=False)
    observer.schedule(_Trigger(wake), str(config.INTAKE), recursive=False)
    observer.start()
    log.info("watching %s and %s", config.rel(config.INBOX), config.rel(config.INTAKE))
    wake.set()
    try:
        while True:
            wake.wait(timeout=RESCAN)
            time.sleep(DEBOUNCE)
            wake.clear()
            before = {e.slug: e.get("status") for e in pipeline.md.parse_talks(config.TALKS_MD)}
            try:
                pipeline.run_once()
            except Exception:  # noqa: BLE001 - keep the service alive
                log.exception("pass failed")
            after = {e.slug: e.get("status") for e in pipeline.md.parse_talks(config.TALKS_MD)}
            for slug, st in after.items():
                if st != before.get(slug) and st[:1] in {"✅", "👤", "⚠"}:
                    _notify(f"{slug}: {st}")
            # files still copying: look again once they've had time to settle
            if any(p.is_file() and not p.name.startswith(".") for p in config.INBOX.iterdir()):
                threading.Timer(config.STABLE_SECONDS + 1, wake.set).start()
    finally:
        observer.stop()
        observer.join()
