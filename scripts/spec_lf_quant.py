"""The quantified conditions and the negated restriction of an object in `check.lp`'s facts (b197; the CNL 4 design,
section 7.4), beside spec_lf_facts, whose walk (`w`) emits them:

- "every K that P is v" in a While or Where clause or a trigger: the universal of codified-1 (spec_facts_np), `uall(R,U,
  K)` with its restrictor `uattr(R,U,T,V)`, `urel(R,Q,U,W)` and what its scope says of it `ucond(R,U,T,V,Pol)`, which
  check.lp reads (`umatch`): a pair is out where an instance of K that meets the restrictor has another value; "every
  K that P is one of `a` or `b`" `uin(R,U,T,V)` of each value (spec_lf_values, b240);
- a count of Ks in a condition ("at least two stages are `done`"): when it admits no K (at most, fewer than, exactly
  0) it says nothing the check reads; otherwise there is a K that meets its restrictor and scope, a role with its
  literals, as "a K that P"; `ccount(R,X,B,N)` keeps the count, so the entailment check never forces it as a premise
  of one K (spec_entail_rules);
- "a K whose T is not v" on a response's object: `onattr(R,X,T,V)`, which check.lp's `gap` and `pag` read as they read
  `oattr`, so a line on a K that is not v clashes only with one on a K known not to be v; "a K that x does not V"
  and "a K that no K2 Vs" `onrel(R,X,Q,D,O)`, read the same way (b240 phase 12).

Anything else in such a box has no translation: a ValueError naming it.
"""
import spec_lf_number
import spec_lf_values
from spec_lf_core import Atom, Box, Ref, least

NEGATED = "no translation of a negated restriction (not) on an object"
BOUNDS = {"at least": "least", "at most": "most", "exactly": "exactly", "more than": "more", "fewer than": "fewer"}


def condition(w, box):
    """An `every` or a `count` box of a While or Where clause or a trigger, positive."""
    if box.op == "every":
        return every(w, box)
    if box.op == "count":
        return count(w, box)
    raise ValueError("no translation of %s in a condition" % box.op)


def every(w, box):
    if len(box.refs) != 1 or box.scope.refs:
        raise ValueError("no translation of every there")
    u = box.refs[0]
    w.emit("uall", u.name, w.ids.kind(u.kind))
    for item in box.body:
        if isinstance(item, Atom) and item.pred == "attr" and item.args[0] == u and not isinstance(item.args[2], Ref):
            w.emit("uattr", u.name, *w.ids.attr(u.kind, item.args[1], item.args[2]))
        elif isinstance(item, Atom) and item.pred in ("rel", "state"):
            q, x, y = w.edge(item)
            if x != u or y is None or y in box.refs:
                raise ValueError("no translation of every there")
            w.emit("urel", q, u.name, w.term(y))
        else:
            raise ValueError("no translation of every there")
    sets = [b for b in box.scope.body if isinstance(b, Box) and spec_lf_values.members(u, b)]
    for b in sets:          # "every K ... is one of `a` or `b`" (b240): `uin` of each value
        for term, value in spec_lf_values.members(u, b):
            w.emit("uin", u.name, *w.ids.attr(u.kind, term, value))
    for item, pol in _literals([b for b in box.scope.body if not any(b is s for s in sets)], "pos"):
        if not (item.pred == "attr" and item.args[0] == u and not isinstance(item.args[2], Ref)):
            raise ValueError("no translation of every there")
        w.emit("ucond", u.name, *w.ids.attr(u.kind, item.args[1], item.args[2]), pol)


def _literals(body, pol):
    """(atom, polarity) of a scope's atoms, through `not` boxes with no referents of their own."""
    for item in body:
        if isinstance(item, Box) and item.op == "not" and not item.refs:
            yield from _literals(item.body, "neg" if pol == "pos" else "pos")
        elif isinstance(item, Atom):
            yield item, pol
        else:
            raise ValueError("no translation of every there")


def count(w, box):
    if box.scope.refs or len(box.refs) != 1 and box.scope.body:
        raise ValueError("no translation of a count there")
    if not box.scope.body:      # the number of Ks compared (b240): its count and signature, whatever it admits
        spec_lf_number.signature(w, box)
    if not least(box.count):
        return
    x = box.refs[0]
    w.roles(box.refs)
    if box.scope.body:
        w.emit("ccount", x.name, BOUNDS[box.count[0]], box.count[1])
    for item in list(box.body) + list(box.scope.body):
        w.literal(item)


def negated(w, box, own):
    """`not` over a response object's attribute ("a stage whose status is not `done`"): `onattr`; over its row or
    state ("a stage that the session does not follow", "a line that no file covers"): `onrel` (b240 phase 12)."""
    item = box.body[0] if len(box.body) == 1 else None
    if isinstance(item, Atom) and item.pred in ("rel", "state"):
        return unrelated(w, item, own, set(box.refs))
    if box.refs or len(box.body) != 1:
        raise ValueError(NEGATED)
    if not (isinstance(item, Atom) and item.pred == "attr" and item.args[0] in own and not isinstance(item.args[2],
                                                                                                     Ref)):
        raise ValueError(NEGATED)
    x, term, value = item.args
    w.emit("onattr", w.term(x), *w.ids.attr(x.kind, term, value))


def unrelated(w, item, own, theirs):
    """`onrel(R,X,Q,D,O)`: the object X is not related by Q to O (a term, or `kind(K)` for "no K", the `not` box's
    own K), D `s` when X is the row's or the state's first side, `o` when its second; read as `onattr` is."""
    q, x, y = w.edge(item)
    obj, d, other = (x, "s", y) if x in own else (y, "o", x)
    if obj not in own or other is None or other in own or len(theirs) > 1 or theirs and other not in theirs:
        raise ValueError(NEGATED)
    w.emit("onrel", w.term(obj), q, d, "kind(%s)" % w.ids.kind(other.kind) if other in theirs else w.term(other))
