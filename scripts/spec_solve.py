"""`model logic` (design §12.3): the codified spec's statements and universal conditions checked together.

  L1  a group cannot happen: no trace makes its witness true with every statement and U on. The unsatisfiable core
      over the `on/1` assumptions names the statements involved. (error)
  L2  two statements whose normalised trees are equal. (warning)
  L3  a `Set` names a status change no transition of the attribute allows. (error)
  L4  a value in a group's pre-state no transition path reaches from an initial value. (warning)

`run(root, capability=None, extra=None)` gives the findings, `report(findings, as_json)` their text and exit code.

The grounding loop of `_ground` is copied from telingo's `imain` (telingo 2.1.3, `telingo/__init__.py`), changed to
ground the states 0..H once and leave the solve to the caller, so that one solve can pass the `on/1` assumptions and
collect the core. telingo's notice:

    MIT License. Copyright (c) 2018 Roland Kaminski. Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software
    without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute,
    sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions: The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
    KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
    PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
    IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import json
import re
from collections import Counter, defaultdict, namedtuple
from pathlib import Path

import spec_grammar
import spec_lexicon
import spec_logic
import spec_read
import spec_tree

HORIZON = 3
ERRORS = ("L1", "L3")
Finding = namedtuple("Finding", "code ids text")
Statement = namedtuple("Statement", "id capability tree")
Group = namedtuple("Group", "id capability statements trees")


def _ground(text, horizon=HORIZON):
    """A clingo Control with the telingo program grounded for the states 0..horizon (telingo's imain, copied)."""
    import clingo
    from clingo import ast
    from clingo.symbol import Function, Number
    from telingo import theory, transformers
    ctl = clingo.Control(["--warn=none"])
    with ast.ProgramBuilder(ctl) as builder:
        _, program_parts = transformers.transform([text], builder.add)
    thy = theory.Theory()
    for step in range(horizon + 1):
        parts = []
        for root_name, part_name, rng in program_parts:
            for i in rng:
                if ((step - i >= 0 and root_name == "always") or (step - i > 0 and root_name == "dynamic") or
                        (step - i == 0 and root_name == "initial")):
                    parts.append((part_name, [Number(step - i), Number(step)]))
        if step > 0:
            ctl.release_external(Function("__final", [Number(step - 1)]))
            ctl.cleanup()
        ctl.ground(parts)
        thy.translate(step, ctl)
    ctl.assign_external(Function("__final", [Number(horizon)]), True)
    return ctl


def _core(ctl):
    """None when a model exists; otherwise the ids of a minimal set of `on/1` assumptions with no model."""
    literals = defaultdict(list)
    for atom in ctl.symbolic_atoms.by_signature("on", 2):
        literals[atom.symbol.arguments[0].string].append(atom.literal)
        ctl.assign_external(atom.symbol, None)

    def unsat(ids):
        found = []
        result = ctl.solve(assumptions=[lit for i in ids for lit in literals[i]], on_core=found.extend)
        return set(found) if result.unsatisfiable else None
    core = unsat(sorted(literals))
    if core is None:
        return None
    keep = sorted(i for i in literals if core & set(literals[i]))
    for ident in list(keep):
        if unsat([i for i in keep if i != ident]) is not None:
            keep.remove(ident)
    return keep


def _order(ident):
    cap, _, local = ident.rpartition("#")
    return (local.startswith("U"), cap, local[:1], int(re.sub(r"\D", "", local) or 0))


def _read(root, extra):
    """{capability name: spec_read.Capability} of the codified capabilities, a drafted file replacing its own."""
    caps = {}
    paths = sorted((Path(root) / "spec" / "capabilities").glob("*.md")) + [Path(p) for p in extra or []]
    for path in paths:
        if spec_read.codified(path):
            cap = spec_read.capability(path)
            caps[cap.name] = cap
    return caps


def _statements(root, caps):
    groups, statements = [], []
    for name, cap in sorted(caps.items()):
        for g in cap.groups:
            mine = []
            for r in g.requirements:
                parsed = spec_grammar.parse(root, r.text)
                if parsed.tree:
                    mine.append(Statement("%s#%s" % (name, r.id), name, parsed.tree))
            statements += mine
            groups.append(Group("%s#%s" % (name, g.id), name, mine, [s.tree for s in mine]))
    for u in spec_read.universal(root):
        parsed = spec_grammar.parse(root, u.text)
        if parsed.tree:
            statements.append(Statement(u.id, None, parsed.tree))
    return groups, statements


def l1(vocab, group, base):
    ctl = _ground(spec_logic.program(base + [spec_logic.witness(vocab, group.id, group.trees)]))
    core = _core(ctl)
    if core is None:
        return []
    own = [s.id for s in group.statements]
    others = sorted((i for i in core if i not in own), key=_order)
    head = "%s (%s) cannot happen: " % (group.id, ", ".join(i.rpartition("#")[2] for i in own))
    if others:
        why = "conflicts with %s" % ", ".join(others)
    elif core:
        why = "it contradicts itself"
    else:
        why = "its pre-state and trigger cannot hold together"
    return [Finding("L1", [group.id] + own + others, head + why)]


def _key(tree):
    """A tree with its lists sorted and its articles made one (an `a` and a `the` of a kind read alike)."""
    if not isinstance(tree, tuple):
        return tree
    fun = tree[0][:-4] + "_An" if tree[0].startswith("k_") and tree[0].endswith("_The") else tree[0]
    return (fun,) + tuple(_key(a) for a in tree[1:])


def l2(statements, scope):
    seen = defaultdict(list)
    for s in statements:
        seen[_key(spec_tree.normal(s.tree))].append(s)
    out = []
    for same in seen.values():
        if len(same) > 1 and any(s.capability in scope for s in same):
            ids = sorted((s.id for s in same), key=_order)
            out.append(Finding("L2", ids, "%s say the same thing" % " and ".join(ids)))
    return out


def _values(vocab, tree, skip=("Becomes",)):
    """(attribute id, the values one of which the tree asks for) of every positive value test in a clause."""
    out = []
    for node in spec_tree.nodes(tree):
        cat, base, part = vocab.decode(node[0])
        if cat == "attribute" and part in ("ThatIs", "Is", "Whose"):
            out.append((base, [vocab.value(m) for m in vocab.members(node[2])]))
        elif cat == "attribute" and part == "Pre":
            out.append((base, [vocab.value(node[1])]))
        elif cat == "condition" and part in ("Pre", "ThatIs", "Is") and base in vocab.cond_attr:
            pos = spec_logic.means_values(vocab, base)[0]
            if pos:
                out.append((vocab.cond_attr[base], pos))
    return [(t, v) for t, v in out if t not in skip]


def _edges(vocab, tid):
    by_text = {vocab.value_text[v].strip("`"): v for v in vocab.attr_values[tid]}
    edges = set()
    for frm, to, _ in vocab.attrs[tid][1].transitions:
        if frm.strip("`") in by_text and to.strip("`") in by_text:
            edges.add((by_text[frm.strip("`")], by_text[to.strip("`")]))
    return edges


def _kind(vocab, tid):
    """`an initiative`, `a request`: the kind of an attribute with its article."""
    kind = vocab.kinds[vocab.attrs[tid][0]]
    return ("an " if kind[:1] in "aeiou" else "a ") + kind


def l3(vocab, statements, scope):
    out = []
    for s in (s for s in statements if s.capability in scope):
        parts = spec_tree.parts(s.tree)
        before = [x for key in ("feat", "cond", "trig") if parts[key] for x in _values(vocab, parts[key])]
        for node in spec_tree.nodes(parts["resp"]):
            cat, tid, part = vocab.decode(node[0])
            edges = _edges(vocab, tid) if cat == "attribute" and part == "Set" else set()
            if not edges:
                continue
            to = vocab.value(node[2])
            starts = [v for t, vals in before if t == tid for v in vals if v != to]
            bad = [v for v in starts if (v, to) not in edges]
            if bad or (not starts and to not in {b for _, b in edges}):
                frm = " from %s" % vocab.value_text[bad[0]] if bad else ""
                out.append(Finding("L3", [s.id], "%s sets the %s of %s%s to %s, which no transition allows" % (
                    s.id, vocab.attrs[tid][1].term, _kind(vocab, tid), frm, vocab.value_text[to])))
    return out


def _reachable(vocab, tid):
    edges = _edges(vocab, tid)
    values = set(vocab.attr_values[tid])
    start = values - {b for _, b in edges}
    if not edges or not start:
        return values
    seen, todo = set(start), list(start)
    while todo:
        v = todo.pop()
        for a, b in edges:
            if a == v and b not in seen:
                seen.add(b)
                todo.append(b)
    return seen


def l4(vocab, groups, scope):
    out = []
    for g in (g for g in groups if g.capability in scope and g.trees and g.trees[0][0] != "Ubiq"):
        parts = spec_tree.parts(g.trees[0])
        for key in ("feat", "cond", "trig"):
            for tid, vals in _values(vocab, parts[key]) if parts[key] else []:
                reach = _reachable(vocab, tid)
                if not set(vals) & reach:
                    out.append(Finding("L4", [g.id], "%s needs %s whose %s is %s, which no transition path "
                                       "reaches" % (g.id, _kind(vocab, tid), vocab.attrs[tid][1].term,
                                                    " or ".join(vocab.value_text[v] for v in vals))))
    return out


def run(root, capability=None, extra=None):
    """The findings of the codified capabilities of the context at `root`, with drafted capability files `extra`;
    with `capability`, only the groups and statements of that capability are checked (against all the others)."""
    vocab = spec_logic.Vocab(spec_lexicon.read(root))
    caps = _read(root, extra)
    scope = set(caps) if capability is None else {capability} & set(caps)
    groups, statements = _statements(root, caps)
    base = [spec_logic.facts(vocab)] + [spec_logic.translate(vocab, s.id, s.tree) for s in statements]
    found = [f for g in groups if g.capability in scope and g.trees for f in l1(vocab, g, base)]
    return found + l2(statements, scope) + l3(vocab, statements, scope) + l4(vocab, groups, scope)


def report(findings, as_json):
    """(text, exit code): one line a finding and a count, or one JSON object; exit 1 on an L1 or an L3."""
    code = 1 if any(f.code in ERRORS for f in findings) else 0
    if as_json:
        return json.dumps({"findings": [f._asdict() for f in findings], "exit": code}), code
    if not findings:
        return "no findings", code
    counts = Counter(f.code for f in findings)
    tail = "%d finding%s: %s" % (len(findings), "" if len(findings) == 1 else "s",
                                 ", ".join("%d %s" % (counts[c], c) for c in sorted(counts)))
    return "\n".join(["%s %s" % (f.code, f.text) for f in findings] + [tail]), code
