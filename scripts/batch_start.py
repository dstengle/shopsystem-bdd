"""`work batch start` (capability batches r1-r3; workflow simplification plan 4, D4-D9, D18): the pick laid on a new
branch `batch-<n>` made at the base's HEAD, and the batch file with the moved items committed on the base.

On `batch-<n>`, in its own worktree, the batch's workspace, each picked item is laid by the laying service, a driven
port (laying, b611: its lines into `spec/`, their ids into `unbuilt:`), the workspace prepared for the batch once
every lay is done (b758: the features written again, the corpus, the catalogues, the Composition), and each item
checked there; one commit then keeps the lay, citing every item it carries. Then the
base gets one commit: `plan.md` with a `pending` task for each item, the picked items `in-batch`, and the items the
pick returned `shaped`. The base checkout's own `spec/` and `features/` are never written, and its branch never
switched; a failure once the branch is made removes its worktree and the branch before it is raised again.

Before the lay is committed (batches r179-r181, r184): an item whose check the laying service fails (a requirement
of it violates a rule of severity error on the laid workspace, which the readiness bar's copy of `spec/` alone could
not find, b478) goes back to `shaped` naming each rule its failure names, and the batch is laid again without it; so does an item one of whose requirements, retiring
none, has a scenario that already passes on the lay, naming the scenario (batch_laid, b488)."""
import time
from pathlib import Path

import backlog_items
import backlog_lifecycle
import batch_driver
import batch_laid
import batch_pick
import batch_timings
import decision_successor
import laying
import shop_files
from batch_git import add_tree, current_branch, git, locked, remove_tree, trees_dir
from batch_plan import Batch, Task, commit, next_name, open_batch
from shop_files import Refused


def labels(items):
    return ", ".join(backlog_items.label(i) for i in items)


def cites(items):
    return "".join("\nItem: %s" % i.name for i in items)


def _returns(root, returned):
    rels = [backlog_items.rel_of(i.name) for i, _ in returned]

    def write():
        for item, _ in returned:
            (Path(root) / backlog_items.rel_of(item.name)).write_text(backlog_items.render(item), encoding="utf-8")
    shop_files.committed(root, rels, "work batch start: no batch; %s -> shaped" % labels(i for i, _ in returned),
                        write)


class _Broken(Exception):
    """The lay broke a rule: (item, reasons) of each picked item whose requirement violates one."""


def _laid(tree, name, picked):
    """Each picked item laid in the batch's workspace by the laying service (batches r179), the workspace prepared for
    the batch once every lay is done (r188), and each item checked there on prepare's reply (r180, r189: one check
    answers both): (the paths changed, the catalogues not written, the decisions superseded, (item, reasons) of each
    item whose check it failed, naming each rule, r181)."""
    changed, broken = [], []
    for item in picked:
        changed += laying.changed(laying.lay(item, tree))
    reply = laying.prepare(tree, name, picked)
    changed += laying.changed(reply)
    unwritten, superseded = reply.content.get("unwritten", []), reply.content.get("superseded", [])
    for item in picked:
        reply = laying.check(item, tree)
        if reply.outcome == "failed":
            broken.append((item, laying.reasons(reply)))
        elif reply.outcome != "done":
            laying.changed(reply)
    return list(dict.fromkeys(changed)), unwritten, superseded, broken


def _build(root, base, picked, returned):
    batch_driver.push_prefix(root)      # a malformed `[batch] push` refused before anything is written
    batch_driver.batch_rules(root)      # and a malformed `[batch] rules`
    name = next_name(root)
    forked = git(root, "rev-parse", "HEAD").stdout.strip()
    tree = trees_dir(root) / name
    try:
        add_tree(root, tree, name, forked)
        changed, unwritten, superseded, broken = _laid(tree, name, picked)
        broken = broken or batch_laid.passing(root, tree, picked)
        if broken:
            raise _Broken(broken)
        if changed:                 # a pick of chore items only lays no line (b316): the commit is still made
            git(tree, "add", "--", *changed)
        git(tree, "commit", "-q", "--allow-empty", "-m", "%s: the requirement lines of %s\n%s" % (
            name, labels(picked), cites(picked)))
        context = shop_files.context_path(root)
        batch = Batch(name=name, ident="batch/%s/%s" % (context, name), status="building", base=base,
                      forked_from=forked, branch=name, pull_request=None,
                      tasks=[Task("t%d" % k, i.name, "pending", "%s-%s" % (name, i.name)) for k, i in enumerate(picked, 1)])
        for item in picked:
            backlog_lifecycle.allocate(item)
        commit(root, batch, picked + [i for i, _ in returned], "work batch start: %s %s" % (name, labels(picked)))
    except BaseException:
        remove_tree(root, tree)
        if git(root, "branch", "--list", name).stdout.strip():
            git(root, "branch", "-D", name)
        raise
    said = decision_successor.said(superseded)
    batch_driver.write(root, batch, picked, unwritten, said)
    return batch, said


def start(root):
    """(the batch or None, the Pick) of `work batch start`, under the lock; the time it took to open a batch kept as
    its opening time (b73)."""
    began = time.monotonic()
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
        while pick.picked:
            try:
                batch, said = _build(root, base, pick.picked, pick.returned)
                batch_timings.kept(root, batch.name, "opening", time.monotonic() - began)
                return batch, pick._replace(superseded=tuple(said))
            except _Broken as err:          # laid again without the items whose lines broke a rule (b478)
                broken = err.args[0]
            for item, reasons in broken:
                backlog_lifecycle.reopen(item, "returned by work batch start: %s" % "; ".join(reasons))
            gone = {i.name for i, _ in broken}
            pick = pick._replace(picked=[i for i in pick.picked if i.name not in gone],
                                 returned=pick.returned + broken)
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
