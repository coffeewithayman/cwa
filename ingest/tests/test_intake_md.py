from cwa_ingest import config
from cwa_ingest import intake_md as md


def test_append_and_parse_entry(repo):
    slug = md.append_entry(config.TALKS_MD, "Breaking IN — BSides SF", {"url": "https://youtu.be/abc", "format": "talk", "status": "⏳ queued"})
    assert slug == "breaking-in-bsides-sf"
    [e] = md.parse_talks(config.TALKS_MD)
    assert e.title == "Breaking IN — BSides SF"
    assert e.get("format") == "talk" and e.get("status") == "⏳ queued"
    # duplicate titles get unique slugs
    assert md.append_entry(config.TALKS_MD, "Breaking IN — BSides SF", {}) == "breaking-in-bsides-sf-2"


def test_user_text_untouched_by_status_writes(repo):
    md.append_entry(config.TALKS_MD, "Talk", {"url": "u", "format": "", "status": "⏳ queued"})
    text = config.TALKS_MD.read_text().replace("### Notes\n", "### Notes\n- please fix the title\n")
    config.TALKS_MD.write_text(text)
    before = config.TALKS_MD.read_text()
    md.set_status(config.TALKS_MD, "talk", "✅ ingested")
    after = config.TALKS_MD.read_text()
    changed = [(a, b) for a, b in zip(before.splitlines(), after.splitlines()) if a != b]
    assert changed == [("- status: ⏳ queued <!-- managed -->", "- status: ✅ ingested <!-- managed -->")]


def test_set_field_only_if_empty_and_insert(repo):
    md.append_entry(config.TALKS_MD, "Talk", {"format": "panel", "status": "⏳"})
    assert not md.set_field(config.TALKS_MD, "talk", "format", "talk", only_if_empty=True)
    assert md.set_field(config.TALKS_MD, "talk", "ayman_speaker", "SPEAKER_01")
    lines = config.TALKS_MD.read_text().splitlines()
    i = lines.index("- ayman_speaker: SPEAKER_01")
    assert lines[i + 1].startswith("- status:")   # inserted before status


def test_renamed_heading_keeps_slug(repo):
    md.append_entry(config.TALKS_MD, "Old title", {"status": "⏳"})
    config.TALKS_MD.write_text(config.TALKS_MD.read_text().replace("## Old title", "## New title"))
    [e] = md.parse_talks(config.TALKS_MD)
    assert e.slug == "old-title" and e.title == "New title"


def test_inbox(repo):
    config.TALKS_MD.write_text(config.TALKS_MD.read_text() + "https://youtu.be/aaa\nhttps://youtu.be/bbb\n")
    assert md.inbox_items(config.TALKS_MD) == ["https://youtu.be/aaa", "https://youtu.be/bbb"]
    md.remove_from_inbox(config.TALKS_MD, "https://youtu.be/aaa")
    assert md.inbox_items(config.TALKS_MD) == ["https://youtu.be/bbb"]


def test_notes_open_and_strike(repo):
    md.append_entry(config.TALKS_MD, "Talk", {"status": "⏳"})
    t = config.TALKS_MD.read_text().replace("### Notes\n", "### Notes\n- fix title\n- ~~done already~~ ✔ x\n")
    config.TALKS_MD.write_text(t)
    notes = md.open_notes(config.INTAKE)
    assert [n for _, _, n in notes] == ["fix title"]
    md.strike_note(config.TALKS_MD, "fix title", "renamed")
    assert md.open_notes(config.INTAKE) == []
    assert "- ~~fix title~~ ✔ renamed" in config.TALKS_MD.read_text()


def test_vocab_parse_and_suggestions(repo):
    v = md.parse_vocab(config.VOCAB_MD)
    assert "CISO" in v.terms and v.corrections["sea so"] == "CISO"
    assert md.add_vocab_suggestions(config.VOCAB_MD, [("cyber ark", "CyberArk", "seen 3×"), ("sea so", "CISO", "dup")]) == 1
    config.VOCAB_MD.write_text(config.VOCAB_MD.read_text().replace('- [ ] "cyber ark"', '- [x] "cyber ark"'))
    assert md.apply_vocab_suggestions(config.VOCAB_MD) == [("cyber ark", "CyberArk")]
    assert md.parse_vocab(config.VOCAB_MD).corrections["cyber ark"] == "CyberArk"
    # struck suggestions are remembered as rejected and never re-suggested
    config.VOCAB_MD.write_text(config.VOCAB_MD.read_text() + '- ~~[ ] "pen test" → pentest~~\n')
    assert "pen test" in md.parse_vocab(config.VOCAB_MD).rejected
    assert md.add_vocab_suggestions(config.VOCAB_MD, [("pen test", "pentest", "")]) == 0


def test_speaker_review_round_trip(repo):
    md.add_speaker_review(config.SPEAKERS_MD, "esw-412", "ESW #412", "voiceprint unsure",
                          {"SPEAKER_00": "a.wav", "SPEAKER_01": "b.wav"})
    assert md.speaker_decisions(config.SPEAKERS_MD) == {}
    config.SPEAKERS_MD.write_text(config.SPEAKERS_MD.read_text().replace("- [ ] SPEAKER_01", "- [x] SPEAKER_01"))
    assert md.speaker_decisions(config.SPEAKERS_MD) == {"esw-412": "SPEAKER_01"}
    md.close_speaker_review(config.SPEAKERS_MD, "esw-412", "Ayman = SPEAKER_01")
    assert md.speaker_decisions(config.SPEAKERS_MD) == {}
    assert "## ~~ESW #412~~ ✔" in config.SPEAKERS_MD.read_text()


def test_timestamps_and_voiceprint_clips(repo):
    assert md.parse_range("39:00–1:02:00") == (2340.0, 3720.0)
    assert md.parse_range("") is None
    config.VOICEPRINT_MD.write_text(config.VOICEPRINT_MD.read_text() + "- https://youtu.be/x 1:00–3:00\n")
    [(idx, src, s, e, done)] = md.voiceprint_clips(config.VOICEPRINT_MD)
    assert (src, s, e, done) == ("https://youtu.be/x", 60.0, 180.0, False)
    md.mark_line(config.VOICEPRINT_MD, idx, "✅ enrolled")
    assert md.voiceprint_clips(config.VOICEPRINT_MD)[0][4] is True
