"""The noun phrases of grammar 4 in the logical form (the CNL 4 design, call 8; I11a): one translation per template of
spec_rgl, spec_rgl_np and spec_rgl_rel, the funs of a template told by their names (`Names`).

A determiner gives a referent's reading: "a" and a bare plural a referent of the part (a bare plural in a response
"every"), "every" an `every` box, "no" (and "nothing") a `not` box, "only" an `only` box, a count ("at least
two", "one") a `count` box (call 4, I15); "the" binds by R2 and R11
(spec_lf_read), else is a referent of the part marked definite and the line refused. An actor and a code are one
referent of the line, a code a constant when it is a word of the context and a parameter when it is not (call 7);
"this K" the run's own K, an indexical (call 6). "the K of x" (R2, b221), "the T of x", "its T" and "the K T" are one
functional image of x, "its" bound to the subject of its clause; a row's modifier, "has", "holds" and "whose" are `rel`
atoms, an attribute's value an `attr` atom; a relative clause restricts its noun by its frame's atom, with its
polarity.
"""
import re

import spec_gf
import spec_lf_core as core
import spec_lf_distinct
import spec_lf_option
import spec_lf_read
import spec_rgl
from spec_lf_core import NP, Atom, Box, NPList


class Names:
    """The vocabulary's things by the names spec_rgl gives their funs."""

    def __init__(self, vocab):
        self.kinds = sorted(((spec_rgl.kid(k), k) for k in vocab.kinds), key=lambda p: -len(p[0]))
        self.actors = {"a_%s_%d" % (spec_rgl.slug(t), n + 1): (t, k) for n, (t, k) in enumerate(vocab.actors)}
        self.attrs = sorted((("t_%s_%d" % (spec_rgl.slug(t.term), n), t) for n, (t, _) in
                             enumerate(vocab.attributes, 1)), key=lambda p: -len(p[0]))
        self.rows = {n: row for n, row in enumerate(vocab.rows, 1)}
        self.verbs = {n: v for n, v in enumerate(vocab.verbs, 1)}

    def kind(self, name):
        """(the kind whose id `name` starts with, the rest of the name after it), or (None, name)."""
        return next(((k, name[len(K) + 1:]) for K, k in self.kinds if name.startswith(K + "_")), (None, name))

    def attr(self, name):
        return next(((t, name[len(T) + 1:]) for T, t in self.attrs if name.startswith(T + "_")), (None, name))

    def value(self, name):
        t, rest = self.attr(name)
        return next(v for v in t.values if "v_" + spec_rgl.slug(v) == rest)

    def row(self, name):
        m = re.match(r"^r(\d+)_.*_(Mod|Has|Holds|Cpd|Gap)$", name)
        return (self.rows[int(m.group(1))], m.group(2)) if m else (None, None)


def fun(tree):
    return tree if isinstance(tree, str) else tree[0]


def args(tree):
    return [] if isinstance(tree, str) else tree[1:]


def unknown(tree):
    return ValueError("the logical form has no translation of the fun %s" % fun(tree))


def code(st, kind, lit):
    """A code's referent: `CodeLit "..."`."""
    text = args(lit)[0].strip('"').replace(spec_gf.PLACEHOLDER, " ")
    word = text.strip("`")
    return core.fixed(st.constant(kind, text, "constant" if word in st.vocab.words else "parameter"))


def np(st, tree):
    """An argument or a noun phrase (K_Arg, K_NP, K_NP0, T_NP) as an NP or an NPList."""
    name, a = fun(tree), args(tree)
    if name in st.names.actors:
        term, kind = st.names.actors[name]
        return core.fixed(st.constant(kind, term, "constant"))
    if name == "k_thing_Nothing":
        return NP(st.ref("thing"), "no")
    kind, rest = st.names.kind(name)
    if kind is not None:
        if rest in ("One", "Simple") or rest.startswith("Up_"):
            return np(st, a[0])
        if rest == "Only":
            found = np(st, a[0])
            found.quant = "only"
            return found
        if rest in ("And", "Or"):
            return NPList(rest.lower(), members(st, a[0]))
        if rest in ("NamedAnd", "SetTo"):     # options (b240)
            return spec_lf_option.np(st, kind, rest, a)
        if rest in ("Code", "Named"):
            return code(st, kind, a[0])
        if rest == "This":
            return core.fixed(st.constant(kind, st.vocab.this[kind], "indexical"))
        if rest == "Det":
            return det(st, a[0], a[1])
        if rest == "Its":
            return its(st, kind)
    t, rest = st.names.attr(name)
    if t is not None:
        return value_np(st, t, owner(st, tree))
    if name == "Count_Up":      # "the number of Ks that P" (b240)
        import spec_lf_number  # here: spec_lf_number imports this module
        return spec_lf_number.np(st, a[0])
    raise unknown(tree)


def members(st, tree):
    name, a = fun(tree), args(tree)
    if name.endswith("_Two"):
        return [np(st, a[0]), np(st, a[1])]
    if name.endswith("_More"):
        return [np(st, a[0])] + members(st, a[1])
    raise unknown(tree)


def head(st, cn):
    """The kind of a common noun's head."""
    row = st.names.row(fun(cn))[0]
    return row[0] if row else st.names.kind(fun(cn))[0]


BOUNDS = {"AtLeast": "at least", "AtMost": "at most", "Exactly": "exactly", "MoreThan": "more than",
          "FewerThan": "fewer than"}


def count(d):
    """A count's (bound, number) of a determiner's tree (call 4, I15): "one K" is exactly one; else None."""
    if fun(d) == "DetOne":
        return ("exactly", 1)
    if fun(d) == "DetCount":
        bound, many = args(d)
        return (BOUNDS[fun(bound)], int(fun(many)[len("Many"):]))
    return None


def det(st, tree, cn):
    """A determiner (its tree) over a common noun: the referent made (or bound) first, then what restricts it."""
    kind, d = head(st, cn), fun(tree)
    said = None
    if count(tree):
        ref = st.ref(kind)
        refs, conds = restrict(st, cn, ref)
        return NP(ref, "count", conds, refs, count=count(tree))
    row, suffix = st.names.row(fun(cn))
    if d in ("DetThe", "DetSame") and suffix == "Mod" and row[1] == "of":
        return of(st, row, np(st, args(cn)[1]))
    if d in spec_lf_distinct.DETS:      # "another K", "two Ks", "the same K" (b240)
        return spec_lf_distinct.det(st, d, cn, kind, restrict)
    if d in ("DetThe", "DetThePl"):
        found = spec_lf_read.the(st, kind, d == "DetThePl")     # R2, R11
        if found is not None:
            refs, conds = restrict(st, cn, found.ref)
            found.restr, found.inner = found.restr + conds, found.inner + refs
            return found
        quant, ref = "a", st.ref(kind, definite=True)
    else:
        quant = {"DetEvery": "every", "DetNo": "no"}.get(d, "a")
        if d == "DetPl" and st.origin == "response":
            quant = "every"
        said = {"DetA": spec_lf_read.article(spec_lf_read.noun(st, kind)),
                "DetPl": spec_lf_read.noun(st, kind, True)}.get(d)
        ref = st.ref(kind)
    refs, conds = restrict(st, cn, ref)
    return NP(ref, quant, conds, refs, said=said)


def of(st, row, x):
    """R2's "the K of X": X read first, then the image of X by the row `K | of | S`, a referent of its own (never an
    earlier K, nor the K whose relative clause holds it), placed after X: in the scope of "every Y", one K of each Y."""
    ref, new = st.image((row, x.ref), row[0])
    if not new:
        return NP(ref, "fixed", deps=[x], new=False)
    return NP(ref, "a", [Atom("rel", ("of", ref, x.ref))], deps=[x], image=True)


def its(st, kind):
    """"its K": the image of the clause's subject by the row `K | of | S`."""
    subject = st.subject
    rows = [r for r in st.names.rows.values() if r[0] == kind and r[1] == "of"]
    spec_lf_read.its(st, [r[2] for r in rows], "its " + spec_lf_read.noun(st, kind))     # R8
    row = next((r for r in rows if subject and r[2] in st.vocab.ancestors(subject.kind)), rows[0])
    ref, new = st.image((row, subject), kind)
    return NP(ref, "a", [Atom("rel", ("of", ref, subject))], image=True) if new else core.fixed(ref)


def owner(st, tnp):
    """The noun phrase whose attribute a T_NP is: "the T of x", "its T", "the K T"."""
    rest = st.names.attr(fun(tnp))[1]
    if rest == "Up":
        return owner(st, args(tnp)[0])
    if rest == "Its":
        t = st.names.attr(fun(tnp))[0]
        spec_lf_read.its(st, next(ks for term, ks in st.vocab.attributes if term is t), "its " + t.term)    # R8
        return core.fixed(st.subject)
    if rest.startswith("Of_"):
        return np(st, args(tnp)[0])
    if rest.startswith("Cpd_"):
        kind, _ = st.names.kind(rest[len("Cpd_"):] + "_")
        return det(st, args(tnp)[0], ["%s_UseN" % spec_rgl.kid(kind), "%s_n" % spec_rgl.kid(kind)])
    raise unknown(tnp)


def value_np(st, t, x):
    """The value of the attribute `t` of `x`, a functional image placed after x."""
    ref, new = st.image((t.term, x.ref), t.term)
    if not new:
        return NP(ref, "fixed", deps=[x], new=False)
    return NP(ref, "a", [Atom("attr", (x.ref, t.term, ref))], deps=[x], image=True)


def restrict(st, cn, ref):
    """(referents, conditions) a common noun puts on its referent `ref`, which R2 passes over while it is read."""
    st.open.append(ref)
    try:
        return restricting(st, cn, ref)
    finally:
        st.open.pop()


def restricting(st, cn, ref):
    name, a = fun(cn), args(cn)
    row, suffix = st.names.row(name)
    if suffix == "Mod":
        return st.apply([np(st, a[1])], lambda r: Atom("rel", (row[1], ref, r[0])))
    if suffix == "Cpd":
        owner_np = det(st, "DetThe", ["%s_UseN" % spec_rgl.kid(row[2]), ""])
        return st.apply([owner_np], lambda r: Atom("rel", ("of", ref, r[0])))
    rest = st.names.kind(name)[1]
    if rest == "UseN":
        return [], []
    refs, conds = restricting(st, a[1], ref)
    pol = a[0] == "PNeg"
    if rest.startswith("Rel_"):
        more = st.clauses.clause(st, core.fixed(ref), a[2], pol)
    elif rest.startswith("Obj_"):
        more = st.clauses.gapped(st, ref, np(st, a[2]), a[3], pol)
    elif rest.startswith("Whose_r"):
        row = st.names.rows[int(re.match(r"Whose_r(\d+)_", rest).group(1))]
        y, new = st.image((row, ref), row[0])
        r2, c2 = st.clauses.clause(st, core.fixed(y), a[2], pol)
        more = ([y] if new else []) + r2, [Atom("rel", ("of", y, ref))] + c2
    elif rest.startswith("Whose_"):
        t, _ = st.names.attr(rest[len("Whose_"):] + "_")
        atom = Atom("attr", (ref, t.term, st.names.value(fun(a[2]))))
        more = [], [Box("not", (), (atom,)) if pol else atom]
    else:
        raise unknown(cn)
    return refs + more[0], conds + more[1]
