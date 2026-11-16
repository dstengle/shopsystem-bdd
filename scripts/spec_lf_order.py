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
import spec_value_kinds
from spec_lf_core import Atom, Box, const

NUMBER, LISTED, WIDTH, TEXT = "by number", "as listed", 6, 64
ORDER = {"After": "after", "Before": "before"}
TIME = re.compile(r"(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2}))?Z?)?")


def order(t):
    """How the attribute entry `t` orders its values, its value order (spec_value_kinds, b275): NUMBER, LISTED, a
    type's name (`number`, `time`, `text`) or None."""
    return spec_value_kinds.value_order(t)


def same(t):
    """What two entries of one word share when they have one value order (b287): its order, and an entry ordered as
    listed its own values too, so that two lists that differ are two orders; None when it has none."""
    how = order(t)
    return (how, tuple(x.strip("`") for x in t.values)) if how == LISTED else how


def dense(t):
    """True when any literal of its kind is a value of `t`: ordered by number, or of a type (b275)."""
    return order(t) not in (None, LISTED)


def key(t, value):
    """The point of `value` (with or without its backticks or quotes) in `t`'s order, a tuple of numbers (WIDTH of
    them, TEXT of a text), or None."""
    v, how = value.strip("`\""), order(t)
    if how == NUMBER and re.fullmatch(r"\d+(?:\.\d+)*", v):
        parts = [int(n) for n in v.split(".")][:WIDTH]
        return tuple(parts + [0] * (WIDTH - len(parts)))
    if how == "number" and re.fullmatch(r"-?\d+(?:\.\d+)?", v):     # a decimal: its floor and fraction (b275)
        whole, _, frac = v.lstrip("-").partition(".")
        n, f = int(whole), int((frac + "0" * 9)[:9])
        n, f = (-n - (1 if f else 0), (10 ** 9 - f) % 10 ** 9) if v.startswith("-") else (n, f)
        return (n, f) + (0,) * (WIDTH - 2)
    if how == "time" and TIME.fullmatch(v):
        return tuple(int(n or 0) for n in TIME.fullmatch(v).groups())
    if how == "text":
        return tuple(ord(c) for c in v[:TEXT]) + (0,) * (TEXT - len(v[:TEXT]))
    bare = [x.strip("`") for x in t.values]
    if how == LISTED and v in bare:
        return (bare.index(v),) + (0,) * (WIDTH - 1)
    return None


def described(t):
    """How `t`'s values are ordered, in words: "ordered by number", "ordered as listed: `a`, `b`", "a number"."""
    how = order(t)
    if how in (NUMBER, LISTED):
        return "ordered " + how + ("" if how == NUMBER else ": " + ", ".join(t.values))
    return "a %s" % how


def point(st, t, tree):
    """The value a `T_Pt` tree names, its words with backticks; a code that is no value noted (the refusal)."""
    if nps.fun(tree).endswith("_PtVal"):
        return st.names.value(nps.fun(nps.args(tree)[0]))
    value = code(nps.args(tree)[0])
    if key(t, value) is None:
        st.notes.append("%s is no value of the %s of a %s, which is %s" % (value, t.term, t.kinds[0], described(t)))
    return value


def code(lit):
    return nps.args(lit)[0].strip('"').replace(spec_rgl.TOKEN, " ")


def cond(st, t, rest, a):
    """(referents, conditions) of `T_Cmp`, `T_Between`, `T_IsCodeOf` or `T_<K>_IsCode`, or None when `rest` is none of them."""
    if rest.endswith("_IsCode") or rest == "IsCodeOf":
        x, value = nps.np(st, a[1]) if rest != "IsCodeOf" else nps.owner(st, a[1]), code(a[2])
        return st.apply([x], lambda r: Atom("attr", (r[0], t.term, value)),
                        1 if a[0] == "PNeg" else None)
    if rest.split("_")[0] in ("CmpT", "SameAs"):     # one thing's value compared with another's (b275, b287)
        import spec_lf_compare  # here: spec_lf_compare imports this module
        return spec_lf_compare.cond(st, t, rest, a)
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
        if tid is None or not dense(t) or key(t, value) is None:
            raise
        terms.emit("ckey", tid, const(value), tup(key(t, value)))
        return tid, const(value)


def tup(k):
    return "(%s)" % ",".join(str(n) for n in k)


def domain(vocab):
    """`dense(T)` of each attribute ordered by number, `vkey(T, V, Key)` of each of an ordered attribute's values, and
    `tcan(T, C)` of each attribute, C the first entry of its word with its value order (`same`, b287: two senses of one word
    compared over one order's cells), T itself when it has none (its values' ids are its own, never another's)."""
    out, first = [], {}
    for tid, (_, t) in sorted(vocab.attrs.items()):
        out.append("tcan(%s,%s)." % (tid, first.setdefault((t.term, same(t)), tid) if order(t) else tid))
        if dense(t):
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
    if order(t) in ("number", "time", "text"):     # a value of a type: any literal of it (b275)
        return listed + typed(order(t), [v.strip("`\"") for v in said])
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


def typed(how, said):
    """Literals of the type `how` a Given may give: around each value said, then a few of their own, each a code."""
    import datetime
    if how == "number":
        ns = [int(float(s)) + d for s in said for d in (-1, 0, 1)] + [1, 2, 3]
        out = [str(n) for n in ns] + [s for s in said]
    elif how == "time":
        days = [datetime.date.fromisoformat(s[:10]) + datetime.timedelta(days=d) for s in said for d in (-1, 1)]
        out = [d.isoformat() for d in days] + ["2026-01-0%d" % n for n in (1, 2, 3)]
    else:
        out = [s + "a" for s in said] + [s[:-1] for s in said if s[:-1]] + ["a", "b", "c"]
    return ["`%s`" % v for v in dict.fromkeys(out)]


def meets(t, v, op, w):
    if op == "=":
        return v == w or key(t, v) is not None and key(t, v) == key(t, w)
    return {"after": key(t, v) > key(t, w), "before": key(t, v) < key(t, w)}[op]


def given(r, item):
    """The Cond tree of the Given of x's value: one on the right side of every point the scenario's first line names
    and, of a thing compared with another (b275), the value spec_lf_compare chose of both."""
    import spec_lf_compare  # here: spec_lf_compare imports this module
    x, term = item.args[0], item.args[1]
    t = own(r, x, term)
    said = bounds(r.pre, x, term)
    value = spec_lf_compare.value_of(r, x, t) or next((v for v in candidates(t, [w for _, w, _ in said if key(t, w)])
                                                       if all(meets(t, v, op, w) == pos for op, w, pos in said)), None)
    if value is None:
        import spec_steps4_boxes  # here: the steps import this module through spec_steps4
        raise spec_steps4_boxes.TraceError("no value of the %s of %s meets the line" % (term, x.name))
    return value_cond(r, x, term, value)


def own(r, x, term, numbered=False):
    """The entry of `term` whose owner kind x is of, up grammar 4's kind tree (b287: two entries of one word); with
    `numbered`, (its number, the entry, its owner kinds)."""
    n, t, ks = next((n, t, ks) for n, (t, ks) in enumerate(r.vocab.attributes, 1) if t.term == term
                    and any(k in ks for k in r.vocab.ancestors(x.kind)))
    return (n, t, ks) if numbered else t


def value_cond(r, x, term, value):
    """The Cond tree "the T of x is `v`", the full form (b257), of a listed value or a code."""
    n, t, ks = own(r, x, term, True)
    k = next(k for k in r.vocab.ancestors(x.kind) if k in ks)
    T = "t_%s_%d" % (spec_rgl.slug(term), n)
    owner = ("%s_Of_%s" % (T, spec_rgl.kid(k)), named(r, x, k) or r.np(x, k))
    if value in t.values:
        return (T + "_IsOf", ("PPos",), owner, ("%s_v_%s" % (T, spec_rgl.slug(value)),))
    return (T + "_IsCodeOf", ("PPos",), owner, ("CodeLit", value))


def named(r, x, k):
    """The K_NP of a code's thing said "the `a` file", in a slot of kind `k`, or None of any other referent."""
    if x.origin not in ("constant", "parameter") or x.value in r.actors:
        return None
    K = spec_rgl.kid(x.kind)
    tree = (K + "_Named", ("CodeLit", x.value), (K + "_UseN", (K + "_n",)))
    return (K + "_Simple", tree) if k == x.kind else ("%s_Up_%s" % (K, spec_rgl.kid(k)), tree)
