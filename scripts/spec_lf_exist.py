"""Existence (b240, construct #7): one translation of spec_rgl_np's `Exists_St`, "x exists", in each place a line is
read.

- the form (`vp`): the atom `exists(x)`, a state of x whose frame takes no object; "x does not exist" puts it under
  `not`, "no K exists" is a `not` box with its K (R3), "a K that exists" restricts the K;
- the check (`literal`, `none`, `restrict`): the one-place fluent `crel(R, exists, X, none, Pol)` (check.lp's state
  whose frame takes no object, b219), "no K exists" `rnone(R, exists, kind(K), none)`, an object's restriction
  `orel(R, exists, X, none)`; `exists` is no verb's id (those are `e_...`), so it never meets a verb's state;
- the steps (`given`): the Given "the file f1 exists", "the file f1 does not exist" and "no file exists".
"""
import spec_rgl
import spec_rgl_np
from spec_lf_core import Atom

PRED = "exists"


def vp(name):
    """(no noun phrases, build(subject, []) -> `exists(subject)`) of `Exists_St`, else None."""
    if name != spec_rgl_np.EXISTS:
        return None
    return [], lambda s, r: Atom(PRED, (s,))


def show(a, term):
    return "%s(%s)" % (PRED, term(a.args[0]))


def literal(terms, item, pos):
    """`crel(R, exists, X, none, Pol)` of `exists(x)` in the pre-state."""
    terms.emit("crel", PRED, terms.term(item.args[0]), "none", "pos" if pos else "neg")


def none(terms, kind):
    """"no K exists": `rnone(R, exists, kind(K), none)`."""
    terms.emit("rnone", PRED, "kind(%s)" % terms.ids.kind(kind), "none")


def restrict(terms, item, pred="orel"):
    """"a K that exists" on a response's object: `orel(R, exists, X, none)` (`rrel` under "only")."""
    terms.emit(pred, PRED, terms.term(item.args[0]), "none")


def given(r, item, pos):
    """The Cond tree of "the file f1 exists" (with `pos` false "does not exist"); a code's thing said with its kind,
    "the `a` file exists", so the step names what exists."""
    x = item.args[0]
    if x.origin in ("constant", "parameter") and x.value not in r.actors and x.kind != "thing":
        K = spec_rgl.kid(x.kind)
        subject = ("k_thing_One", ("%s_Up_k_thing" % K, (K + "_Named", ("CodeLit", x.value), (K + "_UseN", (K + "_n",)))))
    else:
        subject = r.arg(x, "thing")
    return ("k_thing_Holds", ("PPos",) if pos else ("PNeg",), subject, (spec_rgl_np.EXISTS,))
