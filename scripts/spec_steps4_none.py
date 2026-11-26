"""A "no" box of more than one atom said whole as one Given (b716), beside spec_steps4_boxes' `no`, so that the
restriction it puts on its Ks is in the scenario: "no task of the batch is `failed`" the Given "no task of the batch b1
whose status is `failed` exists", "no workspace of a task of the batch holds a kept change that cites an item in the
batch" the Given "no workspace of a task of the batch b1 holds a kept change that cites an item in the batch b1".

The box's first referent is its head, said "no K"; the first atom that mentions it, but the row that is its modifier,
is the Given's condition (its main atom), each other referent "a K". Every other atom describes one referent of the
box: a row `K1 | word | K2` whose K1 it is its modifier ("task of the batch b1", spec_rgl_np's `r<n>_Mod`, one a
referent), a state whose subject it is a subject relative clause ("a kept change that cites an item"), a value of its
attribute "whose T is v" (spec_rgl_rel's `whose_value`). A box of any other shape gives None, and `no` says it by
its link as before, and so does a box that mentions no thing outside it: its link is then a value of one of its Ks,
which keeps the restriction ("no line of a stage is `accepted`": "no line whose outcome is `accepted` exists").
"""
import spec_rgl
import spec_rgl_rel
from spec_lf_core import Atom

kid = spec_rgl.kid
ROWS = ("of", "in")


def whole(r, box):
    """The Givens of the box said whole, or None when it has no such reading."""
    import spec_steps4_boxes  # here: it imports this module
    atoms = [i for i in box.body if isinstance(i, Atom)]
    if len(atoms) != len(box.body) or len(atoms) < 2 or not box.refs or any(
            a.pred not in ("rel", "state", "attr") for a in atoms):
        return None
    if not any(x not in box.refs for a in atoms for x in mentioned(a)):     # no link to drop: `link`'s value of a K
        return None
    head = box.refs[0]
    mods = {}     # a referent -> the atoms that describe it, its modifier row first
    main = None
    for a in atoms:
        x = described(a, box.refs)
        modifier = a.pred == "rel" and x is not None and not any(m.pred == "rel" for m in mods.get(x, ()))
        if modifier and x == head:
            mods.setdefault(x, []).append(a)
        elif main is None and head in mentioned(a):
            main = a
        elif x is not None and x != head and (modifier or a.pred != "rel"):
            mods.setdefault(x, []).append(a)
        else:
            return None
    if main is None:
        return None
    r.dets.update({x: "DetNo" if x == head else "DetA" for x in box.refs})
    try:
        if not all(cn(r, x, mods, set()) for x in box.refs):
            return None
        return [s for a in atoms for s in r.introduce(a)] + [("SCond", r.cond(main))]
    except spec_steps4_boxes.TraceError:
        return None
    finally:
        for x in box.refs:
            r.dets.pop(x, None)
            r.cns.pop(x, None)


def described(a, refs):
    """The referent of the box an atom describes: a row's first place, a state's subject, a value's owner."""
    if a.pred == "rel" and a.args[0] in ROWS:
        x = a.args[1]
    elif a.pred == "state":
        x = a.args[-1][0][1]
    elif a.pred == "attr" and not hasattr(a.args[2], "kind"):
        x = a.args[0]
    else:
        return None
    return x if x in refs else None


def mentioned(a):
    import spec_steps4  # here: it imports spec_steps4_boxes, which imports this module
    return spec_steps4.mentioned(a)


def cn(r, x, mods, seen):
    """True once `r.cns` holds the common noun of `x` with what describes it (the referents it names first)."""
    if x in r.cns or x not in mods:
        return True
    if x in seen:
        return False
    seen.add(x)
    K = kid(x.kind)
    tree = (K + "_UseN", (K + "_n",))
    for a in sorted(mods[x], key=lambda a: a.pred != "rel"):     # its modifier row first
        if not all(cn(r, y, mods, seen) for y in mentioned(a) if y != x and y in r.dets):
            return False
        tree = describe(r, x, a, tree)
        if tree is None:
            return False
    r.cns[x] = tree
    return True


def describe(r, x, a, tree):
    """The common noun `tree` of x with the atom `a` that describes it, or None."""
    if a.pred == "rel":
        word, _, y = a.args
        if tree[0] != kid(x.kind) + "_UseN":     # its modifier is the noun's first
            return None
        for n, (k1, w, k2) in enumerate(r.vocab.rows, 1):
            if w == word and k1 == x.kind and k2 in r.vocab.ancestors(y.kind):
                return ("r%d_%s_Mod" % (n, spec_rgl.slug(word)), (kid(k1) + "_n",), r.np(y, k2))
        return None
    if a.pred == "state":
        subject, _, vp = r.clause(a)
        return spec_rgl_rel.rel_cn(x.kind, subject, tree, (kid(subject) + "_Rel", ("PPos",), vp))
    _, term, value = a.args
    for n, (t, kinds) in enumerate(r.vocab.attributes, 1):
        if t.term == term and value in t.values and any(k in r.vocab.ancestors(x.kind) for k in kinds):
            T = "t_%s_%d" % (spec_rgl.slug(term), n)
            return spec_rgl_rel.whose_value(r.vocab, x.kind, T, ("PPos",), tree, ("%s_v_%s" % (T, spec_rgl.slug(value)),))
    return None
