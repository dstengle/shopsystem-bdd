"""A parked item (plan 4 review, B1 and S2): its requirement lines are taken out of the batch branch before the
review publishes it, so they never reach the base, and once answered it is readied and laid again by the next
batch; a park or an abandon refuses a task worktree with uncommitted work, unless `--discard`."""
import backlog_items
import batch_plan
from backlog_testing import git, state, work
from test_batch_close import merge
from test_batch_tasks import CAP, build, resumed, started, tree  # noqa: F401  (the fixture)

FEATURE = "features/work-queue.feature"


def test_a_parked_item_is_published_without_its_lines_and_laid_again(started, batch_outside):  # noqa: F811
    resumed(started)
    build(started, "t1", "b1", ["r5"])
    assert work(started, "batch", "done", "batch-1", "t1").returncode == 0
    assert work(started, "batch", "park", "batch-1", "b2", "--question", "Which?").returncode == 0
    done = work(started, "batch", "review", "batch-1")
    assert done.returncode == 0, done.stderr
    cap = git(started, "show", "origin/batch-1:%s" % CAP)
    assert "### [g4] Abandon" in cap and "Exit" not in cap and "[r6]" not in cap and "unbuilt: []" in cap, cap
    feature = git(started, "show", "origin/batch-1:%s" % FEATURE)
    assert "@r5" in feature and "@r6" not in feature
    taken = git(started, "log", "-1", "--format=%B", "--grep", "taken out", "batch-1")
    assert taken.startswith('batch-1: the requirement lines of b2 "Exit" taken out') and "Item: b2" in taken, taken
    merge(started, batch_outside)
    assert work(started, "batch", "merged", "batch-1").returncode == 0
    assert "[r6]" not in (started / CAP).read_text() and "@r6" not in (started / FEATURE).read_text()
    assert work(started, "answer", "b2", "This one.").returncode == 0
    ready = work(started, "ready", "b2")
    assert ready.returncode == 0, ready.stderr
    again = work(started, "batch", "start")
    assert again.returncode == 0, again.stderr
    assert again.stdout.splitlines()[0] == 'batch-2 building: t1 b2 "Exit"'
    assert "### [g5] Exit\n- [r6] " in git(started, "show", "batch-2:%s" % CAP)


def test_park_refuses_uncommitted_work(started):  # noqa: F811
    resumed(started)
    (tree(started, "t1") / "wip.py").write_text("half\n")
    before = state(started)
    done = work(started, "batch", "park", "batch-1", "b1", "--question", "Which?")
    assert done.returncode == 1, done.stdout
    assert "wip.py" in done.stderr and str(tree(started, "t1")) in done.stderr and "--discard" in done.stderr
    assert state(started) == before and (tree(started, "t1") / "wip.py").is_file()
    assert backlog_items.find(started, "b1").status == "in-batch"
    done = work(started, "batch", "park", "batch-1", "b1", "--question", "Which?", "--discard")
    assert done.returncode == 0, done.stderr
    assert backlog_items.find(started, "b1").status == "needs-input" and not tree(started, "t1").exists()


def test_abandon_refuses_uncommitted_work(started):  # noqa: F811
    resumed(started)
    path = tree(started, "t2") / CAP
    path.write_text(path.read_text() + "\nmine\n")
    before = state(started)
    done = work(started, "batch", "abandon", "batch-1")
    assert done.returncode == 1 and CAP in done.stderr and str(tree(started, "t2")) in done.stderr, done.stderr
    assert state(started) == before and batch_plan.find(started, "batch-1").status == "building"
    done = work(started, "batch", "abandon", "batch-1", "--discard")
    assert done.returncode == 0, done.stderr
    assert batch_plan.find(started, "batch-1").status == "abandoned"
