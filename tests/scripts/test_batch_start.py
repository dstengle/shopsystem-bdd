"""`work batch start` and `work batch status` (workflow simplification plan 4, Task 3, D4-D9, D18): the pick laid on
a new branch `batch-<n>` with its ids unbuilt and its scenarios generated, the batch file and the moved items
committed on the base, the person's checkout left alone, and where a batch stands printed."""
import json
import pathlib
import sys

import backlog_items
import pytest
from backlog_testing import git, state, work, write_item
from batch_testing import ready_item
from test_backlog_lines import ABANDON, FROBNICATE
from test_batch_pick import SECOND

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain


@pytest.fixture
def two(batch_repo):
    toolchain.require()
    ready_item(batch_repo, "b1", "Abandon", ABANDON, value="high-value", urgency="high-urgency", size="small")
    ready_item(batch_repo, "b2", "Exit", SECOND)
    return batch_repo


def tree(repo, rev="HEAD"):
    return git(repo, "ls-tree", "-r", "--name-only", rev, "--", "spec", "features")


def test_start_writes_the_batch_the_branch_and_the_lines(two):
    done = work(two, "batch", "start")
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines()[0] == 'batch-1 building: t1 b1 "Abandon", t2 b2 "Exit"'
    assert 'b2 "Exit" renumbered: work-queue#g4 -> work-queue#g5, work-queue#r5 -> work-queue#r6' in done.stdout
    assert sorted(git(two, "show", "--name-only", "--format=", "HEAD").split()) == [
        ".shop/backlog/b1.md", ".shop/backlog/b2.md", ".shop/batches/1/plan.md"]
    assert git(two, "log", "-1", "--format=%s").strip() == 'work batch start: batch-1 b1 "Abandon", b2 "Exit"'
    assert [backlog_items.find(two, n).status for n in ("b1", "b2")] == ["in-batch", "in-batch"]
    plan = (two / ".shop/batches/1/plan.md").read_text()
    assert "| t1 | b1 | pending | batch-1-b1 |\n| t2 | b2 | pending | batch-1-b2 |" in plan
    cap = git(two, "show", "batch-1:spec/capabilities/work-queue.md")
    assert "### [g4] Abandon\n- [r5] " in cap and "### [g5] Exit\n- [r6] " in cap and "unbuilt: [r5, r6]" in cap
    feature = git(two, "show", "batch-1:features/work-queue.feature")
    assert "@g4 @r5" in feature and "@g5 @r6" in feature
    message = git(two, "log", "-1", "--format=%B", "batch-1")
    assert message.startswith('batch-1: the requirement lines of b1 "Abandon", b2 "Exit"')
    assert "Item: b1" in message.splitlines() and "Item: b2" in message.splitlines()
    assert git(two, "rev-parse", "batch-1~1").strip() == git(two, "rev-parse", "HEAD~1").strip()
    notes = backlog_items.find(two, "b2").sections["Notes"]
    assert "work-queue#r5 -> work-queue#r6" in notes
    assert "- [r6] " in backlog_items.find(two, "b2").sections["Requirements"]


def test_start_leaves_the_checkout_and_spec_alone(two):
    """Review Focus 2."""
    (two / "notes.txt").write_text("mine\n")
    git(two, "add", "notes.txt")
    git(two, "commit", "-q", "-m", "notes")
    (two / "notes.txt").write_text("mine, edited\n")
    spec = tree(two)
    blobs = git(two, "rev-parse", "HEAD:spec", "HEAD:spec/capabilities")
    assert work(two, "batch", "start").returncode == 0
    assert (two / "notes.txt").read_text() == "mine, edited\n"
    assert git(two, "status", "--porcelain") == " M notes.txt\n"
    assert git(two, "symbolic-ref", "--short", "HEAD").strip() == "main"
    assert tree(two) == spec and git(two, "rev-parse", "HEAD:spec", "HEAD:spec/capabilities") == blobs
    assert "features/" not in git(two, "ls-tree", "-r", "--name-only", "HEAD")


def branches(repo):
    return git(repo, "branch", "--format=%(refname:short)")


def test_start_refuses_while_a_batch_is_open(two):
    assert work(two, "batch", "start").returncode == 0
    ready_item(two, "b3", "Third", ABANDON)
    before, had = state(two), branches(two)
    done = work(two, "batch", "start")
    assert done.returncode == 1 and "batch-1" in done.stderr and "building" in done.stderr, done.stderr
    assert state(two) == before and branches(two) == had


def test_start_refuses_a_detached_head(two):
    git(two, "checkout", "-q", "--detach")
    before, had = state(two), branches(two)
    done = work(two, "batch", "start")
    assert done.returncode == 1 and "detached HEAD" in done.stderr, done.stderr
    assert state(two) == before and branches(two) == had


def test_start_with_no_ready_item_is_refused(batch_repo):
    write_item(batch_repo, "b1", status="shaped")
    before = state(batch_repo)
    done = work(batch_repo, "batch", "start")
    assert done.returncode == 1 and "no item is ready" in done.stderr, done.stderr
    assert state(batch_repo) == before


def test_start_with_only_returns_commits_them(batch_repo):
    toolchain.require()
    ready_item(batch_repo, "b1", "Frobnicate", FROBNICATE)
    done = work(batch_repo, "batch", "start")
    assert done.returncode == 0, done.stderr
    assert "no batch started" in done.stdout and 'b1 "Frobnicate" -> shaped: ' in done.stdout
    assert backlog_items.find(batch_repo, "b1").status == "shaped"
    assert not (batch_repo / ".shop" / "batches").exists() and "batch-1" not in branches(batch_repo)
    assert git(batch_repo, "log", "-1", "--format=%s").strip() == 'work batch start: no batch; b1 "Frobnicate" -> shaped'


def test_status_prints_items_tasks_and_their_statuses(two):
    assert work(two, "batch", "start").returncode == 0
    done = work(two, "batch", "status", "batch-1")
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines() == [
        "batch-1 building, base main, pull request -", "plan: .shop/batches/1/plan.md",
        '  b1 "Abandon" in-batch', '  b2 "Exit" in-batch',
        '  t1 b1 "Abandon": pending, branch batch-1-b1', '  t2 b2 "Exit": pending, branch batch-1-b2']
    assert work(two, "batch", "status").stdout == done.stdout


def test_status_json_is_one_object(two):
    assert work(two, "batch", "start").returncode == 0
    done = work(two, "batch", "status", "batch-1", "--json")
    found = json.loads(done.stdout)["batch"]
    assert found["name"] == "batch-1" and found["status"] == "building" and found["pull_request"] is None
    assert found["items"][0] == {"id": "b1", "title": "Abandon", "status": "in-batch"}
    assert found["tasks"][1] == {"task": "t2", "item": "b2", "status": "pending", "branch": "batch-1-b2"}
    assert found["plan"] == ".shop/batches/1/plan.md" and found["base"] == "main"
