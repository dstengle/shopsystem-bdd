"""The solver of the codified spec (design-r2 §6.3, §5.7): program text, facts and ids in, a result out. No tree is
read here.

`solve(text, on_ids, imax, pools, optimise=False)` runs telingo's own incremental loop (`telingo.imain`, as telingo
ships it) through `Proxy`, which frees the `on/1` externals after each ground, passes the ids in `on_ids` as
assumptions, collects the unsatisfiable core and keeps the optimal models. telingo stops at the first horizon that is
SAT; strong next (`>`) in the program drives that horizon. On UNSAT with `pools` given, it solves once more with each
pool at n × imax + 1, so a pool too small is never reported as a conflict.

`least(models)` is the fixed tie-break: the least model by its sorted atom strings. `cone(facts, gid)` reads the
statements a group's solve needs from the translation's signature facts by `grammar/cone.lp`, and
`horizon_bound(edges, start)` the imax of that solve.
"""
from collections import namedtuple
from pathlib import Path

CAP = 10000
CONE = Path(__file__).resolve().parent.parent / "grammar" / "cone.lp"
Result = namedtuple("Result", "sat horizon core models")


class Undetermined(ValueError):
    """More optimal models than CAP: the trace is not determined."""


class Proxy:
    """The `clingo.Control` that `telingo.imain` drives, with the `on/1` assumptions, the core and the models added
    to each solve. Everything else passes through to the control."""

    def __init__(self, ctl, on_ids, optimise=False):
        self.ctl, self.on_ids, self.optimise = ctl, set(on_ids), optimise
        self.horizon, self.future, self.found, self.models, self.sat = -1, [], [], [], False

    def __getattr__(self, name):
        return getattr(self.ctl, name)

    def _on(self):
        """{literal: id} of the grounded `on/1` atoms (telingo adds the time argument)."""
        return {a.literal: a.symbol.arguments[0].string for a in self.ctl.symbolic_atoms.by_signature("on", 2)}

    def ground(self, parts):
        """Ground, then free each `on/1` external: left at false, the translation would read every one off."""
        self.ctl.ground(parts)
        for atom in self.ctl.symbolic_atoms.by_signature("on", 2):
            self.ctl.assign_external(atom.symbol, None)
        self.horizon += 1

    def solve(self, on_model=None, assumptions=()):
        """imain's solve: its future assumptions, plus the `on/1` literals of the ids switched on."""
        self.future = list(assumptions)
        res = self.attempt(self.on_ids, keep=True)
        self.sat = bool(res.satisfiable)
        return res

    def attempt(self, ids, keep=False):
        """One solve at the grounded horizon with the ids in `ids` on; the core is kept as ids."""
        on = self._on()
        lits = [lit for lit, ident in sorted(on.items()) if ident in ids]
        self.models, core = [], []
        res = self.ctl.solve(assumptions=self.future + lits, on_model=self._model if keep else None,
                             on_core=core.extend)
        self.found = sorted({on[x] for x in core if x in on}) if res.unsatisfiable else []
        return res

    def _model(self, m):
        if len(self.models) > CAP:
            return False
        if not self.optimise or m.optimality_proven or not m.cost:
            self.models.append(sorted(str(s) for s in m.symbols(shown=True)))
        return True


def _control(optimise):
    import clingo
    return clingo.Control(["--warn=none"] + (["--opt-mode=optN", "0"] if optimise else []))


def _run(text, on_ids, imax, optimise):
    import telingo
    from clingo import ast
    from telingo import transformers
    ctl = _control(optimise)
    with ast.ProgramBuilder(ctl) as builder:
        future, parts = transformers.transform([text], builder.add)
    proxy = Proxy(ctl, on_ids, optimise)
    telingo.imain(proxy, future, parts, lambda m, s: None, imin=0, imax=imax)
    return proxy


def _pools(pools, factor=1, plus=0):
    if not pools:
        return ""
    return "\n#program always.\n" + "".join("pool_size(%s,%d).\n" % (k, n * factor + plus)
                                            for k, n in sorted(pools.items()))


def solve(text, on_ids, imax, pools, optimise=False):
    """Result(sat, horizon, core, models): the horizon telingo stopped at, the minimal core over `on_ids` (None
    when SAT) and the models of the last solve (the optimal ones when `optimise`), each its sorted shown atoms."""
    proxy = _run(text + _pools(pools), on_ids, imax, optimise)
    if not proxy.sat and pools:
        proxy = _run(text + _pools(pools, imax, 1), on_ids, imax, optimise)
    if proxy.sat:
        return Result(True, proxy.horizon, None, proxy.models)
    return Result(False, proxy.horizon, minimal_core(proxy, proxy.found), [])


def minimal_core(proxy, core):
    """The core with each id dropped in turn, kept out when the rest is still UNSAT (as in 0.29's `model logic`)."""
    keep = sorted(core)
    for ident in list(keep):
        rest = [i for i in keep if i != ident]
        if proxy.attempt(set(rest)).unsatisfiable:
            keep = rest
    return keep


def least(models):
    """The least model by its sorted atom strings; refused past CAP models, which is deterministic too."""
    if len(models) > CAP:
        raise Undetermined("the group's trace is not determined: more than %d optimal models" % CAP)
    return min(sorted(m) for m in models)


def _text(sym):
    import clingo
    return sym.string if sym.type == clingo.SymbolType.String else str(sym)


def cone(facts, gid):
    """(ids, edges) of a group's cone over the whole spec: the statements in it, sorted, and the `edge/2` pairs among
    the witness and those statements. `facts` is the translation's signature facts (text or lines); the witness's
    own facts carry `gid` as their id."""
    import clingo
    if not isinstance(facts, str):
        facts = "\n".join(facts)
    ctl = clingo.Control(["--warn=none", "--opt-mode=opt"])
    ctl.add("base", [], CONE.read_text() + "\n" + facts + "\nstart(%s)." % _quote(gid))
    ctl.ground([("base", [])])
    last = []
    ctl.solve(on_model=lambda m: last.__setitem__(slice(None), m.symbols(shown=True)))
    ids = sorted(_text(s.arguments[1]) for s in last if s.name == "in_cone")
    nodes = set(ids) | {gid}
    edges = sorted((_text(s.arguments[0]), _text(s.arguments[1])) for s in last if s.name == "edge")
    return ids, [e for e in edges if e[0] in nodes and e[1] in nodes]


def _quote(ident):
    return '"%s"' % ident.replace("\\", "\\\\").replace('"', '\\"')


def horizon_bound(edges, start):
    """imax for a solve from `start`: the longest path over `edges` from it, plus 2; on a cycle reachable from it,
    the number of nodes it reaches, plus 2."""
    succ = {}
    for a, b in edges:
        succ.setdefault(a, set()).add(b)
    seen, order, cycle = {}, [], False
    stack = [(start, iter(sorted(succ.get(start, ()))))]
    seen[start] = "open"
    while stack:
        node, it = stack[-1]
        nxt = next(it, None)
        if nxt is None:
            seen[node] = "done"
            order.append(node)
            stack.pop()
        elif seen.get(nxt) == "open":
            cycle = True
        elif nxt not in seen:
            seen[nxt] = "open"
            stack.append((nxt, iter(sorted(succ.get(nxt, ())))))
    if cycle:
        return len(seen) + 2
    depth = {}
    for node in order:
        depth[node] = max((depth[n] + 1 for n in succ.get(node, ())), default=0)
    return depth[start] + 2
