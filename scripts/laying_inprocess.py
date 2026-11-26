"""The in-process adapter of the laying service (b611; decision 0125), the one wired in: today's lay, lift and check of
an item in a workspace (a worktree of the batch, or of its task), each answered as laying's Response.

`lay`: the item's lines laid into the workspace's `spec/` (backlog_lines' `lay_onto`), their ids appended to
`unbuilt:`, the feature of each service capability laid written again, and the bookkeeping of the lay (b333): the
corpus's blocks (spec_corpus_write), the features and corpus blocks the lay's change of grammar 4's inputs reaches
(batch_reached, b707), spec/index.md's Composition (spec_composition, b606), the adapter contracts annotated (b379),
the catalogues (batch_catalogues) and each accepted decision a retirement leaves unenforced superseded
(decision_successor, b741). `lift`: the reverse (`unlay_lines`). `check`: the rules of `model.lp` of severity error the
item's requirements violate on the laid workspace (`violating`), past those of the workspace's committed state before
the lay (readiness_bound's `before`, b725), kept by the first lay into a clean workspace, else read off a detached
worktree of its HEAD; the solve of one state of the workspace made once for the checks of all the items laid in it."""
import hashlib
import tempfile
from pathlib import Path

import adapter_annotate
import backlog_items
import backlog_lines
import batch_catalogues
import batch_generator
import batch_reached
import decision_successor
import features_generate
import laying
import readiness_bound
import spec_composition
import spec_corpus_write
import spec_read
import spec_unbuilt
from batch_git import git, remove_tree
from shop_files import Refused

_BEFORE, _SOLVED = {}, {}


def lay(item, workspace, command):
    clean = not git(workspace, "status", "--porcelain").stdout.strip()
    if clean:
        _BEFORE[_head(workspace)] = readiness_bound.before(workspace)
    unwritten, superseded = [], []
    changed = lay_lines(workspace, [item], unwritten, command, superseded)
    return laying.done(changed, unwritten=unwritten, superseded=superseded)


def lift(item, workspace, command, base=None):
    return laying.done(unlay_lines(workspace, [item], command, base))


def check(item, workspace):
    found = violating(workspace, [item], _before(workspace))
    return laying.failed(found[0][1]) if found else laying.done([])


def _head(tree):
    return (str(Path(tree).resolve()), git(tree, "rev-parse", "HEAD").stdout.strip())


def _before(tree):
    """The bound check's violations of the workspace's committed state, kept by the lay, else read off a detached
    worktree of its HEAD."""
    key = _head(tree)
    if key not in _BEFORE:
        other = Path(tempfile.mkdtemp(prefix="laying-")) / "head"
        git(tree, "worktree", "add", "-q", "--detach", str(other), key[1])
        try:
            _BEFORE[key] = readiness_bound.before(other)
        finally:
            remove_tree(tree, other)
    return _BEFORE[key]


def _state(tree):
    """The workspace's state: its HEAD, its uncommitted changes and its untracked files."""
    sha = hashlib.sha256(repr(_head(tree)).encode())
    sha.update(git(tree, "diff", "HEAD", "--binary").stdout.encode())
    for rel in git(tree, "ls-files", "-o", "--exclude-standard", "-z").stdout.split("\0"):
        path = Path(tree) / rel
        if rel and path.is_file():
            sha.update(rel.encode() + b"\0" + path.read_bytes())
    return sha.hexdigest()


def _solved(tree):
    """(the model, its violations, their labels) of the workspace's state, solved once a state."""
    from model_check import solve
    from model_facts import Model
    key = _state(tree)
    if key not in _SOLVED:
        _SOLVED.clear()
        model = Model(tree).read()
        _SOLVED[key] = (model,) + tuple(solve(model))
    return _SOLVED[key]


def lay_lines(tree, picked, unwritten=None, command="work batch start", superseded=None):
    """Every picked item's lines laid into the worktree's `spec/` and the bookkeeping of the lay (the module's doc), a
    catalogue that cannot be written added to `unwritten`, `(item, path, old id)` of each decision superseded added to
    `superseded`; a refusal said as `command`'s (b486); the paths changed."""
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
    service capability changed written again (plan 4 review, B1), spec/index.md's Composition again, the operation
    tables as the commit `base` (the batch's base, b479) held them, each decision the items' lay superseded accepted
    again and its successor out (b741); the paths changed."""
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


def violating(tree, picked, before=frozenset()):
    """(item, reasons) of each picked item a requirement of which violates a `model.lp` rule of severity error (a code
    `v...`; `w_...` is a warning) on the laid worktree, each reason naming the requirement and the rule (b478), or of
    the bound check's (v_pb1, v_pb2) whose operation its model lines declare or its lines request, naming the operation
    or the outcome and the rule (readiness_bound, b721), or of v_m9 of a transition its line sets (b731), of those only
    the ones not in `before`, the worktree's before the lay (b725)."""
    from readiness_bar import model_elements
    model, relations, labels = _solved(tree)
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
