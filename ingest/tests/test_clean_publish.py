from cwa_ingest import clean, publish
from cwa_ingest.intake_md import Entry, Vocab

VOCAB = Vocab(terms=["CISO", "zero trust", "non-repudiation", "SOC 2"],
              corrections={"sea so": "CISO", "sock two": "SOC 2", "non repudiation": "non-repudiation"},
              rejected=set())


def test_rules():
    tally = {}
    out = clean.apply_rules("um, so the the sea so said uh we need Zero Trust and non repudiation for sock two.", VOCAB, tally)
    assert out == "So the CISO said we need zero trust and non-repudiation for SOC 2."
    assert tally[("sea so", "CISO")] == 1
    # whole words only
    assert clean.apply_rules("cisco routers", VOCAB, {}) == "Cisco routers"


def test_flags_low_confidence_and_captions():
    transcript = {"segments": [{"start": 0, "end": 5, "speaker": "S0", "text": "We rolled out the frobnicator yesterday",
                                "words": [{"word": "We", "score": 0.99}, {"word": "frobnicator", "score": 0.3, "start": 2}]}]}
    out = clean.clean(transcript, VOCAB, [(0, 5, "totally different words here entirely")])
    reasons = {f["reason"].split(" ")[0] for f in out["flags"]}
    assert {"low", "differs"} <= reasons


def _segs(*spk_text):
    t = 0
    out = []
    for spk, text in spk_text:
        out.append({"start": t, "end": t + 10, "speaker": spk, "text": text})
        t += 10
    return {"segments": out}


def test_scope_panel_keeps_only_ayman_plus_context():
    cleaned = _segs(("S0", "Welcome all"), ("S1", "Question for Ayman?"), ("S2", "My answer"), ("S1", "Other panelist"), ("S2", "More"))
    e = Entry("Panel", {"id": "p", "format": "panel"})
    data = publish.build_transcript(e, cleaned, "S2", offset=100)
    kinds = [(t["speaker"], t["citable"], t["context"]) for t in data["turns"]]
    assert data["scope"] == "ayman"
    assert kinds == [("Speaker 3", False, True), ("Ayman", True, False), ("Speaker 3", False, True), ("Ayman", True, False)]
    assert data["turns"][1]["start"] == 120   # offset applied


def test_scope_interview_keeps_all_but_cites_ayman_only():
    cleaned = _segs(("S0", "Host q"), ("S1", "Ayman a"))
    data = publish.build_transcript(Entry("I", {"id": "i", "format": "interview"}), cleaned, "S1", 0)
    assert data["scope"] == "all"
    assert [(t["speaker"], t["citable"]) for t in data["turns"]] == [("Host", False), ("Ayman", True)]


def test_guess_format():
    assert publish.guess_format({"A": 0.95, "B": 0.05}) == "talk"
    assert publish.guess_format({"A": 0.5, "B": 0.5}) == "interview"
    assert publish.guess_format({"A": 0.4, "B": 0.3, "C": 0.3}) == "panel"


def test_summary_prompt_marks_context():
    from cwa_ingest.enrich import _transcript_text
    data = {"turns": [
        {"speaker": "Host", "citable": False, "lines": [{"t": 0, "text": "What do you think?"}]},
        {"speaker": "Ayman", "citable": True, "lines": [{"t": 5, "text": "Use SSO."}, {"t": 7, "text": "Always."}]},
    ]}
    assert _transcript_text(data) == "[context] Host: What do you think?\nAyman: Use SSO. Always."
