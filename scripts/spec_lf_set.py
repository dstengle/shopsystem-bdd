"""A response that sets an attribute of a thing to a value in grammar 4 (b216; the CNL 4 design, section 7.2: set
among initiates and terminates), one translation of spec_rgl's `<t>_Set` in each place a line is read.

- The logical form (`vp`): "D shall set the T of x to v" (or "its T", bound by R8 to the clause's subject, or "the K
  T") is the atom `initiates(e, subject: D, T(x) = v)`: the act e of D makes T of x v. The value is the post-state,
  never a presupposition of the pre-state; x is the owner the noun phrase names, no image of T is made.
- `model parse --form` (`show`): the atom as `initiates(e2, subject: x3, status(x2) = done)`.
- `model logic`'s facts (`facts`): the act `resp(R,I,Pol,set(T,V),D,X)`, the set of design-r3 §3,
  and, when it obliges, `set(R,I,X,T,V)`, which check.lp's two states read as the post-state.
- `features generate`'s Then (`then`): "D sets the T of x to v" in the present, with its polarity (`k_agent_Does`).
"""
import spec_rgl
from spec_lf_core import Atom

PRED = "initiates"


def vp(st, tree, owner):
    """(the noun phrases of a `<t>_Set` verb phrase, build(subject, their referents) -> its atom), or None for
    another fun; `owner(st, tnp)` translates "the T of x" to x's noun phrase (spec_lf_np.owner)."""
    name = tree if isinstance(tree, str) else tree[0]
    t, rest = st.names.attr(name)
    if t is None or rest != "Set":
        return None
    tnp, val = tree[1], tree[2]
    value = st.names.value(val if isinstance(val, str) else val[0])
    return [owner(st, tnp)], lambda s, r: Atom(PRED, (st.event(), s, r[0], t.term, value))


def show(a, term):
    e, doer, x, attr, value = a.args
    return "%s(%s, subject: %s, %s(%s) = %s)" % (PRED, e, term(doer), attr, term(x), value)


def facts(walk, atom, polarity):
    """The facts of a setting act, `polarity` its `resp`'s (pos, neg or may)."""
    _, doer, x, attr, value = atom.args
    tid, vid = walk.ids.attr(x.kind, attr, value)
    walk.acts += 1
    if polarity == "pos":
        walk.emit("set", walk.acts, walk.term(x), tid, vid)
    walk.emit("resp", walk.acts, polarity, "set(%s,%s)" % (tid, vid), walk.term(doer), walk.term(x))


def then(reader, atom, pos):
    """The Then tree of a setting act: `k_agent_Does` over `<t>_Set` of "the T of x" and the value's fun; None
    when no attribute of x's kind is the atom's."""
    _, doer, x, attr, value = atom.args
    for n, (t, kinds) in enumerate(reader.vocab.attributes, 1):
        k = next((k for k in kinds if k in reader.vocab.ancestors(x.kind)), None)
        if t.term == attr and k is not None:
            T = "t_%s_%d" % (spec_rgl.slug(attr), n)
            owner = ("%s_Of_%s" % (T, spec_rgl.kid(k)), reader.np(x, k))
            return ("k_agent_Does", ("PPos",) if pos else ("PNeg",), reader.arg(doer, "agent"),
                    (T + "_Set", owner, ("%s_v_%s" % (T, spec_rgl.slug(value)),)))
    return None
