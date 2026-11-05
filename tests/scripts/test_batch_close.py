"""`work batch merged` and `work batch abandon` (workflow simplification plan 4, Task 6, D13, D14): the merge of the
pull request delivers the batch's in-batch items, once gh says it is merged and its merge commit is in the base; an
abandoned batch returns its items to `ready`, its pull request closed."""
import json

import backlog_items
import batch_plan
import pytest
from backlog_testing import git, state, work
from batch_testing import gh_calls
from test_batch_review import URL, both_done  # noqa: F401  (the fixture)
from test_batch_tasks import started  # noqa: F401  (the fixture)


def statuses(repo, *names):
    return [backlog_items.find(repo, n).status for n in names]


@pytest.fixture
def reviewed(both_done):  # noqa: F811
    done = work(both_done, "batch", "review", "batch-1")
    assert done.returncode == 0, done.stderr
    return both_done


def merge(repo, where, oid=None):
    git(repo, "merge", "-q", "--no-ff", "batch-1", "-m", "merge the pull request")
    oid = oid or git(repo, "rev-parse", "HEAD").strip()
    (where / "gh-state.json").write_text(json.dumps({URL: {"state": "MERGED", "mergeCommit": {"oid": oid}}}))


def test_merged_delivers_the_in_batch_items(reviewed, batch_outside):
    merge(reviewed, batch_outside)
    done = work(reviewed, "batch", "merged", "batch-1")
    assert done.returncode == 0, done.stderr
    assert statuses(reviewed, "b1", "b2") == ["delivered", "delivered"]
    assert batch_plan.find(reviewed, "batch-1").status == "merged"
    assert git(reviewed, "log", "-1", "--format=%s").strip() == (
        'work batch merged: batch-1 -> merged; b1 "Abandon", b2 "Exit" delivered')
    assert not list((reviewed / ".shop" / "worktrees").glob("batch-1*"))
    assert git(reviewed, "branch", "--list", "batch-1-b1") == ""
    cap = (reviewed / "spec/capabilities/work-queue.md").read_text()
    assert "- [r5] " in cap and "- [r6] " in cap and "unbuilt: []" in cap
    assert git(reviewed, "status", "--porcelain") == ""


def test_merged_leaves_a_parked_item(both_done, batch_outside):  # noqa: F811
    assert work(both_done, "batch", "park", "batch-1", "b2", "--question", "Which?").returncode == 0
    assert work(both_done, "batch", "review", "batch-1").returncode == 0
    merge(both_done, batch_outside)
    assert work(both_done, "batch", "merged", "batch-1").returncode == 0
    assert statuses(both_done, "b1", "b2") == ["delivered", "needs-input"]
    assert "batch-1-b2" in git(both_done, "branch", "--list", "batch-1-b2")


def test_merged_refuses_an_open_pull_request(reviewed):
    before = state(reviewed)
    done = work(reviewed, "batch", "merged", "batch-1")
    assert done.returncode == 1 and URL in done.stderr and "OPEN" in done.stderr, done.stderr
    assert state(reviewed) == before


def test_merged_refuses_a_merge_not_pulled(reviewed, batch_outside):
    merge(reviewed, batch_outside, oid="0" * 40)
    before = state(reviewed)
    done = work(reviewed, "batch", "merged", "batch-1")
    assert done.returncode == 1 and "git pull" in done.stderr, done.stderr
    assert state(reviewed) == before and statuses(reviewed, "b1") == ["in-batch"]


def test_abandon_returns_the_items(started):  # noqa: F811
    assert work(started, "batch", "resume", "batch-1").returncode == 0
    done = work(started, "batch", "abandon", "batch-1")
    assert done.returncode == 0, done.stderr
    assert statuses(started, "b1", "b2") == ["ready", "ready"]
    assert batch_plan.find(started, "batch-1").status == "abandoned"
    assert git(started, "log", "-1", "--format=%s").strip() == (
        'work batch abandon: batch-1 -> abandoned; b1 "Abandon", b2 "Exit" -> ready')
    assert not list((started / ".shop" / "worktrees").glob("batch-1*"))
    assert "batch-1-b1" in git(started, "branch", "--list", "batch-1-b1")
    assert git(started, "status", "--porcelain") == ""


def test_abandon_closes_the_pull_request(reviewed, batch_outside, monkeypatch):
    monkeypatch.setenv("STUB_GH_FAIL", "pr close")
    before = state(reviewed)
    done = work(reviewed, "batch", "abandon", "batch-1")
    assert done.returncode == 1 and "gh pr close failed" in done.stderr, done.stderr
    assert state(reviewed) == before and batch_plan.find(reviewed, "batch-1").status == "in-review"
    monkeypatch.delenv("STUB_GH_FAIL")
    done = work(reviewed, "batch", "abandon", "batch-1")
    assert done.returncode == 0, done.stderr
    assert gh_calls(batch_outside)[-1] == ["pr", "close", URL]
    assert batch_plan.find(reviewed, "batch-1").status == "abandoned"


def test_abandon_refuses_a_merged_batch(reviewed, batch_outside):
    merge(reviewed, batch_outside)
    assert work(reviewed, "batch", "merged", "batch-1").returncode == 0
    before = state(reviewed)
    done = work(reviewed, "batch", "abandon", "batch-1")
    assert done.returncode == 1 and "batch-1 is merged" in done.stderr, done.stderr
    assert state(reviewed) == before
