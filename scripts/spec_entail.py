"""The entailment check of `model logic` (the CNL 4 design, I13a; its study's comp.py, ported): L8, a requirement each
of whose Thens other requirements entail, named with the premises of each Then.

Each response I of a requirement L is a query q(L,I) when some other requirement on L's trigger, untriggered, or (on a
run) refusing could give it (`index`). Its world holds what L states, each such premise is one clingo rule over it
(spec_entail_rules), and every query is answered in one stratified model of grammar/entail.lp (parts of CHUNK
queries, each its own solve). A counted response (`count`, I15) is never a query. Response I is entailed when it is forced. A codified-2 line reads as its check facts
(spec_lf_facts), so the form's meaning is what the check reads; codified-1 lines are read alike.

The bridge, the CLI pack's definition "A tool refuses a command when it exits with an error on it.", is used when the
context imports a pack that defines refuse so (`refuse_defined`): an error exit on a run is a refusal of its command,
which fires the premises on a refusal (a universal condition: change nothing).

`entailed(facts, bridge)` gives {(L, I): {M}}; `findings(root, ctx, scope)` the L8 findings of the requirements of
the capabilities in `scope`."""
import re
from collections import defaultdict
from pathlib import Path

import clingo
import spec_facts
import spec_packs
from spec_entail_rules import Premises, parse, q
from spec_solve_pairs import Finding, order

ENTAIL = Path(__file__).resolve().parent.parent / "grammar" / "entail.lp"
CHUNK = 1000
REFUSE = re.compile(r"^- A tool refuses a command when it exits with an error on it\.$", re.MULTILINE)


def _gives(f):
    g = {(a[1], a[2]) for a in f["resp"]}
    if ("pos", "change_nothing") in g:
        g.add(("neg", "e_change"))
    return g


def index(P):
    """{(L, I): [M]}: the premises asked of each response that some other requirement could give, sorted."""
    by_trig, untrig, refusers = defaultdict(list), [], []
    for r in P.reqs:
        t = P.trig.get(r)
        if t is None:
            untrig.append(r)
        else:
            by_trig[tuple(t[:2])].append(r)
            if t[:2] == ["does", "e_refuse"]:
                refusers.append(r)
    gives = {r: _gives(f) for r, f in P.reqs.items()}
    out = {}
    for L, f in P.reqs.items():
        lt, base = P.trig.get(L), P.base[L]
        same = [M for M in by_trig[tuple(lt[:2])] if P.base[M] != base] if lt else []
        ran = lt is not None and lt[0] == "ran"
        counted = {a[0] for a in f["count"]}
        for j, p, e, d, x in f["resp"]:
            if j in counted:    # a count's Then is never asked: "a K" given does not give "at least n Ks" (I15)
                continue
            cand = [M for M in same + untrig + (refusers if ran else []) if (p, e) in gives[M] and P.base[M] != base]
            own = any(j2 != j and (p2, e2) == (p, e) for j2, p2, e2, _, _ in f["resp"]) or (
                (p, e) == ("neg", "e_change") and ("pos", "change_nothing") in gives[L])
            if not cand and not own:
                continue
            use = set(cand)
            if ran:     # the premises an error exit on L's run brings in: its refusers, and the lines that exit so
                use |= {M for M in same if any(a[1:3] == ["pos", "exit_error"] for a in P.reqs[M]["resp"])}
                use |= {M for M in refusers if P.base[M] != base}
            out[(L, j)] = sorted(use)
    return out


def programs(facts, bridge=True, chunk=CHUNK):
    """(the program text of each part of `chunk` queries, the Premises read)."""
    reqs, dom = parse(facts)
    P = Premises(reqs, dom)
    idx = index(P)
    domain = [f for f in facts if f.split("(")[0] in ("kind", "sub", "val", "dalt", "dlit")]
    keys, rules, out = sorted(idx), {}, []
    background = ENTAIL.read_text()
    for n in range(0, len(keys), chunk):
        parts, used = list(domain), set()
        for L, I in keys[n:n + chunk]:
            ms, Q = idx[(L, I)], "q(%s,%s)" % (q(L), I)
            parts += P.world(L, I, Q, bridge)
            parts += ["use(%s,%s)." % (Q, q(M)) for M in ms]
            conds = {a[1] for M in ms for a in reqs[M]["ccond"]} & {a[0] for a in dom["dalt"]}
            parts += ["dask(%s,%s)." % (Q, c) for c in sorted(conds)]
            used |= set(ms)
        for M in sorted(used):
            if M not in rules:
                rules[M] = P.rule(M)
            parts += rules[M]
        out.append("\n".join(parts + [background]))
    return out, P


def entailed(facts, bridge=True, chunk=CHUNK):
    """{(L, I): {M}}: each response I of L that other requirements M entail (I a string, as the facts number it)."""
    found = defaultdict(set)
    for prog in programs(facts, bridge, chunk)[0]:
        ctl = clingo.Control(["--warn=none", "-t", "1"])
        ctl.add("base", [], prog)
        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                for s in model.symbols(shown=True):
                    if s.name == "ent":
                        found[(s.arguments[0].string, str(s.arguments[1].number))].add(s.arguments[2].string)
    return found


def refuse_defined(root):
    """True when the context imports a pack whose `## Definitions` define refuse by an error exit (the bridge)."""
    for name in spec_packs.imports(root):
        path = spec_packs.path_of(root, name)
        if path is not None and REFUSE.search(Path(path).read_text()):
            return True
    return False


def restating(facts, bridge=True):
    """{requirement: [(Then, [premises])]} of each requirement (a split read as one) each of whose Thens other
    requirements entail; a universal condition is a premise, never reported."""
    found = entailed(facts, bridge)
    reqs, _ = parse(facts)
    splits = defaultdict(list)
    for r, f in reqs.items():
        if f["resp"] and "#" in r:
            splits[spec_facts.split(r)].append(r)
    out = {}
    for base, rs in splits.items():
        thens = [(r, j) for r in sorted(rs) for j, *_ in reqs[r]["resp"]]
        if all(found.get(t) for t in thens):
            out[base] = [(j if r == base else "%s Then %s" % (r[len(base) + 1:], j),
                          sorted({spec_facts.split(m) for m in found[(r, j)]}, key=order)) for r, j in thens]
    return out


def findings(root, ctx, scope):
    """The L8 findings of the codified-2 requirements (`cnl4`) of the capabilities in `scope`, every line a premise;
    a codified-1 line keeps the findings it had (none of L8), and with no codified-2 line in scope nothing is solved."""
    four = {s.id for s in ctx.statements if any(f.startswith("cnl4(") for f in ctx.facts[s.id])}
    if not any(spec_facts.split(i).rpartition("#")[0] in scope for i in four):
        return []
    facts = list(ctx.domain) + [f for s in ctx.statements for f in ctx.facts[s.id]]
    bridge = refuse_defined(root)
    refusers = {s.id for s in ctx.statements if any(',does,e_refuse,' in f for f in ctx.facts[s.id] if
                                                     f.startswith("trig("))}
    out = []
    for r, thens in restating(facts, bridge).items():
        if r.rpartition("#")[0] not in scope or r not in {spec_facts.split(i) for i in four}:
            continue
        said = "; ".join("Then %s by %s" % (j, " and ".join(m + (" (through the definition of refuse)" if bridge and m in
                                                                   refusers else "") for m in ms)) for j, ms in thens)
        out.append(Finding("L8", [r] + sorted({m for _, ms in thens for m in ms}, key=order),
                           "%s says nothing other requirements do not: %s" % (r, said)))
    return out
