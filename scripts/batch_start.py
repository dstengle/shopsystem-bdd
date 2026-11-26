"""`work batch start` (capability batches r1-r3; workflow simplification plan 4, D4-D9, D18): the pick laid on a new
branch `batch-<n>` made at the base's HEAD, and the batch file with the moved items committed on the base.

On `batch-<n>`, in its own worktree, one commit lays every picked item's lines into `spec/`, appends their ids to each
capability's `unbuilt:` and writes each service capability's feature again; it cites every item it carries. Then the
base gets one commit: `plan.md` with a `pending` task for each item, the picked items `in-batch`, and the items the
pick returned `shaped`. The base checkout's own `spec/` and `features/` are never written, and its branch never
switched; a failure once the branch is made removes its worktree and the branch before it is raised again.

Before the lay is committed, `spec check`'s rules run on the worktree once (b478): an item a requirement of which
violates a rule of severity error there, which the readiness bar's copy of `spec/` alone could not find, goes back to
`shaped` naming the rule, and the batch is laid again without it; so does an item one of whose requirements, retiring
none, has a scenario that already passes on the lay, naming the scenario (batch_laid, b488)."""
import time
from pathlib import Path

import adapter_annotate
import backlog_items
import backlog_lifecycle
import backlog_lines
import batch_catalogues
import batch_driver
import batch_generator
import batch_laid
import batch_pick
import batch_reached
import batch_timings
import decision_successor
import features_generate
import readiness_bound
import shop_files
import spec_composition
import spec_corpus_write
import spec_read
import spec_unbuilt
from batch_git import add_tree, current_branch, git, locked, remove_tree, trees_dir
from batch_plan import Batch, Task, commit, next_name, open_batch
from shop_files import Refused


def labels(items):
    return ", ".join(backlog_items.label(i) for i in items)


def cites(items):
    return "".join("\nItem: %s" % i.name for i in items)


def lay_lines(tree, picked, unwritten=None, command="work batch start", superseded=None):
    """Every picked item's lines laid into the worktree's `spec/`, their ids appended to `unbuilt:`, the feature of
    each service capability laid written again, and the bookkeeping of the lay (b333): the corpus's blocks
    (spec_corpus_write), the features and corpus blocks the lay's change of grammar 4's inputs reaches (batch_reached, b707), spec/index.md's Composition (spec_composition, b606), the adapter contracts annotated (b379) and the catalogues (batch_catalogues), a catalogue
    that cannot be written added to `unwritten`; each accepted decision a retirement leaves unenforced superseded
    (decision_successor, b741), `(item, path, old id)` added to `superseded`; a refusal said as `command`'s (b486);
    the paths changed."""
    ids, files, before = {}, [], batch_reached.digest(tree)
    for item in picked:
        backlog_lines.lay_onto(tree, item, files)
        for block in backlog_lines.read(item, backlog_items.rel_of(item.name)):
            ids.setdefault(block.capability, []).extend(r for g in block.groups for r, _ in g.requirements)
    changed = []
    for capability, listed in ids.items():
        path = backlog_lines.capability_file(tree, capability)
        path.write_text(spec_unbuilt.with_unbuilt(path.read_text(), listed))
        changed += _generated(tree, capability, command)
    changed += spec_corpus_write.write(tree, picked)
    changed += decision_successor.lay(tree, picked, superseded)
    changed += batch_reached.regenerated(tree, before, set(ids))
    changed += spec_composition.write(tree)
    changed += _annotated(tree)
    catalogues, problems = batch_catalogues.write(tree, ["%s#%s" % (c, r) for c, rs in ids.items() for r in rs])
    if unwritten is not None:
        unwritten.extend(problems)
    return list(dict.fromkeys(changed + files + catalogues))


def _annotated(tree):
    """Each adapter contract of the worktree that does not hold the requirements governing its operations written as
    `spec annotate` writes it (b379); their paths."""
    found = adapter_annotate.stale(tree)
    for rel, text in found:
        (Path(tree) / rel).write_text(text, encoding="utf-8")
    return [Path(rel).as_posix() for rel, _ in found]


def _generated(tree, capability, command):
    """The capability file's path and, for a service capability, its feature written again from it."""
    path = backlog_lines.capability_file(tree, capability)
    changed = [path.relative_to(tree).as_posix()]
    if spec_read.capability(path).frontmatter.get("group") == "guarantees":
        return changed
    try:
        text = batch_generator.generate(tree, path)     # the tree's own generator, where it holds one (b740)
    except features_generate.GenerateError as err:
        raise Refused("%s: features generate of %s failed: %s" % (command, capability, err)) from None
    feature = Path(tree) / "features" / ("%s.feature" % capability)
    feature.parent.mkdir(parents=True, exist_ok=True)
    feature.write_text(text)
    return changed + [feature.relative_to(tree).as_posix()]


def unlay_lines(tree, items, command, base=None):
    """Every item's lines taken out of the worktree's `spec/` and their ids out of `unbuilt:`, and the feature of each
    service capability changed written again (plan 4 review, B1), spec/index.md's Composition again, the operation tables as the commit `base` (the
    batch's base, b479) held them, each decision the items' lay superseded accepted again and its successor out (b741);
    the paths changed."""
    changed = []
    for item in items:
        ids = backlog_lines.ids(backlog_lines.read(item, backlog_items.rel_of(item.name)))
        for capability in backlog_lines.unlay(tree, item, changed, base):
            path = backlog_lines.capability_file(tree, capability)
            path.write_text(spec_unbuilt.without_unbuilt(
                path.read_text(), [i.split("#")[1] for i in ids if i.split("#")[0] == capability]))
            changed += _generated(tree, capability, command)
    changed += decision_successor.unlay(tree, items)
    changed += spec_composition.write(tree)
    return list(dict.fromkeys(changed))


def _returns(root, returned):
    rels = [backlog_items.rel_of(i.name) for i, _ in returned]

    def write():
        for item, _ in returned:
            (Path(root) / backlog_items.rel_of(item.name)).write_text(backlog_items.render(item), encoding="utf-8")
    shop_files.committed(root, rels, "work batch start: no batch; %s -> shaped" % labels(i for i, _ in returned),
                        write)


class _Broken(Exception):
    """The lay broke a rule: (item, reasons) of each picked item whose requirement violates one."""


def violating(tree, picked, before=frozenset()):
    """(item, reasons) of each picked item a requirement of which violates a `model.lp` rule of severity error (a code
    `v...`; `w_...` is a warning) on the laid worktree, each reason naming the requirement and the rule (b478), or of
    the bound check's (v_pb1, v_pb2) whose operation its model lines declare or its lines request, naming the operation
    or the outcome and the rule (readiness_bound, b721), or of v_m9 of a transition its line sets (b731), of those only the ones not in `before`, the worktree's before
    the lay (b725)."""
    from model_check import solve
    from model_facts import Model
    from readiness_bar import model_elements
    model = Model(tree).read()
    relations, labels = solve(model)
    bound = {(name, tuple(str(a) for a in args)) for name, args in relations
             if name in readiness_bound.KEPT} - set(before)
    found = []
    for item in picked:
        blocks = backlog_lines.read(item, backlog_items.rel_of(item.name))
        mine = set(backlog_lines.ids(blocks))
        ops = readiness_bound.operations(model_elements(blocks), model.facts, mine)
        reasons = readiness_bound.reasons(bound, ops, labels)
        reasons += readiness_bound.transitions(bound, model.facts, mine, labels)     # v_m9 of its own line (b731)
        for name, args in relations:
            short = [str(a).rsplit("/", 1)[-1] for a in args]
            for k, node in enumerate(short):
                if name.startswith("v") and node in mine:
                    others = short[:k] + short[k + 1:]
                    reasons.append("%s: %s %s%s" % (node, name, labels.get(name, ""),
                                                    ": with %s" % ", ".join(others) if others else ""))
        if reasons:
            found.append((item, list(dict.fromkeys(reasons))))
    return found


def _build(root, base, picked, returned):
    batch_driver.push_prefix(root)      # a malformed `[batch] push` refused before anything is written
    batch_driver.batch_rules(root)      # and a malformed `[batch] rules`
    name = next_name(root)
    forked = git(root, "rev-parse", "HEAD").stdout.strip()
    tree = trees_dir(root) / name
    try:
        add_tree(root, tree, name, forked)
        unwritten, superseded = [], []
        before = readiness_bound.before(tree)       # the base's unhandled outcomes are no picked item's (b725)
        changed = lay_lines(tree, picked, unwritten, superseded=superseded)
        broken = violating(tree, picked, before) or batch_laid.passing(root, tree, picked)
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
    out += ["%s -> shaped: %s" % (backlog_items.label(i), r[0]) for i, r in pick.returned]
    out += ["%s left out: %s" % (backlog_items.label(i), r[0]) for i, r in pick.left_out]
    for item in pick.picked:
        pairs = pick.renumbered.get(item.name)
        out += ["%s renumbered: %s" % (backlog_items.label(item), ", ".join("%s -> %s" % p for p in pairs))] if pairs \
            else []
    return "\n".join(out)
