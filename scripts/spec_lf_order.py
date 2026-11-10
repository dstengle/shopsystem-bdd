"""Ordered comparison (b240, construct #6; the CNL 4 design, sections 6.2 and 7.2, call 9): an attribute whose entry
says `Order:` has ordered values, `Order: by number.` (a code of numbers joined by dots is a value, compared number by
number, as a release is) or `Order: as listed.` (its `Values:` in the order they are listed, and only those). One
translation of spec_rgl_np's `T_Cmp`, `T_Between`, `T_IsCodeOf` and `T_<K>_IsCode` in each place a line is read:

- the form (`cond`, `code`): "the T of x is after v" the atom `cmp(x, T, after, v)` (the design's `cmp(x, A, op, v)`,
  the time pack's comparison said of an attribute), "is after v and before w" two of them; a code that is no value of
  the attribute a note, which spec_lf_read gives as the line's refusal; `show` its line in `model parse --form`;
- the check (`literal`, `value_ids`, `domain`): `ccmp(R, X, T, Op, Key, Pol)`, a value's point as a tuple (`key`),
  the entry's values' points `vkey(T, V, Key)` and `dense(T)` of an order by number, a line's code of a value no entry
  lists `ckey(R, T, V, Key)`; grammar/check.lp reads them exactly over the points a pair names and the gaps between;
- the steps (`given`): one value on the right side of every point the scenario's first line names for x's T, a value
  the entry lists first, given "the file f1 is `2.0.0`".
"""
import re

import spec_lf_np as nps
import spec_rgl
from spec_lf_core import Atom, Box, const

NUMBER, LISTED, WIDTH = "by number", "as listed", 6
ORDER = {"After": "after", "Before": "before"}


def order(t):
    """NUMBER, LISTED or None: how the attribute entry `t` orders its values."""
    said = " ".join(getattr(t, "order", "").lower().split())
    return said if said in (NUMBER, LISTED) else None


def key(t, value):
    """The point of `value` (with or without its backticks) in `t`'s order, a tuple of WIDTH numbers, or None."""
    v, how = value.strip("`"), order(t)
    if how == NUMBER and re.fullmatch(r"\d+(?:\.\d+)*", v):
        parts = [int(n) for n in v.split(".")][:WIDTH]
        return tuple(parts + [0] * (WIDTH - len(parts)))
    bare = [x.strip("`") for x in t.values]
    if how == LISTED and v in bare:
        return (bare.index(v),) + (0,) * (WIDTH - 1)
    return None


def point(st, t, tree):
    """The value a `T_Pt` tree names, its words with backticks; a code that is no value noted (the refusal)."""
    if nps.fun(tree).endswith("_PtVal"):
        return st.names.value(nps.fun(nps.args(tree)[0]))
    value = code(nps.args(tree)[0])
    if key(t, value) is None:
        how = order(t) + ("" if order(t) == NUMBER else ": " + ", ".join(t.values))
        st.notes.append("%s is no value of the %s of a %s, which is ordered %s" % (value, t.term, t.kinds[0], how))
    return value


def code(lit):
    return nps.args(lit)[0].strip('"').replace(spec_rgl.TOKEN, " ")


def cond(st, t, rest, a):
    """(referents, conditions) of `T_Cmp`, `T_Between`, `T_IsCodeOf` or `T_<K>_IsCode`, or None when `rest` is none of them."""
    if rest.endswith("_IsCode") or rest == "IsCodeOf":
        x, value = nps.np(st, a[1]) if rest != "IsCodeOf" else nps.owner(st, a[1]), code(a[2])
        return st.apply([x], lambda r: Atom("attr", (r[0], t.term, value)),
                        1 if a[0] == "PNeg" else None)
    if rest == "Cmp":
        op, value = ORDER[nps.fun(a[2])], point(st, t, a[3])
        return st.apply([nps.owner(st, a[1])], lambda r: Atom("cmp", (r[0], t.term, op, value)),
                        1 if a[0] == "PNeg" else None)
    if rest != "Between":
        return None
    first, second = (ORDER[nps.fun(a[1])], point(st, t, a[2])), (ORDER[nps.fun(a[3])], point(st, t, a[4]))
    made = []

    def build(r):
        made.append(Atom("cmp", (r[0], t.term) + first))
        return made[-1]
    refs, conds = st.apply([nps.owner(st, a[0])], build)
    return refs, pair(conds, made, second)


def pair(conds, made, second):
    """`conds` with the second comparison of "after v and before w" after each first one."""
    out = []
    for c in conds:
        if isinstance(c, Box):
            c = Box(c.op, c.refs, tuple(pair(c.body, made, second)),
                    c.scope and Box(c.scope.op, c.scope.refs, tuple(pair(c.scope.body, made, second))), c.count)
        out.append(c)
        if any(c is m for m in made):
            out.append(Atom("cmp", c.args[:2] + second))
    return out


def show(a, term):
    x, t, op, v = a.args
    return "cmp(%s(%s)) %s %s" % (t, term(x), op, v)


# --- the check ---------------------------------------------------------------------------------------------------
def entry(ids, kind, term):
    """(attribute id, its entry) of `term` of a thing of `kind`, up grammar 4's kind tree, or (None, None)."""
    for k in ids.above(kind):
        for tid, (kid, t) in ids.v.attrs.items():
            if t.term == term and kid == ids.v.by_term.get(k):
                return tid, t
    return None, None


def literal(terms, atom, pos):
    """`ccmp(R, X, T, Op, Key, Pol)` of a comparison in the pre-state."""
    x, term, op, value = atom.args
    tid, t = entry(terms.ids, x.kind, term)
    if tid is None or key(t, value) is None:
        raise ValueError("no translation of a comparison of the %s of a %s" % (term, x.kind))
    terms.emit("ccmp", terms.term(x), tid, op, tup(key(t, value)), "pos" if pos else "neg")


def value_ids(terms, kind, term, value):
    """(attribute id, value id) of a value of an attribute; a code no entry lists of one ordered by number its own
    constant, its point `ckey`."""
    try:
        return terms.ids.attr(kind, term, value)
    except ValueError:
        tid, t = entry(terms.ids, kind, term)
        if tid is None or order(t) != NUMBER or key(t, value) is None:
            raise
        terms.emit("ckey", tid, const(value), tup(key(t, value)))
        return tid, const(value)


def tup(k):
    return "(%s)" % ",".join(str(n) for n in k)


def domain(vocab):
    """`dense(T)` of each attribute ordered by number, `vkey(T, V, Key)` of each of an ordered attribute's values."""
    out = []
    for tid, (_, t) in sorted(vocab.attrs.items()):
        if order(t) == NUMBER:
            out.append("dense(%s)." % tid)
        for vid in vocab.attr_values[tid] if order(t) else ():
            k = key(t, vocab.value_text[vid])
            if k is not None:
                out.append("vkey(%s,%s,%s)." % (tid, vid, tup(k)))
    return out


# --- the steps -----------------------------------------------------------------------------------------------------
def bounds(items, x, term, pos=True):
    """[(op, value, pos)] of what `items` (a pre-state) say of x's `term`: comparisons, and values ("=")."""
    out = []
    for i in items:
        if isinstance(i, Box) and i.op == "not" and not i.refs:
            out += bounds(i.body, x, term, not pos)
        elif isinstance(i, Atom) and i.pred == "cmp" and len(i.args) == 4 and i.args[:2] == (x, term):
            out.append((i.args[2], i.args[3], pos))
        elif isinstance(i, Atom) and i.pred == "attr" and i.args[:2] == (x, term) and isinstance(i.args[2], str):
            out.append(("=", i.args[2], pos))
    return out


def candidates(t, said):
    """The values a Given may give, those the entry lists first, each in its order."""
    listed = sorted(t.values, key=lambda v: key(t, v) or ())
    if order(t) != NUMBER:
        return listed
    more = set()
    for v in list(t.values) + said:
        n = [int(p) for p in v.strip("`").split(".")]
        more |= {".".join(map(str, n[:-1] + [n[-1] + 1])), ".".join(map(str, n + [1]))}
        if any(n):
            k = max(i for i, p in enumerate(n) if p)
            more.add(".".join(map(str, n[:k] + [n[k] - 1] + [0] * (len(n) - k - 1))))
    return listed + sorted(("`%s`" % v for v in more), key=lambda v: (v.count("."), key(t, v)))


def meets(t, v, op, w):
    if op == "=":
        return v == w or key(t, v) is not None and key(t, v) == key(t, w)
    return {"after": key(t, v) > key(t, w), "before": key(t, v) < key(t, w)}[op]


def given(r, item):
    """The Cond tree of the Given of x's value: one on the right side of every point the scenario's first line names."""
    x, term = item.args[0], item.args[1]
    n, t, ks = next((n, t, ks) for n, (t, ks) in enumerate(r.vocab.attributes, 1) if t.term == term)
    k = next(k for k in r.vocab.ancestors(x.kind) if k in ks)
    said = bounds(r.pre, x, term)
    value = next((v for v in candidates(t, [w for _, w, _ in said if key(t, w)])
                  if all(meets(t, v, op, w) == pos for op, w, pos in said)), None)
    if value is None:
        import spec_steps4_boxes  # here: the steps import this module through spec_steps4
        raise spec_steps4_boxes.TraceError("no value of the %s of %s meets the line" % (term, x.name))
    T = "t_%s_%d" % (spec_rgl.slug(term), n)
    if value in t.values:
        return ("%s_%s_Is" % (T, spec_rgl.kid(k)), ("PPos",), r.np(x, k), ("%s_v_%s" % (T, spec_rgl.slug(value)),))
    return ("%s_%s_IsCode" % (T, spec_rgl.kid(k)), ("PPos",), r.np(x, k), ("CodeLit", value))
