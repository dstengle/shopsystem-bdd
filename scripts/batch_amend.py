"""`work batch amend <item>` (batches r81-r83, b460; r198-r201, b874): an `in-batch` item whose lines changed (`work
line` on it, drafting r38-r40) applied again to the specification of its task's workspace, and nowhere else: the
batch's own specification is rebuilt from the base at submit (batch_rebuild).

In the task's worktree (made, and removed again, when it is not there) the paths the specification service's apply
writes are put back as the commit the task's branch was made at holds them, the item's new ids renumbered past that
specification's and the batch's other in-batch items', the item checked by the readiness bar over it (r96, b486) and
applied by the specification service (spec_apply's `apply`: its features by the workspace's own feature generator, its
corpus, r199, r200), in one commit citing the item whose `Applied:` line names that commit; the item committed on the
base when its ids move. A line applied before with the same text keeps its place in `unbuilt:`, built or not; a new or
changed line is unbuilt, and a line the item no longer holds is gone with the put back. A `done` task is set `running`
again, so that its new lines are built. Refused, changing nothing, unless the item is `in-batch` (naming it, r83), its
batch `building` on its base, its task's branch there, the item's file committed and the task's worktree free of
uncommitted changes; refused too when the item's lines do not meet the readiness bar, or the workspace's feature
generator is unresponsive (r201, naming it). All or nothing: the base's commit is made once the worktree is applied,
and a failure after it puts it back in a commit of its own with the branch reset; a refusal is said as `work batch
amend`'s. With `--finding f<m>` (batches r125, b600), an amend that fixes an open review finding of the batch cites it
(`Finding: f<m>`), so that `work batch review`'s fix loop (batch_fix) takes the commit as the finding's; a finding the
batch holds no open one of is refused naming it. With none given, the commit cites every open finding of the amended
item (r171, b740)."""
import re
import shutil
from pathlib import Path

import backlog_items
import backlog_lines
import batch_applied
import batch_findings
import batch_plan
import batch_rebuild
import readiness_bar
import spec_apply
import spec_read
import spec_unbuilt
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
from batch_tasks import building, lines_commit, tree_of
from plumbing import shop_files
from plumbing.shop_files import Refused

COMMAND = "work batch amend"
APPLIED = "Applied: "


def _lines(item):
    """{capability: {r<n>: text}} of the item's requirement lines."""
    out = {}
    for block in backlog_lines.read(item, backlog_items.rel_of(item.name)):
        out.setdefault(block.capability, {}).update((r, t) for g in block.groups for r, t in g.requirements)
    return out


def _unbuilt(tree, capabilities):
    """{capability: [its `unbuilt:` ids]} of each capability file the tree holds."""
    out = {}
    for name in capabilities:
        path = Path(tree) / "spec" / "capabilities" / ("%s.md" % name)
        found = re.search(r"(?m)^unbuilt:[ \t]*\[(.*)\][ \t]*$", path.read_text()) if path.is_file() else None
        out[name] = [one.strip() for one in found.group(1).split(",") if one.strip()] if found else []
    return out


def _keep_built(tree, old, new, before):
    """Each capability's `unbuilt:` as it was before the relay, less the ids the item no longer holds, with each new
    or reworded id of the item after them; the paths changed."""
    changed = []
    for name, lines in new.items():
        path = Path(tree) / "spec" / "capabilities" / ("%s.md" % name)
        if not path.is_file():
            continue
        had, was = before.get(name, []), old.get(name, {})
        wanted = [i for i in had if i not in was or i in lines]
        wanted += [i for i in lines if i not in had and was.get(i) != lines[i]]
        text = path.read_text()
        now = spec_unbuilt.without_unbuilt(text, _unbuilt(tree, [name])[name])
        now = spec_unbuilt.with_unbuilt(now, wanted)
        if now != text:
            path.write_text(now)
            changed.append(path.relative_to(tree).as_posix())
    return changed


def _held(tree, capabilities):
    """{capability: {r<n>: text}} of the requirement lines each capability file of the tree holds."""
    out = {}
    for name in capabilities:
        path = Path(tree) / "spec" / "capabilities" / ("%s.md" % name)
        found = spec_read.capability(path) if path.is_file() else None
        out[name] = {r.id: r.text for g in (found.groups if found else []) for r in g.requirements}
    return out


def relay(tree, item, base, root=None, taken=None):
    """The item applied again to the task's worktree (batches r198-r200): the paths the apply writes put back as the
    task's starting commit `base` holds them (batch_rebuild's `taken`), its new ids renumbered past the worktree's and
    `taken`'s ({capability: ids} of the batch's other items) when it is given, checked by the readiness bar over the
    worktree with `root` (b486), applied by the specification service, and each line applied before with the same
    text kept as built as it was; the paths changed and the renumbered pairs."""
    touched = git(tree, "diff", "--name-only", base, "HEAD", "--", "spec/capabilities").stdout.split()
    caps = set(_lines(item)) | {Path(p).stem for p in touched}
    before, had = _unbuilt(tree, caps), _held(tree, caps)
    batch_rebuild.taken(tree, base, ())
    now = _held(tree, caps)
    old = {c: {r: t for r, t in lines.items() if now[c].get(r) != t} for c, lines in had.items()}
    pairs = backlog_lines.renumber(tree, item, taken) if taken is not None else []
    if root is not None:
        _bar(root, tree, item)
    changed = list(batch_applied.refused(spec_apply.apply(tree, [item], COMMAND), COMMAND)["changed"])
    changed += _keep_built(tree, old, _lines(item), before)
    return list(dict.fromkeys(changed)), pairs


def _bar(root, tree, item):
    """The item's lines checked as `work ready` checks them, the batch's workspace less the lines it laid before in
    place of `spec/` (batches r96); an item left with no line passes, its lines taken out (r90). Refused naming the
    item and the bar's reasons."""
    blocks = backlog_lines.read(item, backlog_items.rel_of(item.name))
    lined = backlog_lines.ids(blocks) or any(b.retired for b in blocks) or blocks.adapters
    reasons = (readiness_bar.unsettled(root, item) + (readiness_bar.well_formed(tree, item)[0] if lined else [])
               + readiness_bar.decision_reasons(root, blocks))
    if reasons:
        raise Refused("%s: %s does not meet the readiness bar:\n%s" % (
            COMMAND, backlog_items.label(item), "\n".join("  " + r for r in reasons)),
            reason="item not ready", names=["item:%s" % item.name])


def _commit(tree, batch, item, changed, base, findings=()):
    """The amendment's commit, citing the item and each review finding it is for (b600, b740), its `Applied:` line
    the commit its paths were put back as."""
    if changed:
        git(tree, "add", "-A", "--", *changed)
    git(tree, "commit", "-q", "--allow-empty", "-m", "%s: the requirement lines of %s amended\n\n%s%s\nItem: %s%s" % (
        batch.name, backlog_items.label(item), APPLIED, base, item.name, "".join("\nFinding: %s" % f for f in findings)))


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
            for capability, lines in _lines(other).items():
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
            base = git(root, "rev-parse", "%s^" % lines_commit(root, batch, task)).stdout.strip()
            changed, pairs = relay(there, item, base, root=root, taken=_others(root, batch, item))
            reopened = task.status == "done"
            if reopened:
                task.status = "running"
            if pairs or reopened:
                undo = _based(root, batch, item)
            _commit(there, batch, item, changed, base, findings)
            laid_on.append(task.branch)
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
