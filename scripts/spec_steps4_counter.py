"""Scenarios that can fail (b273), beside spec_steps4 and spec_steps4_boxes, whose Reader (`r`) they extend:

- a counter-example of a response's `every` or `only` with a restriction: one more K brought in that meets its
  restriction but the last atom of it, which it fails (another value of the attribute, else the atom negated: "the
  worktree w1 does not hold the file f3"), a value no "no" box of the precondition denies of it, else no
  counter-example (`denied`, b732), and the Then of the scope's acts negated on it (`counter`); an `every`
  keeps its two members and their Thens (`each`), an `only` asserts no act on a member, since it obliges none;
- an upper bound of a response's count ("at most n", "exactly n", "fewer than n", "one"): one K past the upper bound
  brought in, each meeting the restriction, and one Then of the count as the line says it ("`work` prints at most
  three files in the worktree w1", `upper`), the counted K said so where a step names it (`np`), which a handler checks
  by counting;
- every and a count in a precondition: each K the first line's parts put in the box's restriction is one of the box's
  (`members`), so "every line of the stage" holds of the line the While brings in, and a count is given at its
  boundary (`boundary`: n of at least, at most and exactly n, n + 1 of more than n, n - 1 of fewer than n) counting
  them (`given`);
- holds-exactly's only half in a precondition ("no file in the worktree w1 that is not P", b309): a K brought in that
  fails P (another value of its attribute, "covers no line") and the Given that the collection does not hold it
  (`excluded`), in place of "the worktree w1 holds no file", which the every half's member contradicts.
"""
from dataclasses import replace

import spec_lf_number
import spec_rgl
import spec_steps4_boxes as boxes
from spec_lf_core import Atom, Box, Ref, least

kid = spec_rgl.kid
UPPER = {"at most": 0, "exactly": 0, "fewer than": -1}     # the upper bound of a count, from its number
BOUNDS = {"at least": "AtLeast", "at most": "AtMost", "exactly": "Exactly", "more than": "MoreThan",
          "fewer than": "FewerThan"}


def renamed(box, k):
    return {x: replace(x, name="%s.%d" % (x.name, k)) for x in box.refs + box.scope.refs}


def introduce(r, x):
    r.brought.append((kid(x.kind) + "_Given", (kid(x.kind) + "_n",), ("NameLit", r.name(x))))


# --- every and only in a response -----------------------------------------------------------------------------------
def each(r, box):
    """The Thens of an `every` box said of two Ks, each brought in with its restrictor (`brought`), the second K's
    acts marked `again`, numbered as the first's (spec_lf_facts reads the box's acts once); then its counter-example."""
    out = []
    for copy in (1, 2):
        m = renamed(box, copy)
        for x in box.refs:
            introduce(r, m[x])
        r.brought += [s for c in boxes.subst(box.body, m) for s in boxes.restrictor(r, c)]
        acts = r.acts(boxes.subst(box.scope.body, m))
        out += acts if copy == 1 else [("again" if act else act, tree) for act, tree in acts]
    return out + counter(r, box, 3, None)


def failing(box):
    """The place of the restriction's last atom a counter-example fails, else None."""
    places = [n for n, i in enumerate(box.body) if isinstance(i, Atom) and i.pred in ("rel", "state", "attr")
              and not (i.pred == "attr" and isinstance(i.args[2], Ref))]
    return places[-1] if places else None


def counter(r, box, k, act):
    """[(act, Then)] of a counter-example of a box with a restriction: a K that fails it, the scope negated on it."""
    n = failing(box)
    if n is None or box.scope.refs:     # a scope's own K, which a negated Then would name with no Given
        return []
    m = renamed(box, k)
    body = boxes.subst(box.body, m)
    held = body[:n] + body[n + 1:]
    if values(r, body[n], held) == []:     # every other value a no box of the precondition denies (b732)
        return []
    for x in box.refs:
        introduce(r, m[x])
    r.brought += [s for c in held for s in boxes.restrictor(r, c)]
    r.brought.append(("SCond", unmet(r, body[n], held)))
    return [(act, tree) for _, tree in r.acts(boxes.subst(box.scope.body, m), False)]


def unmet(r, atom, held=None):
    """The Cond tree of an atom a thing fails: another value of its attribute, else the atom negated; given what the
    thing `held` meets besides, the first other value no "no" box of the precondition denies of it (b732)."""
    free = values(r, atom, held)
    return r.cond(Atom("attr", atom.args[:2] + (free[0],))) if free else r.cond(atom, False)


def values(r, atom, held=None):
    """The other values of an attribute atom's attribute, less those a "no" box of the precondition denies of its
    thing when it meets `held` besides ([] when each is denied); None for an atom of no attribute with values."""
    if atom.pred != "attr":
        return None
    x, term, value = atom.args     # of the attribute entry spec_steps4's `cond` says it by
    t = next((t for t, kinds in r.vocab.attributes if t.term == term
              and any(k in r.vocab.ancestors(x.kind) for k in kinds)), None)
    others = [v for v in (t.values if t else ()) if v != value]
    if not others:
        return None
    return [v for v in others if v not in denied(r, x, term, held)] if held is not None else others


def denied(r, x, term, held):
    """The values of the attribute `term` that a "no" box of the precondition (a `not` box of one K, x's kind or one
    above it) denies of x: each box whose other atoms, x put in, are among `held`."""
    out = set()
    for b in r.pre:
        if not (isinstance(b, Box) and b.op == "not" and len(b.refs) == 1
                and b.refs[0].kind in r.vocab.ancestors(x.kind) and all(isinstance(i, Atom) for i in b.body)):
            continue
        body = boxes.subst(b.body, {b.refs[0]: x})
        values = [a.args[2] for a in body if a.pred == "attr" and a.args[:2] == (x, term)
                  and not isinstance(a.args[2], Ref)]
        rest = [a for a in body if not (a.pred == "attr" and a.args[:2] == (x, term))]
        if len(values) == 1 and all(a in held for a in rest):
            out.add(values[0])
    return out


def only(r, box):
    """[(act, Then)] of "V only Ks that P": its counter-example, no act on a member; with no restriction the K
    brought in with the Then on it, as before."""
    found = counter(r, box, 1, True)
    if found:
        return found
    boxes.bring(r, box)
    return r.acts(box.scope.body)


# --- counts ----------------------------------------------------------------------------------------------------------
def upper(r, box):
    """[(act, Then)] of a response's count with an upper bound: one K past it, each with the restriction, and the
    Then of the count; None for a count with none."""
    bound, n = box.count
    if bound not in UPPER or isinstance(n, Ref):
        return None
    if not 1 <= n <= 10:
        raise boxes.TraceError("no step of a count of %d" % n)
    for c in boxes.copies(box, n + UPPER[bound] + 1):
        boxes.bring(r, c)
    det = ("DetOne",) if (bound, n) == ("exactly", 1) else ("DetCount", (BOUNDS[bound],), ("Many%d" % n,))
    r.counted[box.refs[0]] = (det, spec_lf_number.cn(r, box)[1])
    return [(True, tree) for _, tree in r.acts(box.scope.body)][:1]


def np(r, ref, slot):
    """The `K_NP` tree of a counted K in a slot: "at most three files in the worktree w1"."""
    det, cn = r.counted[ref]
    K, S = kid(ref.kind), kid(slot)
    tree = (K + "_Det", det, cn)
    if slot not in r.vocab.ancestors(ref.kind):
        raise boxes.TraceError("no step of a %s in a slot of %s" % (ref.kind, slot))
    return (S + "_Simple", tree) if ref.kind == slot else ("%s_Up_%s" % (K, S), tree)


# --- every and counts in a precondition ------------------------------------------------------------------------------
def members(r, box, atoms):
    """The referents outside a box of one K that the first line's parts say meet each of `atoms` in its place."""
    if len(box.refs) != 1 or not atoms or not all(isinstance(a, Atom) for a in atoms):
        return []
    x = box.refs[0]
    said = [i for i in r.pre if isinstance(i, Atom)]
    candidates = dict.fromkeys(y for a in said for y in _refs(a) if y != x and y.kind == x.kind
                               and y.origin in ("while", "trigger"))
    return [y for y in candidates if all(boxes.subst(a, {x: y}) in said for a in atoms)]


def _refs(atom):
    for a in atom.args:
        for y in (a if isinstance(a, tuple) else (a,)):
            y = y[1] if isinstance(y, tuple) and len(y) == 2 else y
            if isinstance(y, Ref):
                yield y


def said(r, y, item):
    """True when the first line's parts give the member y a value of each attribute `item` gives it (an `or` box of
    values among them), which the member keeps."""
    terms = {a.args[1] for a in r.pre if isinstance(a, Atom) and a.pred == "attr" and a.args[0] == y}
    atoms = [a for case in item.body for a in case.body] if isinstance(item, Box) and item.op == "or" else [item]
    return all(isinstance(a, Atom) and a.pred == "attr" and a.args[0] == y and a.args[1] in terms for a in atoms)


def boundary(count):
    """As many things as a count admits nearest to a number it does not admit."""
    bound, n = count
    if isinstance(n, Ref):
        return least(count)
    return {"at most": n, "fewer than": n - 1}.get(bound, least(count))


def given(r, box):
    """The Given steps of `every` or a count in a condition: the scope said of each member the parts give, else of
    one K brought in with its restriction (every); the boundary's number of Ks, the members among them (count)."""
    if box.op == "every":
        found, out = members(r, box, list(box.body)), []
        for y in found:
            out += [s for sub in boxes.subst(box.scope.body, {box.refs[0]: y}) if not said(r, y, sub)
                    for s in r.given(sub)]
        if not found or any(isinstance(sub, Box) and sub.op == "or" for sub in box.scope.body):
            out += [s for sub in list(box.body) + list(box.scope.body) for s in r.given(sub)]     # a case shown too
        return out
    found = members(r, box, list(box.body) + list(box.scope.body))
    return [s for c in boxes.copies(box, max(boundary(box.count) - len(found), 0))
            for sub in list(c.body) + list(c.scope.body) for s in r.given(sub)]


def excluded(r, box):
    """The Givens of a "no" box of one K with a `not` inside it and its row `K | in | y`: the K brought in, each
    inner `not` said of it (one value by another value) and "y does not hold" it; [] for a box of another shape."""
    k, inner = box.refs[0] if len(box.refs) == 1 else None, [i for i in box.body if isinstance(i, Box)]
    links = [i for i in box.body if isinstance(i, Atom) and i.pred == "rel" and i.args[:2] == ("in", k)]
    if k is None or len(links) != 1 or not inner or len(inner) + 1 != len(box.body):
        return []
    if any(b.op != "not" for b in inner):
        return []
    r.known.add(k)
    out = [(kid(k.kind) + "_Given", (kid(k.kind) + "_n",), ("NameLit", r.name(k)))]
    for b in inner:
        single = not b.refs and len(b.body) == 1 and isinstance(b.body[0], Atom) and b.body[0].pred == "attr"
        out += [("SCond", unmet(r, b.body[0]))] if single else r.given(b)
    return out + [("SCond", r.cond(links[0], False))]
