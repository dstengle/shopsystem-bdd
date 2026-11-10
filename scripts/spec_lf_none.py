"""A "no" box with a negated restriction inside it, in `check.lp`'s facts (b238; b240 phase 12), beside spec_lf_facts,
whose walk (`w`) emits them: "the item has no dependency on an item whose status is not `delivered`", "a session has
no worktree that holds a file whose version is not `2.0.0`". The box is read whole, not atom by atom: `nobox(R,N,K1,K2)`
its own Ks (K2 `none` for a box of one), `nbrel(R,N,Q,L,Rt)` each row or state between them or to a thing outside the
box (a side `o1`, `o2` for its own Ks, else the outer thing's term), and `nbattr(R,N,O,T,V,Pol)` each value of its own
Ks, `neg` for one under the inner `not`. check.lp puts a pair out when instances of its Ks in the merged state meet
every row it says and every value, a `neg` value met by another value known (or the value known not to hold).

A box of more than two Ks of its own, or with anything but rows, states and values of its own Ks (a `not` over
values only), has no translation: a ValueError naming it.
"""
from spec_lf_core import Atom, Box, Ref

NO = "no translation of no there"


def nested(box):
    """True for a "no" box that holds a `not` box: the shape read here."""
    return box.op == "not" and bool(box.refs) and any(isinstance(i, Box) for i in box.body)


def facts(w, box):
    if len(box.refs) > 2:
        raise ValueError(NO)
    w.noboxes = getattr(w, "noboxes", 0) + 1
    n, sides = "n%d" % w.noboxes, {r: "o%d" % k for k, r in enumerate(box.refs, 1)}
    kinds = [w.ids.kind(r.kind) for r in box.refs] + ["none"]
    w.emit("nobox", n, kinds[0], kinds[1])

    def side(r):
        return sides[r] if r in sides else w.term(r)

    def value(item, pol):
        x, term, v = item.args
        if x not in sides or isinstance(v, Ref):
            raise ValueError(NO)
        w.emit("nbattr", n, sides[x], *w.ids.attr(x.kind, term, v), pol)

    for item in box.body:
        if isinstance(item, Atom) and item.pred == "attr":
            value(item, "pos")
        elif isinstance(item, Atom) and item.pred in ("rel", "state"):
            q, x, y = w.edge(item)
            if y is None:
                raise ValueError(NO)
            w.emit("nbrel", n, q, side(x), side(y))
        elif isinstance(item, Box) and item.op == "not" and not item.refs and all(
                isinstance(i, Atom) and i.pred == "attr" for i in item.body):
            for i in item.body:
                value(i, "neg")
        else:
            raise ValueError(NO)
