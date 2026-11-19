"""Orders (b275, `order-by` and `order-by-every`): ", ordered by T, in ascending order" (or "in descending order")
after a collection that holds members by a row `K1 | in | K2`, T an attribute of K1 ("a worktree that holds a file,
ordered by version, in descending order": spec_rgl_np's `r<n>_in_By_<T>`), or after "every K" of any act (b300), T an
attribute of K ("every file, ordered by version, in ascending order": `<T>_<K>_Every`). One translation in each place
a line is read:

- the form (`np`): one atom `ordered(x, T, ascending|descending)` beside the clause's atom (spec_lf_core's NP
  `order`), x the every's K, or of a collection its members' (b334, decision 0093): an every box over the Ks of the
  row, restricted by `in(m, the collection)`, with `ordered(m, T, direction)` in its scope (`held` reads it), so an
  `ordered` atom always names a K that has T; an order on an attribute with no value order (spec_value_kinds) a note
  naming the attribute, which spec_lf_read gives as the line's refusal; `show` its line in `model parse --form`;
  an order only where it has a reading (b285, decision 0093: a property of what a response prints): one in a While
  or Where clause, a trigger, or an act the line forbids (inside a `not` box) refused naming it (`misplaced`);
- the check (`facts`): `ordered(R, I, T, Dir)` of the response's act I (of a collection's members, the act on the
  collection the box restricts them by), a fact: two lines that require one
  collection, or one printing, in opposite orders on one trigger are an L1 (grammar/check.lp), and nothing else is
  proved of it;
- the steps (`member`, `values`, `every`, `then`, the members of `held`'s box, not an every's R6 Ks): three members with distinct values of T, given in neither the order nor its
  reverse (the second, the third, the first), and the Then that states the order, the response's act on the
  collection or the "every K" with its order, which features_vocab4 reads (`read`).
"""
import re
from dataclasses import replace

import spec_lf_order
import spec_rgl
from spec_lf_core import Atom, Box, Ref

PRED = "ordered"
BY = re.compile(r"^r(\d+)_[a-z0-9_]+?_By_(t_[a-z0-9_]+_\d+)$")
DIRS = {"Ascending": "ascending", "Descending": "descending"}
FUNS = {v: k for k, v in DIRS.items()}
RANKS = (1, 2, 0)       # the members' values in neither order: the second, the third, the first of three sorted


def np(st, tree, nps):
    """The NP of an order's tree, its `order` the atom, or None when the tree is none."""
    name, a = nps.fun(tree), nps.args(tree)
    by = BY.match(name)
    if by:
        t, found = st.names.attr(by.group(2) + "_")[0], nps.np(st, a[0])
    else:
        t, rest = st.names.attr(name)
        if t is None or not rest.endswith("_Every"):
            return None
        found = nps.det(st, "DetEvery", a[0])
    if spec_lf_order.order(t) is None:
        st.notes.append("the %s of a %s has no value order: its entry says neither Order: nor Type:, so no %s comes "
                        "before another, and nothing is ordered by it" % (t.term, t.kinds[0], t.term))
    d = DIRS[nps.fun(a[1])]
    if not by:
        return replace(found, order=Atom(PRED, (found.ref, t.term, d)))
    row = st.names.rows[int(by.group(1))]       # the members, the Ks of the row K | in | Y (b334, decision 0093)
    m = st.ref(row[0])
    return replace(found, order=Box("every", (m,), (Atom("rel", (row[1], m, found.ref)),),
                                    Box("scope", (), (Atom(PRED, (m, t.term, d)),))))


def held(box):
    """(the member referent, the collection, the order atom) of an order on a collection's members (b334): an every
    box of one K restricted only by `in(m, y)`, y outside it, with one `ordered(m, ...)` in its scope; else None."""
    if not isinstance(box, Box) or box.op != "every" or len(box.refs) != 1 or len(box.body) != 1 \
            or box.scope is None or len(box.scope.body) != 1:
        return None
    (m,), (rel,), (atom,) = box.refs, box.body, box.scope.body
    if not (isinstance(rel, Atom) and rel.pred == "rel" and rel.args[1] == m and isinstance(atom, Atom)
            and atom.pred == PRED and atom.args[0] == m):
        return None
    return m, rel.args[2], atom


def unmodified(found):
    """`found`, the noun phrase of a modifier ("every file in the worktree"); an order on it is no meaning (b328): the
    order after "every K in the Y" is the every's (`<T>_<K>_Every`), never the Y's inside the modifier, which no act
    acts on (decision 0093), so spec_meaning.one drops that tree."""
    if getattr(found, "order", None) is not None:
        raise ValueError("an order on the noun phrase of a modifier has no reading: an order is a property of what a "
                         "response acts on")
    return found


def show(a, term):
    x, t, d = a.args
    return "ordered(%s, %s, %s)" % (term(x), t, d)


PLACES = {"while": "a precondition", "where": "a precondition", "when": "the trigger", "if": "the trigger"}


def _within(conds, negated):
    """(the order atom, whether a `not` box holds it) of each order in `conds`."""
    for c in conds:
        if isinstance(c, Box):
            inner = negated or c.op == "not"
            yield from _within(c.body, inner)
            if c.scope is not None:
                yield from _within([c.scope], inner)
        elif isinstance(c, Atom) and c.pred == PRED:
            yield c, negated


def misplaced(form):
    """The refusal of an order with no reading (b285): in a precondition, in the trigger or in a forbidden act; or
    None. An order is a property of what a response prints (decision 0093)."""
    for part in form.parts:
        for atom, negated in _within([part], False):
            said = '"ordered by %s, in %s order"' % (atom.args[1], atom.args[2])
            if part.op in PLACES:
                return ("%s is in %s: an order is a property of what a response prints, and has no reading there"
                        % (said, PLACES[part.op]))
            if negated:
                return ("%s is in an act the line forbids: an order is a property of what a response prints, and "
                        "\"not in this order\" has no reading" % said)
    return None


# --- the check -----------------------------------------------------------------------------------------------------
def facts(walk, atom, act):
    """`ordered(R, I, T, Dir)` of the act `act` (its number) whose object the order is on."""
    _, term, d = atom.args
    walk.emit("ordered", act, '"%s"' % term, d)


# --- the steps -----------------------------------------------------------------------------------------------------
def member(vocab, atom):
    """(None, the attribute entry and its kinds) of an order: the entry of its word that is the ordered K's own, up
    its kind tree (b288: of a word of two senses, the K's sense, not the first entry of the word; b334: the K a
    collection's members are, never the collection); an order no entry of its word is the K's refused naming the
    term."""
    x, term, _ = atom.args
    entries = [(n, t, ks) for n, (t, ks) in enumerate(vocab.attributes, 1) if t.term == term]
    up = vocab.ancestors(x.kind)
    own = next((e for e in entries if any(k in e[2] for k in up)), None)
    if own:
        return None, own
    raise boxes().TraceError("no %s has a %s: no entry of %s is an attribute of its kind" % (x.kind, term, term))


def values(t):
    """Three distinct values of `t`, sorted, of its listed values or its candidates."""
    pool = [v for v in spec_lf_order.candidates(t, []) if spec_lf_order.key(t, v) is not None]
    seen, out = set(), []
    for v in pool:      # the listed values first, then the others the order has
        if spec_lf_order.key(t, v) not in seen:
            seen.add(spec_lf_order.key(t, v))
            out.append(v)
    if len(out) < 3:
        import spec_steps4_boxes  # here: the steps import this module through spec_steps4
        raise spec_steps4_boxes.TraceError("the %s has fewer than three values to order" % t.term)
    out = sorted(out[:3], key=lambda v: spec_lf_order.key(t, v))
    return [out[i] for i in RANKS]


def of(box):
    """The order atom in an every box's scope, or None."""
    return next((i for i in box.scope.body if isinstance(i, Atom) and i.pred == PRED), None) if box.scope else None


def swap(tree, old, new):
    """`tree` with each subtree equal to `old` replaced by `new`."""
    if tree == old:
        return new
    return tuple(swap(a, old, new) for a in tree) if isinstance(tree, tuple) else tree


def said(r, event, x, arg):
    """The Then of `event` (its object x) said of the order's noun phrase: `arg` a function of a slot's kind giving
    the order's argument in that slot. The collection is found in the Then by the slot its frame takes, x's kind or a
    kind above it (b298: "return a worktree", b300: "give every file", whose frames name no `thing`)."""
    tree = r.does(event, True)
    for slot in r.vocab.ancestors(x.kind):
        old = r.arg(x, slot)
        if _holds(tree, old):
            return swap(tree, old, arg(slot))
    import spec_steps4_boxes  # here: the steps import this module through spec_steps4
    raise spec_steps4_boxes.TraceError("no step of an order of %s there" % x.kind)


def _holds(tree, sub):
    return tree == sub or isinstance(tree, tuple) and any(_holds(a, sub) for a in tree)


def every(r, box):
    """[(act, Then)] of a printed every ordered by T (b275): three Ks, each brought in with its restrictor and a value
    of T, in neither the order nor its reverse, the scope's acts said of each, and the Then that states the order."""
    import spec_steps4_counter as counter  # here: the steps import this module through spec_steps4
    atom = of(box)
    plain = Box(box.op, box.refs, box.body, Box("scope", box.scope.refs, tuple(i for i in box.scope.body
                                                                             if i is not atom)))
    x, term, d = atom.args
    _, (n, t, _) = member(r.vocab, atom)
    out, first = [], None
    for copy, v in enumerate(values(t), 1):
        m = counter.renamed(plain, copy)
        for y in plain.refs:
            counter.introduce(r, m[y])
        r.brought += [s for c in boxes().subst(plain.body, m) for s in boxes().restrictor(r, c)]
        r.brought.append(("SCond", spec_lf_order.value_cond(r, m[x], term, v)))
        acts = r.acts(boxes().subst(plain.scope.body, m))
        out += acts if copy == 1 else [("again" if act else act, tree) for act, tree in acts]
        first = first or m
    event = next(i for i in boxes().subst(plain.scope.body, first) if isinstance(i, Atom) and i.pred == "event")
    K = spec_rgl.kid(x.kind)
    np0 = ("t_%s_%d_%s_Every" % (spec_rgl.slug(term), n, K), (K + "_UseN", (K + "_n",)), (FUNS[d],))
    return out + [(None, said(r, event, first[x], _slotted(x.kind, np0)))]


def _slotted(kind, np0):
    """The order's argument in a slot of kind `slot`, `kind`'s own or one above it (b298, b300)."""
    K = spec_rgl.kid(kind)

    def arg(slot):
        S = spec_rgl.kid(slot)
        return (S + "_One", (K + ("_Simple" if slot == kind else "_Up_" + S), np0))
    return arg


def then(r, box, body):
    """[(act, Then)] of an order on a collection's members (b275, b334: the every box `held` reads): three members
    it holds brought in (the first the K the line says it holds, b286), each with a value of T in neither the order
    nor its reverse, and the Then of the act on the collection that states the order."""
    m, x, atom = held(box)
    _, term, d = atom.args
    _, (n, t, _) = member(r.vocab, atom)
    up = r.vocab.ancestors(x.kind)
    row = next(w for w in r.vocab.rows if w[0] == m.kind and w[1] == box.body[0].args[0] and w[2] in up)
    r.bring_in(x)
    said_held = [i.args[1] for i in body if isinstance(i, Atom) and i.pred == "rel" and i.args[0] == row[1]
                 and i.args[2] == x and row[0] in r.vocab.ancestors(i.args[1].kind)]
    for k, v in enumerate(values(t), 1):     # the K the line says it holds the first member (b286)
        y = said_held[0] if k == 1 and said_held else Ref("%s.m%d" % (x.name, k), row[0], "response")
        r.bring_in(y)
        r.brought += [("SCond", r.cond(Atom("rel", (row[1], y, x)))),
                      ("SCond", spec_lf_order.value_cond(r, y, term, v))]
    event = next(i for i in body if isinstance(i, Atom) and i.pred == "event" and x in [z for _, z in i.args[3]])
    R = next(j for j, w in enumerate(r.vocab.rows, 1) if w == row)
    by = ("r%d_in_By_t_%s_%d" % (R, spec_rgl.slug(term), n), r.np0(x)[1], (FUNS[d],))
    return [(None, said(r, event, x, _slotted(x.kind, by)))]


def boxes():
    import spec_steps4_boxes  # here: the steps import this module through spec_steps4
    return spec_steps4_boxes


def read(names, text, tree):
    """(attribute, direction, the ordered noun phrase as the step says it: "the worktree w1", "every file") of the
    order a step's tree states, or None (features_vocab4's Call `order`)."""
    nodes = [tree]
    while nodes:
        node = nodes.pop(0)
        if not isinstance(node, tuple):
            continue
        by = BY.match(node[0])
        t, rest = names.attr(by.group(2) + "_" if by else node[0])
        if t is not None and (by or rest.endswith("_Every")):
            said = text(node[1]) if by else "every " + text(node[1])
            return t.term, DIRS[node[2][0]], said
        nodes += list(node[1:])
    return None
