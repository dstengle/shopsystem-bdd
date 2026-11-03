"""`model logic` (design-r2 §6.4): the codified spec's statements and universal conditions checked together, each
group by one solve on spec_engine (telingo's own incremental loop) over its cone.

  L1  a group cannot happen: its program (the cone's statements, the U's in it, the transition guards and the
      group's witness) is UNSAT at the cone's horizon bound. The core over the `on/1` assumptions names the
      requirement and U ids. (error)
  L2  two statements whose normalised trees are equal. (warning)
  L3  a `Set` no transition allows: an L1 whose core holds a transition guard `T:<attribute>@<kind>`. (error)
  L4  a value the group's pre-state needs that no trace reaches: asked of the solver (`>?`) for each labelled
      state-0 value of the group's model. (warning)

`run(root, capability=None, extra=None, groups=None)` gives the findings, `report(findings, as_json)` their text and
exit code. A condition whose sentence parses as a `Def` is defined by its rule; any other is primitive.
"""
import json
import multiprocessing
import os
import re
from collections import Counter, defaultdict, namedtuple
from pathlib import Path

import spec_engine
import spec_grammar
import spec_lexicon
import spec_logic
import spec_read
import spec_tree

ERRORS = ("L1", "L3")
Finding = namedtuple("Finding", "code ids text")
Statement = namedtuple("Statement", "id capability tree")
Group = namedtuple("Group", "id capability statements trees")
REACH = """#program always.
%(facts)s
{ does(env,set(%(a)s,W),x) : val(W) } 1.
attr(x,A,V) :- does(env,set(A,V),x).
:- attr(x,A,V), attr(x,A,W), V < W.
#program initial.
1 { attr(x,%(a)s,V) : initial(V) } 1.
:- not &tel{ attr(x,%(a)s,%(v)s) | >? attr(x,%(a)s,%(v)s) }.
#program dynamic.
attr(x,A,V) :- 'attr(x,A,V), not does(env,set(A,_),x).
:- does(env,set(%(a)s,W),x), 'attr(x,%(a)s,V), V != W, not trans(V,W).
"""


def _order(ident):
    cap, _, local = ident.rpartition("#")
    return (local.startswith("U"), cap, local[:1], int(re.sub(r"\D", "", local) or 0))


def _q(ident):
    return '"%s"' % ident


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


SIG = re.compile(r'^(trig|eff)\(("(?:[^"\\]|\\.)*"),(does\([^)]*\)),(.+),(\w+)\)\.$')


def anyone(facts):
    """The signature facts with each trigger whose doer is anyone (`does(anyone)`: a thing undergoes an event, a value
    becomes another) repeated for every doer of that event the facts name, so `grammar/cone.lp` matches it."""
    found = [SIG.match(f) for f in facts]
    doers = defaultdict(set)
    for m in filter(None, found):
        doers[m.group(4)].add(m.group(3))
    out = list(facts)
    for m in found:
        if m and m.group(1) == "trig" and m.group(3) == "does(anyone)":
            out += ["trig(%s,%s,%s,%s)." % (m.group(2), d, m.group(4), m.group(5))
                    for d in sorted(doers[m.group(4)] - {"does(anyone)"})]
    return out


def definitions(root, lex, vocab):
    """The rules of the conditions whose sentence parses as a `Def`; each is marked defined in `vocab`."""
    out = []
    for term in lex.of("condition"):
        text = lex.definition(term)
        try:
            tree = spec_grammar.parse(root, text, grammar="Def").tree if text else None
        except spec_grammar.GrammarError:
            return out
        if tree and tree[0] in vocab.def_funs:
            out.append(spec_logic.definition(vocab, tree))
            vocab.define(vocab.def_funs[tree[0]][0])
    return out


class Context:
    """One context's translation: the vocabulary, the facts and definitions, every statement's Rules and the
    signature facts the cones are drawn over."""

    def __init__(self, root, extra):
        lex = spec_lexicon.read(root)
        self.vocab = spec_logic.Vocab(lex)
        self.base = definitions(root, lex, self.vocab)
        self.base.insert(0, spec_logic.facts(self.vocab))
        self.caps = _read(root, extra)
        self.groups, self.statements = _statements(root, self.caps)
        self.rules = {s.id: spec_logic.translate(self.vocab, s.id, s.tree) for s in self.statements}
        self.sigs = [f for r in self.rules.values() for f in r.sigs] + ["sub(%s,%s)." % p for p in self.vocab.subs]
        self.guards = self.vocab.guards()
        self.reached = {}


def _pooled(parts):
    """The program of these parts with its pools as facts: spec_engine retries no larger pool for it."""
    sizes = spec_logic.pool_sizes(parts)
    return spec_logic.program(parts) + "\n#program always.\n" + "".join(
        "pool_size(%s,%d).\n" % kv for kv in sorted(sizes.items()))


def solve(ctx, group):
    """spec_engine's Result for one group: its cone, horizon bound and pools, with every guard on. An UNSAT cone is
    confirmed on its core alone, where spec_engine retries each pool at n × imax + 1: the core is UNSAT there, so
    the whole cone is too. Only when that core is SAT is the whole cone solved with the retry (design-r2 §6.2)."""
    wit = spec_logic.witness(ctx.vocab, group.id, group.trees[0], group.statements[0].id)
    own = ["own(%s,%s)." % (_q(group.id), _q(s.id)) for s in group.statements]
    ids, edges = spec_engine.cone(anyone(ctx.sigs + wit.sigs) + own, group.id)
    imax, on = spec_engine.horizon_bound(edges, group.id), ids + sorted(ctx.guards)
    parts = ctx.base + [ctx.rules[i] for i in ids] + [wit]
    res = spec_engine.solve(_pooled(parts), on, imax, {})
    if res.sat:
        return res
    core = ctx.base + [ctx.rules[i] for i in res.core if i in ctx.rules] + [wit]
    found = spec_engine.solve(spec_logic.program(core), res.core, imax, spec_logic.pool_sizes(core))
    if not found.sat:
        return found
    return spec_engine.solve(spec_logic.program(parts), on, imax, spec_logic.pool_sizes(parts))


def _kind(vocab, tid):
    """`an initiative`, `a request`: the kind of an attribute with its article."""
    kind = vocab.kinds[vocab.attrs[tid][0]]
    return ("an " if kind[:1] in "aeiou" else "a ") + kind


def unsat(ctx, group, core):
    """The L1 or L3 of a group whose program has no model, from its core."""
    own = [s.id for s in group.statements]
    guards = [i for i in core if i in ctx.guards]
    named = sorted((i for i in core if i not in guards), key=_order)
    if guards:
        tid = ctx.guards[guards[0]]
        v = ctx.vocab
        for sid in named:
            for to, froms in (x[1:] for x in ctx.rules[sid].l3 if x[0] == tid):
                bad = [f for f in froms if (f, to) not in v.transitions(tid)]
                frm = " from %s" % v.value_text[bad[0]] if bad else ""
                return Finding("L3", [group.id] + named + guards, "%s sets the %s of %s%s to %s, which no transition "
                               "allows" % (sid, v.attrs[tid][1].term, _kind(v, tid), frm, v.value_text[to]))
    others = [i for i in named if i not in own]
    head = "%s (%s) cannot happen: " % (group.id, ", ".join(i.rpartition("#")[2] for i in own))
    if others:
        why = "conflicts with %s" % ", ".join(others)
    elif named or guards:
        why = "it contradicts itself"
    else:
        why = "its pre-state and trigger cannot hold together"
    return Finding("L1", [group.id] + [i for i in own if i in named] + others + guards, head + why)


def reachable(vocab, tid, vid):
    """True when a trace from an initial value of the attribute (one no transition enters, or any when every one
    is entered) reaches `vid` through the transitions, asked of the solver with `>?`."""
    values, edges = vocab.attr_values[tid], vocab.transitions(tid)
    entered = {b for _, b in edges}
    facts = ["val(%s)." % w for w in values] + ["initial(%s)." % w for w in values if w not in entered or
                                                  entered >= set(values)]
    facts += ["trans(%s,%s)." % e for e in edges]
    program = REACH % {"facts": "\n".join(facts), "a": tid, "v": vid}
    return spec_engine.solve(program, [], len(values), {}).sat


def _needed(group, model):
    """(attribute id, value id) of each labelled state-0 value of the group's model: its features, condition and the
    restrictions of its trigger and subject."""
    import clingo
    out = set()
    for text in model:
        if not text.startswith("lab(%s," % _q(group.id)):
            continue
        sym = clingo.parse_term(text)
        part, what, time = sym.arguments[1], sym.arguments[2], sym.arguments[3].number
        if time == 0 and what.name == "attr" and (part.name in ("cond", "feat") or (
                part.name == "mod" and part.arguments[0].number == 0)):
            out.add((what.arguments[1].name, what.arguments[2].name))
    return sorted(out)


def l4(ctx, group, model):
    out = []
    for tid, vid in _needed(group, model):
        if tid not in ctx.vocab.attrs or not ctx.vocab.transitions(tid):
            continue
        if (tid, vid) not in ctx.reached:
            ctx.reached[(tid, vid)] = reachable(ctx.vocab, tid, vid)
        if not ctx.reached[(tid, vid)]:
            out.append(Finding("L4", [group.id], "%s needs %s whose %s is %s, which no transition path reaches" % (
                group.id, _kind(ctx.vocab, tid), ctx.vocab.attrs[tid][1].term, ctx.vocab.value_text[vid])))
    return out


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


def run(root, capability=None, extra=None, groups=None):
    """The findings of the codified capabilities of the context at `root`, with drafted capability files `extra`;
    with `capability`, only the groups and statements of that capability are checked (against all the others), and
    with `groups` (ids `<cap>#g<n>`) only those groups."""
    ctx = Context(root, extra)
    scope = set(ctx.caps) if capability is None else {capability} & set(ctx.caps)
    todo = [g for g in ctx.groups if g.capability in scope and g.trees and (groups is None or g.id in groups)]
    found = [f for out in _map(ctx, todo) for f in out]
    return sorted(found + l2(ctx.statements, scope), key=lambda f: f.code)


def check(ctx, group):
    """The L1, L3 or L4 findings of one group."""
    res = solve(ctx, group)
    return l4(ctx, group, res.models[0]) if res.sat else [unsat(ctx, group, res.core)]


_CTX = []


def _check(index):
    return check(_CTX[0], _CTX[0].todo[index])


def _map(ctx, todo):
    """`check` of each group, in order; side by side in forked processes when there are many (each solve is
    independent, and the results are put back in the groups' order)."""
    workers = min(os.cpu_count() or 1, len(todo) // 8)
    if workers < 2 or multiprocessing.get_start_method(allow_none=True) not in (None, "fork"):
        return [check(ctx, g) for g in todo]
    ctx.todo, _CTX[:] = todo, [ctx]
    with multiprocessing.get_context("fork").Pool(workers) as pool:
        return pool.map(_check, range(len(todo)), chunksize=1)


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
