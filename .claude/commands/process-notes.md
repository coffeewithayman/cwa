---
description: Work through Ayman's open notes in intake/*.md, apply each one, and strike it through
---

Process every open note in the intake files.

1. Run `npm run notes` to list open notes (bullets under a `### Notes` heading that aren't `~~struck~~`).
2. For each note, figure out what it asks for and do it:
   - **Metadata** (title, format, date, event, category, topics, clip): edit the entry's field in
     `intake/talks.md`. A title change means editing the `## ` heading (the `id` stays the same).
   - **Transcript wording at a timestamp** ("at 14:20 I said SOC 2, transcript has sock two"):
     if it's a recurring mis-hearing, add a row to the Corrections table in `intake/vocab.md`;
     if it's a one-off, edit that line in `src/content/transcripts/<slug>.json` directly.
   - **Speaker mix-ups**: set `ayman_speaker:` on the entry (see `ingest/cache/<slug>/speakers.json`
     for the labels and scores).
   - **Re-run requests**: `npm run ingest -- --only <slug>` (add `--reclean` after vocab changes,
     `--force` to start over).
3. Verify the change took effect (re-read the field / transcript line, or check the entry's status).
4. Strike the note through in place, keeping Ayman's original wording:
   `- ~~<original note>~~ ✔ <what you did> <YYYY-MM-DD>`
5. If a note is ambiguous or can't be done, don't strike it. Add an indented reply under it:
   `  - ↳ <question or reason> (<YYYY-MM-DD>)`

Never rewrite or delete Ayman's text other than wrapping a handled note in `~~ ~~`.
Finish with a short summary: which notes were handled, which still need him.
