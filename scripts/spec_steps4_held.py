"""The Then of "V a K that holds only K2s that P" and "... that holds at most n K2s" (b272), beside spec_steps4_boxes:
an `only` or a `count` box over the row or state of a response's object said of the object, "the worktree w1 holds
only files whose version is `2.0.0`", "the worktree w1 holds at most three files" (`cond`); its K2s are named by no
step. A count with an upper bound ("at most n", "exactly n", "fewer than n") has its counter-example (b296): one K2
past the bound brought in before the When, each with the restriction's values, held by no step, so a program that
puts every given K2 into the object fails the Then (`then`). A restrictor other than values of the K2, or a count past
ten, is a TraceError naming it.
"""
import spec_rgl
from spec_lf_core import Atom, Ref
import spec_steps4_boxes as boxes
from spec_steps4_boxes import TraceError

kid = spec_rgl.kid

BOUNDS = {"at least": "AtLeast", "at most": "AtMost", "exactly": "Exactly", "more than": "MoreThan",
          "fewer than": "FewerThan"}


def then(r, box):
    """[(None, Then)] of an `only` or a `count` box over the row or state of a response's object: the Then said of
    the object, and of a count with an upper bound, one K2 past it brought in with the restriction."""
    tree = cond(r, box)
    import spec_steps4_counter as counter  # here: it imports spec_steps4_boxes, which imports this module
    if box.op == "count" and box.count[0] in counter.UPPER:
        for c in boxes.copies(box, box.count[1] + counter.UPPER[box.count[0]] + 1):
            boxes.bring(r, c)
    return [(None, ("SCond", tree))]


def cond(r, box):
    """The `Cond` tree of an `only` or a `count` box over the row or state of a response's object, said of the
    object: its K's slot an `only` noun phrase ("only files whose version is `2.0.0`") or a counted one ("at most
    three files"), its restrictor a "whose" of each value."""
    k = box.refs[0]
    r.names[k] = "\0held"     # a placeholder in the slot of k, replaced below; k is named by no step
    cond = r.cond(box.scope.body[0])
    del r.names[k]
    K, cn = kid(k.kind), (kid(k.kind) + "_UseN", (kid(k.kind) + "_n",))
    for c in box.body:
        if not (isinstance(c, Atom) and c.pred == "attr" and not isinstance(c.args[2], Ref) and c.args[0] == k):
            raise TraceError("no Then of %s with a restriction of that" % box.op)
        T = next(("t_%s_%d" % (spec_rgl.slug(t.term), n) for n, (t, kinds) in enumerate(r.vocab.attributes, 1)
                  if t.term == c.args[1] and any(x in r.vocab.ancestors(k.kind) for x in kinds)), None)
        if T is None:
            raise TraceError("no Then of the %s of a %s" % (c.args[1], k.kind))
        cn = (K + "_Whose_" + T, ("PPos",), cn, ("%s_v_%s" % (T, spec_rgl.slug(c.args[2])),))
    if box.op == "only":
        det = ("DetPl",)
    elif box.count[0] in BOUNDS and isinstance(box.count[1], int) and 1 <= box.count[1] <= 10:
        det = ("DetCount", (BOUNDS[box.count[0]],), ("Many%d" % box.count[1],))
    else:
        raise TraceError("no Then of a count of %s" % (box.count,))
    return _slot(cond, (K + "_Det", det, cn), box.op == "only")


def _slot(tree, np0, only):
    """`tree` with the argument that names the placeholder given `np0` in place of its instance (`K_Only` for
    "only")."""
    if not isinstance(tree, tuple):
        return tree
    if len(tree) == 2 and tree[0].endswith("_One") and isinstance(tree[1], tuple) and len(tree[1]) == 2 and \
            isinstance(tree[1][1], tuple) and ("NameLit", "\0held") in tree[1][1]:
        S = tree[0][:-len("_One")]
        return (S + ("_Only" if only else "_One"), (tree[1][0], np0))
    return tuple(_slot(t, np0, only) for t in tree)
