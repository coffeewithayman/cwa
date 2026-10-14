import os
import time

from cwa_ingest import config, inbox
from cwa_ingest import intake_md as md


def _age(path, seconds):
    t = time.time() - seconds
    os.utime(path, (t, t))


def test_recording_with_sidecar_and_duplicate(repo, monkeypatch):
    monkeypatch.setattr(config, "STABLE_SECONDS", 0)
    rec = config.INBOX / "bsides-2024.mp4"
    rec.write_bytes(b"fake video")
    (config.INBOX / "bsides-2024.md").write_text(
        "# Breaking IN — BSides SF 2024\n- format: talk\n- event: BSides SF\n- topics: careers\n\n### Notes\n- check audio at 5:00\n")
    inbox.process_inbox_files()
    [e] = md.parse_talks(config.TALKS_MD)
    assert e.title == "Breaking IN — BSides SF 2024"
    assert e.get("format") == "talk" and e.get("event") == "BSides SF"
    assert e.get("file") == "media/library/breaking-in-bsides-sf-2024.mp4"
    assert (config.LIBRARY / "breaking-in-bsides-sf-2024.mp4").exists()
    assert e.notes == ["check audio at 5:00"]
    assert not any(config.INBOX.glob("bsides-2024.*"))
    # same bytes under another name -> duplicate, no new entry
    (config.INBOX / "copy.mp4").write_bytes(b"fake video")
    inbox.process_inbox_files()
    assert len(md.parse_talks(config.TALKS_MD)) == 1
    assert any(config.FAILED.glob("copy.mp4.duplicate-of-*"))


def test_file_still_copying_is_left_alone(repo, monkeypatch):
    monkeypatch.setattr(config, "STABLE_SECONDS", 30)
    (config.INBOX / "growing.mp4").write_bytes(b"partial")
    assert inbox.process_inbox_files() is True        # still copying
    assert md.parse_talks(config.TALKS_MD) == []
    assert (config.INBOX / "growing.mp4").exists()


def test_link_list(repo, monkeypatch):
    monkeypatch.setattr(config, "STABLE_SECONDS", 0)
    added = []
    monkeypatch.setattr("cwa_ingest.pipeline.add_url", lambda u: added.append(u) or "slug")
    (config.INBOX / "links.txt").write_text("https://youtu.be/aaa\nsome text https://youtu.be/bbb\n")
    inbox.process_inbox_files()
    assert added == ["https://youtu.be/aaa", "https://youtu.be/bbb"]
    assert not (config.INBOX / "links.txt").exists()
