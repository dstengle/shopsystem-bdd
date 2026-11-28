"""`work batch start` (capability batches r1-r3; workflow simplification plan 4, D4-D9, D18; b874): the pick, a new
branch `batch-<n>` made at the base's HEAD with no commit of its own, each picked item applied to the specification of
its task's workspace, and the batch file with the moved items committed on the base.

Each picked item gets its task's worktree `batch-<n>-t<k>` on its branch at opening, where the specification service
applies it alone (an item it depends on picked before it applied there first), the specification is validated with it
and one commit on the task's branch keeps it (batch_applied; batches r194-r197, r202). An item whose validation fails
(a requirement of it violates a rule of severity error on its workspace, which the readiness bar's copy of `spec/`
alone could not find, b478) goes back to `shaped` naming each rule, as does one a requirement of which, retiring none,
has a scenario that already passes before it is built (batch_laid, b488), and so does each picked item that depends
on it, directly or not (batches r203, b889); no other item is applied again. Then the base
gets one commit: `plan.md` with a `pending` task for each kept item, the kept items `in-batch`, and the items given
back `shaped`. The base checkout's own `spec/` and `features/` are never written, and its branch never switched; a
failure once the branch is made removes the worktrees and branches made before it is raised again."""
import time
from pathlib import Path

import backlog_items
import backlog_lifecycle
import batch_applied
import batch_driver
import batch_pick
import batch_timings
import decision_successor
from batch_git import current_branch, git, locked, remove_tree, trees_dir
from batch_plan import Batch, Task, commit, next_name, open_batch
from plumbing import phases, shop_files
from plumbing.shop_files import Refused


def labels(items):
    return ", ".join(backlog_items.label(i) for i in items)


def _returns(root, returned):
    rels = [backlog_items.rel_of(i.name) for i, _ in returned]

    def write():
        for item, _ in returned:
            (Path(root) / backlog_items.rel_of(item.name)).write_text(backlog_items.render(item), encoding="utf-8")
    shop_files.committed(root, rels, "work batch start: no batch; %s -> shaped" % labels(i for i, _ in returned),
                        write)


def _build(root, base, pick):
    """(the batch or None, the Pick): the batch's branch made at the base's HEAD, each picked item applied to its
    task's workspace (batch_applied), the items given back reopened; the batch and its plan committed on the base once
    an item is kept. A failure removes every worktree and branch made before it is raised again."""
    batch_driver.push_prefix(root)      # a malformed `[batch] push` refused before anything is written
    batch_driver.batch_rules(root)      # and a malformed `[batch] rules`
    name = next_name(root)
    forked = git(root, "rev-parse", "HEAD").stdout.strip()
    made = []
    try:
        git(root, "branch", name, forked)
        kept, broken, left = batch_applied.applied(root, name, forked, pick.picked, made)
        for item, reasons in broken + left:         # an item depending on one reopened is reopened with it (r203)
            backlog_lifecycle.reopen(item, "returned by work batch start: %s" % "; ".join(reasons))
        pick = pick._replace(picked=[d.item for d in kept], returned=pick.returned + broken + left)
        if not kept:
            _removed(root, name, made)
            return None, pick
        with phases.phase(phases.COMMIT):
            kept = batch_applied.numbered(root, name, kept)
            batch = _committed(root, base, name, forked, kept, pick.returned)
    except BaseException:
        with phases.phase(phases.COMMIT):
            _removed(root, name, made)
        raise
    said = decision_successor.said([s for d in kept for s in d.superseded])
    batch_driver.write(root, batch, pick.picked, [u for d in kept for u in d.unwritten], said)
    return batch, pick._replace(superseded=tuple(said))


def _removed(root, name, made):
    for tree, branch in made:
        batch_applied.drop(root, tree, branch)
    for tree in trees_dir(root).glob("%s-t*" % name) if trees_dir(root).is_dir() else ():
        remove_tree(root, tree)
    if git(root, "branch", "--list", name).stdout.strip():
        git(root, "branch", "-D", name)


def _committed(root, base, name, forked, kept, returned):
    """The batch's plan, a `pending` task of each kept item on its branch, with the moved items, on the base."""
    context = shop_files.context_path(root)
    batch = Batch(name=name, ident="batch/%s/%s" % (context, name), status="building", base=base,
                  forked_from=forked, branch=name, pull_request=None,
                  tasks=[Task("t%d" % k, d.item.name, "pending", d.branch) for k, d in enumerate(kept, 1)])
    picked = [d.item for d in kept]
    for item in picked:
        backlog_lifecycle.allocate(item)
    commit(root, batch, picked + [i for i, _ in returned], "work batch start: %s %s" % (name, labels(picked)))
    return batch


def start(root):
    """(the batch or None, the Pick) of `work batch start`, under the lock; the time it took to open a batch kept as
    its opening time (b73), and the time of each of its phases (b876: plumbing.phases' stopwatch)."""
    began = time.monotonic()
    phases.started()
    try:
        return _start(root, began)
    finally:
        phases.stopped()


def _start(root, began):
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
        with phases.phase(phases.PICK):
            pick = batch_pick.pick(root)
        batch = None
        if pick.picked:
            batch, pick = _build(root, base, pick)
        if batch is not None:
            batch_timings.kept_phases(root, batch.name, phases.stopped())
            batch_timings.kept(root, batch.name, "opening", time.monotonic() - began)
            return batch, pick
        if pick.returned:
            _returns(root, pick.returned)
        return None, pick


def said(root, batch, pick):
    """What `work batch start` prints."""
    out = []
    if batch is not None:
        out.append("%s building: %s" % (batch.name, ", ".join(
            "%s %s" % (t.task, backlog_items.label(i)) for t, i in zip(batch.tasks, pick.picked))))
        out.append("batch brief: %s" % batch_driver.path(root, batch.name))
        out += list(pick.superseded)
    else:
        out.append("no batch started")
    out += ["%s -> shaped: %s" % (backlog_items.label(i), "; ".join(r)) for i, r in pick.returned]     # every rule (r181)
    out += ["%s left out: %s" % (backlog_items.label(i), r[0]) for i, r in pick.left_out]
    for item in pick.picked:
        pairs = pick.renumbered.get(item.name)
        out += ["%s renumbered: %s" % (backlog_items.label(item), ", ".join("%s -> %s" % p for p in pairs))] if pairs \
            else []
    return "\n".join(out)
