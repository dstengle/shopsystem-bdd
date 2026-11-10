"""Identity and distinctness in the logical form (b240, construct #2), one translation of Base's determiners
`DetAnother`, `DetDifferent`, `DetTwo` and `DetSame` over a common noun, written out in grammar/language.md
(Constructs, "another K" ...):

- "another K" and "a different K": a referent of its part, as "a K", and the atom `distinct(y, x)`, x the latest
  earlier referent of kind K that R2 would bind "the K" to (both of a pair "two Ks" gave); with none the line is
  refused naming the noun, as R2 refuses "the K" (`another`);
- "two Ks": two referents, the second `distinct` from the first, as "a K and a K" (an `and` list); what restricts
  the noun restricts each, a referent its restriction makes outside a box shared, one made in a box made again for the
  second; the pair kept in the State, so that a later "the K" is refused and "another K" is distinct from both (`two`);
- "the same K": "the K" (R2), else, after "two Ks" of another kind, one new K the pair shares (`same`).

`show` writes the atom for `model parse --form`; the check and the steps have no reading of it yet (phase 9): a
form that holds it is refused by both, naming it (`refuse`).
"""
import spec_lf_read
from spec_lf_core import NP, Atom, Box, NPList, Ref

PRED = "distinct"
DETS = ("DetAnother", "DetDifferent", "DetTwo", "DetSame")


def det(st, d, cn, kind, restrict):
    """The NP (or the NPList of "two Ks") of the determiner `d` over the common noun `cn` of kind `kind`; `restrict`
    is spec_lf_np's, (referents, conditions) a common noun puts on a referent."""
    if d == "DetTwo":
        return two(st, cn, kind, restrict)
    if d == "DetSame":
        return same(st, cn, kind, restrict)
    return another(st, cn, kind, restrict, "another" if d == "DetAnother" else "a different")


def antecedents(st, kind, said):
    """The referents "another K" (`said`) is distinct from, or [] with the refusal noted."""
    refs = [r for r in st.refs if r.origin in spec_lf_read.ACCESSIBLE and r not in st.open and r not in st.boxed]
    bound = next((r for r in reversed(refs) if kind in st.vocab.ancestors(r.kind)), None)
    if bound is not None:
        return list(st.pairs.get(bound, (bound,)))
    hidden = [r for r in st.refs if r in st.boxed and kind in st.vocab.ancestors(r.kind)]
    if hidden:
        st.notes.append(spec_lf_read.inside(st, said, hidden[-1], st.boxed[hidden[-1]]))
    else:
        st.notes.append('"%s" has no antecedent: no earlier noun phrase gives %s'
                        % (said, spec_lf_read.article(spec_lf_read.noun(st, kind))))
    return []


def another(st, cn, kind, restrict, word):
    said = "%s %s" % (word, spec_lf_read.noun(st, kind))
    xs = antecedents(st, kind, said)
    ref = st.ref(kind)
    refs, conds = restrict(st, cn, ref)
    return NP(ref, "a", [Atom(PRED, (ref, x)) for x in xs] + conds, refs, said=said)


def two(st, cn, kind, restrict):
    said = "two " + spec_lf_read.noun(st, kind, True)
    x = st.ref(kind)
    refs, conds = restrict(st, cn, x)
    y = st.ref(kind)
    again = [rename(st, c, {x: y}) for c in conds]
    st.pairs[x] = st.pairs[y] = (x, y)
    return NPList("and", [NP(x, "a", conds, refs, said=said),
                          NP(y, "a", [Atom(PRED, (y, x))] + again, [], said=said)])


def rename(st, item, mapping):
    """`item` (an atom or a box) said of the second of a pair: each referent in `mapping` replaced, each referent a
    box makes made again."""
    if isinstance(item, Box):
        fresh = {r: st.ref(r.kind) for r in item.refs}
        inner = dict(mapping)
        inner.update(fresh)
        return Box(item.op, tuple(fresh[r] for r in item.refs), tuple(rename(st, c, inner) for c in item.body),
                   rename(st, item.scope, inner) if item.scope is not None else None, item.count)
    return Atom(item.pred, _sub(item.args, mapping))


def _sub(x, mapping):
    if isinstance(x, Ref):
        return mapping.get(x, x)
    if isinstance(x, tuple):
        return tuple(_sub(y, mapping) for y in x)
    return x


def same(st, cn, kind, restrict):
    said = "the same " + spec_lf_read.noun(st, kind)
    seen = len(st.notes)
    found = spec_lf_read.the(st, kind, said=said)     # R2, R11
    if found is not None:
        refs, conds = restrict(st, cn, found.ref)
        found.restr, found.inner = found.restr + conds, found.inner + refs
        return found
    shared = st.pairs and not any(kind in st.vocab.ancestors(r.kind) for r in st.pairs)
    if shared:
        del st.notes[seen:]
    ref = st.ref(kind, definite=not shared)
    refs, conds = restrict(st, cn, ref)
    return NP(ref, "a", conds, refs, said=said)


def held(items):
    """The first `distinct` atom of `items` (a form's parts, boxes, atoms) at any depth, or None."""
    for c in items:
        if isinstance(c, Box):
            found = held(c.body) or (held([c.scope]) if c.scope is not None else None)
            if found is not None:
                return found
        elif c.pred == PRED:
            return c
    return None


def refuse(form, error):
    """Raise `error` naming the first `distinct` atom of `form`: the check and the steps read none yet (phase 9)."""
    found = held(form.parts)
    if found is not None:
        raise error("no translation of distinct(%s, %s)" % (found.args[0].name, found.args[1].name))


def show(a, term):
    return "%s(%s)" % (PRED, ", ".join(term(x) for x in a.args))
