"""`work batch merged` and `work batch abandon` (capability batches r9, r10; workflow simplification plan 4, D13,
D14): a batch closed, in one commit on the base branch.

The person merges the pull request; `merged` records it once gh says it is `MERGED` and its merge commit is in the
base's history (else `git pull` first): every `in-batch` item `delivered`, the batch `merged`, its worktrees removed
and the merged item branches deleted. `abandon` closes the pull request when there is one, returns every `in-batch`
item to `ready` and removes the worktrees; the branches are kept. It refuses while a task worktree has uncommitted
changes, unless `--discard`; `merged` removes them as they are, their work merged. Both remove the batch brief's
folder `batch-<n>-driver` (r14) and the batch's review folders, `batch-<n>-review-<k>` beside its worktrees, whose
findings the review's record already holds (r15, r16)."""
import re
import shutil
import subprocess

import backlog_items
import batch_gh
import batch_plan
from batch_git import locked, remove_tree, trees_path
from batch_tasks import refuse_loose
from shop_files import Refused


def _items(root, batch, status):
    return [i for i in (backlog_items.find(root, t.item) for t in batch.tasks) if i.status == status]


def _open(root, name, command, statuses):
    batch = batch_plan.find(root, name)
    batch_plan.on_base(root, batch)
    if batch.status not in statuses:
        raise Refused("%s: %s is %s; %s takes a batch that is %s" % (command, batch.name, batch.status, command,
                                                                     " or ".join(statuses)))
    return batch


def _remove_trees(root, batch):
    trees = trees_path(root)
    for tree in [trees / batch.name] + [trees / ("%s-%s" % (batch.name, t.task)) for t in batch.tasks]:
        remove_tree(root, tree)
    shutil.rmtree(trees / ("%s-driver" % batch.name), ignore_errors=True)     # the batch brief (r14)
    for folder in trees.glob("%s-review-*" % batch.name):
        if re.fullmatch(r"%s-review-[1-9]\d*" % re.escape(batch.name), folder.name) and folder.is_dir():
            shutil.rmtree(folder)


def merged(root, name):
    """The batch `merged` and its in-batch items `delivered` (D13)."""
    command = "work batch merged"
    with locked(root):
        batch = _open(root, name, command, ("in-review", "awaiting-merge"))
        if not batch.pull_request:
            raise Refused("%s: %s has no pull request" % (command, batch.name))
        state, oid = batch_gh.state(root, batch.pull_request, command)
        if state != "MERGED" or not oid:
            raise Refused("%s: the pull request %s of %s is %s, not merged" % (command, batch.pull_request, batch.name,
                                                                             state))
        if subprocess.run(["git", "merge-base", "--is-ancestor", oid, "HEAD"], cwd=root,
                          capture_output=True).returncode != 0:
            raise Refused("%s: the merge commit %s of %s is not in %s here; run git pull, then %s again" % (
                command, oid[:7], batch.pull_request, batch.base, command))
        items = _items(root, batch, "in-batch")
        for item in items:
            item.status = "delivered"
        batch.status = "merged"
        batch_plan.commit(root, batch, items, "%s: %s -> merged; %s delivered" % (
            command, batch.name, ", ".join(map(backlog_items.label, items))))
        _remove_trees(root, batch)
        for task in batch.tasks:
            if task.item in {i.name for i in items}:
                subprocess.run(["git", "branch", "-q", "-d", task.branch], cwd=root, capture_output=True)
        return batch


def abandon(root, name, discard=False):
    """The batch `abandoned`, its pull request closed, its in-batch items `ready` (D14); refused while a task
    worktree has uncommitted changes, unless `discard` (S2)."""
    command = "work batch abandon"
    with locked(root):
        batch = _open(root, name, command, ("building", "in-review"))
        if not discard:
            refuse_loose(root, batch, batch.tasks, command)
        if batch.pull_request:
            batch_gh.close(root, batch.pull_request, command)
        items = _items(root, batch, "in-batch")
        for item in items:
            item.status = "ready"
        batch.status = "abandoned"
        batch_plan.commit(root, batch, items, "%s: %s -> abandoned; %s -> ready" % (
            command, batch.name, ", ".join(map(backlog_items.label, items))))
        _remove_trees(root, batch)
        return batch
