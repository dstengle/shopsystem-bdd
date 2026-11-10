"""The logical form of a grammar 4 requirement (the CNL 4 design, call 8, section 7; I11a): what a line means, as
referents, atoms and boxes (spec_lf_core's types), made from its tree by one translation per template (spec_lf_clause
for the rule and its clauses, spec_lf_np for its noun phrases), and written out for `model parse --form` (`show`).
It is the meaning spec_meaning compares the trees of a line by (call 2): two trees with one form are one meaning.
The reading rules (R1-R12) and their refusals are spec_lf_read's (I11b): "the", "its" and a negated clause are
resolved or noted as they are translated, and `spec_lf_read.refusal` reads the form and the notes.
"""
import spec_lf_clause
import spec_lf_core
import spec_lf_np
import spec_lf_time
import spec_meaning
from spec_lf_core import Box, Ref

_names = {}


def form(vocab, tree):
    """The Form of `tree` (a grammar 4 tree's text) over the context's Vocab `vocab`."""
    return translate(vocab, tree)[0]


def translate(vocab, tree):
    """(the Form of `tree`, the State of its translation, whose `notes` are the reading rules' refusals met)."""
    if id(vocab) not in _names:
        _names.clear()
        _names[id(vocab)] = (vocab, spec_lf_np.Names(vocab))
    st = spec_lf_core.State(vocab, _names[id(vocab)][1])
    st.clauses = spec_lf_clause
    return spec_lf_clause.rule(st, spec_meaning.read(tree)), st


def term(x):
    if isinstance(x, Ref):
        return x.name
    if isinstance(x, tuple):
        return ": ".join(term(y) for y in x)
    return str(x)


def atom(a):
    if a.pred == "event":
        e, verb, n, roles = a.args
        return "%s%s(%s)" % (verb, "#%d" % n if n > 1 else "", ", ".join([e] + [term(r) for r in roles]))
    if a.pred == "state":
        verb, n, roles = a.args
        return "%s%s(%s)" % (verb, "#%d" % n if n > 1 else "", ", ".join(term(r) for r in roles))
    if a.pred == "rel":
        word, x, y = a.args
        return "%s(%s, %s)" % (word, term(x), term(y))
    if a.pred in ("history", "cmp"):
        return spec_lf_time.show(a, term)
    x, attr, v = a.args
    return "%s(%s) = %s" % (attr, term(x), term(v))


def ref(r):
    if r.origin == "indexical":
        return '%s: %s "%s"' % (r.name, r.kind, r.value)
    said = " %s" % r.value if r.value is not None else (" (the)" if r.definite else "")
    return "%s: %s%s" % (r.name, r.kind, said)


def box(b, depth):
    pad = "  " * depth
    op = b.op + (" %s %d" % b.count if b.count else "")
    head = pad + op + (" [%s]" % ", ".join(ref(r) for r in b.refs) if b.refs else "")
    out = [head]
    for c in b.body:
        out += box(c, depth + 1) if isinstance(c, Box) else [pad + "  " + atom(c)]
    if b.scope is not None:
        out += box(b.scope, depth + 1)
    return out


def show(f):
    """The form as lines: its modality and fixed referents (each with its origin), then each part as a box."""
    out = ["%s [%s]" % (f.modality, ", ".join("%s (%s)" % (ref(r), r.origin) for r in f.fixed))]
    for p in f.parts:
        out += box(p, 1)
    return "\n".join(out)

