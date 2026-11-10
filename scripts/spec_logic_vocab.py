"""The lexicon's side of the logic (design-r3 §3): a codified-2 context's words by the ids the check names them by,
and the domain facts for `grammar/check.lp` (kinds, sub-kinds, actors and each actor's kind, values, transitions,
`initial/3`, the functional relations, the prose conditions).

`Vocab(lexicon, parents)` is read from the context's layered lexicon (spec_rgl_vocab.lexicon), packs included, with
the kind tree of grammar 4 (`parents`, spec_rgl_vocab: `thing` and `agent` among its kinds). An attribute or a
condition of more than one kind is suffixed with the kind's id. A relation is named by its row's id
(`spec_relations.rid`), shared by every row its `Kind of:` expansion gives.

A condition (an adjective) is **prose** to the check: grammar 4 reads no definition of it, so a clash that depends on
it is an L6 (design-r3 §3.2, `prose(C)`).
"""
import spec_lexicon
import spec_lf_order
import spec_relations

# A relation row with no cardinality whose word is one of these prepositions relates a thing to one thing: a stage is
# for one node and with one result (a call of report-checker-gaps; "one" says it, any other word does not).
PREPOSITIONS = ("for", "with", "on", "of", "in")


def functional(row):
    """Whether a relation row relates each thing of its first kind to at most one of its second."""
    card = row.cardinality.strip().lower()
    return card == "one" or (not card and row.word.strip().lower() in PREPOSITIONS)


def _bare(text):
    return text.strip().strip("`")


class Vocab:
    """The ids of a layered lexicon's words, by category: kinds (with grammar 4's kind tree), attributes (with their
    kind, values and transitions), conditions, functional relations, events, actors and resources."""

    def __init__(self, lexicon, parents):
        ids = lexicon.ids()
        self.kinds = {ids[t.key]: t.term for t in lexicon.of("kind")}
        taken = set(self.kinds.values())
        self.kinds.update({spec_lexicon.ident(k, "kind"): k for k in parents if k not in taken})
        by_term = {term: kid for kid, term in self.kinds.items()}
        self.by_term = by_term
        self.events = {ids[t.key]: t.term for t in lexicon.of("event")}
        self.actors = {ids[t.key]: t.term for t in lexicon.of("actor")}
        self.actor_kinds = {ids[t.key]: by_term[t.supertype] for t in lexicon.of("actor") if t.supertype in by_term}
        self.resources = {ids[t.key]: t for t in lexicon.of("resource")}
        self.attrs, self.attr_values, self.value_text, seen = {}, {}, {}, set()
        for t in lexicon.of("attribute"):
            for kind in t.kinds:
                if kind not in by_term or not t.values or any((kind, v) in seen for v in t.values):
                    continue
                seen |= {(kind, v) for v in t.values}
                tid = ids[t.key] if len(t.kinds) == 1 else "%s_%s" % (ids[t.key], by_term[kind])
                self.attrs[tid] = (by_term[kind], t)
                self.attr_values[tid] = [ids[("value", v, (kind, t.term))] for v in t.values]
                self.value_text.update(zip(self.attr_values[tid], t.values))
        self.conds, self.cond_terms = {}, {}
        for t in lexicon.of("condition"):
            for kind in (k for k in t.kinds if k in by_term):
                cid = ids[t.key] if len(t.kinds) == 1 else "%s_%s" % (ids[t.key], by_term[kind])
                self.conds[cid], self.cond_terms[cid] = by_term[kind], t.term
        self.functional = {spec_relations.rid(row) for row in lexicon.rows if functional(row)}
        subs = _under(parents)
        self.subs = sorted((by_term[s], by_term[k]) for k, under in subs.items() for s in under
                           if k in by_term and s in by_term)

    def transitions(self, tid):
        """The (from, to) value ids of an attribute's `Transitions:`."""
        by_text = {_bare(self.value_text[v]): v for v in self.attr_values[tid]}
        return sorted({(by_text[_bare(a)], by_text[_bare(b)]) for a, b, _ in self.attrs[tid][1].transitions
                       if _bare(a) in by_text and _bare(b) in by_text})


def _under(parents):
    """{kind: every kind under it, at any depth} of a kind tree {kind: its parent}."""
    out = {k: set() for k in parents}
    for k in parents:
        seen, up = {k}, parents[k]
        while up is not None and up not in seen:
            out.setdefault(up, set()).add(k)
            seen.add(up)
            up = parents.get(up)
    return out


def domain(vocab):
    """The lexicon's facts for `grammar/check.lp` (design-r3 §3): kinds, sub-kinds, actors with the kind each is a
    kind of (`akind`, b121), each attribute's values in their order, its transitions, and its initial values: those
    no transition enters, or every value when each one is entered; an ordered attribute's points (spec_lf_order); each
    condition `prose(C)`."""
    out = ["kind(%s)." % k for k in sorted(vocab.kinds)]
    out += ["sub(%s,%s)." % pair for pair in vocab.subs]
    out += ["actor(%s)." % a for a in sorted(vocab.actors)]
    out += ["akind(%s,%s)." % pair for pair in sorted(vocab.actor_kinds.items())]
    out += ["fun(%s)." % r for r in sorted(vocab.functional)]
    for tid, (kid, _) in sorted(vocab.attrs.items()):
        values, edges = vocab.attr_values[tid], vocab.transitions(tid)
        entered = {b for _, b in edges}
        out += ["val(%s,%s,%s)." % (kid, tid, v) for v in values]
        out += ["trans(%s,%s,%s,%s)." % (kid, tid, a, b) for a, b in edges]
        out += ["initial(%s,%s,%s)." % (kid, tid, v) for v in values if v not in entered or entered >= set(values)]
    out += ["prose(%s)." % c for c in sorted(vocab.conds)]
    return out + spec_lf_order.domain(vocab)

