"""`work batch review` (capability batches r7, r8, r11-r13; workflow simplification plan 4, D5, D10, D11): the batch
published as one pull request.

Under the lock: every task of an `in-batch` item must be `done`, and every commit on their branches since the lines
commit must cite its item (or an earlier in-batch item, whose branch it merged) and leave `.shop/` alone. Then, in the
batch's worktree, the specification is rebuilt from the batch's base with every in-batch item applied in task order,
in one commit citing them (batch_rebuild, reviews r17-r20, b874: a parked item applied nowhere), each in-batch item's
branch is merged into `batch-<n>` with `--no-ff` in task order, each after the ones before, the paths the apply writes
kept as the rebuild holds them with what the task changed there after its last apply, a change that does not merge
refused naming the path (batch_merge) (a parked item's branch never is, so its commits stay out), the
tests run there (the ids a failed run names kept under the batch's name, batch_rerun, for the poll's `fix task`:
batch_broken, b696, with each task branch's head as submitted, so that a later commit reads as a fix, b713), the branch is pushed to the base's remote, and a draft pull request is created through gh unless the
batch has one already (plan 5's fix loop pushes only, once each commit since the last review cites an open finding
and each open finding has a commit: `batch_fix.check`). Last, the batch is `in-review` with its pull request,
committed on the base. A refusal while merging, testing, pushing or creating puts `batch-<n>` (and the remote's) back
where it was and commits nothing."""
import shutil
import subprocess

import backlog_items
import batch_base_merge
import batch_broken
import batch_fix
import batch_merge
import batch_plan
import batch_rebuild
import batch_timings
from batch_git import (
    git,
    locked,
    push,
    remote,
    remote_head,
    remove_tree,
    tree_for,
    trees_dir,
    trees_path,
)
from batch_tasks import (
    building,
    citable,
    item_ids,
    lines_commit,
    task_label,
    tests_pass,
    uncited,
    under_shop,
)
from plumbing import batch_gh
from plumbing.shop_files import Refused

COMMAND = "work batch review"


def title(batch, items):
    return "%s: %s" % (batch.name, "; ".join(i.title for i in items))


def body(root, batch):
    """The pull request's body (D11): each in-batch item with its requirement ids, each parked one named."""
    lines = ["The %s batch: each item's requirement lines are built, its generated scenarios its acceptance tests."
             % batch.name, ""]
    for task in batch.tasks:
        item = backlog_items.find(root, task.item)
        if item.status == "in-batch":
            lines.append("- %s: %s" % (backlog_items.label(item), ", ".join(item_ids(root, item))))
        else:
            lines.append("- parked: %s (%s)" % (backlog_items.label(item), item.status))
    return "\n".join(lines) + "\n"


def checked(root, batch):
    """The tasks of the in-batch items, once each is done and its commits are as the review wants (r12, r13)."""
    tasks = [(t, backlog_items.find(root, t.item)) for t in batch.tasks]
    mine = [(t, i) for t, i in tasks if i.status == "in-batch"]
    late = ["%s: %s: %s is %s, not done" % (COMMAND, batch.name, task_label(root, t), t.status)
            for t, _ in mine if t.status != "done"]
    if late:
        raise Refused("\n".join(late))
    if not mine:
        raise Refused("%s: %s has no item that is in-batch" % (COMMAND, batch.name))
    for task, item in mine:
        since = lines_commit(root, batch, task)
        shop = under_shop(root, since, task.branch)
        if shop:
            raise Refused("%s: %s: a commit on %s changes %s, which only the base branch's batch commands change" % (
                COMMAND, task_label(root, task), task.branch, ", ".join(shop)))
        bare = uncited(root, since, task.branch, citable(root, batch, task))
        if bare:
            raise Refused("%s: %s: a commit on %s cites no item (an `Item: %s` line): %s" % (
                COMMAND, task_label(root, task), task.branch, item.name, "; ".join(bare)))
    return mine


def _merge(root, tree, batch, task, item, mine, owned):
    """The item's branch merged after the ones before it; a conflict left names the other items whose branches
    conflict with it (reviews r8)."""
    others = [(backlog_items.label(i), t.branch) for t, i in mine if t.branch != task.branch]
    try:
        batch_merge.merge(tree, task.branch, "%s: %s\n\nItem: %s" % (batch.name, backlog_items.label(item), item.name),
                          backlog_items.label(item), others, owned,
                          lines_commit(root, batch, task, last=True))     # its own changes kept (review f1)
        batch_merge.built(tree, task.branch, item_ids(root, item))     # a line its task built after an amend (b600)
    except Refused as refused:
        raise Refused("%s: %s: %s into %s" % (COMMAND, task_label(root, task), refused, batch.branch)) from None


def _put_back(root, tree, before, name, branch, remote_before, pushed):
    git(tree, "reset", "-q", "--hard", before)
    if pushed:
        target = ("+%s:refs/heads/%s" % (remote_before, branch)) if remote_before else ":refs/heads/%s" % branch
        subprocess.run(["git", "push", "-q", name, target], cwd=root, capture_output=True)


def review(root, name):
    """The pull request's URL (r8): the batch merged, tested, pushed and published, and `in-review`."""
    with locked(root):
        if batch_plan.find(root, name).status == "awaiting-merge":     # its branch merged its base (b492)
            return batch_base_merge.resubmit(root, batch_plan.find(root, name), COMMAND, tests_pass)
        batch = building(root, name, COMMAND)
        mine = checked(root, batch)
        batch_fix.check(root, batch, mine, COMMAND)     # a batch with a recorded review: its fixes (plan 5, D11)
        fresh = not trees_path(root).is_dir()
        tree = trees_dir(root) / batch.name
        try:
            made = tree_for(root, tree, batch.branch, COMMAND)
        except BaseException:
            if fresh:
                shutil.rmtree(trees_path(root), ignore_errors=True)
            raise
        before = git(tree, "rev-parse", "HEAD").stdout.strip()
        where = remote(root, batch.base)
        remote_before, pushed = remote_head(root, where, batch.branch), False
        try:
            owned = batch_rebuild.rebuild(root, tree, batch, list({i.name: i for _, i in mine}.values()),
                                          [(t.branch, item_ids(root, i)) for t, i in mine], COMMAND)   # r17-r20
            for task, item in mine:
                _merge(root, tree, batch, task, item, mine, owned)
            batch_broken.submitted(root, batch, [t for t, _ in mine])      # a later commit a fix (b713)
            with batch_timings.timed(root, batch.name, "review"):       # the test run's duration (b73)
                tests_pass(root, tree, "%s: %s" % (COMMAND, batch.name), key=batch.name)   # its failures kept (b696)
            push(root, where, batch.branch, COMMAND)
            pushed = True
            url = batch.pull_request or batch_gh.create(
                root, batch.base, batch.branch, title(batch, [i for _, i in mine]), body(root, batch), COMMAND)
        except BaseException:
            _put_back(root, tree, before, where, batch.branch, remote_before, pushed)
            if made:        # the worktree (and its directory) this review made, so the checkout is as it was
                remove_tree(root, tree)
            if fresh:
                shutil.rmtree(trees_path(root), ignore_errors=True)
            raise
        batch.status, batch.pull_request = "in-review", url
        batch_plan.commit(root, batch, [], "%s: %s -> in-review %s" % (COMMAND, batch.name, url))
        return url
