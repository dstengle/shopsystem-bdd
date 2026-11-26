"""`work batch amend` (batches r81-r83, b460): an in-batch item's lines changed by `work line` laid again on the batch
branch and its task's branch, a new id renumbered past the other items', a line laid before with the same text kept
built on the task's branch, and a later park taking out the lines the amend laid."""
import re

import backlog_items
import batch_plan
from backlog_testing import git, state, work
from test_batch_pick import THIRD
from test_batch_tasks import CAP, build, resumed, started, tree  # noqa: F401  (the fixture)


def unbuilt(text):
    return re.search(r"(?m)^unbuilt: \[(.*)\]$", text).group(1).split(", ")


def test_an_amended_item_is_laid_again_renumbered_and_its_built_lines_kept(started):  # noqa: F811
    resumed(started)
    build(started, "t1", "b1", ["r5"])
    assert work(started, "batch", "done", "batch-1", "t1").returncode == 0
    drafted = work(started, "line", "b1", "--into", "work-queue", "--group", "Abandon again", THIRD)
    assert drafted.returncode == 0, drafted.stderr
    assert "work-queue#r6" in drafted.stdout          # r6 is b2's on the batch branch
    done = work(started, "batch", "amend", "b1")
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines()[0] == 'batch-1 b1 "Abandon" amended: laid on batch-1, batch-1-b1', done.stdout
    assert 'work-queue#r6 -> work-queue#r7' in done.stdout
    item = backlog_items.find(started, "b1")
    assert "- [r7] %s" % THIRD in item.sections["Requirements"]
    assert next(t.status for t in batch_plan.find(started, "batch-1").tasks) == "running"
    lined = git(started, "show", "batch-1:%s" % CAP)
    assert "- [r7] %s" % THIRD in lined and "- [r6] " in lined and unbuilt(lined) == ["r5", "r6", "r7"], lined
    task = git(started, "show", "batch-1-b1:%s" % CAP)
    assert "- [r7] %s" % THIRD in task and unbuilt(task) == ["r6", "r7"], task
    assert "Laid: " in git(started, "log", "-1", "--format=%B", "batch-1")
    parked = work(started, "batch", "park", "batch-1", "b1", "--question", "Which?")
    assert parked.returncode == 0, parked.stderr
    left = git(started, "show", "batch-1:%s" % CAP)
    assert "[r5]" not in left and "[r7]" not in left and "- [r6] " in left and unbuilt(left) == ["r6"], left


def test_amend_refuses_an_item_not_in_batch_and_a_loose_worktree(started):  # noqa: F811
    resumed(started)
    before = state(started)
    done = work(started, "batch", "amend", "b9")
    assert done.returncode == 1
    (tree(started, "t1") / "wip.py").write_text("half\n")
    done = work(started, "batch", "amend", "b1")
    assert done.returncode == 1 and "wip.py" in done.stderr, done.stderr
    assert state(started) == before


def test_a_failed_amend_puts_back_the_bases_commit_with_the_branches(started):  # noqa: F811
    """b486: the base's commit of the plan and the item, made once the lines are relaid, is undone with the branches
    when a branch's commit then fails (here a commit-msg hook refusing the `Laid:` commits)."""
    resumed(started)
    build(started, "t1", "b1", ["r5"])
    assert work(started, "batch", "done", "batch-1", "t1").returncode == 0
    assert work(started, "line", "b1", "--into", "work-queue", "--group", "Abandon again", THIRD).returncode == 0
    files = [batch_plan.rel_of("batch-1"), backlog_items.rel_of("b1")]
    was = [(started / rel).read_text() for rel in files]
    heads = [git(started, "rev-parse", b).strip() for b in ("batch-1", "batch-1-b1")]
    hook = started / ".git" / "hooks" / "commit-msg"
    hook.write_text("#!/bin/sh\n! grep -q '^Laid: ' \"$1\"\n")
    hook.chmod(0o755)
    done = work(started, "batch", "amend", "b1")
    assert done.returncode == 1 and "Laid: " in done.stderr, done.stderr
    assert [(started / rel).read_text() for rel in files] == was
    assert [git(started, "rev-parse", b).strip() for b in ("batch-1", "batch-1-b1")] == heads
    assert "undone" in git(started, "log", "-1", "--format=%s")
    assert not git(started, "status", "--porcelain").strip()


def test_an_amend_takes_the_item_out_against_the_batchs_base(started, monkeypatch):  # noqa: F811
    """b704 f1: the amend's take-out is given the batch's base, as park's and review's are, so an import, a table or
    a model line the base held is put back as it held it."""
    import batch_amend
    import batch_parked
    import laying_inprocess
    resumed(started)
    assert work(started, "line", "b1", "--into", "work-queue", "--group", "Abandon again", THIRD).returncode == 0
    bases, unlay = [], laying_inprocess.unlay_lines
    monkeypatch.setattr(laying_inprocess, "unlay_lines",
                        lambda tree, items, command, base=None: bases.append(base) or unlay(tree, items, command, base))
    batch_amend.amend(started, "b1")
    base = batch_parked.base_of(started, batch_plan.find(started, "batch-1"))
    assert base and bases == [base, base], (bases, base)
