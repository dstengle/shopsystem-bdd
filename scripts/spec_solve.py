"""`model logic` (design-r3 §6): the codified spec's requirements and universal conditions checked together, by one
brave clingo solve of the context's facts (`spec_context`, read once) and the fixed meta-encoding `grammar/check.lp`.
The shown atoms are the findings:

  L0  the check did not finish within LIMIT seconds; the findings so far are listed. Or the solve is unsatisfiable
      (check.lp has no model of the facts), naming the capabilities checked. (error)
  L1  `clash(A,B,Why)`: A and B fire on one trigger in one consistent pre-state and demand opposite things, or
      `clash(A,A,self)`: A contradicts itself. Its text has the merged pre-state of one witness, from one normal
      solve of check.lp's part `witness` for every pair (spec_solve_pairs). (error)
  L2  two statements whose normalised trees are equal. (warning)
  L3  `bad_set`: a set no transition allows. (error)
  L4  `unreachable`: a value a pre-state needs that no transition path reaches. (warning)
  L5  `lint`: an untriggered positive event obligation, with the requirements that react to its event. (warning)
  L6  `maybe(A,B,Why,C)`: a clash whose every witness depends on the prose condition C (one side says C of a thing
      the other says more of); defining C in the controlled language decides it. (warning)
  aside  `coded(A,B)` never `fit(A,B)`: a pair that shares a code no unification keeps one thing, set aside alone,
      every other pair's findings kept. (warning)

`run(root, capability=None, extra=None)` gives the findings, `report(findings, as_json)` their text and exit code.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

import clingo
import spec_context
import spec_facts
import spec_findings
import spec_solve_pairs
import spec_tree
from spec_solve_pairs import Finding
from spec_solve_pairs import order as _order

ERRORS = ("L0", "L1", "L3")
LIMIT = 20.0
CHECK = Path(__file__).resolve().parent.parent / "grammar" / "check.lp"


def _ground(program):
    ctl = clingo.Control(["--warn=none"])
    ctl.add("base", [], program)
    ctl.ground([("base", [])])
    return ctl


def _solve(ctl, limit, brave=True):
    """(the shown atoms of the last model, sorted; whether the solve finished within `limit` seconds; whether it
    found a model, or did not finish) of a grounded program. Brave, the last model holds every atom some model has;
    past the limit, the atoms found so far."""
    ctl.configuration.solve.enum_mode = "brave" if brave else "auto"
    ctl.configuration.solve.models = 0 if brave else 1
    last = []

    def model(m):
        last[:] = [str(s) for s in m.symbols(shown=True)]
    with ctl.solve(on_model=model, async_=True) as handle:
        done = handle.wait(limit)
        if not done:
            handle.cancel()
        sat = not done or not handle.get().unsatisfiable
    return sorted(last), done, sat


def solve(program, limit, brave=True):
    """`_solve` of `program`, grounded: its atoms and whether it finished."""
    return _solve(_ground(program), limit, brave)[:2]


def _key(tree):
    """A tree with its lists sorted and its articles made one (an `a` and a `the` of a kind read alike)."""
    if not isinstance(tree, tuple):
        return tree
    fun = tree[0][:-4] + "_An" if tree[0].startswith("k_") and tree[0].endswith("_The") else tree[0]
    return (fun,) + tuple(_key(a) for a in tree[1:])


def l2(statements, scope):
    seen = defaultdict(list)
    for s in statements:     # a grammar 4 tree (a text) is one meaning already (spec_meaning)
        seen[s.tree if isinstance(s.tree, str) else _key(spec_tree.normal(s.tree))].append(s)
    out = []
    for same in seen.values():
        if len(same) > 1 and any(s.capability in scope for s in same):
            ids = sorted((s.id for s in same), key=_order)
            out.append(Finding("L2", ids, "%s say the same thing" % " and ".join(ids)))
    return out


def _findings(ctl, words, atoms):
    syms = [clingo.parse_term(a) for a in atoms]
    args = defaultdict(list)
    for sym in syms:
        args[sym.name].append([s.string if s.type == clingo.SymbolType.String else s for s in sym.arguments])
    out = spec_solve_pairs.clashes(ctl, lambda c: _solve(c, LIMIT, brave=False)[0], words,
                                   [(a, b, str(w)) for a, b, w in args["clash"]],
                                   [(a, b, str(w), c) for a, b, w, c in args["maybe"]])
    out += spec_solve_pairs.aside(args["coded"], args["fit"])
    seen = set()
    for code, name, write in (("L3", "bad_set", words.bad_set), ("L4", "unreachable", words.unreachable)):
        for r, *rest in args[name]:
            finding = Finding(code, [spec_facts.split(r)], write(spec_facts.split(r), *rest))
            if (code, finding.text) not in seen:
                seen.add((code, finding.text))
                out.append(finding)
    lints = defaultdict(set)
    for r, e, t in args["lint"]:
        lints[(r, e)] |= set() if isinstance(t, clingo.Symbol) else {spec_facts.split(t)}
    done = set()
    for (r, e), reactors in sorted(lints.items(), key=lambda kv: (_order(spec_facts.split(kv[0][0])), str(kv[0]))):
        reactors = sorted(reactors, key=_order)
        finding = Finding("L5", [spec_facts.split(r)] + reactors, words.lint(r, e, reactors))
        if (finding.ids[0], str(e)) not in done:
            done.add((finding.ids[0], str(e)))
            out.append(finding)
    return out


def _names(finding, scope):
    return any(i.rpartition("#")[0] in scope for i in finding.ids)


def run(root, capability=None, extra=None):
    """The findings of the codified capabilities of the context at `root`, with drafted capability files `extra` laid
    over it (a draft replacing the capability of its name). The solve is always the whole context; `capability`
    keeps the findings that name one of its requirements."""
    ctx = spec_context.load(root, extra or ())
    facts = [f for s in ctx.statements for f in ctx.facts[s.id]]
    program = "\n".join(ctx.domain + facts + [CHECK.read_text()])
    ctl = _ground(program)
    atoms, done, sat = _solve(ctl, LIMIT)
    found = _findings(ctl, spec_findings.Words(root, ctx), atoms)
    scope = set(ctx.caps) if capability is None else {capability} & set(ctx.caps)
    if capability is not None:
        found = [f for f in found if _names(f, scope)]
    found += l2(ctx.statements, scope)
    if not done and scope:
        found.append(Finding("L0", [], "the check did not finish in %d s; the findings so far are listed" % LIMIT))
    if not sat and scope:
        found.append(Finding("L0", [], "the check of %s is unsatisfiable: grammar/check.lp has no model of its facts, "
                             "so no finding of it can be listed" % ", ".join(sorted(scope))))
    return sorted(found, key=lambda f: (f.code, _order(f.ids[0]) if f.ids else ()))


def report(findings, as_json):
    """(text, exit code): one line a finding and a count, or one JSON object; exit 1 on an L0, L1 or L3."""
    code = 1 if any(f.code in ERRORS for f in findings) else 0
    if as_json:
        return json.dumps({"findings": [f._asdict() for f in findings], "exit": code}), code
    if not findings:
        return "no findings", code
    counts = Counter(f.code for f in findings)
    tail = "%d finding%s: %s" % (len(findings), "" if len(findings) == 1 else "s",
                                 ", ".join("%d %s" % (counts[c], c) for c in sorted(counts)))
    return "\n".join(["%s %s" % (f.code, f.text) for f in findings] + [tail]), code
