"""Membership and emptiness over a row `K1 | in | K2` (b274), one translation of spec_rgl_np's `r<n>_in_In`,
`r<n>_in_Exactly` and `K2_Holds_Nothing` in each place a line is read:

- is-in, "x is in y": the row's atom `in(x, y)`, the one "y holds x" gives, so every reader reads it as holds-relation;
- holds-exactly, "y holds exactly the Ks that P": every plus only, `every [k: K] P scope in(k, y)` beside
  `not [k2: K] not P, in(k2, y)` (`vp`); the check reads the every half as an `every` object and the "no K that is not
  P" half on a response's object, of an act of any frame, as `onrel(R,X,Q,D,such(K,...))` and its every half as
  `onrel(R,X,Q,D,all(K,...))`, P each value `(T,V,Pol)` and each row or state to another thing `(Q,D,O,Pol)` (b297),
  each entailed only by the same restriction on the other side (`negated`, `every`); the steps bring in a K that is
  not P and say that y does not hold it (`absent`);
- "y holds nothing": `not [t: thing] in(t, y)`, no thing of any kind a row lets y's kind hold; the check's
  pre-state an `rnone` of each such kind (`none`), on a response's object an `onrel` to `kind(K)` of each (b297,
  `nothing_on`); the steps' Given "the worktree w1 holds nothing" (`given`), on a response's object its Then.
"""
from spec_lf_core import NP, Atom, Box, NPList, Ref

IN = "in"


def suffix(name):
    """The fun's construct: `In`, `Exactly` or `Nothing`, else None."""
    if name.endswith("_Holds_Nothing"):
        return "Nothing"
    tail = name.rsplit("_", 1)[-1]
    return tail if tail in ("In", "Exactly") and name.startswith("r") else None


def vp(st, tree, nps):
    """(the verb phrase's noun phrases, build(subject, their referents)) of a membership verb phrase, or None."""
    name, a = nps.fun(tree), nps.args(tree)
    said = suffix(name)
    if said == "Nothing":
        return [NP(st.ref("thing"), "no")], lambda s, r: Atom("rel", (IN, r[0], s))
    if said is None:
        return None
    row, _ = st.names.row(name)
    if said == "In":
        return [nps.np(st, a[0])], lambda s, r: Atom("rel", (row[1], s, r[0]))
    kind = nps.head(st, a[0])
    every = st.ref(kind)
    refs, conds = nps.restrict(st, a[0], every)
    other = st.ref(kind)
    refs2, conds2 = nps.restrict(st, a[0], other)
    members = [NP(every, "every", conds, refs), NP(other, "no", [Box("not", tuple(refs2), tuple(conds2))])]
    return [NPList("and", members)], lambda s, r: Atom("rel", (row[1], r[0], s))


# --- the check's facts (spec_lf_facts, spec_lf_quant) ---------------------------------------------------------------
def held(w, kind):
    """(relation id, the kind held) of each row `K | in | S` whose S is `kind` or a kind above it."""
    up = w.ids.above(kind)
    return [(rid, k1) for k1, word, k2, rid in w.ids.rows if word == IN and k2 in up]


def nothing(item, own):
    """True for "y holds nothing": `in(t, y)`, t a thing of the box's own."""
    return (isinstance(item, Atom) and item.pred == "rel" and item.args[0] == IN and item.args[1] in own
            and item.args[1].kind == "thing")


def none(w, item):
    """"y holds nothing" in the pre-state: `rnone` of each kind a row lets y's kind hold."""
    y = item.args[2]
    for q, k1 in held(w, y.kind):
        w.emit("rnone", q, "kind(%s)" % w.ids.kind(k1), w.term(y))


def negated(w, box, own):
    """"y holds no K that is not P" on a response's object y (holds-exactly's second half, or said so): `onrel` of y
    to `such(K,...)`, P's values and rows (`neg` under the inner `not`); None for a box of another shape."""
    k = next((r for r in box.refs if any(_link(i, r) for i in box.body)), None)
    links = [i for i in box.body if _link(i, k)]
    return _opaque(w, k, box.refs, links, [i for i in box.body if i not in links], own, "such")


def every(w, box, own):
    """"y holds every K that P" on a response's object y (holds-exactly's first half): `onrel` of y to
    `all(K,...)`, a restriction check.lp matches only with the same one on the other side, as it matches `such`; None
    for a box of another shape."""
    links = list(box.scope.body)
    if box.scope.refs or len(links) != 1:
        return None
    k = next((r for r in box.refs if _link(links[0], r)), None)
    return _opaque(w, k, box.refs, links, list(box.body), own, "all")


def nothing_on(w, box, own):
    """"a worktree that holds nothing" on a response's object y: `onrel` of y to `kind(K)` of each kind a row lets
    y's kind hold; None for a box of another shape."""
    if len(box.body) != 1 or not nothing(box.body[0], set(box.refs)) or box.body[0].args[2] not in own:
        return None
    y = box.body[0].args[2]
    for q, k1 in held(w, y.kind):
        w.emit("onrel", w.term(y), q, "o", "kind(%s)" % w.ids.kind(k1))
    return True


def _link(item, k):
    return k is not None and isinstance(item, Atom) and item.pred == "rel" and k in item.args[1:]


def _opaque(w, k, refs, links, rest, own, name):
    """The `onrel` of the object a box's K is linked to by its one row, the K's restriction its term: each value
    `(T,V,Pol)`, each row or state to another thing `(Q,D,O,Pol)` (O `kind(K2)` of a K2 of the box's own, or
    `such(K2,...)` of one the box restricts in its turn, b315); or None."""
    if k is None or len(links) != 1 or not rest:
        return None
    said = []
    if not _said(w, k, set(refs) - {k}, rest, "pos", said):
        return None
    q, x, y = w.edge(links[0])
    obj, d = (y, "o") if x == k else (x, "s")
    if obj not in own:
        return None
    w.emit("onrel", w.term(obj), q, d, "%s(%s,%s)" % (name, w.ids.kind(k.kind), ",".join(said)))
    return True


def _touches(w, item, k):
    """True when `item` is a value of k, or a row or a state with k on one side."""
    if isinstance(item, Atom) and item.pred == "attr":
        return item.args[0] == k
    return isinstance(item, Atom) and item.pred in ("rel", "state") and k in w.edge(item)[1:]


def _said(w, k, theirs, items, pol, said, inner=(), hop=0):
    """Append to `said` what `items` say of k under `pol`, each thing of the box's own that k reaches by a row or a
    state and that the items restrict in their turn (by a value, or a row or state to a third thing) said as
    `such(K2,...)`, one hop and no further (b315); False for what has no such reading, an item left unsaid among them."""
    flip = "neg" if pol == "pos" else "pos"
    loose = [i for i in items if not isinstance(i, Box) and not _touches(w, i, k)]
    for item in [i for i in items if i not in loose]:
        if isinstance(item, Box):
            body = list(item.body)      # a not box of several items: one says k, the rest the things it reaches
            if item.op != "not" or len(body) > 1 and sum(_touches(w, i, k) for i in body) != 1:
                return False
            if not _said(w, k, theirs | set(item.refs), body, flip, said, tuple(inner) + tuple(item.refs), hop):
                return False
        elif item.pred == "attr":
            if isinstance(item.args[2], Ref):
                return False
            said.append("(%s,%s,%s)" % (*w.ids.attr(k.kind, item.args[1], item.args[2]), pol))
        elif not _reach(w, k, theirs, item, pol, said, inner, hop, loose):
            return False
    return not loose


def _reach(w, k, theirs, item, pol, said, inner, hop, loose):
    q, x, y = w.edge(item)
    d, other = ("s", y) if x == k else ("o", x)
    if other is None or other == k or (inner and other not in inner):
        return False
    term = "kind(%s)" % w.ids.kind(other.kind) if other in theirs else w.term(other)
    own = [i for i in loose if other in theirs and _touches(w, i, other)]
    if own:
        sub = []
        if hop or not _said(w, other, theirs - {other}, own, "pos", sub, inner, hop + 1):
            return False
        term = "such(%s,%s)" % (w.ids.kind(other.kind), ",".join(sub))
        loose[:] = [i for i in loose if i not in own]
    said.append("(%s,%s,%s,%s)" % (q, d, term, pol))
    return True


# --- the steps (spec_steps4, spec_steps4_boxes) ---------------------------------------------------------------------
def given(r, atom, pol):
    """The `Cond` tree of "y holds nothing" said of y, or None for another atom."""
    import spec_rgl
    word, t, y = atom.args
    if word != IN or t.kind != "thing" or r.dets.get(t) != "DetNo":
        return None
    for k1, w2, k2 in r.vocab.rows:
        if w2 == IN and k2 in r.vocab.ancestors(y.kind):
            K2 = spec_rgl.kid(k2)
            return (K2 + "_Holds", pol, r.arg(y, k2), (K2 + "_Holds_Nothing",))
    return None


def absent(r, box, bring):
    """[(None, Then)] of "y holds no K that is not P" in a response: a K that is not P brought in with its restrictor,
    and the Then that y does not hold it; None for a box of another shape."""
    if len(box.refs) != 1:
        return None
    k = box.refs[0]
    links = [i for i in box.body if isinstance(i, Atom) and i.pred == "rel" and k in i.args[1:]]
    if len(links) != 1 or len(box.body) < 2:
        return None
    bring(r, Box("not", box.refs, tuple(i for i in box.body if i is not links[0])))
    return [(None, ("SCond", r.cond(links[0], False)))]


def no_member(r, box):
    """[(None, Then)] of "y holds no K" in a response (b299): a K brought in that y does not hold, its counter-example
    (a tool that puts every K into y fails the Then), and the Then "the worktree w1 holds no file" said of no K; None
    for a box of another shape ("holds nothing" of no thing is b297's, a K that P `absent`'s)."""
    if len(box.refs) != 1 or len(box.body) != 1:
        return None
    k, link = box.refs[0], box.body[0]
    if not (isinstance(link, Atom) and link.pred == "rel" and link.args[:2] == (IN, k)) or k.kind == "thing":
        return None
    import spec_rgl
    K = spec_rgl.kid(k.kind)
    r.brought.append((K + "_Given", (K + "_n",), ("NameLit", r.name(k))))
    r.dets[k] = "DetNo"
    try:
        return [(None, ("SCond", r.cond(link)))]
    finally:
        r.dets.pop(k)
