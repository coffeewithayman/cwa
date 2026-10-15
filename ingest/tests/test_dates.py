from datetime import date

from cwa_ingest import dates


def no_sched(url):
    raise AssertionError(f"unexpected fetch of {url}")


def test_sched_link_wins_over_upload_date():
    info = {"title": "BSidesSF 2015 - Federating AWS CLI", "upload_date": "20231202",
            "description": "Federating AWS CLI\n\nhttps://bsidessf2015.sched.com/event/2t9Z/federating-aws-cli"}
    seen = []
    d, note = dates.talk_date(info, fetch_sched=lambda u: seen.append(u) or date(2015, 4, 20))
    assert (d, seen) == ("2015-04-20", ["https://bsidessf2015.sched.com/event/2t9Z/federating-aws-cli"])
    assert "sched" in note


def test_sched_page_text():
    page = '<div class="sched-event-details-timeandplace">Monday April 20, 2015 5:00pm - 6:00pm PDT</div>'
    assert dates.dates_in(dates.re.sub(r"<[^>]+>", " ", page)) == [date(2015, 4, 20)]


def test_date_written_in_description():
    knox = {"title": "Why We Break Things", "upload_date": "20200502",
            "description": "Recorded on May 1st, 2020 for the 6th annual BSides Knoxville"}
    ccsf = {"title": "Cloud Security and Infosec Careers", "upload_date": "20190502",
            "description": "A talk given at City College San Francisco on May 1, 2019"}
    assert dates.talk_date(knox, fetch_sched=no_sched)[0] == "2020-05-01"
    assert dates.talk_date(ccsf, fetch_sched=no_sched)[0] == "2019-05-01"


def test_news_dates_in_description_are_ignored():
    info = {"title": "Weekly news - ESW #480", "upload_date": "20261012",
            "description": "News: on March 3, 2026 a vendor announced..."}
    assert dates.talk_date(info, fetch_sched=no_sched) == ("2026-10-12", "")


def test_old_year_in_title_is_flagged():
    d, note = dates.talk_date({"title": "BSidesSF 2015 - Something", "upload_date": "20231202"}, fetch_sched=no_sched)
    assert d == "2023-12-02" and "2015" in note


def test_livestream_release_date():
    info = {"title": "Live", "upload_date": "20240110", "release_date": "20240108"}
    assert dates.talk_date(info, fetch_sched=no_sched)[0] == "2024-01-08"
