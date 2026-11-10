"""`work batch reviewed` (workflow simplification plan 5, Task 3, D10, D12, D13, D15): the findings file recorded
under `.shop/batches/<n>/`, posted on the pull request, and the batch set `building` by a fix-now finding or
`awaiting-merge` by a clean review, whose pull request is marked ready for the person's merge."""
import json
import subprocess
import sys

import backlog_items
import batch_findings
import batch_plan
import pytest
from backlog_testing import SCRIPTS, git, state, work
from batch_testing import commit_on, gh_calls
from review_testing import (
    CLEAN,
    FIX_NOW_B1,
    URL,
    findings,
    head,
    ok,
    published,
    scratch,
)


@pytest.fixture
def briefed(batch_repo):
    published(batch_repo)
    ok(work(batch_repo, "batch", "brief", "batch-1"))
    return batch_repo


def reviewed(repo, text):
    findings(repo).write_text(text)
    return work(repo, "batch", "reviewed", "batch-1")


def record(repo, k=1):
    rel = batch_findings.rel_of("batch-1", k)
    return batch_findings.parse((repo / rel).read_text(), rel)


@pytest.mark.requirement("pr-review#r13")
def test_r13_a_fix_now_finding_sends_the_batch_back_to_building(briefed, batch_outside):
    done = ok(reviewed(briefed, FIX_NOW_B1))
    assert batch_plan.find(briefed, "batch-1").status == "building"
    assert git(briefed, "show", "--name-only", "--format=", "HEAD").split() == [
        ".shop/batches/1/plan.md", ".shop/batches/1/review-1.md"]
    assert git(briefed, "log", "-1", "--format=%s").strip() == (
        'work batch reviewed: batch-1 review 1 -> building; open f1 b1 "Abandon"')
    r = record(briefed)
    assert r.result == "fix-now" and [f.fid for f in r.findings] == ["f1", "f2"] and r.head == head(briefed)
    calls = gh_calls(batch_outside)
    assert calls[-1][:3] == ["pr", "comment", URL] and calls[-1][3] == "--body-file"
    assert not [c for c in calls if c[:2] == ["pr", "ready"]]
    assert done.stdout.splitlines() == [
        "batch-1 review 1: 2 findings, 1 fix now -> building",
        '  open f1 Important b1 "Abandon" src/b1.txt:1: abandon leaves the initiative started']


@pytest.mark.requirement("pr-review#r15")
def test_r15_a_clean_review_awaits_the_merge(briefed, batch_outside):
    done = ok(reviewed(briefed, CLEAN))
    assert batch_plan.find(briefed, "batch-1").status == "awaiting-merge"
    assert record(briefed).result == "clean" and gh_calls(batch_outside)[-1] == ["pr", "ready", URL]
    assert done.stdout.strip() == ("batch-1 review 1: 0 findings -> awaiting-merge; the pull request %s is ready for "
                                   "the person's merge" % URL)
    git(briefed, "merge", "-q", "--no-ff", "batch-1", "-m", "merge the pull request")
    (batch_outside / "gh-state.json").write_text(json.dumps(
        {URL: {"state": "MERGED", "mergeCommit": {"oid": head(briefed, "HEAD")}}}))
    ok(work(briefed, "batch", "merged", "batch-1"))
    assert [backlog_items.find(briefed, n).status for n in ("b1", "b2")] == ["delivered", "delivered"]


def test_reviewed_refuses_a_batch_that_is_building(briefed):
    ok(reviewed(briefed, FIX_NOW_B1))
    again = work(briefed, "batch", "reviewed", "batch-1")
    assert again.returncode == 1 and "work batch reviewed: batch-1 is building" in again.stderr, again.stderr


def test_reviewed_refuses_without_a_findings_file(briefed):
    before = state(briefed)
    done = work(briefed, "batch", "reviewed", "batch-1")
    assert done.returncode == 1 and str(scratch(briefed) / "brief.md") in done.stderr and "pr-reviewer" in done.stderr
    assert state(briefed) == before


MALFORMED = {"grade": FIX_NOW_B1.replace("### Important fix now", "### Major fix now"),
             "triage": FIX_NOW_B1.replace("### Important fix now", "### Important later"),
             "item": FIX_NOW_B1.replace("- item: b1", "- item: b9")}


@pytest.mark.parametrize("case", sorted(MALFORMED))
def test_reviewed_refuses_a_malformed_findings_file(briefed, batch_outside, case):
    """Review Focus 1."""
    before, calls = state(briefed), gh_calls(batch_outside)
    done = reviewed(briefed, MALFORMED[case])
    assert done.returncode == 1 and "findings.md" in done.stderr, done.stderr
    assert done.stderr.startswith("work: work batch reviewed: batch-1: "), done.stderr
    assert state(briefed) == before and gh_calls(batch_outside) == calls
    assert batch_plan.find(briefed, "batch-1").status == "in-review"


def test_reviewed_refuses_without_a_brief(briefed):
    """Review M6: a findings file with no brief is refused as that, not as a moved branch."""
    (scratch(briefed) / "brief.md").unlink()
    before = state(briefed)
    done = reviewed(briefed, CLEAN)
    assert done.returncode == 1 and "has no brief %s" % (scratch(briefed) / "brief.md") in done.stderr, done.stderr
    assert "moved" not in done.stderr and "run work batch brief batch-1" in done.stderr
    assert state(briefed) == before


def test_one_finding_is_said_in_the_singular(briefed):
    """Review M4."""
    one = CLEAN.replace("None.", "### Minor observation: a note\n- item: -\n- where: -\nA note.")
    assert ok(reviewed(briefed, one)).stdout.startswith("batch-1 review 1: 1 finding -> awaiting-merge")


def test_reviewed_refuses_a_stale_brief(briefed, batch_outside):
    """Review Focus 2."""
    commit_on(briefed, "batch-1", "src/late.txt", "late\n", "late\n\nItem: b1")
    before, calls = state(briefed), gh_calls(batch_outside)
    done = reviewed(briefed, CLEAN)
    assert done.returncode == 1 and "work batch brief" in done.stderr, done.stderr
    assert state(briefed) == before and gh_calls(batch_outside) == calls
    assert not (briefed / batch_findings.rel_of("batch-1", 1)).exists()


@pytest.mark.parametrize("fail, text", [("pr comment", FIX_NOW_B1), ("pr ready", CLEAN)], ids=["comment", "ready"])
def test_a_failing_gh_records_nothing(briefed, monkeypatch, fail, text):
    """Review Focus 5."""
    monkeypatch.setenv("STUB_GH_FAIL", fail)
    before = state(briefed)
    done = reviewed(briefed, text)
    assert done.returncode == 1 and "gh %s failed" % fail in done.stderr, done.stderr
    assert batch_plan.find(briefed, "batch-1").status == "in-review" and state(briefed) == before
    assert not (briefed / batch_findings.rel_of("batch-1", 1)).exists()
    monkeypatch.delenv("STUB_GH_FAIL")
    ok(work(briefed, "batch", "reviewed", "batch-1"))
    assert (briefed / batch_findings.rel_of("batch-1", 1)).is_file()


def test_model_check_takes_the_review_record(briefed):
    ok(reviewed(briefed, FIX_NOW_B1))
    done = subprocess.run([sys.executable, str(SCRIPTS / "model"), "--root", str(briefed), "check"],
                          capture_output=True, text=True, timeout=120)
    assert done.returncode != 2, done.stdout + done.stderr
    assert "review-1.md" not in done.stdout + done.stderr


def test_status_shows_the_reviews(briefed):
    assert "reviews: none" in ok(work(briefed, "batch", "status", "batch-1")).stdout
    ok(reviewed(briefed, FIX_NOW_B1))
    said = ok(work(briefed, "batch", "status", "batch-1")).stdout
    assert 'reviews: 1, last fix-now; open f1 b1 "Abandon"' in said
    data = json.loads(ok(work(briefed, "batch", "status", "batch-1", "--json")).stdout)["batch"]
    assert data["reviews"] == [{"review": 1, "result": "fix-now", "findings": ["f1", "f2"]}]
    assert data["open"] == ["f1"]
