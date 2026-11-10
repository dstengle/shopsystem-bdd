"""The lexicon's side of the logic (design-r3 §3): each fun of the generated `Typed` module traced back to its lexicon
entry, and the domain facts for `grammar/check.lp` (kinds, sub-kinds, actors and each actor's kind, values,
transitions, `initial/3`).

A codified-2 context's Vocab (`Vocab(lexicon, parents)`, spec_lf_facts) is read from its layered lexicon, packs
included, with the kind tree of grammar 4 (`parents`, spec_rgl_vocab: `thing` and `agent` among its kinds).

The fun names are the ones `spec_typed.modules` gives: `<kind>_<det>`, `<attribute>_<part>`, `<condition>_<part>`,
`rel_<k1>_<word>_<k2>` (a relation row's modifier), its `_Atom` (its clause) and `_AtomNot` (the clause negated), a value's own id and `n_<word>` for an
attribute's bare word. An attribute or a condition of more than one kind is suffixed with the kind's id. A relation
is named by its row's id (`spec_relations.rid`), shared by every row its `Kind of:` expansion gives.

A condition is **defined** when its sentence parses as a `Def` (spec_facts.define reads it and marks it with
`Vocab.define`) and **opaque** otherwise (design-r3 §3.2).
"""
import spec_lexicon
import spec_relations
import spec_typed
import spec_typed_def
import spec_typed_verbs

CORE = {"Ubiq", "When", "While", "Where", "IfThen", "WhileWhen", "WhereWhen", "WhereWhile", "WhileIf", "WhereIf",
        "Shall", "ShallNot", "OneVP", "AndVP", "OneVPor", "OrVP", "OneResp", "AndResp", "ActorSubj", "NPSubj",
        "Runs", "RunsOn", "IsRun", "Happens", "HappensI", "HappensTo", "Does", "DoesNot", "CondOne", "CondAnd",
        "CondOr", "Holds",
        "HoldsA", "IsFree", "FeatGiven", "FeatAtom", "Do", "DoI", "DoTo", "Print", "ExitOk", "ExitErr", "ChangeNothing",
        "Hold", "HoldA", "HoldAtMost", "CodeNP", "QuotedNP", "QuotedFor", "Only", "OneNP", "MoreNP", "CodeLit", "CmdCode",
        "CmdActor", "QuotedLit", "CountNum", "CountCode"}
KIND_PARTS = {"An", "Every", "The", "No", "AtMostOne", "One", "Pl", "Its", "Named", "It", "toNP", "NumberOf"}
ATTR_PARTS = {"One", "More", "ThatIs", "ThatIsNot", "Whose", "WhoseNot", "Pre", "Is", "IsNot", "Becomes", "Set", "Of"}
COND_PARTS = {"Pre", "ThatIs", "ThatIsNot", "Is", "IsNot"}


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
    """The ids of one lexicon's grammar, by category: kinds (with their supertypes), attributes (with their kind,
    values and transitions), conditions, relations, events, actors and resources."""

    def __init__(self, lexicon, parents=None):
        ids = lexicon.ids()
        self.kinds = {ids[t.key]: t.term for t in lexicon.of("kind")}
        taken = set(self.kinds.values())
        self.kinds.update({spec_lexicon.ident(k, "kind"): k for k in parents or () if k not in taken})
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
        self.words = {"n_" + spec_lexicon.ident(t.term, "attribute")[2:] for t in lexicon.of("attribute")}
        self.conds, self.cond_terms, self.defined = {}, {}, set()
        for t in lexicon.of("condition"):
            for kind in (k for k in t.kinds if k in by_term):
                cid = ids[t.key] if len(t.kinds) == 1 else "%s_%s" % (ids[t.key], by_term[kind])
                self.conds[cid], self.cond_terms[cid] = by_term[kind], t.term
        by_cond = {(self.cond_terms[c], self.kinds[k]): c for c, k in self.conds.items()}
        self.def_funs = {fun: (by_cond[pair], by_term[pair[1]])
                         for fun, pair in spec_typed_def.funs(lexicon).items() if pair in by_cond}
        self.def_lits = {}   # {condition id: (kind id, its Def clause)}, from spec_facts.define
        self.rels, self.rel_kinds = {}, {}
        for k1, word, k2, rid in lexicon.relations():
            if k1 in by_term and k2 in by_term:
                self.rels[spec_typed.relation_fun(by_term[k1], word, by_term[k2])] = rid
                self.rel_kinds.setdefault(rid, set()).add((by_term[k1], by_term[k2]))
        self.functional = {spec_relations.rid(row) for row in lexicon.rows if functional(row)}
        subs = spec_relations.subkinds(lexicon) if parents is None else _under(parents)
        self.subs = sorted((by_term[s], by_term[k]) for k, under in subs.items() for s in under
                           if k in by_term and s in by_term)

    def decode(self, fun):
        """(category, id of the lexicon entry, part) of a typed fun; (None, None, None) for any other."""
        if fun in self.value_text:
            return "value", fun, None
        if fun in self.rels:
            return "relation", self.rels[fun], None
        if fun.endswith("_Atom") and fun[:-5] in self.rels:
            return "relation", self.rels[fun[:-5]], "Atom"
        if fun.endswith("_AtomNot") and fun[:-8] in self.rels:
            return "relation", self.rels[fun[:-8]], "AtomNot"
        for cat, names in (("kind", self.kinds), ("event", self.events), ("actor", self.actors),
                           ("resource", self.resources)):
            if fun in names:
                return cat, fun, None
        if fun in self.words:
            return "attribute_word", fun, None
        prefix, _, part = fun.rpartition("_")
        for cat, names, parts in (("kind", self.kinds, KIND_PARTS), ("attribute", self.attrs, ATTR_PARTS),
                                  ("condition", self.conds, COND_PARTS)):
            if prefix in names and part in parts:
                return cat, prefix, part
        return None, None, None

    def covers(self, fun):
        """True when the logic has a translation of the fun: a typed verb fun's is that of its normal form
        (spec_typed_verbs)."""
        return fun in CORE or spec_typed_verbs.SEP in fun or self.decode(fun)[0] is not None

    def define(self, cid):
        """Mark a condition as defined by a `Def` sentence: its literals stand in for it (design-r3 §3.2)."""
        self.defined.add(cid)

    @staticmethod
    def value(t):
        return t[0]

    def members(self, t):
        """The members of a value list or a noun phrase list, or the one value."""
        fun = t[0]
        if fun == "OneNP" or (fun.endswith("_One") and self.decode(fun)[0] == "attribute"):
            return [t[1]]
        if fun == "MoreNP" or (fun.endswith("_More") and self.decode(fun)[0] == "attribute"):
            return [t[1]] + self.members(t[2])
        return [t]

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
    no transition enters, or every value when each one is entered."""
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
    return out

