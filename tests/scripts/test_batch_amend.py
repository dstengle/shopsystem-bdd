"""`work batch amend` (batches r81-r83, b460; r198, b874): an in-batch item's lines changed by `work line` applied
again on its task's branch alone, a new id renumbered past the other items', a line applied before with the same text
kept built, the batch's branch left as it was."""
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
    assert done.stdout.splitlines()[0] == 'batch-1 b1 "Abandon" amended: applied on batch-1-b1', done.stdout
    assert 'work-queue#r6 -> work-queue#r7' in done.stdout
    item = backlog_items.find(started, "b1")
    assert "- [r7] %s" % THIRD in item.sections["Requirements"]
    assert next(t.status for t in batch_plan.find(started, "batch-1").tasks) == "running"
    forked = batch_plan.find(started, "batch-1").forked_from
    assert git(started, "rev-parse", "batch-1").strip() == forked
    task = git(started, "show", "batch-1-b1:%s" % CAP)
    assert "- [r7] %s" % THIRD in task and "- [r5] " in task and "- [r6] " not in task, task
    assert unbuilt(task) == ["r7"], task
    assert "Applied: %s" % forked in git(started, "log", "-1", "--format=%B", "batch-1-b1")


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
    when the branch's commit then fails (here a commit-msg hook refusing the `Applied:` commit)."""
    resumed(started)
    build(started, "t1", "b1", ["r5"])
    assert work(started, "batch", "done", "batch-1", "t1").returncode == 0
    assert work(started, "line", "b1", "--into", "work-queue", "--group", "Abandon again", THIRD).returncode == 0
    files = [batch_plan.rel_of("batch-1"), backlog_items.rel_of("b1")]
    was = [(started / rel).read_text() for rel in files]
    heads = [git(started, "rev-parse", b).strip() for b in ("batch-1", "batch-1-b1")]
    hook = started / ".git" / "hooks" / "commit-msg"
    hook.write_text("#!/bin/sh\n! grep -q '^Applied: ' \"$1\"\n")
    hook.chmod(0o755)
    done = work(started, "batch", "amend", "b1")
    assert done.returncode == 1 and "Applied: " in done.stderr, done.stderr
    assert [(started / rel).read_text() for rel in files] == was
    assert [git(started, "rev-parse", b).strip() for b in ("batch-1", "batch-1-b1")] == heads
    assert "undone" in git(started, "log", "-1", "--format=%s")
    assert not git(started, "status", "--porcelain").strip()


def test_an_amend_puts_back_what_its_task_started_from(started):  # noqa: F811
    """b874: the apply's paths put back as the commit the task's branch was made at holds them, so a line the item no
    longer holds leaves the task's specification, and the batch's branch is never written."""
    resumed(started)
    assert work(started, "line", "b1", "--reword", "work-queue#r5", THIRD).returncode == 0
    done = work(started, "batch", "amend", "b1")
    assert done.returncode == 0, done.stderr
    task = git(started, "show", "batch-1-b1:%s" % CAP)
    item = backlog_items.find(started, "b1").sections["Requirements"]
    rid = re.search(r"- \[(r\d+)\] %s" % re.escape(THIRD), item).group(1)
    assert "- [%s] %s" % (rid, THIRD) in task and task.count("### [g") == git(
        started, "show", "batch-1:%s" % CAP).count("### [g") + 1, task
