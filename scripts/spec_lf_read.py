"""The reading rules of grammar 4 over the logical form (the CNL 4 design, call 5, section 7.3; I11b), written out
with their test lines in grammar/language.md.

Most rules are readings the translation (spec_lf_clause, spec_lf_np) already gives: R1 ("a K" a referent of its
part: any K in a While clause or a trigger, a new one in a response), R3 ("no K" a `not` box over its own clause),
R5 ("only" an `only` box, obliging nothing), R6 ("every K" in a response an `every` box), R10 (a code no word of the
context names a parameter) and R11 ("this K" the run's own K). R7 (counts) is I15's and R9 (edge, level, the If
precedence, inertia) the check's (I12a, I12b). This module holds the rest, and the refusals:

- R2: "the K" binds to the latest earlier referent of kind K (a part's, an actor, a code, an indexical), else to the image of a row `K | of | S` of the one earlier
  referent of kind S (the worktree of the session), else to the run's own K when K's entry has `This:`; else the
  line is refused, naming the noun (`the`).
- R4: "does not V a K" in a While or Where clause is refused (`negated`): it reads as "Vs no K" and as "a K that X
  does not V"; the writer says one of them. Under "shall not" in a response, "a K" stays any K.
- R8: "its" binds to the subject of its clause; the line is refused when that subject is of no kind the relation
  needs, or when another referent of such a kind was given before it (`its`).
- R12: a line with no trigger, and neither "always" nor "never", whose response obliges an act (an event outside a
  `not` or `only` box) is refused: it would oblige in every state. A "shall not" or "only" line with no trigger
  forbids or restricts in every state, which is its meaning (`refusal`). A "may" line obliges nothing (I17).

The translation keeps the refusals of R2, R4 and R8 in its State's `notes` as it meets them; `refusal` gives the
first of them, else R12's.
"""
import spec_frames
import spec_lf_core as core
from spec_lf_core import NP, Atom, Box, NPList

PARTS = ("while", "trigger", "response")
ACCESSIBLE = PARTS + ("constant", "indexical", "parameter")


def article(noun):
    return ("an " if noun[:1] in "aeiou" else "a ") + noun


def noun(st, kind, plural=False):
    return st.vocab.nouns.get(kind, (kind, kind + "s"))[1 if plural else 0]


def words(st, ref):
    """How a referent is said: an actor's or a code's words, else "the" and its noun."""
    return ref.value if ref.value and ref.origin != "indexical" else "the " + noun(st, ref.kind)


def _image(st, row, y):
    ref, new = st.image((row, y), row[0])
    return NP(ref, "a", [Atom("rel", ("of", ref, y))]) if new else core.fixed(ref)


def the(st, kind, plural=False):
    """R2 and R11: the NP "the K" binds to, or None, the refusal noted (the caller makes a definite referent)."""
    bound = next((r for r in reversed(st.refs) if r.origin in ACCESSIBLE and kind in st.vocab.ancestors(r.kind)), None)
    if bound is not None:
        return core.fixed(bound)
    rows = [r for r in st.names.rows.values() if r[0] == kind and r[1] == "of"]
    found = list(dict.fromkeys((r, y) for r in rows for y in st.refs
                               if y.origin in ACCESSIBLE and r[2] in st.vocab.ancestors(y.kind)))
    if len(found) == 1:
        return _image(st, *found[0])
    if kind in st.vocab.this:
        return core.fixed(st.constant(kind, st.vocab.this[kind], "indexical"))
    said = "the " + noun(st, kind, plural)
    more = (': %d earlier noun phrases may give it: say "the %s of" one of them' % (len(found), noun(st, kind))
            if found else ": no earlier noun phrase, functional relation or declared indexical gives %s"
            % article(noun(st, kind)))
    st.notes.append('"%s" has no antecedent%s' % (said, more))
    return None


def its(st, kinds, said):
    """R8: note the refusal of "its ..." (`said`) when the clause's subject is of none of `kinds`, the kinds the
    relation needs, or when another referent of one of them was given before."""
    s = st.subject

    def fits(r):
        return any(k in st.vocab.ancestors(r.kind) for k in kinds)
    if s is None or not fits(s):
        who = words(st, s) if s is not None else "nothing"
        st.notes.append('"%s" binds to %s, the subject of its clause, which has no %s'
                        % (said, who, said.split(" ", 1)[1]))
        return
    others = [r for r in st.refs if r != s and r.origin in ACCESSIBLE and fits(r)]
    if others:
        st.notes.append('"%s" binds to %s, the subject of its clause, and %s was given before it: say "the %s of" '
                        'one of them' % (said, words(st, s), article(noun(st, others[0].kind)), said.split(" ", 1)[1]))


def note(st, why):
    """A refusal met while translating, once."""
    if why not in st.notes:
        st.notes.append(why)


def verb(st, vptree):
    """(the base form, the third person form) of a verb phrase's verb or row."""
    name = vptree if isinstance(vptree, str) else vptree[0]
    row = st.names.row(name)[0]
    if row:
        return ("have", "has") if row[1] == "of" else ("hold", "holds")
    n = int(name.rsplit("_", 3 if name.startswith("g_") else 2)[1])
    term = st.names.verbs[n].term
    return term.term, spec_frames.s3(term)


def negated(st, subject, args, vptree):
    """R4: note the refusal of a negated clause in a While or Where clause with "a K" (or a bare plural) after its
    verb; `subject` is the clause's subject (a Ref), `args` the noun phrases after it."""
    if st.origin != "while":
        return
    for a in args:
        for m in a.members if isinstance(a, NPList) else [a]:
            if isinstance(m, NP) and m.quant == "a" and m.new and m.said and not m.ref.definite:
                base, s3 = verb(st, vptree)
                k = noun(st, m.ref.kind)
                st.notes.append('the While clause says "does not %s %s", which reads two ways: say "%s no %s" or '
                                '"%s that %s does not %s"' % (base, m.said, s3, k, article(k), words(st, subject),
                                                              base))
                return


def obliges(box):
    """Whether a box obliges an act: an event in it outside a `not` or `only` box, or a count that admits none."""
    for c in box.body:
        if isinstance(c, Atom) and c.pred == "event":
            return True
        if isinstance(c, Box) and (c.op == "every" and obliges(c.scope) or c.op in ("or", "case") and obliges(c)
                                   or c.op == "count" and core.least(c.count) and obliges(c.scope)):
            return True
    return False


def refusal(vocab, tree):
    """The refusal of a grammar 4 tree by the reading rules (its words after "refused: "), or None."""
    import spec_lf  # spec_lf's translation imports this module
    form, st = spec_lf.translate(vocab, tree)
    if st.notes:
        return "refused: " + st.notes[0]
    ops = {p.op for p in form.parts}
    if not ops & {"when", "if"} and form.modality == "shall" \
            and any(obliges(p) for p in form.parts if p.op == "response"):
        return ('refused: the line has no trigger and neither "always" nor "never": it would oblige its response in '
                'every state')
    return None
