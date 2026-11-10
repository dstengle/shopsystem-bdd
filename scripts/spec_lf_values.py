"""Value sets and a value's absence (b240, construct #4): one translation of spec_rgl_np's `T_IsOneOf`, `T_IsNoneOf`,
`T_<K>_IsOneOf`, `T_<K>_IsNoneOf` and `T_<K>_HasNo` in each place a line is read.

- the form (`cond`): "is one of `a` or `b`" an `or` box, a case a value; "is not `a` or `b`" a `not` box a value
  (none of them: a thing whose T has no value is none of them too); "x has no T" the atom `T(x) = none`, `NONE`, a
  value no entry lists; a list that names a value twice a note, which spec_lf_read gives as the line's refusal;
- the check: `NONE` is the value `ABSENT` (spec_lf_ids), a fact of its own that no listed value meets; an `or` of
  values in an `every` box's scope `uin(R, U, T, V)` of each (`members`, read by spec_lf_quant);
- the steps (`given`): the Given "the stage s1 has no priority" of `T(x) = none`.
"""
import spec_lf_np as nps
import spec_rgl
from spec_lf_core import Atom, Box, Ref

NONE, ABSENT = "none", "absent"


def listed(st, tree):
    """The values a `T_Vals` tree lists, in order."""
    a = nps.args(tree)
    if nps.fun(tree).endswith("_Vals2"):
        return [st.names.value(nps.fun(a[0])), st.names.value(nps.fun(a[1]))]
    return [st.names.value(nps.fun(a[0]))] + listed(st, a[1])


def cond(st, t, rest, a):
    """(referents, conditions) of a value set or an absence, or None when `rest` is none of them."""
    if rest.endswith("_HasNo"):
        return st.apply([nps.np(st, a[0])], lambda r: Atom("attr", (r[0], t.term, NONE)))
    if not rest.endswith(("IsOneOf", "IsNoneOf")):
        return None
    x = nps.owner(st, a[0]) if rest in ("IsOneOf", "IsNoneOf") else nps.np(st, a[0])
    values = listed(st, a[1])
    twice = next((v for n, v in enumerate(values) if v in values[:n]), None)
    if twice:
        st.notes.append("the list of the %s of a %s names %s twice" % (t.term, t.kinds[0], twice))
    if rest.endswith("IsOneOf"):
        return st.apply([x], lambda r: Box("or", (), tuple(Box("case", (), (Atom("attr", (r[0], t.term, v)),))
                                                           for v in values)))
    made = []

    def build(r):
        made.append(Atom("attr", (r[0], t.term, values[0])))
        return made[-1]
    refs, conds = st.apply([x], build)
    return refs, spread(conds, made, lambda m: [Box("not", (), (Atom("attr", m.args[:2] + (v,)),)) for v in values])


def spread(conds, made, fn):
    """`conds` with each atom in `made` replaced by the items `fn` gives of it, inside any box."""
    out = []
    for c in conds:
        if any(c is m for m in made):
            out += fn(c)
            continue
        if isinstance(c, Box):
            c = Box(c.op, c.refs, tuple(spread(c.body, made, fn)),
                    c.scope and Box(c.scope.op, c.scope.refs, tuple(spread(c.scope.body, made, fn))), c.count)
        out.append(c)
    return out


def members(u, box):
    """[(attribute, value)] of an `or` box of an `every` box's scope whose every case says one value of `u`'s
    attribute, or None."""
    out = []
    for case in box.body:
        item = case.body[0] if len(case.body) == 1 and not case.refs else None
        if not (isinstance(item, Atom) and item.pred == "attr" and item.args[0] == u
                and not isinstance(item.args[2], Ref)):
            return None
        out.append(item.args[1:])
    return out if box.op == "or" and len({t for t, _ in out}) == 1 else None


def given(r, item, pos):
    """The Cond tree of "the stage s1 has no priority" of `T(x) = none`."""
    import spec_steps4_boxes  # here: the steps import this module through spec_steps4
    x, term, _ = item.args
    if not pos:
        raise spec_steps4_boxes.TraceError("no step of a %s that has a %s" % (x.kind, term))
    for n, (t, kinds) in enumerate(r.vocab.attributes, 1):
        k = next((k for k in kinds if k in r.vocab.ancestors(x.kind)), None)
        if t.term == term and k is not None:
            return ("t_%s_%d_%s_HasNo" % (spec_rgl.slug(term), n, spec_rgl.kid(k)), r.np(x, k))
    raise spec_steps4_boxes.TraceError("no step of the %s of a %s" % (term, x.kind))
