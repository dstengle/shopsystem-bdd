"""Orders (b275, `order-by` and `order-by-every`): ", ordered by T, in ascending order" (or "in descending order")
after a collection that holds members by a row `K1 | in | K2`, T an attribute of K1 ("a worktree that holds a file,
ordered by version, in descending order": spec_rgl_np's `r<n>_in_By_<T>`), or after a printed "every K", T an
attribute of K ("every file, ordered by version, in ascending order": `<T>_<K>_Every`). One translation in each place
a line is read:

- the form (`np`): one atom `ordered(x, T, ascending|descending)` beside the clause's atom (spec_lf_core's NP
  `order`), x the collection or the every's K; an order on an attribute with no value order (spec_value_kinds) a note
  naming the attribute, which spec_lf_read gives as the line's refusal; `show` its line in `model parse --form`;
- the check (`facts`): `ordered(R, I, T, Dir)` of the response's act I, a fact: two lines that require one
  collection, or one printing, in opposite orders on one trigger are an L1 (grammar/check.lp), and nothing else is
  proved of it;
- the steps (`member`, `values`, `every`, `then`): three members with distinct values of T, given in neither the order nor its
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
    return replace(found, order=Atom(PRED, (found.ref, t.term, DIRS[nps.fun(a[1])])))


def show(a, term):
    x, t, d = a.args
    return "ordered(%s, %s, %s)" % (term(x), t, d)


# --- the check -----------------------------------------------------------------------------------------------------
def facts(walk, atom, act):
    """`ordered(R, I, T, Dir)` of the act `act` (its number) whose object the order is on."""
    _, term, d = atom.args
    walk.emit("ordered", act, '"%s"' % term, d)


# --- the steps -----------------------------------------------------------------------------------------------------
def member(vocab, atom):
    """(the member kind, the attribute entry and its kinds) of an order: the K1 of a row `K1 | in | K2` of the
    collection's kind whose K1 has the attribute, or the every's own kind."""
    x, term, _ = atom.args
    n, t, ks = next((n, t, ks) for n, (t, ks) in enumerate(vocab.attributes, 1) if t.term == term)
    if any(k in ks for k in vocab.ancestors(x.kind)):
        return None, (n, t, ks)
    row = next(r for r in vocab.rows if r[1] == "in" and r[2] in vocab.ancestors(x.kind)
               and any(k in ks for k in vocab.ancestors(r[0])))
    return row, (n, t, ks)


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
    """The Then of `event` (its object x) said of the order's noun phrase `arg`, a `k_thing_Arg` tree."""
    tree = r.does(event, True)
    old = r.arg(x, "thing")
    if not _holds(tree, old):
        import spec_steps4_boxes  # here: the steps import this module through spec_steps4
        raise spec_steps4_boxes.TraceError("no step of an order of %s there" % x.kind)
    return swap(tree, old, arg)


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
    arg = ("t_%s_%d_%s_Every" % (spec_rgl.slug(term), n, K), (K + "_UseN", (K + "_n",)), (FUNS[d],))
    return out + [(None, said(r, event, first[x], arg))]


def then(r, atom, body):
    """[(act, Then)] of an order on a collection (b275): three members it holds brought in, each with a value of T
    in neither the order nor its reverse, and the Then of the act on the collection that states the order."""
    x, term, d = atom.args
    row, (n, t, _) = member(r.vocab, atom)
    r.bring_in(x)
    for k, v in enumerate(values(t), 1):
        y = Ref("%s.m%d" % (x.name, k), row[0], "response")
        r.bring_in(y)
        r.brought += [("SCond", r.cond(Atom("rel", ("in", y, x)))), ("SCond", spec_lf_order.value_cond(r, y, term, v))]
    event = next(i for i in body if isinstance(i, Atom) and i.pred == "event" and x in [z for _, z in i.args[3]])
    R = next(j for j, w in enumerate(r.vocab.rows, 1) if w == row)
    K = spec_rgl.kid(x.kind)
    by = ("r%d_in_By_t_%s_%d" % (R, spec_rgl.slug(term), n), r.np0(x)[1], (FUNS[d],))
    return [(None, said(r, event, x, ("k_thing_One", (K + "_Up_k_thing", by) if x.kind != "thing" else by)))]


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
