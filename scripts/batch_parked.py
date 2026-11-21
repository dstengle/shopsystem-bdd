"""A parked item's lines out of a batch (capability batches r17, r18; b47): `work batch park` takes the item's lines
out of `batch-<n>` at once, in one commit citing it (`take_out`), and `work batch done` runs a task's tests in a
worktree of the task's head with every parked item's lines taken out (`tested_tree`), so that a parked item's scenario
holds up no other task. Both take the lines out as `work batch review` does (`batch_start.unlay_lines`), each item as it
was laid (`as_laid`, b324; after `work batch amend`, as it last laid it, b460): an item reshaped after its park is
taken out by the lines the batch branch holds."""
import contextlib
import re

import backlog_items
import batch_plan
import batch_start
from batch_git import GitFailed, git, is_tree, remove_tree, tree_for, trees_dir


def parked(root, batch):
    """The items of the batch's tasks that are no longer `in-batch`."""
    return [i for i in (backlog_items.find(root, t.item) for t in batch.tasks) if i.status != "in-batch"]


def as_laid(root, batch, items):
    """Each of `items` as `work batch start` laid it (batches r45, b324): its file in the base's commit that added the
    batch's plan, its ids renumbered; the item as it now reads when that commit or its file there is not found."""
    added = base_of(root, batch)
    laid = []
    for item in items:
        rel = backlog_items.rel_of(item.name)
        source = amended(root, batch, item) or added
        try:
            laid.append(backlog_items.parse(git(root, "show", "%s:%s" % (source, rel)).stdout, rel) if source else item)
        except GitFailed:
            laid.append(item)
    return laid


def base_of(root, batch):
    """The base's commit that added the batch's plan, which the batch was laid on (b479), or None."""
    added = git(root, "log", "--diff-filter=A", "--format=%H", "--", batch_plan.rel_of(batch.name)).stdout.split()
    return added[-1] if added else None


def amended(root, batch, item):
    """The base's commit named by the `Laid:` line of the latest `work batch amend` commit of the item on the batch
    branch (b460), or None."""
    try:
        body = git(root, "log", "-1", "--format=%B", "--all-match", "--grep=^Item: %s$" % item.name,
                   "--grep=^Laid: ", batch.branch, "--").stdout
    except GitFailed:
        return None
    found = re.search(r"(?m)^Laid: ([0-9a-f]{7,40})$", body)
    return found.group(1) if found else None


def take_out(root, batch, items, command):
    """`items`' lines taken out of the batch branch in its worktree (made, and removed again, when it is not there) in
    one commit citing them; none when they are out already. The branch's head before, to put it back with."""
    tree = trees_dir(root) / batch.name
    made = tree_for(root, tree, batch.branch, command)
    try:
        before = git(tree, "rev-parse", "HEAD").stdout.strip()
        changed = batch_start.unlay_lines(tree, as_laid(root, batch, items), command, base_of(root, batch))
        if changed and git(tree, "status", "--porcelain", "--", *changed).stdout.strip():
            git(tree, "add", "--", *changed)
            git(tree, "commit", "-q", "-m", "%s: the requirement lines of %s taken out\n%s" % (
                batch.name, batch_start.labels(items), batch_start.cites(items)))
        return before
    finally:
        if made:
            remove_tree(root, tree)


def put_back(root, batch, before):
    """The batch branch back at `before`, after a command that took lines out of it failed."""
    tree = trees_dir(root) / batch.name
    if is_tree(tree, batch.branch):
        git(tree, "reset", "-q", "--hard", before)
    else:
        git(root, "update-ref", "refs/heads/%s" % batch.branch, before)


@contextlib.contextmanager
def tested_tree(root, batch, task, tree, head, command):
    """The worktree to run the task's tests in: `tree` itself while no item of the batch is parked, else a detached
    worktree of `head` beside it with the parked items' lines taken out, removed afterwards."""
    items = parked(root, batch)
    if not items:
        yield tree
        return
    other = trees_dir(root) / ("%s-%s-tested" % (batch.name, task.task))
    remove_tree(root, other)
    git(root, "worktree", "add", "-q", "--detach", str(other), head)
    try:
        batch_start.unlay_lines(other, as_laid(root, batch, items), command, base_of(root, batch))
        yield other
    finally:
        remove_tree(root, other)
