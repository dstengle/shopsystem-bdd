"""One requirement's facts (`spec_facts`) as the atoms `spec_steps.Reader` reads (design-r3 §5): a role as the
instance `o(K,V)`, a pre-state, object or set fact as a fluent (`attr`, `cond`, `rel`, `holds`, `over`, `given`), the
trigger as `ran`, `ran_any`, `does` or `set_to`, a response as `does` (`holds` for a hold), and an
`every` role's contrast.

`own` keeps what a scenario reads of a requirement: its first way through when it is split, and a positive defined
condition without the literals of its definition that follow it (the requirement's own words, not its expansion).
"""
import clingo

PRE = ("feat", "cond", "ccond", "crel", "holds", "free")
OBJ = ("oattr", "onot", "orel", "ocond")
F = clingo.Function


def name_of(sym):
    """The name of a function symbol (a constant included), or None for a string or a number."""
    return sym.name if sym.type == clingo.SymbolType.Function else None


def _expansion(logic, rid, var, cid, n, obj):
    """The facts a positive defined condition `cid` on `var` adds after its own, over each way through its
    definition; `n` is the number of roles before it. A codified-1 line's definition under a codified-2 index is
    followed in the old vocabulary it is written in, its facts mapped to the layered ids (`under`, spec_context_ids)."""
    import spec_facts
    ids = getattr(logic, "under", None)
    if ids is not None:
        return set(ids.facts(_expansion(ids.old, rid, var, ids.back[cid], n, obj)))
    kid, clause = logic.def_lits[cid]
    out, seq = set(), []
    while seq is not None:
        w = spec_facts.Walk(logic, rid, seq)
        w.n, w.bound, w.expanding = n, {kid: var}, {cid}
        w.clause(clause, obj)
        out.update(w.out)
        seq = spec_facts._next(w.taken, w.options)
    return out


def own(logic, facts):
    """The parsed facts a requirement's scenario reads."""
    syms = [clingo.parse_term(f.rstrip(".")) for f in facts]
    first = next((s.arguments[0] for s in syms if s.name == "disj"), None)
    out, skip, roles = [], set(), 0
    for text, sym in zip(facts, syms):
        if sym.name == "disj" or (first is not None and sym.arguments[0] != first) or text in skip:
            continue
        out.append(sym)
        roles += sym.name == "role"
        a = sym.arguments
        if sym.name in ("ccond", "ocond") and a[3].name == "pos" and a[2].name in logic.def_lits:
            skip |= _expansion(logic, a[0].string, a[1].name, a[2].name, roles, sym.name == "ocond")
    return out


def subst(sym, inst):
    """`sym` with each role variable replaced by its instance."""
    if name_of(sym) is None:
        return sym
    if not sym.arguments:
        return inst.get(sym.name, sym)
    return F(sym.name, [subst(a, inst) for a in sym.arguments])


def instances(syms, n, shared):
    """{role variable: its instance} of the n-th requirement of a group: its named code, the first requirement's
    role of the same kind and rank among that kind's roles (`shared`), or a new instance."""
    named = {s.arguments[1].name: s.arguments[2] for s in syms if s.name == "named"}
    inst, rank = dict(named), {}
    for s in (s for s in syms if s.name == "role" and s.arguments[1].name not in named):
        var, kid = s.arguments[1].name, s.arguments[2]
        rank[kid.name] = rank.get(kid.name, 0) + 1
        key = (kid.name, rank[kid.name])
        if n == 0 or key not in shared:
            shared.setdefault(key, F("o", [kid, F("r%d%s" % (n, var))]))
        inst[var] = shared[key]
    return inst


def fluent(sym):
    """(positive, atom) of a pre-state, object or set fact over instances."""
    a = sym.arguments
    pos = a[-1].name == "pos" if sym.name in ("cond", "ccond", "crel", "ocond") else sym.name != "onot"
    if sym.name in ("cond", "oattr", "onot", "set"):
        return pos, F("attr", list(a[-4:-1] if sym.name == "cond" else a[-3:]))
    if sym.name in ("ccond", "ocond"):
        return pos, F("cond", [a[2], a[1]])
    if sym.name in ("crel", "orel"):
        return pos, F("rel", list(a[1:4]))
    if sym.name == "holds":
        return True, F("holds", list(a[1:3]))
    if sym.name == "free":
        return False, F("over", [a[1]])
    return True, F("given", [a[1]])


def trigger(sym):
    """The When atom of a `trig` fact."""
    _, p, e, d, x = sym.arguments
    if p.name == "ran":
        return F("ran_any", [e]) if name_of(d) == "any" else F("ran", [d, e, x])
    if p.name == "does":
        return F("does", [d, e, x])
    return F("set_to", [x] + list(e.arguments))


def response(sym, x=None):
    """(positive, atom) of a `resp` fact; with `x`, its absence on the contrast `x`."""
    _, _, pol, e, d, obj = sym.arguments
    if name_of(e) == "hold":
        return pol.name == "pos", F("holds", [d, e.arguments[0]])
    return (pol.name == "pos" if x is None else False), F("does", [d, e, obj if x is None else x])


def contrast(logic, syms, var, inst, n):
    """(instance, (positive, atom)) of one more thing of an `every` role's kind that fails its restriction: for a
    value, the first in the attribute's order the restriction excludes; for a condition, its opposite. None when
    the role has no restriction or none fails it."""
    pre = [s for s in syms if s.name in ("cond", "ccond") and s.arguments[1].name == var]
    if not pre or name_of(inst[var]) != "o":
        return None
    c = F("o", [inst[var].arguments[0], F("c%d%s" % (n, var))])
    if pre[0].name == "ccond":
        return c, (pre[0].arguments[3].name != "pos", F("cond", [pre[0].arguments[2], c]))
    tid = pre[0].arguments[2]
    pos = [s.arguments[3].name for s in pre if s.name == "cond" and s.arguments[2] == tid
           and s.arguments[4].name == "pos"]
    neg = [s.arguments[3].name for s in pre if s.name == "cond" and s.arguments[2] == tid
           and s.arguments[4].name == "neg"]
    order = logic.attr_values.get(tid.name, [])
    fail = [v for v in order if v not in pos] if pos else [v for v in order if v in neg]
    return (c, (True, F("attr", [c, tid, F(fail[0])]))) if fail else None
