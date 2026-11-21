"""`work batch amend <item>` (batches r81-r83, b460): an `in-batch` item whose lines changed (`work line` on it,
drafting r38-r40) laid again on its batch's branch `batch-<n>` and on its task's branch, when the task has one.

On each, in its worktree (made, and removed again, when it is not there), the item's lines as last laid
(`batch_parked.as_laid`) are taken out and its lines as they now read laid in (`batch_start.unlay_lines`,
`lay_lines`), in one commit citing the item, whose `Laid:` line names the base's commit that holds the item as laid,
so that a later park, review or amend takes out the lines the branch holds. Its new ids are renumbered past the
batch branch's (the other items' lines laid there), the item committed on the base when they move. A line laid
before with the same text keeps its place in `unbuilt:`, built or not; a new or changed line is unbuilt, and a line
the item no longer holds leaves `unbuilt:` and the corpus. A `done` task is set `running` again, so that its new
lines are built. Refused, changing nothing, unless the item is `in-batch` (naming it, r83), its batch `building` on
its base, the item's file committed and the task's worktree free of uncommitted changes."""
import re
from pathlib import Path

import backlog_items
import backlog_lines
import batch_parked
import batch_plan
import batch_start
import spec_corpus_write
import spec_unbuilt
from batch_git import git, has_branch, is_tree, locked, remove_tree, tree_for, trees_dir, uncommitted
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


def relay(tree, old, new, renumber=False):
    """`old`'s lines out of the worktree and `new`'s in (renumbered past the tree's first, with `renumber`); the
    paths changed and the renumbered pairs."""
    caps = set(_lines(old)) | set(_lines(new))
    before = _unbuilt(tree, caps)
    changed = batch_start.unlay_lines(tree, [old], COMMAND)
    pairs = backlog_lines.renumber(tree, new, {}) if renumber else []
    changed += batch_start.lay_lines(tree, [new])
    changed += _keep_built(tree, _lines(old), _lines(new), before)
    changed += _corpus(tree, _lines(old), _lines(new))
    return list(dict.fromkeys(changed)), pairs


def _commit(tree, batch, item, changed, laid):
    if changed:
        git(tree, "add", "-A", "--", *changed)
    git(tree, "commit", "-q", "--allow-empty", "-m", "%s: the requirement lines of %s amended\n\n%s%s\nItem: %s" % (
        batch.name, backlog_items.label(item), LAID, laid, item.name))


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
        raise Refused("%s: %s has uncommitted changes; commit them with work line first" % (COMMAND, rel))
    tree = tree_of(root, batch, task)
    loose = uncommitted(tree) if is_tree(tree, task.branch) else []
    if loose:
        raise Refused("%s: %s has uncommitted changes in %s: %s; commit them on %s with `Item: %s` first" % (
            COMMAND, backlog_items.label(item), tree, ", ".join(loose), task.branch, item.name))
    return item, batch, task


def amend(root, name):
    """(the batch, the task, the branches laid on, the renumbered pairs) of `work batch amend`, under the lock."""
    with locked(root):
        item, batch, task = _checked(root, name)
        old = batch_parked.as_laid(root, batch, [item])[0]
        tree = trees_dir(root) / batch.name
        made, heads, laid_on = tree_for(root, tree, batch.branch, COMMAND), {}, []
        try:
            heads[batch.branch] = (tree, git(tree, "rev-parse", "HEAD").stdout.strip())
            changed, pairs = relay(tree, old, item, renumber=True)
            reopened = task.status == "done"
            if reopened:
                task.status = "running"
            if pairs or reopened:
                batch_plan.commit(root, batch, [item], "%s: %s %s" % (COMMAND, batch.name, backlog_items.label(item)))
            laid = git(root, "rev-parse", "HEAD").stdout.strip()
            _commit(tree, batch, item, changed, laid)
            laid_on.append(batch.branch)
            if has_branch(root, task.branch):
                laid_on.append(_task(root, batch, task, old, item, laid, heads))
        except BaseException:
            for branch, (where, head) in heads.items():
                if is_tree(where, branch):
                    git(where, "reset", "-q", "--hard", head)
                else:
                    git(root, "update-ref", "refs/heads/%s" % branch, head)
            raise
        finally:
            if made:
                remove_tree(root, tree)
        return batch, task, laid_on, pairs


def _task(root, batch, task, old, item, laid, heads):
    """The item laid again on its task's branch, in its worktree (made, and removed again, when it is not there)."""
    tree = tree_of(root, batch, task)
    made = tree_for(root, tree, task.branch, COMMAND)
    try:
        heads[task.branch] = (tree, git(tree, "rev-parse", "HEAD").stdout.strip())
        changed, _ = relay(tree, old, item)
        _commit(tree, batch, item, changed, laid)
        return task.branch
    finally:
        if made:
            remove_tree(root, tree)


def said(root, batch, task, laid_on, pairs):
    """What `work batch amend` prints."""
    item = backlog_items.find(root, task.item)
    out = ["%s %s amended: laid on %s" % (batch.name, backlog_items.label(item), ", ".join(laid_on))]
    if pairs:
        out.append("%s renumbered: %s" % (backlog_items.label(item), ", ".join("%s -> %s" % p for p in pairs)))
    if task.status == "running" and len(laid_on) > 1:
        out.append("%s: %s, its worktree %s" % (task.task, task.status, tree_of(root, batch, task)))
    return "\n".join(out)
