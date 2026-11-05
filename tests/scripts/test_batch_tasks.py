"""`work batch resume`, `done` and `park` (workflow simplification plan 4, Task 4, D10, D12, D15-D18): one task an
item in its worktree, carried on from any session, done when its ids are built and its tests pass, parked with a
question while the rest of the batch builds."""
import pathlib
import re
import subprocess
import sys

import backlog_items
import batch_plan
import pytest
from backlog_testing import SCRIPTS, git, state, work
from batch_testing import commit_on, ready_item
from test_backlog_lines import ABANDON
from test_batch_pick import SECOND

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

CAP = "spec/capabilities/work-queue.md"


@pytest.fixture
def started(batch_repo):
    toolchain.require()
    ready_item(batch_repo, "b1", "Abandon", ABANDON, value="high-value", urgency="high-urgency", size="small")
    ready_item(batch_repo, "b2", "Exit", SECOND)
    done = work(batch_repo, "batch", "start")
    assert done.returncode == 0, done.stderr
    return batch_repo


def tree(repo, task):
    return repo / ".shop" / "worktrees" / ("batch-1-%s" % task)


def tasks(repo):
    return {t.task: t.status for t in batch_plan.find(repo, "batch-1").tasks}


def resumed(repo):
    done = work(repo, "batch", "resume", "batch-1")
    assert done.returncode == 0, done.stderr
    return done


def build(repo, task, item, ids):
    """In the task's worktree: `ids` taken out of `unbuilt:`, committed citing the item."""
    path = tree(repo, task) / CAP
    text = path.read_text()
    listed = re.search(r"(?m)^unbuilt: \[(.*)\]$", text).group(1).split(", ")
    path.write_text(text.replace("unbuilt: [%s]" % ", ".join(listed),
                                 "unbuilt: [%s]" % ", ".join(r for r in listed if r not in ids)))
    git(tree(repo, task), "commit", "-q", "-am", "build %s" % item, "-m", "Item: %s" % item)


def test_resume_makes_worktrees_and_runs_pending_tasks(started):
    lines = git(started, "rev-parse", "batch-1").strip()
    done = resumed(started)
    assert tasks(started) == {"t1": "running", "t2": "running"}
    for task, item in (("t1", "b1"), ("t2", "b2")):
        assert git(tree(started, task), "symbolic-ref", "--short", "HEAD").strip() == "batch-1-%s" % item
        assert git(tree(started, task), "rev-parse", "HEAD").strip() == lines
    assert git(started, "log", "-1", "--format=%s").strip().startswith("work batch resume: batch-1")
    assert git(started, "show", "--name-only", "--format=", "HEAD").split() == [".shop/batches/1/plan.md"]
    out = done.stdout.splitlines()
    assert out[0] == "batch-1 building: plan .shop/batches/1/plan.md"
    assert out[1] == ('t1 b1 "Abandon": running in %s on batch-1-b1: build work-queue#r5; then work batch done '
                      'batch-1 t1, or work batch park batch-1 b1 --question <text>' % tree(started, "t1"))
    before = state(started)
    again = resumed(started)
    assert state(started) == before and again.stdout == done.stdout


def test_resume_recreates_a_lost_worktree_with_its_commits(started):
    """Review Focus 5."""
    resumed(started)
    sha = commit_on(started, "batch-1-b1", "src/b1.txt", "half\n", "half of b1\n\nItem: b1")
    git(started, "worktree", "remove", "--force", str(tree(started, "t1")))
    git(started, "worktree", "prune")
    resumed(started)
    assert git(tree(started, "t1"), "rev-parse", "HEAD").strip() == sha
    assert git(tree(started, "t1"), "symbolic-ref", "--short", "HEAD").strip() == "batch-1-b1"
    assert tasks(started)["t1"] == "running"


def test_resume_asks_nothing(started):
    done = subprocess.run([sys.executable, str(SCRIPTS / "work"), "--root", str(started), "batch", "resume", "batch-1"],
                          stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=60)
    assert done.returncode == 0, done.stderr
    assert not [line for line in (done.stdout + done.stderr).splitlines() if line.rstrip().endswith("?")]


def test_done_marks_the_task_done(started):
    resumed(started)
    build(started, "t1", "b1", ["r5"])
    done = work(started, "batch", "done", "batch-1", "t1")
    assert done.returncode == 0, done.stderr
    assert tasks(started) == {"t1": "done", "t2": "running"}
    assert git(started, "log", "-1", "--format=%s").strip() == 'work batch done: batch-1 t1 b1 "Abandon"'
    assert tree(started, "t1").is_dir()


def failing_tests(repo):
    (repo / ".shop" / "delivery.toml").write_text("[batch]\ntests = \"python3 -c 'import sys; sys.exit(3)'\"\n")
    git(repo, "commit", "-q", "-am", "failing tests")


CASES = {
    "pending": (lambda repo: None, 't1 b1 "Abandon" is pending'),
    "uncommitted": (lambda repo: (tree(repo, "t1") / "loose.txt").write_text("x\n"), "loose.txt"),
    "shop": (lambda repo: commit_on(repo, "batch-1-b1", ".shop/backlog/b1.md", "x\n", "edit\n\nItem: b1"),
             ".shop/backlog/b1.md"),
    "uncited": (lambda repo: commit_on(repo, "batch-1-b1", "src/x.txt", "x\n", "no trailer"), '"no trailer"'),
    "unbuilt": (lambda repo: None, "work-queue#r5"),
    "tests": (failing_tests, "exit 3"),
}


@pytest.mark.parametrize("case", sorted(CASES))
def test_done_refuses(started, case):
    if case != "pending":
        resumed(started)
    if case not in ("pending", "unbuilt"):
        build(started, "t1", "b1", ["r5"])
    make, named = CASES[case]
    make(started)
    plan = (started / ".shop/batches/1/plan.md").read_text()
    before = state(started)
    done = work(started, "batch", "done", "batch-1", "t1")
    assert done.returncode == 1, (done.stdout, done.stderr)
    assert named in done.stderr, done.stderr
    if case == "uncited":
        assert re.search(r"[0-9a-f]{7} \"no trailer\"", done.stderr), done.stderr
    if case == "tests":
        assert "python3 -c 'import sys; sys.exit(3)'" in done.stderr
    assert (started / ".shop/batches/1/plan.md").read_text() == plan and state(started) == before


def test_two_dones_at_once_both_land(started):
    """Review Focus 1."""
    resumed(started)
    build(started, "t1", "b1", ["r5"])
    build(started, "t2", "b2", ["r6"])
    head = git(started, "rev-parse", "HEAD").strip()
    procs = [subprocess.Popen([sys.executable, str(SCRIPTS / "work"), "--root", str(started), "batch", "done",
                               "batch-1", t], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
             for t in ("t1", "t2")]
    results = [p.communicate(timeout=120) + (p.returncode,) for p in procs]
    assert [r[2] for r in results] == [0, 0], results
    assert tasks(started) == {"t1": "done", "t2": "done"}
    assert len(git(started, "rev-list", "%s..HEAD" % head).split()) == 2


def test_park_parks_the_item_and_keeps_the_rest(started):
    resumed(started)
    done = work(started, "batch", "park", "batch-1", "b1", "--question", "Which reading?")
    assert done.returncode == 0, done.stderr
    item = backlog_items.find(started, "b1")
    assert item.status == "needs-input" and item.question == "Which reading?"
    assert "parked from batch-1; its work is on branch batch-1-b1" in item.sections["Notes"]
    assert tasks(started) == {"t1": "pending", "t2": "running"}
    assert not tree(started, "t1").exists() and "batch-1-b1" in git(started, "branch", "--list", "batch-1-b1")
    assert batch_plan.find(started, "batch-1").status == "building"
    again = resumed(started)
    assert tasks(started)["t1"] == "pending" and 't1 b1 "Abandon": parked (needs-input)' in again.stdout


def abandoned(repo):
    path = repo / ".shop/batches/1/plan.md"
    path.write_text(path.read_text().replace("status: building", "status: abandoned"))
    git(repo, "commit", "-q", "-am", "abandoned by hand")


@pytest.mark.parametrize("args, named", [
    (("resume", "batch-1"), "abandoned"),
    (("done", "batch-1", "t1"), "abandoned"),
    (("park", "batch-1", "b1", "--question", "Q"), "abandoned"),
])
def test_moves_refuse_the_wrong_status(started, args, named):
    abandoned(started)
    before = state(started)
    done = work(started, "batch", *args)
    assert done.returncode == 1 and "batch-1" in done.stderr and named in done.stderr, done.stderr
    assert state(started) == before


def test_park_refuses_an_item_not_in_the_batch(started):
    ready_item(started, "b3", "Third", ABANDON)
    before = state(started)
    done = work(started, "batch", "park", "batch-1", "b3", "--question", "Q")
    assert done.returncode == 1 and 'b3 "Third"' in done.stderr and "batch-1" in done.stderr, done.stderr
    assert state(started) == before


def test_batch_commands_refuse_off_the_base_branch(started):
    resumed(started)
    build(started, "t1", "b1", ["r5"])
    git(started, "checkout", "-q", "-b", "elsewhere")
    before = state(started)
    for args in (("resume", "batch-1"), ("done", "batch-1", "t1"), ("park", "batch-1", "b2", "--question", "Q")):
        done = work(started, "batch", *args)
        assert done.returncode == 1, (args, done.stderr)
        assert "batch-1 is built from main; run it on main, not elsewhere" in done.stderr, done.stderr
    assert state(started) == before
