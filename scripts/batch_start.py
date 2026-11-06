"""`work batch start` (capability batches r1-r3; workflow simplification plan 4, D4-D9, D18): the pick laid on a new
branch `batch-<n>` made at the base's HEAD, and the batch file with the moved items committed on the base.

On `batch-<n>`, in its own worktree, one commit lays every picked item's lines into `spec/`, appends their ids to each
capability's `unbuilt:` and writes each service capability's feature again; it cites every item it carries. Then the
base gets one commit: `plan.md` with a `pending` task for each item, the picked items `in-batch`, and the items the
pick returned `shaped`. The base checkout's own `spec/` and `features/` are never written, and its branch never
switched; a failure once the branch is made removes its worktree and the branch before it is raised again."""
import contextlib
import io
from pathlib import Path

import backlog_items
import backlog_lines
import batch_driver
import batch_pick
import features_generate
import shop_files
import spec_read
import spec_unbuilt
from batch_git import add_tree, current_branch, git, locked, remove_tree, trees_dir
from batch_plan import Batch, Task, commit, next_name, open_batch
from shop_files import Refused


def labels(items):
    return ", ".join(backlog_items.label(i) for i in items)


def cites(items):
    return "".join("\nItem: %s" % i.name for i in items)


def lay_lines(tree, picked):
    """Every picked item's lines laid into the worktree's `spec/`, their ids appended to `unbuilt:`, and the feature
    of each service capability laid written again; the paths changed."""
    ids, files = {}, []
    for item in picked:
        backlog_lines.lay_onto(tree, item, files)
        for block in backlog_lines.read(item, backlog_items.rel_of(item.name)):
            ids.setdefault(block.capability, []).extend(r for g in block.groups for r, _ in g.requirements)
    changed = []
    for capability, listed in ids.items():
        path = backlog_lines.capability_file(tree, capability)
        path.write_text(spec_unbuilt.with_unbuilt(path.read_text(), listed))
        changed += _generated(tree, capability, "work batch start")
    return list(dict.fromkeys(changed + files))


def _generated(tree, capability, command):
    """The capability file's path and, for a service capability, its feature written again from it."""
    path = backlog_lines.capability_file(tree, capability)
    changed = [path.relative_to(tree).as_posix()]
    if spec_read.capability(path).frontmatter.get("group") == "guarantees":
        return changed
    try:
        with contextlib.redirect_stderr(io.StringIO()):     # the groups it skips are the bar's to name
            text = features_generate.generate(tree, path)
    except features_generate.GenerateError as err:
        raise Refused("%s: features generate of %s failed: %s" % (command, capability, err)) from None
    feature = Path(tree) / "features" / ("%s.feature" % capability)
    feature.parent.mkdir(parents=True, exist_ok=True)
    feature.write_text(text)
    return changed + [feature.relative_to(tree).as_posix()]


def unlay_lines(tree, items, command):
    """Every item's lines taken out of the worktree's `spec/` and their ids out of `unbuilt:`, and the feature of each
    service capability changed written again (plan 4 review, B1); the paths changed."""
    changed = []
    for item in items:
        ids = backlog_lines.ids(backlog_lines.read(item, backlog_items.rel_of(item.name)))
        for capability in backlog_lines.unlay(tree, item, changed):
            path = backlog_lines.capability_file(tree, capability)
            path.write_text(spec_unbuilt.without_unbuilt(
                path.read_text(), [i.split("#")[1] for i in ids if i.split("#")[0] == capability]))
            changed += _generated(tree, capability, command)
    return list(dict.fromkeys(changed))


def _returns(root, returned):
    rels = [backlog_items.rel_of(i.name) for i, _ in returned]

    def write():
        for item, _ in returned:
            (Path(root) / backlog_items.rel_of(item.name)).write_text(backlog_items.render(item), encoding="utf-8")
    shop_files.committed(root, rels, "work batch start: no batch; %s -> shaped" % labels(i for i, _ in returned),
                        write)


def _build(root, base, picked, returned):
    batch_driver.push_prefix(root)      # a malformed `[batch] push` refused before anything is written
    name = next_name(root)
    forked = git(root, "rev-parse", "HEAD").stdout.strip()
    tree = trees_dir(root) / name
    try:
        add_tree(root, tree, name, forked)
        changed = lay_lines(tree, picked)
        git(tree, "add", "--", *changed)
        git(tree, "commit", "-q", "-m", "%s: the requirement lines of %s\n%s" % (name, labels(picked), cites(picked)))
        context = shop_files.context_path(root)
        batch = Batch(name=name, ident="batch/%s/%s" % (context, name), status="building", base=base,
                      forked_from=forked, branch=name, pull_request=None,
                      tasks=[Task("t%d" % k, i.name, "pending", "%s-%s" % (name, i.name)) for k, i in enumerate(picked, 1)])
        for item in picked:
            item.status = "in-batch"
        commit(root, batch, picked + [i for i, _ in returned], "work batch start: %s %s" % (name, labels(picked)))
    except BaseException:
        remove_tree(root, tree)
        if git(root, "branch", "--list", name).stdout.strip():
            git(root, "branch", "-D", name)
        raise
    batch_driver.write(root, batch, picked)
    return batch


def start(root):
    """(the batch or None, the Pick) of `work batch start`, under the lock."""
    with locked(root):
        base = current_branch(root)
        if base is None:
            raise Refused("work batch start: the checkout is on a detached HEAD; run it on the branch the batch is to be "
                          "built from")
        loose = git(root, "status", "--porcelain", "--untracked-files=all", "--", "spec", "features").stdout
        if loose.strip():
            raise Refused("work batch start: spec/ or features/ has uncommitted changes, and the lines are laid on the "
                          "commit: %s; commit them or put them away first" % ", ".join(
                              line[3:] for line in loose.splitlines()))
        found = open_batch(root)
        if found is not None:
            raise Refused("work batch start: %s is %s; one batch is open at a time" % (found.name, found.status))
        if not any(i.status == "ready" for i in backlog_items.items(root)):
            raise Refused("work batch start: no item is ready")
        pick = batch_pick.pick(root)
        if not pick.picked:
            if pick.returned:
                _returns(root, pick.returned)
            return None, pick
        return _build(root, base, pick.picked, pick.returned), pick


def said(root, batch, pick):
    """What `work batch start` prints."""
    out = []
    if batch is not None:
        out.append("%s building: %s" % (batch.name, ", ".join(
            "%s %s" % (t.task, backlog_items.label(i)) for t, i in zip(batch.tasks, pick.picked))))
        out.append("batch brief: %s" % batch_driver.path(root, batch.name))
    else:
        out.append("no batch started")
    out += ["%s -> shaped: %s" % (backlog_items.label(i), r[0]) for i, r in pick.returned]
    out += ["%s left out: %s" % (backlog_items.label(i), r[0]) for i, r in pick.left_out]
    for item in pick.picked:
        pairs = pick.renumbered.get(item.name)
        out += ["%s renumbered: %s" % (backlog_items.label(item), ", ".join("%s -> %s" % p for p in pairs))] if pairs \
            else []
    return "\n".join(out)
