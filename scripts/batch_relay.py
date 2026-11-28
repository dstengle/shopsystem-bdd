"""An item applied again to a task's workspace (batches r198-r200, r204; b874, b889), which `work batch amend` makes:
the paths the specification service's apply writes put back as the commit the batch forks from holds them, then the
in-batch items the task's item depends on, directly or not (`blockers`, in task order), and the item applied there in
one apply, so that a dependent's workspace keeps every blocker's lines; a line applied before with the same text keeps
its place in `unbuilt:`, built or not (`relay`). The amended item's new ids are renumbered and checked by the
readiness bar (`bar`); each in-batch item depending on it, directly or not (`dependents`), is applied again on its
own task's workspace with the amended item among its blockers (r204)."""
import re
from pathlib import Path

import backlog_items
import backlog_lines
import batch_applied
import batch_rebuild
import readiness_bar
import spec_apply
import spec_read
import spec_unbuilt
from batch_git import git
from plumbing.shop_files import Refused

COMMAND = "work batch amend"


def item_lines(item):
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


def relay(tree, item, base, root=None, taken=None, before=()):
    """The item applied again to the task's worktree (batches r198-r200, r204): the paths the apply writes put back as
    `base` holds them (batch_rebuild's `taken`: the commit the batch forks from), its new ids renumbered past the
    worktree's and `taken`'s ({capability: ids} of the batch's other items) when it is given, checked by the readiness
    bar over the worktree with `root` (b486), applied by the specification service after the items `before` (its
    blockers), and each line applied before with the same text kept as built as it was; the paths changed and the
    renumbered pairs."""
    items = list(before) + [item]
    touched = git(tree, "diff", "--name-only", base, "HEAD", "--", "spec/capabilities").stdout.split()
    caps = {c for one in items for c in item_lines(one)} | {Path(p).stem for p in touched}
    unbuilt, had = _unbuilt(tree, caps), _held(tree, caps)
    batch_rebuild.taken(tree, base, ())
    now = _held(tree, caps)
    old = {c: {r: t for r, t in held.items() if now[c].get(r) != t} for c, held in had.items()}
    pairs = backlog_lines.renumber(tree, item, taken) if taken is not None else []
    if root is not None:
        bar(root, tree, item)
    changed = list(batch_applied.refused(spec_apply.apply(tree, items, COMMAND), COMMAND)["changed"])
    new = {}
    for one in items:
        for capability, held in item_lines(one).items():
            new.setdefault(capability, {}).update(held)
    changed += _keep_built(tree, old, new, unbuilt)
    return list(dict.fromkeys(changed)), pairs


def bar(root, tree, item):
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


def _closure(names, depends_on, among):
    """The names of `among` (in order) that the names depend on, directly or not, by `depends_on` ({name: names})."""
    found, todo = set(), [d for n in names for d in depends_on.get(n, ())]
    while todo:
        n = todo.pop()
        if n in among and n not in found:
            found.add(n)
            todo += depends_on.get(n, ())
    return [n for n in among if n in found]


def _in_batch(root, batch):
    """[item] of the batch's tasks' items that are `in-batch`, in task order."""
    found = [backlog_items.find(root, t.item) for t in batch.tasks]
    return [i for i in found if i.status == "in-batch"]


def blockers(root, batch, item):
    """[item] of the batch's in-batch items the item depends on, directly or not, in task order."""
    items = _in_batch(root, batch)
    by_name = {i.name: i for i in items}
    depends_on = dict({i.name: i.depends_on for i in items}, **{item.name: item.depends_on})
    names = _closure([item.name], depends_on, [i.name for i in items if i.name != item.name])
    return [by_name[n] for n in names]


def dependents(root, batch, item):
    """[item] of the batch's in-batch items that depend on the item, directly or not, in task order."""
    return [i for i in _in_batch(root, batch) if i.name != item.name and item.name in
            {b.name for b in blockers(root, batch, i)}]
