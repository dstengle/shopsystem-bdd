"""Each picked item applied to the specification of its task's workspace at opening (batches r194-r197, r202, b874):
the task's worktree `batch-<n>-t<k>` made on its branch `batch-<n>-<item>`, from the base's commit the batch forks
from, or, of an item that depends on an item picked before it, from that item's task branch, so that the dependent's
workspace holds the lines of the item it depends on (r202; any other picked item it depends on, directly or not, is
applied there before it). There the specification service applies the item (spec_apply's `apply`), and once the apply
completed validates the specification with the item (r195: spec_apply_check's `violating`, past the workspace's
committed state); an item whose validation fails goes back `shaped` naming each rule it violates (r196), as does one a
requirement of which, retiring none, has a scenario that passes before it is built (batch_laid, b488). A validated item
is kept in one commit on its task's branch citing it (r197). An item given back takes its worktree and branch with it,
and is applied in no other task's workspace: no other item is applied again; an item picked that depends on it is left
out, `ready`. Nothing is committed on the batch's branch. The worktrees of the tasks kept are numbered in pick order
(`numbered`); an apply refused (an unresponsive feature generator) refuses the opening, naming it (`refused`). The
items whose picked dependencies are decided are applied side by side, each in a process of its own (`_wave`)."""
import concurrent.futures
import multiprocessing
import os
from collections import namedtuple

import backlog_items
import batch_laid
import spec_apply
import spec_apply_check
from batch_git import add_tree, git, has_branch, remove_tree, trees_dir
from plumbing import phases
from plumbing.shop_files import Refused

COMMAND = "work batch start"
Applied = namedtuple("Applied", "item branch tree changed unwritten superseded")


def subject(name, item):
    """The subject of the commit that keeps an item applied at opening."""
    return "%s: the requirement lines of %s" % (name, backlog_items.label(item))


def branch_of(name, item):
    return "%s-%s" % (name, item.name)


def refused(reply, command=COMMAND):
    """An apply's reply other than done refused, naming what it says (the feature generator)."""
    if reply.outcome != "done":
        raise Refused("%s: the specification service answered %s: %s" % (
            command, reply.outcome, "; ".join(e["reason"] for e in reply.errors)))
    return reply.content


def _work(root, tree, before_items, item):
    """In the task's worktree: the item applied, validated and its scenarios run; (the apply's content, the reasons
    it is given back, a refusal's text or None, the phases timed), so that it can run in a process of its own."""
    phases.started()
    try:
        spec_apply_check.keep(tree)
        with phases.phase(phases.LAY):
            content = refused(spec_apply.apply(tree, before_items + [item]))
        with phases.phase(phases.CHECK):
            found = spec_apply_check.violating(tree, [item], spec_apply_check.before(tree))
        reasons = found[0][1] if found else []
        if not reasons:
            with phases.phase(phases.SCENARIOS):
                passing = batch_laid.passing(root, tree, [item])
            reasons = passing[0][1] if passing else []
        return content, reasons, None, phases.stopped()
    except Refused as err:
        return None, [], str(err), phases.stopped()


def _worked(args):
    return _work(*args)


def _wave(root, jobs):
    """`_work` of each job ((root, tree, before items, item)), side by side in processes of their own when there is
    more than one (b874: an opening's applies run in parallel), each one's phases added with its share."""
    if len(jobs) == 1:
        timing = phases.running()
        was = phases.stopped()          # the one job times itself in this process: kept, and resumed after it
        out = [_work(*jobs[0])]
        if timing:
            phases.started()
            phases.added(was)
    else:
        context = multiprocessing.get_context("fork")
        with concurrent.futures.ProcessPoolExecutor(min(len(jobs), os.cpu_count() or 1), mp_context=context) as pool:
            out = list(pool.map(_worked, jobs))
    for _, _, _, timed in out:
        phases.added(timed, 1.0 / len(jobs))
    return out


def _kept(root, name, tree, branch, item, content):
    changed = list(dict.fromkeys(content["changed"]))
    with phases.phase(phases.COMMIT):
        if changed:
            git(tree, "add", "-A", "--", *changed)
        git(tree, "commit", "-q", "--allow-empty", "-m", "%s\n\nItem: %s" % (subject(name, item), item.name))
    return Applied(item, branch, tree, changed, content.get("unwritten", []), content.get("superseded", []))


def drop(root, tree, branch):
    """The worktree and its branch removed."""
    remove_tree(root, tree)
    if has_branch(root, branch):
        git(root, "branch", "-D", branch)


def applied(root, name, forked, picked, made):
    """([Applied] of each picked item kept, in pick order, [(item, reasons)] of each given back, [(item, reasons)] of
    each left out); each worktree and branch made listed in `made` as it is made, for the caller to remove on a
    failure. The items are applied in waves, side by side: each wave the items whose picked dependencies are all
    decided, a dependent's worktree made from its blocker's task branch once that is committed."""
    kept, held, broken, left, decided = {}, {}, [], [], set()
    names = [i.name for i in picked]
    while len(decided) < len(picked):
        wave, jobs, settled = [], [], set(decided)
        for item in picked:
            mine = _closure(item, picked)
            if item.name in decided or not set(mine) <= settled:
                continue
            decided.add(item.name)
            gone = [n for n in mine if n not in kept]
            if gone:
                left.append((item, ["it depends on %s, which work batch start gave back" % ", ".join(gone)]))
                continue
            start = kept[mine[-1]].branch if mine else forked
            before = [kept[n].item for n in mine if n not in held[mine[-1]]] if mine else []
            tree, branch = trees_dir(root) / ("%s-t%d" % (name, names.index(item.name) + 1)), branch_of(name, item)
            made.append((tree, branch))
            with phases.phase(phases.COMMIT):
                add_tree(root, tree, branch, start)
            wave.append((item, tree, branch, mine))
            jobs.append((root, tree, before, item))
        for (item, tree, branch, mine), (content, reasons, refusal, _) in zip(wave, _wave(root, jobs) if jobs else []):
            if refusal is not None:
                raise Refused(refusal)
            if reasons:
                drop(root, tree, branch)
                broken.append((item, reasons))
                continue
            kept[item.name] = _kept(root, name, tree, branch, item, content)
            held[item.name] = set(mine) | (held[mine[-1]] if mine else set()) | {item.name}
    return [kept[n] for n in names if n in kept], broken, left


def _closure(item, picked):
    """The picked items before it the item depends on, directly or not, in pick order."""
    by_name = {i.name: i for i in picked[:picked.index(item)]}
    found, todo = set(), [d for d in item.depends_on if d in by_name]
    while todo:
        n = todo.pop()
        if n not in found:
            found.add(n)
            todo += [d for d in by_name[n].depends_on if d in by_name]
    return [n for n in by_name if n in found]


def numbered(root, name, kept):
    """Each kept task's worktree moved to `batch-<n>-t<k>`, k its place among the kept; [Applied] with their trees."""
    out = []
    for k, done in enumerate(kept, 1):
        tree = trees_dir(root) / ("%s-t%d" % (name, k))
        if tree != done.tree:
            git(root, "worktree", "move", str(done.tree), str(tree))
        out.append(done._replace(tree=tree))
    return out
