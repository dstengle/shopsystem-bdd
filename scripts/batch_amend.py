"""`work batch amend <item>` (batches r81-r83, b460): an `in-batch` item whose lines changed (`work line` on it,
drafting r38-r40) laid again on its batch's branch `batch-<n>` and on its task's branch, when the task has one.

On each, in its worktree (made, and removed again, when it is not there), the item's lines as last laid
(`batch_parked.as_laid`) are taken out against the batch's base (`batch_parked.base_of`, as a park takes them out:
b704) and its lines as they now read laid in (the laying service's lift and lay, laying, b611), in one commit citing the
item, whose `Laid:` line names the base's commit that holds the item as laid, so that a later park, review or amend
takes out the lines the branch holds. Its new ids are renumbered past the batch branch's (the other items' lines
laid there), the item committed on the base when they move. A line laid
before with the same text keeps its place in `unbuilt:`, built or not; a new or changed line is unbuilt, and a line
the item no longer holds leaves `unbuilt:` and the corpus. A `done` task is set `running` again, so that its new
lines are built. Refused, changing nothing, unless the item is `in-batch` (naming it, r83), its batch `building` on
its base, the item's file committed and the task's worktree free of uncommitted changes; refused too when the
item's lines, laid over the batch's workspace less its old ones, do not meet the readiness bar (r96, b486). All or
nothing: the base's commit is made once both worktrees are relaid, and a failure after it puts it back in a commit of
its own with the branches reset; a refusal is said as `work batch amend`'s. With `--finding f<m>` (batches r125,
b600), an amend that fixes an open review finding of the batch cites it (`Finding: f<m>`) in each commit, so that
`work batch review`'s fix loop (batch_fix) takes the commit as the finding's; a finding the batch holds no open one of
is refused naming it. With none given, each commit cites every open finding of the amended item (r171, b740)."""
import re
import shutil
from pathlib import Path

import backlog_items
import backlog_lines
import batch_findings
import batch_parked
import batch_plan
import laying
import readiness_bar
import shop_files
import spec_corpus_write
import spec_unbuilt
from batch_git import (
    git,
    has_branch,
    is_tree,
    locked,
    remove_tree,
    tree_for,
    trees_dir,
    trees_path,
    uncommitted,
)
from batch_tasks import building, tree_of
from shop_files import Refused

COMMAND = "work batch amend"
LAID = "Laid: "


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


def _corpus(tree, old, new):
    """The corpus blocks of the ids the item laid before and holds no more taken out; the paths changed."""
    changed = []
    for name, lines in old.items():
        path = Path(tree) / spec_corpus_write.CORPUS / ("%s.md" % name)
        gone = [i for i in lines if i not in new.get(name, {})]
        if not gone or not path.is_file():
            continue
        text = was = path.read_text()
        for ident in gone:
            text = spec_corpus_write.without_block(text, ident)
        if text != was:
            path.write_text(text)
            changed.append(path.relative_to(tree).as_posix())
    return changed


def relay(tree, old, new, renumber=False, root=None, base=None, batch=None):
    """`old`'s lines out of the worktree, against the commit `base` (the batch's base, as a park takes them out: b704),
    and `new`'s in (renumbered past the tree's first, with `renumber`), the worktree then prepared for the batch (its
    name) with `new` (b758); with `root`, `new` checked by the readiness bar over the worktree before it is laid
    (b486); the paths changed and the renumbered pairs."""
    caps = set(_lines(old)) | set(_lines(new))
    before = _unbuilt(tree, caps)
    changed = laying.changed(laying.lift(old, tree, COMMAND, base), COMMAND)
    pairs = backlog_lines.renumber(tree, new, {}) if renumber else []
    if root is not None:
        _bar(root, tree, new)
    changed += laying.changed(laying.lay(new, tree, COMMAND), COMMAND)
    changed += laying.changed(laying.prepare(tree, batch, [new], COMMAND), COMMAND)
    changed += _keep_built(tree, _lines(old), _lines(new), before)
    changed += _corpus(tree, _lines(old), _lines(new))
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


def _commit(tree, batch, item, changed, laid, findings=()):
    """The amendment's commit, citing the item and each review finding it is for (b600, b740)."""
    if changed:
        git(tree, "add", "-A", "--", *changed)
    git(tree, "commit", "-q", "--allow-empty", "-m", "%s: the requirement lines of %s amended\n\n%s%s\nItem: %s%s" % (
        batch.name, backlog_items.label(item), LAID, laid, item.name, "".join("\nFinding: %s" % f for f in findings)))


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


def amend(root, name, finding=None):
    """(the batch, the task, the branches laid on, the renumbered pairs) of `work batch amend`, under the lock: the
    lines relaid in each worktree first, then the base's commit of the item and the plan, then each branch's commit;
    a failure puts the branches back and, once it is made, the base's commit (b486)."""
    fresh = not trees_path(root).exists()
    with locked(root):
        item, batch, task = _checked(root, name)
        findings = _finding(root, batch, item, finding)
        old = batch_parked.as_laid(root, batch, [item])[0]
        base = batch_parked.base_of(root, batch)
        heads, made, laid_on, undo = {}, [], [], None
        try:
            tree = _tree(root, trees_dir(root) / batch.name, batch.branch, heads, made)
            changed, pairs = relay(tree, old, item, renumber=True, root=root, base=base,
                                  batch=batch.name)
            trees = [(tree, batch.branch, changed)]
            if has_branch(root, task.branch):
                there = _tree(root, tree_of(root, batch, task), task.branch, heads, made)
                trees.append((there, task.branch, relay(there, old, item, base=base, batch=batch.name)[0]))
            reopened = task.status == "done"
            if reopened:
                task.status = "running"
            if pairs or reopened:
                undo = _based(root, batch, item)
            laid = git(root, "rev-parse", "HEAD").stdout.strip()
            for where, branch, paths in trees:
                _commit(where, batch, item, paths, laid, findings)
                laid_on.append(branch)
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
    out = ["%s %s amended: laid on %s" % (batch.name, backlog_items.label(item), ", ".join(laid_on))]
    if pairs:
        out.append("%s renumbered: %s" % (backlog_items.label(item), ", ".join("%s -> %s" % p for p in pairs)))
    if task.status == "running" and len(laid_on) > 1:
        out.append("%s: %s, its worktree %s" % (task.task, task.status, tree_of(root, batch, task)))
    return "\n".join(out)
