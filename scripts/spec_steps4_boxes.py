"""The steps of the boxes and images of a codified-2 group's forms (b197; the CNL 4 design, sections 7.2-7.4), beside
spec_steps4, whose Reader (`r`) they extend:

- in a While or Where clause or a trigger: "every K that P is Q" one K brought in with a Given of its restrictor and
  of its scope; a count of Ks the fewest Ks it admits (`spec_lf_core.least`: none for at most and fewer than), each
  brought in so; "no K that P" no Given of a K, its condition a Given said of "no K" ("no stage is `done`"); an `or`
  the case its scenario takes (`Reader.pick`: one scenario a case, as codified-1's R#n);
- in a response: "V only Ks that P" a K brought in with its restrictor and the Then on it (R5); a count the bound's
  number of Ks (one past it for "more than"), each brought in with its restrictor and the Thens said of each, or for
  "at most n" and "fewer than n" one past the most it admits (n + 1, n) with the Then on the last of them negated; a
  `not` over a response object's attribute ("a stage whose status is not `done`") a Given of the K that does not
  meet it, the K brought in;
- "the number of Ks that P" printed two Ks brought in, compared with a parameter the Given of the comparison
  (spec_lf_number, b240);
- "the T of x" whose value is a referent (an image): no step of its own, the referent named "the T of x" where a
  step says it (`image`), so no Given names its value.
A box of any other shape is a TraceError naming it.
"""
from dataclasses import replace

import spec_lf_number
import spec_lf_option
import spec_rgl
from spec_lf_core import Atom, Box, Ref, least

kid = spec_rgl.kid


class TraceError(Exception):
    """A group with no scenario: a construct of its form with no step."""


def given(r, box, pos):
    """The Given steps of a box of a condition."""
    if box.op == "not" and not box.refs:
        return [s for sub in box.body for s in r.given(sub, not pos)]
    if box.op == "not" and pos:     # "no K that P": said of "no K", no K brought in
        return no(r, box)
    if box.op == "every" and pos:
        return [s for sub in list(box.body) + list(box.scope.body) for s in r.given(sub)]
    if box.op == "count" and pos and isinstance(box.count[1], Ref):    # compared with a parameter (b240)
        return spec_lf_number.compared(r, box)
    if box.op == "count" and pos:
        return [s for c in copies(box, least(box.count)) for sub in list(c.body) + list(c.scope.body)
                for s in r.given(sub)]
    if box.op == "or" and pos:
        case = box.body[r.pick(len(box.body))]
        return [s for sub in case.body for s in r.given(sub)]
    raise TraceError("no Given of %s" % box.op)


def no(r, box):
    """"no K that P": one atom said of "no K"; of a box of more than one (b238, b240 phase 12), its link to a thing
    outside it ("the item i1 has no dependency"), else a value of its K ("no line is `accepted`"), which makes the
    box's state hold, unless another Given says the link of that thing."""
    atoms = [i for i in box.body if isinstance(i, Atom) and i.pred != "event"]
    if len(atoms) != len(box.body) or len(atoms) != 1:
        atoms, refs = link(r, box)
    else:
        refs = box.refs
    r.dets.update({x: "DetNo" if k == 0 else True for k, x in enumerate(refs)})     # "no K Vs a K2"
    try:
        return r.given(atoms[0])
    finally:
        for x in refs:
            r.dets.pop(x)


def none_whose(r, x, T, pol, value):
    """The Cond tree of a value said of "no K": "no item whose status is `idea` exists", the full form (b257), since
    "the status of no item" does not read."""
    K = kid(x.kind)
    cn = (K + "_Whose_" + T, ("PPos",), (K + "_UseN", (K + "_n",)), value)
    np = (K + "_Det", ("DetNo",), cn)
    return ("k_thing_Holds", pol, ("k_thing_One", ("%s_Up_k_thing" % K, np) if x.kind != "thing" else
                                   ("k_thing_Simple", np)), ("Exists_St",))


def link(r, box):
    """([the atom], [its own K]) a box of more than one item is said by: its row or state to a thing outside it, else
    a value of one of its Ks."""
    import spec_steps4
    rows = [i for i in box.body if isinstance(i, Atom) and i.pred in ("rel", "state")]
    for a in rows:
        own = [x for x in spec_steps4.mentioned(a) if x in box.refs]
        outer = [x for x in spec_steps4.mentioned(a) if x not in box.refs]
        if len(own) == 1 and len(outer) == 1 and not any(
                isinstance(i, Atom) and i.pred == a.pred and i.args[0] == a.args[0] and outer[0] in i.args
                for i in r.pre):
            return [a], own
        if len(own) == 1 and len(outer) == 1:
            raise TraceError("no Given of no there")
    for a in box.body:
        if isinstance(a, Atom) and a.pred == "attr" and a.args[0] in box.refs and not isinstance(a.args[2], Ref):
            return [a], [a.args[0]]
    raise TraceError("no Given of no there")


def copies(box, n):
    """`n` copies of a box, each with its referents renamed `<name>.<k>` (spec_steps4's `each` names them so)."""
    out = []
    for k in range(1, n + 1):
        m = {x: replace(x, name="%s.%d" % (x.name, k)) for x in box.refs + box.scope.refs}
        out.append(subst(box, m))
    return out


def restrictor(r, c):
    """The Givens of one item of a response K's restrictor: a box as a condition's ("no file covers the line l1",
    "the session s1 does not follow the stage s2"), an atom its condition."""
    return r.given(c) if isinstance(c, Box) else [("SCond", r.cond(c))]


def bring(r, box):
    """Each referent of a response box brought in by a Given (`brought`), with its restrictor."""
    for x in box.refs:
        r.brought.append((kid(x.kind) + "_Given", (kid(x.kind) + "_n",), ("NameLit", r.name(x))))
    for c in box.body:
        r.brought += restrictor(r, c)


def acts(r, box, pos):
    """[(act number or None, Then tree)] of an `only`, a `count` or a negated restriction in a response."""
    if box.op == "number" and pos:      # a printed number (b240): two Ks it counts
        spec_lf_number.bring(r, box)
        return []
    numbers = [b for b in box.body if isinstance(b, Box) and b.op == "number"]
    if box.op == "not" and pos and numbers and len(box.body) == len(numbers) + 1:     # "not print the number of"
        for b in numbers:
            spec_lf_number.bring(r, b)
        return r.acts([box.body[-1]], False)
    if box.op == "only" and pos:
        bring(r, box)
        return r.acts(box.scope.body)
    if box.op == "count" and pos:
        bound, n = box.count
        upper = {"at most": n + 1, "fewer than": n}.get(bound)
        out = []
        for k, c in enumerate(copies(box, upper or least(box.count)), 1):
            bring(r, c)
            if upper is None or k == upper:
                found = r.acts(c.scope.body, upper is None)
                out += found if not out else [("again" if act else act, tree) for act, tree in found]
        return out
    events = [i for i in box.body if isinstance(i, Atom) and i.pred == "event"]
    if box.op == "not" and pos and box.refs and len(events) == 1 and not any(
            isinstance(i, Box) and i.op != "not" for i in box.body):     # "shall not V a K that P" (b237)
        bring(r, replace(box, body=tuple(i for i in box.body if i is not events[0])))
        return [(True, r.does(events[0], False))]
    if box.op == "not" and not box.refs and restriction(box):
        for x in mentioned(box):
            r.bring_in(x)
        r.brought += r.given(box, pos)
        return []
    raise TraceError("no Then of %s" % box.op)


def restriction(box):
    """True for a `not` over attributes of response referents and nothing else: a negated restriction."""
    return all(isinstance(i, Atom) and i.pred == "attr" and not isinstance(i.args[2], Ref)
               and i.args[0].origin == "response" for i in box.body)


def mentioned(box):
    return list(dict.fromkeys(i.args[0] for i in box.body))


def fits(vocab, frame, roles):
    """True when an atom's referents are of the kinds of a frame (fun, subject kind, slot kinds), or under them."""
    _, subject, kinds = frame
    refs = [roles[0][1]] + spec_lf_option.slots(roles)
    pairs = zip(refs, [subject] + list(kinds))
    return all(k in vocab.ancestors(x.kind) for r, k in pairs for x in (r if isinstance(r, tuple) else (r,))
               if hasattr(x, "kind"))


def image(r, atom):
    """True when `atom` is "the T of x" whose value is a referent, kept as that referent's name (`images`)."""
    if atom.pred != "attr" or not isinstance(atom.args[2], Ref):
        return False
    x, term, value = atom.args
    for n, (t, kinds) in enumerate(r.vocab.attributes, 1):
        k = next((k for k in kinds if k in r.vocab.ancestors(x.kind)), None)
        if t.term == term and k is not None:
            T = "t_%s_%d" % (spec_rgl.slug(term), n)
            r.images[value] = (T, k, x)
            return True
    raise TraceError("no step of the %s of a %s" % (term, x.kind))


def np_image(r, ref, slot):
    """The `K_NP` tree of an image in a slot: "the T of x", a thing; a printed number's spec_lf_number's."""
    if ref in r.numbers:
        return spec_lf_number.step_np(r, ref, slot)
    T, k, owner = r.images[ref]
    if slot != "thing":
        raise TraceError("no step of the %s of a %s in a slot of %s" % (T, k, slot))
    return ("%s_Up" % T, ("%s_Of_%s" % (T, kid(k)), r.np(owner, k)))


def subst(x, m):
    """`x` (a referent, an atom, a box or a tuple of them) with each referent in `m` replaced."""
    if isinstance(x, Ref):
        return m.get(x, x)
    if isinstance(x, Atom):
        return Atom(x.pred, subst(x.args, m))
    if isinstance(x, Box):
        return replace(x, refs=subst(x.refs, m), body=subst(x.body, m), scope=subst(x.scope, m))
    if isinstance(x, (tuple, list)):
        return type(x)(subst(i, m) for i in x)
    return x
