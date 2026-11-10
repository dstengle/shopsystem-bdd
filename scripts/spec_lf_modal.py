"""Modality in the check's facts (the CNL 4 design, section 4.5, I17), beside spec_lf_facts: a permission's acts are
`resp(R,I,may,E,D,X)`, which `grammar/check.lp` pairs with a "shall not" line of the act (L7, `forbid(A,B)`); a
necessity, "a K1 always (never) Qs a K2", is read by no rule of the check: it is its `form(R,nec)` and `cnl4(R)`
only, so it is neither refused nor a premise of a pair, and hides no finding (no line asks the check to read it)."""


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
    """A necessity's facts, emitted on `walk` (a spec_lf_facts Walk): its form and mark only, no premise."""
    walk.emit("form", "nec")
    walk.out.append("cnl4(%s)." % walk.rid)
    return walk.out
