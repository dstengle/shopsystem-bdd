"""`work batch amend <item>` (batches r81-r83, b460; r198-r201, b874; r204, b889): an `in-batch` item whose lines
changed (`work line` on it, drafting r38-r40) applied again to the specification of its task's workspace and of the
task's workspace of each in-batch item depending on it, and nowhere else: the batch's own specification is rebuilt
from the base at submit (batch_rebuild).

In the task's worktree (made, and removed again, when it is not there) the paths the specification service's apply
writes are put back as the commit the batch forks from holds them, the item's new ids renumbered past that
specification's and the batch's other in-batch items', the item checked by the readiness bar over it (r96, b486) and
applied by the specification service after the in-batch items it depends on, so that every blocker's lines stay
(batch_relay; spec_apply's `apply`: its features by the workspace's own feature generator, its corpus, r199, r200), in
one commit citing the item whose `Applied:` line names that commit; the item committed on the base when its ids move.
Each in-batch item depending on it, directly or not, is applied again so in its own task's worktree, with its blockers
as the base now holds them, in a commit citing it and the amended item (r204), its task too set `running` when `done`. A line applied before with the same text keeps its place in `unbuilt:`, built or not; a new or
changed line is unbuilt, and a line the item no longer holds is gone with the put back. A `done` task is set `running`
again, so that its new lines are built. Refused, changing nothing, unless the item is `in-batch` (naming it, r83), its
batch `building` on its base, its task's branch there, the item's file committed and the task's worktree, and each
dependent's, free of uncommitted changes; refused too when the item's lines do not meet the readiness bar, or the workspace's feature
generator is unresponsive (r201, naming it). All or nothing: the base's commit is made once the worktree is applied,
and a failure after it puts it back in a commit of its own with the branch reset; a refusal is said as `work batch
amend`'s. With `--finding f<m>` (batches r125, b600), an amend that fixes an open review finding of the batch cites it
(`Finding: f<m>`), so that `work batch review`'s fix loop (batch_fix) takes the commit as the finding's; a finding the
batch holds no open one of is refused naming it. With none given, the commit cites every open finding of the amended
item (r171, b740)."""
import shutil
from pathlib import Path

import backlog_items
import batch_findings
import batch_plan
import batch_relay
from batch_git import (
    git,
    has_branch,
    is_tree,
    locked,
    remove_tree,
    tree_for,
    trees_path,
    uncommitted,
)
from batch_relay import relay  # noqa: F401  (batches_handlers_amended's too)
from batch_tasks import building, tree_of
from plumbing import shop_files
from plumbing.shop_files import Refused

COMMAND = "work batch amend"
APPLIED = "Applied: "


def _commit(tree, batch, item, changed, base, findings=(), cites=()):
    """The amendment's commit, citing the item and each review finding it is for (b600, b740), its `Applied:` line
    the commit its paths were put back as; on a dependent's task branch, citing the dependent first (`cites`)."""
    if changed:
        git(tree, "add", "-A", "--", *changed)
    git(tree, "commit", "-q", "--allow-empty", "-m", "%s: the requirement lines of %s amended\n\n%s%s%s\nItem: %s%s" % (
        batch.name, backlog_items.label(item), APPLIED, base, "".join("\nItem: %s" % c.name for c in cites), item.name,
        "".join("\nFinding: %s" % f for f in findings)))


def _followed(root, batch, item, heads, made):
    """[(task, its worktree, its item)] of each in-batch item of the batch depending on the item, directly or not
    (batches r204), its worktree made when it is not there; refused while one has uncommitted changes."""
    out = []
    for dependent in batch_relay.dependents(root, batch, item):
        task = next(t for t in batch.tasks if t.item == dependent.name)
        if not has_branch(root, task.branch):
            continue
        tree = tree_of(root, batch, task)
        loose = uncommitted(tree) if is_tree(tree, task.branch) else []
        if loose:
            raise Refused("%s: %s, which depends on %s, has uncommitted changes in %s: %s; commit them on %s first" % (
                COMMAND, backlog_items.label(dependent), backlog_items.label(item), tree, ", ".join(loose),
                task.branch))
        out.append((task, _tree(root, tree, task.branch, heads, made), dependent))
    return out


def _finding(root, batch, item, finding):
    """The open review findings of the batch an amend is for: the one given, refused naming it when the batch has no
    such open one; with none given, each open finding of the amended item (batches r171, b740)."""
    held = batch_findings.open_findings(root, batch.name)
    if finding is None:
        return [f.fid for f in held if f.item == item.name]
    if finding in {f.fid for f in held}:
        return [finding]
    raise Refused("%s: %s has no open review finding %s" % (COMMAND, batch.name, finding),
                  reason="review finding not open", names=["review finding:%s" % finding])


def _checked(root, name):
    """(the item, its batch, its task), refused unless the item is `in-batch` in a building batch."""
    item = backlog_items.find(root, name)
    if item.status != "in-batch":
        raise Refused("%s: %s is %s; %s takes an item that is in-batch" % (
            COMMAND, backlog_items.label(item), item.status, COMMAND), reason="item not in batch",
            names=["item:%s" % item.name])
    batch = batch_plan.of_item(root, item.name)
    if batch is None:
        raise Refused("%s: %s is in no batch's plan" % (COMMAND, backlog_items.label(item)),
                      reason="item not in batch", names=["item:%s" % item.name])
    batch = building(root, batch.name, COMMAND)
    task = next(t for t in batch.tasks if t.item == item.name)
    rel = backlog_items.rel_of(item.name)
    if git(root, "status", "--porcelain", "--", rel).stdout.strip():
        raise Refused("%s: %s has uncommitted changes; commit them with shop work line first" % (COMMAND, rel))
    tree = tree_of(root, batch, task)
    loose = uncommitted(tree) if is_tree(tree, task.branch) else []
    if loose:
        raise Refused("%s: %s has uncommitted changes in %s: %s; commit them on %s with `Item: %s` first" % (
            COMMAND, backlog_items.label(item), tree, ", ".join(loose), task.branch, item.name))
    return item, batch, task


def _others(root, batch, item):
    """{capability: ids} of the batch's other in-batch items, which the amended item's new ids are renumbered past."""
    taken = {}
    for task in batch.tasks:
        other = backlog_items.find(root, task.item)
        if other.name != item.name and other.status == "in-batch":
            for capability, lines in batch_relay.item_lines(other).items():
                taken.setdefault(capability, set()).update(lines)
    return taken


def amend(root, name, finding=None):
    """(the batch, the task, the branches applied on, the renumbered pairs) of `work batch amend`, under the lock: the
    item applied again in its task's worktree first, then the base's commit of the item and the plan, then the task
    branch's commit; a failure puts the branch back and, once it is made, the base's commit (b486)."""
    fresh = not trees_path(root).exists()
    with locked(root):
        item, batch, task = _checked(root, name)
        findings = _finding(root, batch, item, finding)
        if not has_branch(root, task.branch):
            raise Refused("%s: %s has no branch %s" % (COMMAND, backlog_items.label(item), task.branch))
        heads, made, laid_on, undo = {}, [], [], None
        try:
            there = _tree(root, tree_of(root, batch, task), task.branch, heads, made)
            base = batch.forked_from
            changed, pairs = relay(there, item, base, root=root, taken=_others(root, batch, item),
                                   before=batch_relay.blockers(root, batch, item))
            followed = _followed(root, batch, item, heads, made)
            reopened = [t for t in [task] + [t for t, _, _ in followed] if t.status == "done"]
            for one in reopened:
                one.status = "running"
            if pairs or reopened:
                undo = _based(root, batch, item)
            _commit(there, batch, item, changed, base, findings)
            laid_on.append(task.branch)
            for other, where, dependent in followed:     # each dependent applied again with it, as the base holds it
                changed, _ = relay(where, dependent, base, before=batch_relay.blockers(root, batch, dependent))
                _commit(where, batch, item, changed, base, cites=[dependent])
                laid_on.append(other.branch)
        except BaseException:
            for branch, (where, head) in heads.items():
                if is_tree(where, branch):
                    git(where, "reset", "-q", "--hard", head)
                    git(where, "clean", "-fdq")
                else:
                    git(root, "update-ref", "refs/heads/%s" % branch, head)
            if undo is not None:
                undo()
            for where in made:
                remove_tree(root, where)
            if fresh:            # the worktrees folder and its `.gitignore` made for this amend (U17)
                shutil.rmtree(trees_path(root), ignore_errors=True)
            raise
        for where in made:
            remove_tree(root, where)
        return batch, task, laid_on, pairs


def _tree(root, tree, branch, heads, made):
    """The branch's worktree (made, and listed in `made`, when it is not there), its head kept in `heads`."""
    if tree_for(root, tree, branch, COMMAND):
        made.append(tree)
    heads[branch] = (tree, git(tree, "rev-parse", "HEAD").stdout.strip())
    return tree


def _based(root, batch, item):
    """The plan and the item committed on the base; what puts them back as they were in a commit of its own."""
    rels = [batch_plan.rel_of(batch.name), backlog_items.rel_of(item.name)]
    was = [(Path(root) / rel).read_bytes() for rel in rels]
    batch_plan.commit(root, batch, [item], "%s: %s %s" % (COMMAND, batch.name, backlog_items.label(item)))

    def undo():
        def write():
            for rel, data in zip(rels, was):
                (Path(root) / rel).write_bytes(data)
        shop_files.committed(root, rels, "%s: %s %s undone" % (COMMAND, batch.name, backlog_items.label(item)), write)
    return undo


def said(root, batch, task, laid_on, pairs):
    """What `work batch amend` prints."""
    item = backlog_items.find(root, task.item)
    out = ["%s %s amended: applied on %s" % (batch.name, backlog_items.label(item), ", ".join(laid_on))]
    if pairs:
        out.append("%s renumbered: %s" % (backlog_items.label(item), ", ".join("%s -> %s" % p for p in pairs)))
    if task.status == "running":
        out.append("%s: %s, its worktree %s" % (task.task, task.status, tree_of(root, batch, task)))
    return "\n".join(out)
