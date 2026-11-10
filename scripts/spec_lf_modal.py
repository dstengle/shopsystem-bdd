"""Modality in the check's facts (the CNL 4 design, section 4.5, I17), beside spec_lf_facts: a permission's acts are
`resp(R,I,may,E,D,X)`, which `grammar/check.lp` pairs with a "shall not" line of the act (L7, `forbid(A,B)`); a
necessity, "a K1 always (never) Qs a K2", is no rule but a premise of every pair, `nec(R,always|never,Q,Kx,Ky)` with
its relation's two kinds in the order of the check's `crel`, and `necsub(R,1|2)`, the place of its subject among
them (the one "always" quantifies over). A necessity with a While clause, or with more than one relation or state in
its clause, has no translation and is refused naming it."""
from spec_lf_core import Atom


def necessary(walk, form):
    """True when `form` is a necessity, its facts emitted on `walk` (a spec_lf_facts Walk); else the walk is told
    whether it is a permission (`walk.may`), and a modality with no translation raises ValueError."""
    walk.may = form.modality == "may"
    if form.modality in ("always", "never"):
        necessity(walk, form)
        return True
    if form.modality not in ("shall", "may"):
        raise ValueError("no translation of the rule %s %s" % (form.modality, " ".join(p.op for p in form.parts)))
    return False


def polarity(walk, pos):
    """The polarity of an act: `may` for a positive act of a permission, else `pos` or `neg`."""
    return ("may" if walk.may else "pos") if pos else "neg"


def necessity(walk, form):
    """The facts of a necessity's form, emitted on `walk` (a spec_lf_facts Walk)."""
    ops = tuple(p.op for p in form.parts)
    if ops != ("holds",):
        raise ValueError("no translation of a necessity under %s" % ops[0])
    body = form.parts[0].body
    if len(body) != 1 or not isinstance(body[0], Atom) or body[0].pred not in ("rel", "state"):
        raise ValueError("no translation of a necessity over more than one relation or state")
    q, x, y = walk.edge(body[0])
    subject = 2 if body[0].pred == "rel" else 1     # "a session has a worktree" is crel(of, worktree, session)
    walk.emit("form", "nec")
    walk.out.append("cnl4(%s)." % walk.rid)
    walk.emit("nec", form.modality, q, walk.ids.kind(x.kind), walk.ids.kind(y.kind))
    walk.emit("necsub", subject)
    return walk.out
