"""A group's minimal trace read into Steps trees (design-r2 §7): the scenario of `features generate`.

`trace(ctx, group)` solves the group's program (spec_solve's cone, the U's in it, the transition guards and the
group's witness) on telingo's own incremental loop with the minimisation of `grammar/background.lp` (design-r2 §7.2),
enumerating every optimal model projected on what the reader reads: the labels of the group and of its statements
(`lab/3`) and the fluents of state 0. The least projected model by its sorted atom strings is the trace. An UNSAT
program is the group's L1, refused with its text.

`read(model, gid, own, logic, steps)` reads that model into `[(keyword, Steps tree)]` by the atom table of design-r2
§7.3, never a requirement tree. Givens: the witness's labels at state 0 (`feat(i)`, `cond(i)`, `mod(0,j)`), then each
state-0 fluent no label names whose things the scenario mentions (sorted). When: the `trig` label. Thens: each
statement's `resp(i)` labels at the state after the trigger (the trigger's own state when it has none), each followed
by its `mod(i,j)`, then its `no(i)`. Instances are named by their kind's letter and a counter, in order of first
mention (spec_trace_steps, the atom table). `traces(ctx, groups)` solves many groups side by side.
"""
import multiprocessing
import os

import spec_engine
import spec_logic
import spec_solve
from spec_steps import Reader, TraceError, is_instance, text_of, things

PROJECT = """
#program always.
%s
seen(I,P,A) :- lab(I,P,A), focus(I).
#project seen/3.
#show seen/3.
#program initial.
init(attr(X,A,V)) :- attr(X,A,V).
init(rel(R,X,Y)) :- rel(R,X,Y).
init(cond(C,X)) :- cond(C,X).
init(given(F)) :- given(F).
init(holds(X,R)) :- holds(X,R).
#project init/1.
#show init/1.
"""
FLAGS = ["--warn=none", "--opt-mode=optN", "0", "--project=project"]
_JOB = []


class _Proxy(spec_engine.Proxy):
    """spec_engine's Proxy keeping, of each optimal model, only the projected atoms."""

    def _model(self, m):
        if len(self.models) > spec_engine.CAP:
            return False
        if m.optimality_proven or not m.cost:
            self.models.append(sorted(str(s) for s in m.symbols(shown=True) if s.name in ("seen", "init")))
        return True


def _q(text):
    return '"%s"' % text


def cone(ctx, group):
    """(statement ids, edges, witness) of the group's cone over the whole spec (spec_engine.cone)."""
    wit = spec_logic.witness(ctx.vocab, group.id, group.trees[0], group.statements[0].id)
    own = ["own(%s,%s)." % (_q(group.id), _q(s.id)) for s in group.statements]
    return spec_engine.cone(spec_solve.anyone(ctx.sigs + wit.sigs) + own, group.id) + (wit,)


def trace(ctx, group):
    """The least optimal projected model of the group's trace, as sorted atom strings; TraceError when none."""
    import clingo
    import telingo
    from clingo import ast
    from telingo import transformers
    ids, edges, wit = cone(ctx, group)
    parts = ctx.base + [ctx.rules[i] for i in ids] + [wit]
    text = spec_logic.program(parts, optimise=True) + "\n#program always.\n" + "".join(
        "pool_size(%s,%d).\n" % kv for kv in sorted(spec_logic.pool_sizes(parts).items()))
    text += PROJECT % "".join("focus(%s)." % _q(i) for i in [group.id] + [s.id for s in group.statements])
    ctl = clingo.Control(FLAGS)
    with ast.ProgramBuilder(ctl) as builder:
        future, program = transformers.transform([text], builder.add)
    proxy = _Proxy(ctl, ids + sorted(ctx.guards), True)
    telingo.imain(proxy, future, program, lambda m, s: None, imin=0, imax=spec_engine.horizon_bound(edges, group.id))
    if proxy.sat and proxy.models:
        try:
            return spec_engine.least(proxy.models)
        except spec_engine.Undetermined as err:
            raise TraceError("%s: %s" % (group.id, err))
    res = spec_solve.solve(ctx, group)
    if not res.sat:
        raise TraceError(spec_solve.unsat(ctx, group, res.core).text)
    raise TraceError("%s: the group's trace needs more instances than its pools give" % group.id)


def _trace(index):
    ctx, groups = _JOB
    try:
        return trace(ctx, groups[index])
    except TraceError as err:
        return str(err)


def traces(ctx, groups):
    """{group id: its trace, or the reason it has none}, side by side in forked processes when there are many."""
    _JOB[:] = [ctx, groups]
    workers = min(os.cpu_count() or 1, len(groups) // 4)
    if workers < 2 or multiprocessing.get_start_method(allow_none=True) not in (None, "fork"):
        found = [_trace(i) for i in range(len(groups))]
    else:
        with multiprocessing.get_context("fork").Pool(workers) as pool:
            found = pool.map(_trace, range(len(groups)), chunksize=1)
    return {g.id: f for g, f in zip(groups, found)}


def _sign(sym):
    return (False, sym.arguments[0]) if sym.name == "neg" else (True, sym)


def _part_key(part):
    return part.name, tuple(x.number for x in part.arguments)


def _extra(sym, mentioned, logic):
    """True when a state-0 fluent no label names is a Given: a primitive fact about things the scenario mentions."""
    mine = things(sym)
    if not mine or any(x not in mentioned for x in mine):
        return False
    a = sym.arguments
    if sym.name == "cond":
        return a[0].name not in logic.defined
    if sym.name == "rel":
        return all(is_instance(x) or text_of(x) is not None for x in a[1:])
    return sym.name != "holds" or is_instance(a[0])


def read(model, gid, own, logic, steps):
    """[(keyword, Steps tree)] of one trace: `own` are the group's statement ids, in order."""
    import clingo
    seen, init = [], []
    for text in model:
        sym = clingo.parse_term(text)
        (seen if sym.name == "seen" else init).append(sym)
    labels = [s for s in seen if s.arguments[0].string == gid]
    trig = [s.arguments[2] for s in labels if s.arguments[1].name == "trig"]
    at = 1 if trig else 0
    pre = [_sign(s.arguments[2]) for s in sorted(
        (s for s in labels if s.arguments[3].number == 0 and s.arguments[1].name in ("feat", "cond", "mod")),
        key=lambda s: ({"feat": 0, "cond": 1, "mod": 2}[s.arguments[1].name], _part_key(s.arguments[1]),
                       str(s.arguments[2])))]
    thens = []
    for n, ident in enumerate(own):
        mine = [s for s in seen if s.arguments[0].string == ident and s.arguments[3].number == at]
        for s in mine:
            p = s.arguments[1]
            key = (n, p.name == "no", p.arguments[0].number, p.name == "mod", _part_key(p))
            thens.append((key,) + ((False, s.arguments[2]) if p.name == "no" else _sign(s.arguments[2])))
    thens.sort(key=lambda t: (t[0], str(t[2])))
    # a value the trace holds says more than a value it does not: `is not v` is left to the value's own Given
    valued = {tuple(f.arguments[0].arguments[:2]) for f in init if f.arguments[0].name == "attr"}
    pre = [p for p in dict.fromkeys(pre) if p[0] or p[1].name != "attr" or tuple(p[1].arguments[:2]) not in valued]
    mentioned = {x for a in [a for _, a in pre] + trig + [t[2] for t in thens] for x in things(a)}
    named = {a for _, a in pre}
    extra = sorted((f.arguments[0] for f in init if f.arguments[1].number == 0 and f.arguments[0] not in named
                    and _extra(f.arguments[0], mentioned, logic)), key=str)
    r = Reader(logic, steps)
    for sym in [a for _, a in pre] + extra + trig + [t[2] for t in thens]:
        r.mention(sym)
    out = []
    for positive, sym in pre + [(True, x) for x in extra]:
        out += [("given", t) for t in r.given(sym, positive) if ("given", t) not in out]
    out += [("when", r.when(t)) for t in trig]
    done = sorted({(key, steps.text(step), step) for key, step in ((t[0], r.then(t[2], t[1])) for t in thens)})
    return out + list(dict.fromkeys(("then", step) for _, _, step in done))
