"""cwa-ingest: run | watch | enroll | notes | compile."""

from __future__ import annotations

import argparse
import logging
import sys

from . import config


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="cwa-ingest", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="one pass: inbox, reviews, then process every talk that changed")
    run.add_argument("--only", metavar="SLUG", help="process just this talk")
    run.add_argument("--force", action="store_true", help="redo every step, ignoring the cache")
    run.add_argument("--reclean", action="store_true", help="re-apply vocab/cleanup without re-transcribing")
    sub.add_parser("watch", help="keep running; react to media/inbox and intake/*.md")
    sub.add_parser("enroll", help="build the voiceprint from intake/voiceprint.md")
    sub.add_parser("notes", help="list open notes in intake/*.md")
    sub.add_parser("compile", help="rebuild src/data/talks.json only")
    args = p.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
    for noisy in ("speechbrain", "pyannote", "urllib3", "httpx", "whisperx", "lightning", "pytorch_lightning"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    if args.cmd == "run":
        from .pipeline import run_once
        run_once(only=args.only, force=args.force, reclean=args.reclean)
    elif args.cmd == "watch":
        from .watch import watch
        watch()
    elif args.cmd == "enroll":
        from .enroll import enroll
        print(f"enrolled {enroll()} clip(s)")
    elif args.cmd == "notes":
        from .intake_md import open_notes
        notes = open_notes(config.INTAKE)
        for path, heading, note in notes:
            print(f"{config.rel(path)} · {heading}\n  - {note}")
        print(f"\n{len(notes)} open note(s)")
    elif args.cmd == "compile":
        from . import intake_md as md
        from .publish import compile_catalog
        print(f"{compile_catalog(md.parse_talks(config.TALKS_MD))} talks -> {config.rel(config.SITE_DATA)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
