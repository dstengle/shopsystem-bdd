"""One thing's value compared with another's (b275, `value-compare` and `value-same`): "the T of x is (not) after|before
the T of y", both sides one attribute of one value order (spec_value_kinds), and "the T of x is (not) the same as the T
of y", of any attribute. One translation of spec_rgl_np's `T_CmpT` and `T_SameAs` in each place a line is read:

- the form (`cond`): one atom `cmp2(x, T, op, y)`, op after, before or same, shown `cmp(T(x1), after, T(x2))`
  (`show`); a comparison of an attribute with no value order a note naming the attribute, which spec_lf_read gives
  as the line's refusal;
- the check (`literal`): `ccmp2(R, X, T, Op, Y, Pol)`, which grammar/check.lp reads over the cells of the points the
  pair names: two lines whose comparisons of the same two values contradict never fire together;
- the steps (`values`): a value of each thing that meets every comparison and value the line names, which
  spec_lf_order's Givens give.
"""
import spec_lf_np as nps
import spec_lf_order
from spec_lf_core import Atom, Box

PRED = "cmp2"
OPS = {"After": "after", "Before": "before"}


def cond(st, t, rest, a):
    """(referents, conditions) of `T_CmpT` or `T_SameAs`, or None when `rest` is neither."""
    if rest == "CmpT":
        op, y = OPS[nps.fun(a[2])], a[3]
        if spec_lf_order.order(t) is None:
            st.notes.append("the %s of a %s has no value order: its entry says neither Order: nor Type:, so one %s "
                            "is never after or before another" % (t.term, t.kinds[0], t.term))
    elif rest == "SameAs":
        op, y = "same", a[2]
    else:
        return None
    x, y = nps.owner(st, a[1]), nps.owner(st, y)
    return st.apply([x, y], lambda r: Atom(PRED, (r[0], t.term, op, r[1])), 2 if a[0] == "PNeg" else None)


def show(a, term):
    x, t, op, y = a.args
    return "cmp(%s(%s), %s, %s(%s))" % (t, term(x), op, t, term(y))


# --- the check -----------------------------------------------------------------------------------------------------
def literal(terms, atom, pos):
    """`ccmp2(R, X, T, Op, Y, Pol)` of a comparison of two things' values in the pre-state."""
    x, term, op, y = atom.args
    tid, _ = spec_lf_order.entry(terms.ids, x.kind, term)
    if tid is None:
        raise ValueError("no translation of a comparison of the %s of a %s" % (term, x.kind))
    terms.emit("ccmp2", terms.term(x), tid, op, terms.term(y), "pos" if pos else "neg")


# --- the steps -----------------------------------------------------------------------------------------------------
def said(items, pos=True):
    """[(x, T, op, y, pos)] of every comparison of two things' values `items` (a pre-state) say."""
    out = []
    for i in items:
        if isinstance(i, Box) and i.op == "not" and not i.refs:
            out += said(i.body, not pos)
        elif isinstance(i, Atom) and i.pred == PRED:
            out.append(i.args + (pos,))
    return out


def holds(t, v, op, w, pos):
    k, m = spec_lf_order.key(t, v), spec_lf_order.key(t, w)
    if op == "same":
        return (v == w or k is not None and k == m) == pos
    return (k is not None and m is not None and (k > m if op == "after" else k < m)) == pos


def values(r, t, refs):
    """{referent: value} of `refs`' values of `t` that meet every comparison the pre-state says of them and every
    value and point spec_lf_order's bounds say of each, the first in candidate order; None when none does."""
    comps = [c for c in said(r.pre) if c[1] == t.term]
    own = {x: spec_lf_order.bounds(r.pre, x, t.term) for x in refs}
    pool = spec_lf_order.candidates(t, [w for b in own.values() for _, w, _ in b if spec_lf_order.key(t, w)])
    chosen = {}

    def fits(x, v):
        chosen[x] = v
        ok = all(spec_lf_order.meets(t, v, op, w) == pos for op, w, pos in own[x]) and all(
            holds(t, chosen[a], op, chosen[b], pos) for a, _, op, b, pos in comps if a in chosen and b in chosen)
        del chosen[x]
        return ok

    def go(i):
        if i == len(refs):
            return True
        for v in pool:
            if fits(refs[i], v):
                chosen[refs[i]] = v
                if go(i + 1):
                    return True
                del chosen[refs[i]]
        return False
    return dict(chosen) if go(0) else None


def value_of(r, x, t):
    """The value the Givens give x's `t` when the scenario's first line compares x's with another thing's, else None;
    chosen once a Reader for every thing compared."""
    memo = r.__dict__.setdefault("compared", {})
    if t.term not in memo:
        refs = list(dict.fromkeys(z for a, term, _, b, _ in said(r.pre) if term == t.term for z in (a, b)))
        memo[t.term] = values(r, t, refs) if refs else {}
        if memo[t.term] is None:
            import spec_steps4_boxes  # here: the steps import this module through spec_steps4
            raise spec_steps4_boxes.TraceError("no values of the %s meet the line's comparisons" % t.term)
    return memo[t.term].get(x)


def given(r, item):
    """The Givens of a comparison of two things' values: each thing brought in, and its value."""
    x, term, _, y = item.args
    t = next(t for t, _ in r.vocab.attributes if t.term == term)
    return r.introduce(item) + [("SCond", spec_lf_order.value_cond(r, z, term, value_of(r, z, t))) for z in (x, y)]
