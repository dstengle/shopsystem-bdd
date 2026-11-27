"""The specification service's check of what an item applied brings (b871, checking r164-r167), beside spec_apply.

`violating(tree, items, before)`: (item, reasons) of each item a requirement of which violates a `model.lp` rule of
severity error on the tree it was applied to (b478), or of the bound check's (v_pb1, v_pb2) whose operation its model
lines declare or its lines request (readiness_bound, b721), or of v_m9 of a transition its line sets (b731), of those
only the ones not in `before`, the tree's before the apply (b725); the solve of one state of a tree made once for the
checks of all the items applied to it. `before(tree)`: those of the tree's committed state, kept by `keep` before
the first apply into a clean tree, else read off a detached worktree of its HEAD. `past(root)`: every finding of
`spec check` on `root` (its violations and warnings, as (code, args) of strings), which `spec check --item` leaves out
of what it reports of the root with the item applied, so it returns only what the item brings (r167)."""
import hashlib
import json
import os
import tempfile
from pathlib import Path

import backlog_items
import backlog_lines
import readiness_bound
from batch_git import GitFailed, git, remove_tree

_BEFORE, _SOLVED = {}, {}


def head(tree):
    return (str(Path(tree).resolve()), git(tree, "rev-parse", "HEAD").stdout.strip())


def keep(tree):
    """The bound check's violations of the tree's committed state kept, when the tree is clean, for `before`."""
    if not git(tree, "status", "--porcelain").stdout.strip():
        _BEFORE[head(tree)] = readiness_bound.before(tree)


def before(tree):
    """The bound check's violations of the tree's committed state, kept by `keep`, else read off a detached worktree
    of its HEAD."""
    key = head(tree)
    if key not in _BEFORE:
        other = Path(tempfile.mkdtemp(prefix="apply-")) / "head"
        git(tree, "worktree", "add", "-q", "--detach", str(other), key[1])
        try:
            _BEFORE[key] = readiness_bound.before(other)
        finally:
            remove_tree(tree, other)
    return _BEFORE[key]


def _state(tree):
    """The tree's state: its HEAD, its uncommitted changes and its untracked files."""
    sha = hashlib.sha256(repr(head(tree)).encode())
    sha.update(git(tree, "diff", "HEAD", "--binary").stdout.encode())
    for rel in git(tree, "ls-files", "-o", "--exclude-standard", "-z").stdout.split("\0"):
        path = Path(tree) / rel
        if rel and path.is_file():
            sha.update(rel.encode() + b"\0" + path.read_bytes())
    return sha.hexdigest()


def _solved(tree):
    """(the model, its violations, their labels) of the tree's state, solved once a state."""
    from model_check import solve
    from model_facts import Model
    key = _state(tree)
    if key not in _SOLVED:
        _SOLVED.clear()
        model = Model(tree).read()
        _SOLVED[key] = (model,) + tuple(solve(model))
    return _SOLVED[key]


def violating(tree, items, before=frozenset()):
    """(item, reasons) of each item that brings a violation of severity error (the module's doc), each reason naming
    the requirement, the operation, the outcome or the line, and the rule."""
    from readiness_bar import model_elements
    model, relations, labels = _solved(tree)
    bound = {(name, tuple(str(a) for a in args)) for name, args in relations
             if name in readiness_bound.KEPT} - set(before)
    found = []
    for item in items:
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


def past(root):
    """Every finding `(code, args)` of `spec check` on `root`, its violations and its warnings, args as strings, with
    its unresolved references and its file problems; of a git worktree kept on disk by its state (`_kept`)."""
    from model_check import solve
    from model_facts import Model
    path = _kept(root)
    try:
        data = json.loads(path.read_text()) if path else None
        return {(c, tuple(a)) for c, a in data["found"]}, set(data["dangling"]), set(data["problems"])
    except (OSError, ValueError, KeyError, TypeError):
        pass
    model = Model(root).read()
    found = {(name, tuple(str(a) for a in args)) for name, args in solve(model)[0]}
    if path:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(".tmp%d" % os.getpid())
            tmp.write_text(json.dumps({"found": sorted(found), "dangling": model.dangling,
                                       "problems": model.problems}))
            os.replace(tmp, path)
        except OSError:
            pass
    return found, set(model.dangling), set(model.problems)


def _kept(root):
    """Where `past` keeps the findings of `root`'s state: under the readiness bar's cache, by what readiness_before's
    key reads and the worktree's HEAD, changes and untracked files; None when `root` is no git worktree."""
    import readiness_before
    try:
        state = _state(root)
    except GitFailed:       # no git worktree: nothing kept
        return None
    digest = hashlib.sha256((readiness_before.key(root) + state).encode()).hexdigest()
    return readiness_before._base().parent / "apply-past" / ("%s.json" % digest)


def brought(root, item):
    """The check `spec check --item` makes of the specification with `item` applied (r164-r167): given (the model,
    its findings, their labels), the findings `root` has not (`past`), the model's unresolved references and file
    problems likewise, and the reasons of the bound check (v_pb1, v_pb2) and of v_m9 the item brings, naming its
    operation, its outcome or its line (readiness_bound)."""
    from readiness_bar import model_elements
    blocks = backlog_lines.read(item, backlog_items.rel_of(item.name))
    mine = set(backlog_lines.ids(blocks))

    def check(model, found, labels):
        found_before, dangling, problems = past(root)       # solved only when `spec check` asks
        kept = [f for f in found if (f[0], tuple(str(a) for a in f[1])) not in found_before]
        new = {(name, tuple(str(a) for a in args)) for name, args in kept}
        ops = readiness_bound.operations(model_elements(blocks), model.facts, mine)
        reasons = readiness_bound.reasons(new, ops, labels) + readiness_bound.transitions(new, model.facts, mine, labels)
        model.dangling = [d for d in model.dangling if d not in dangling]
        model.problems = [p for p in model.problems if p not in problems]
        return kept, list(dict.fromkeys(reasons))
    return check
