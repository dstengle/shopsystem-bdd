"""The time constructs of grammar 4 in the logical form (the CNL 4 design, section 7.2, call 9; I16), one translation
per template of spec_rgl_time.

- "x is after y", "x is before y": `cmp(x, after, y)`, `cmp(x, before, y)`, y a moment's referent (a code among them).
- "x is within the last N units": `cmp(x, after, now - N units)`, now the moment of the trigger; its bound is
  `Ago(N, unit)`.
- "S has V-ed O" (the perfect of an action verb): `history(verb, sense, roles)`, the frame's atom as a state that the
  action sets and nothing unsets; "since m" a role of its own after the frame's.
Each takes its clause's polarity as a condition does: what follows the subject under `not`. `model logic` has no
reading of them yet: spec_lf_facts refuses a line holding a comparison or a history, naming it.
"""
from dataclasses import dataclass

import spec_lf_clause
import spec_lf_core as core
import spec_lf_np as nps
import spec_lf_read
import spec_rgl
import spec_rgl_time
import spec_rgl_vocab
from spec_lf_core import Atom

ORDER = {"After": "after", "Before": "before"}


@dataclass(frozen=True)
class Ago:
    """now - n units: the bound "within the last n units" puts on a moment."""
    n: int
    unit: str


def amount(tree):
    name, a = nps.fun(tree), nps.args(tree)
    if name == "AmountInt":
        return int(a[0])
    return spec_rgl_time.NUMBERS.index(name[len("A_"):]) + 1


def ago(st, span):
    """The Ago of a Span's tree, `u_<unit>_Span amount`."""
    slug = nps.fun(span)[len("u_"):-len("_Span")]
    unit = next(u for u in spec_rgl_time.units(st.vocab) if spec_rgl.slug(u) == slug)
    return Ago(amount(nps.args(span)[0]), unit)


def history(st, subject, vptree, neg, since=None):
    """(referents, conditions) of "S has V-ed O" (and "since m"): the frame's atom made a history."""
    saved, events, st.subject = st.subject, st.events, spec_lf_clause.subject_of(subject)
    args, build = spec_lf_clause.vp(st, vptree)
    st.subject = saved
    if neg:
        noted = len(st.notes)
        spec_lf_read.negated(st, spec_lf_clause.subject_of(subject), args, vptree)     # R4
        st.notes[noted:] = [perfect(st, note, vptree) for note in st.notes[noted:]]
    extra = [nps.np(st, since)] if since is not None else []

    def made(r):
        _, verb, sense, roles = build(r[0], r[1:1 + len(args)]).args
        st.events = events      # a history is no event of the line
        return Atom("history", (verb, sense, roles + ((("since", r[-1]),) if extra else ())))
    return core.apply([subject] + args + extra, made, 1 if neg else None)


def perfect(st, note, vptree):
    """R4's refusal of a negated history said in the perfect: "has not ended a stage", "has ended no stage"."""
    base, s3 = spec_lf_read.verb(st, vptree)
    term = st.names.verbs[int(nps.fun(vptree).rsplit("_", 2)[1])].term
    pp = term.forms[1].split()[0] if len(term.forms) > 1 else (base + "d" if base.endswith("e") else base + "ed")
    return (note.replace('"does not %s ' % base, '"has not %s ' % pp).replace('"%s no ' % s3, '"has %s no ' % pp)
            .replace(' does not %s"' % base, ' has not %s"' % pp))


def cond(st, tree):
    """(referents, conditions) of a time construct's condition, or None when `tree` is no such condition."""
    name, a = nps.fun(tree), nps.args(tree)
    rest = st.names.kind(name)[1]
    neg = 1 if a and a[0] == "PNeg" else None
    if rest == "Within":
        bound = ago(st, a[2])
        return core.apply([nps.np(st, a[1])], lambda r: Atom("cmp", (r[0], "after", bound)), neg)
    if rest == "Cmp":
        op = ORDER[nps.fun(a[2])]
        return core.apply([nps.np(st, a[1]), nps.np(st, a[3])], lambda r: Atom("cmp", (r[0], op, r[1])), neg)
    if rest in ("Done", "DoneSince"):
        return history(st, nps.np(st, a[1]), a[2], bool(neg), a[3] if rest == "DoneSince" else None)
    return None


def show(a, term):
    """A time atom as `model parse --form` prints it: `has end(x1, object: x2)`, `cmp(x1) after now - 7 days`."""
    if a.pred == "history":
        verb, n, roles = a.args
        return "has %s%s(%s)" % (verb, "#%d" % n if n > 1 else "", ", ".join(term(r) for r in roles))
    x, op, y = a.args
    bound = "now - %d %s" % (y.n, y.unit if y.n == 1 else spec_rgl_vocab.regular_plural(y.unit)) if isinstance(y, Ago) else term(y)
    return "cmp(%s) %s %s" % (term(x), op, bound)
