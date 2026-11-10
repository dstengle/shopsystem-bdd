"""The number of Ks (b240, construct #3): one translation of spec_rgl_np's `K_NumberOf`, `Count_Up` and `Count_Cmp` in
each place a line is read.

- the form: "the number of Ks that P" (`np`) a referent of kind `number` and a `number` box over the Ks it counts,
  made inside it with what restricts them (`Box("number", Ks, restrictions, count=the number's referent)`); "the
  number of Ks that P is more than n" (`cond`) R7's count box over the Ks with an empty scope, n a number word, a
  code of digits, or any other code as a parameter (a referent of kind `number`); `show`, the box's head line;
- the check: a printed number (`facts`) an object whose restrictions are the counted Ks' (`oattr(R,X,counts,K)` and
  the Ks' attributes and edges said of X), so two numbers of two sets of things are two things; a compared number
  (`signature`, spec_lf_quant's count) `ccount(R,X,B,N)` (`pcount` of a parameter) with the counted K's restrictions
  as `csig(R,X,L,Y,Pol)`, `csiga(R,X,T,V,Pol)`, which check.lp's `#count` reads;
- the steps: a printed number brings in two Ks with their restrictions (`bring`) and is said "the number of lines of
  the stage s1" where a step says it (`step_np`); a comparison with a parameter the Given of itself (`compared`).
"""
from dataclasses import replace

import spec_lf_np as nps
import spec_rgl
from spec_lf_core import NP, Atom, Box, Ref

KIND, COUNTS = "number", "counts"
OPS = {"Count_OpMore": "more than", "Count_OpLess": "fewer than", "Count_OpAtLeast": "at least",
       "Count_OpAtMost": "at most", "Count_OpIs": "exactly"}


# --- the form ---------------------------------------------------------------------------------------------------
def counted(st, tree):
    """(the counted referent, the referents and conditions of its restrictions) of a `K_NumberOf` tree."""
    cn = nps.args(tree)[0]
    if st.names.kind(nps.fun(tree))[1] != "NumberOf":
        raise nps.unknown(tree)
    ref = st.ref(nps.head(st, cn))
    refs, conds = nps.restrict(st, cn, ref)
    return ref, refs, conds


def np(st, tree):
    """The NP of "the number of Ks that P": its referent, restricted by the `number` box."""
    num = st.ref(KIND)
    ref, refs, conds = counted(st, tree)
    return NP(num, "a", [Box("number", tuple(dict.fromkeys([ref] + refs)), tuple(conds), None, num)])


def cond(st, tree):
    """(referents, conditions) of "the number of Ks that P is more than n", or None for another condition."""
    if nps.fun(tree) != "Count_Cmp":
        return None
    x, op, val = nps.args(tree)
    ref, refs, conds = counted(st, x)
    if nps.fun(val) == "Count_Code":
        lit = nps.args(val)[0]
        word = nps.args(lit)[0].strip('"').strip("`")
        n = int(word) if word.isdigit() else nps.code(st, KIND, lit).ref
    else:
        n = int(nps.fun(val)[len("Count_"):])
    box = Box("count", tuple(dict.fromkeys([ref] + refs)), tuple(conds), Box("scope"), (OPS[nps.fun(op)], n))
    st.close([box])
    return [], [box]


def show(b, term):
    """The head of a `number` box or of a count box: "number x4 of", "count more than 3", "count more than x3"."""
    if b.op == "number":
        return "number %s of" % term(b.count)
    return "%s %s %s" % (b.op, b.count[0], term(b.count[1]))


# --- the check --------------------------------------------------------------------------------------------------
def literals(body, pol="pos"):
    """(atom, polarity) of a restriction's atoms, through `not` boxes with no referents of their own."""
    for item in body:
        if isinstance(item, Box) and item.op == "not" and not item.refs:
            yield from literals(item.body, "neg" if pol == "pos" else "pos")
        elif isinstance(item, Atom):
            yield item, pol
        else:
            raise ValueError("no translation of the number of things there")


def said(w, y, box):
    """[(attr, (T, V), pol) or (edge, (L, Y), pol)] of what the restrictions say of the counted `y`."""
    out = []
    for item, pol in literals(box.body):
        if item.pred == "attr" and item.args[0] == y and not isinstance(item.args[2], Ref):
            out.append(("attr", w.ids.attr(y.kind, item.args[1], item.args[2]), pol))
        elif item.pred in ("rel", "state"):
            q, a, b = w.edge(item)
            if y not in (a, b) or a == b:
                raise ValueError("no translation of the number of things there")
            out.append(("edge", ("r(%s)" % q, b) if a == y else ("i(%s)" % q, a), pol))
        else:
            raise ValueError("no translation of the number of things there")
    return out


def facts(w, box):
    """A printed number: its referent an object restricted as the Ks it counts are."""
    x, y = box.count, box.refs[0]
    w.roles(box.refs[1:])
    w.emit("oattr", w.term(x), COUNTS, w.ids.kind(y.kind))
    for what, (a, b), pol in said(w, y, box):
        if what == "attr":
            w.emit("oattr" if pol == "pos" else "onattr", w.term(x), a, b)
        elif pol == "pos":
            q = a[2:-1]
            w.emit("orel", q, *((w.term(x), w.term(b)) if a.startswith("r(") else (w.term(b), w.term(x))))
        else:
            raise ValueError("no translation of the number of things there")


def signature(w, box):
    """A compared number: the counted K a role, its count and the restrictions it is counted by."""
    y, (bound, n) = box.refs[0], box.count
    import spec_lf_quant  # here: spec_lf_quant imports this module
    w.roles(box.refs)
    if isinstance(n, Ref):
        w.emit("pcount", y.name, spec_lf_quant.BOUNDS[bound], w.term(n))
    else:
        w.emit("ccount", y.name, spec_lf_quant.BOUNDS[bound], n)
    for what, (a, b), pol in said(w, y, box):
        if what == "attr":
            w.emit("csiga", y.name, a, b, pol)
        else:
            w.emit("csig", y.name, a, w.term(b), pol)


# --- the steps --------------------------------------------------------------------------------------------------
def cn(r, box):
    """The `K_CN` tree of the counted K: its row's modifier innermost, then each attribute and state of it."""
    y = box.refs[0]
    K = spec_rgl.kid(y.kind)
    tree, mods = (K + "_UseN", (K + "_n",)), []
    for item, pol in literals(box.body):
        p = ("PPos",) if pol == "pos" else ("PNeg",)
        if item.pred == "rel" and item.args[1] == y and pol == "pos" and tree[0].endswith("_UseN"):
            n = next(n for n, (k1, word, k2) in enumerate(r.vocab.rows, 1) if k1 == y.kind and word == item.args[0]
                     and k2 in r.vocab.ancestors(item.args[2].kind))      # of the rows of the word, the one of its kinds
            tree = ("r%d_%s_Mod" % (n, spec_rgl.slug(item.args[0])), (K + "_n",), r.np(item.args[2], r.vocab.rows[
                n - 1][2]))
        elif item.pred == "attr" and item.args[0] == y:
            T = next("t_%s_%d" % (spec_rgl.slug(t.term), n) for n, (t, _) in enumerate(r.vocab.attributes, 1)
                     if t.term == item.args[1])
            mods.append(("%s_Whose_%s" % (K, T), p, (("%s_v_%s" % (T, spec_rgl.slug(item.args[2])),),)))
        elif item.pred == "state" and item.args[2][0][1] == y:
            verb, sense, roles = item.args
            fun, subject, slots = r.frame(verb, sense, roles)
            vp = (fun,) + tuple(r.arg(x[1], k) for x, k in zip([x for x in roles[1:] if len(x) == 2], slots))
            mods.append(("%s_Rel_%s" % (K, spec_rgl.kid(subject)), p, (vp,)))
        else:
            raise _trace("no step of the number of %ss there" % y.kind)
    for fun, p, rest in mods:       # "lines of the stage whose outcome is `accepted`": a clause around the noun
        tree = (fun, p, tree) + rest
    return (K + "_NumberOf", tree)


def _trace(why):
    import spec_steps4_boxes  # here: the steps import this module through spec_steps4_boxes
    return spec_steps4_boxes.TraceError(why)


def bring(r, box):
    """A printed number: two Ks it counts brought in with their restrictions; the number named where said."""
    import spec_steps4_boxes as boxes  # here: the steps import this module through spec_steps4_boxes
    r.numbers[box.count] = box
    for k in (1, 2):
        m = {x: replace(x, name="%s.%d" % (x.name, k)) for x in box.refs}
        boxes.bring(r, boxes.subst(box, m))


def step_np(r, ref, slot):
    """The `K_NP` tree of a printed number in a slot: "the number of lines of the stage s1", a thing."""
    if slot != "thing":
        raise _trace("no step of a number in a slot of %s" % slot)
    return ("Count_Up", cn(r, r.numbers[ref]))


def compared(r, box):
    """The Given of a comparison with a parameter: "the number of lines of the stage s1 is more than `limit`", the
    things its restrictions name brought in first."""
    out = []
    for item, _ in literals(box.body):
        for x in item.args[2] if item.pred == "state" else item.args[1:]:
            x = x[1] if isinstance(x, tuple) else x
            if isinstance(x, Ref) and x not in box.refs and x not in r.known and x.origin in ("while", "trigger"):
                r.known.add(x)
                out.append((spec_rgl.kid(x.kind) + "_Given", (spec_rgl.kid(x.kind) + "_n",), ("NameLit", r.name(x))))
    op = next(k for k, v in OPS.items() if v == box.count[0])
    return out + [("SCond", ("Count_Cmp", cn(r, box), (op,), ("Count_Code", ("CodeLit", box.count[1].value))))]
