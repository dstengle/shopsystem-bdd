"""A codified-1 line's facts under a codified-2 index (b151): the line is translated with the old lexicon's Vocab,
whose funs its tree carries, and each id of its facts is then mapped to the layered Vocab's id of the same entry,
matched by its term and kind, so the facts, the domain and every reader of them stay in the layered space.

The old lexicon numbers every entry of a word (`c_closed`, `c_closed_2` ...); the layered one keeps only the highest
layer's entries of it, numbered again. An id of the old lexicon whose entry the layered one left out has no
counterpart: the line that uses it is refused (`Unmapped`), naming the word.
"""
import clingo


class Unmapped(ValueError):
    """An id of the old vocabulary with no entry of its term and kind in the layered one."""


def _keys(v):
    """{id: (category, term, kind, value)} of each id a fact can carry."""
    out = {k: ("kind", t) for k, t in v.kinds.items()}
    for cat, names in (("event", v.events), ("actor", v.actors)):
        out.update({i: (cat, t) for i, t in names.items()})
    out.update({i: ("resource", t.term) for i, t in v.resources.items()})
    for tid, (kid, entry) in v.attrs.items():
        out[tid] = ("attribute", entry.term, v.kinds[kid])
        out.update({vid: ("value", entry.term, v.kinds[kid], v.value_text[vid]) for vid in v.attr_values[tid]})
    out.update({c: ("condition", v.cond_terms[c], v.kinds[k]) for c, k in v.conds.items()})
    out.update({r: ("relation", r) for r in v.rel_kinds})
    out.update({w: ("word", w) for w in v.words})
    return out


class Ids:
    """The old Vocab's ids mapped to the layered Vocab's (`old` and `layered` the same Vocab: every id itself)."""

    def __init__(self, old, layered):
        self.old, self.layered = old, layered
        theirs = {key: i for i, key in _keys(layered).items()}
        self.ids, self.missing = {}, {}
        for i, key in _keys(old).items():
            if key in theirs:
                self.ids[i] = theirs[key]
            else:
                self.missing[i] = key
        self.back = {new: i for i, new in self.ids.items()}

    def same(self):
        return self.old is self.layered

    def symbol(self, sym):
        if sym.type != clingo.SymbolType.Function:
            return sym
        if not sym.arguments:
            if sym.name in self.missing:
                key = self.missing[sym.name]
                raise Unmapped("the %s %s%s has no entry in the layered lexicon" % (
                    key[0], key[1], " of %s" % key[2] if len(key) > 2 else ""))
            return clingo.Function(self.ids.get(sym.name, sym.name), [], sym.positive)
        return clingo.Function(sym.name, [self.symbol(a) for a in sym.arguments], sym.positive)

    def fact(self, text):
        """One fact `p(...).` with its ids mapped."""
        if self.same():
            return text
        return "%s." % self.symbol(clingo.parse_term(text.rstrip().rstrip(".")))

    def facts(self, texts):
        return [self.fact(t) for t in texts]

    def domain(self, def_facts):
        """The old Vocab's facts of its defined conditions mapped, each of an id with no counterpart left out (no line
        can use it), and `prose(C)` of each layered condition the old Vocab has none of."""
        if self.same():
            return def_facts
        out = []
        for text in def_facts:
            try:
                out.append(self.fact(text))
            except Unmapped:
                continue
        return out + ["prose(%s)." % c for c in sorted(self.layered.conds) if c not in self.back]

    def lay(self):
        """The layered Vocab given the old one's defined conditions, by their layered ids, and this map, for a reader
        that follows a definition (spec_steps_facts) in the old vocabulary it is written in."""
        if self.same():
            return
        v = self.layered
        v.def_lits = {self.ids[c]: (self.ids[k], clause) for c, (k, clause) in self.old.def_lits.items()
                      if c in self.ids and k in self.ids}
        v.defined = set(v.def_lits)
        v.under = self
