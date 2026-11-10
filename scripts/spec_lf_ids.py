"""The check's names of a codified-2 context's words (the CNL 4 design, I12a), for spec_lf_facts: each kind, actor,
verb, attribute and value, and relation row by the ids its logic Vocab (spec_logic_vocab) gives the codified-1 facts,
so both kinds of file name one word alike; an attribute or a row found for a kind or a kind above it in grammar 4's
kind tree. A word with no id raises ValueError naming it.
"""
import spec_lexicon


class Ids:
    """The check's names of a codified-2 context's words, from its logic Vocab (spec_logic_vocab) and lexicon."""

    def __init__(self, vocab, lexicon, parents):
        self.v = vocab
        self.actors = {term: aid for aid, term in vocab.actors.items()}
        self.events = {term: eid for eid, term in vocab.events.items()}
        self.parents = dict(parents)
        self.rows = list(lexicon.relations())

    def kind(self, kind):
        return self.v.by_term.get(kind) or spec_lexicon.ident(kind, "kind")

    def above(self, kind):
        out, up = [], kind
        while up is not None and up not in out:
            out.append(up)
            up = self.parents.get(up, "thing" if up != "thing" else None)
        return out

    def attr(self, kind, term, value):
        """(attribute id, value id) of `term` of a thing of `kind`."""
        for k in self.above(kind):
            for tid, (kid, entry) in self.v.attrs.items():
                if entry.term == term and kid == self.v.by_term.get(k):
                    vid = next((x for x in self.v.attr_values[tid] if self.v.value_text[x] == value), None)
                    if vid is not None:
                        return tid, vid
        raise ValueError("no translation of the value %s of %s" % (value, term))

    def relation(self, word, k1, k2):
        up1, up2 = self.above(k1), self.above(k2)
        for a, w, b, rid in self.rows:
            if w == word and a in up1 and b in up2:
                return rid
        raise ValueError("no translation of the relation %s %s %s" % (k1, word, k2))

    def event(self, term):
        if term not in self.events:
            raise ValueError("no translation of the verb %s" % term)
        return self.events[term]
