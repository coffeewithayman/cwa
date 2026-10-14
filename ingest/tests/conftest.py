import shutil
from pathlib import Path

import pytest

from cwa_ingest import config

REPO_INTAKE = Path(__file__).resolve().parents[2] / "intake"


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A throwaway copy of the intake files + media folders; config points at it."""
    intake = tmp_path / "intake"
    shutil.copytree(REPO_INTAKE, intake)
    # Start from the empty templates, not whatever real talks are in the repo.
    talks = (intake / "talks.md").read_text().split("## Inbox")[0]
    (intake / "talks.md").write_text(talks + "## Inbox\n<!-- Paste URLs here, one per line. -->\n\n")
    speakers = (intake / "speakers.md").read_text().split("\n## ")[0]
    (intake / "speakers.md").write_text(speakers + "\n")
    paths = {
        "REPO": tmp_path, "INTAKE": intake,
        "TALKS_MD": intake / "talks.md", "VOCAB_MD": intake / "vocab.md",
        "SPEAKERS_MD": intake / "speakers.md", "TAXONOMY_MD": intake / "taxonomy.md",
        "VOICEPRINT_MD": intake / "voiceprint.md",
        "MEDIA": tmp_path / "media", "INBOX": tmp_path / "media/inbox",
        "FAILED": tmp_path / "media/inbox/_failed", "LIBRARY": tmp_path / "media/library",
        "REGISTRY": tmp_path / "media/library/.registry.json",
        "CACHE": tmp_path / "cache", "META": tmp_path / "meta",
        "SITE_DATA": tmp_path / "talks.json", "SITE_TRANSCRIPTS": tmp_path / "transcripts",
    }
    for k, v in paths.items():
        monkeypatch.setattr(config, k, v)
    (tmp_path / "media/inbox").mkdir(parents=True)
    return tmp_path
