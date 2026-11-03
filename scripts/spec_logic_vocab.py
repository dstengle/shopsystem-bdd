"""The lexicon's side of the logic: each fun of the generated `Typed` module traced back to its lexicon entry
(design §9.2, §12.1), the values a condition's `Means:` reads, and the context's facts for the background theory
(§12.2).

The fun names are the ones `spec_typed.modules` gives (P2's p2-grammar.md, "Typed fun names"): `<kind>_<det>`,
`<attribute>_<part>`, `<condition>_<part>`, a relation's own id, a value's own id and `n_<word>` for an attribute's
bare word. An attribute or a condition of more than one kind is suffixed with the kind's id.
"""
import re

import spec_lexicon

CORE = {"Ubiq", "When", "While", "Where", "IfThen", "WhileWhen", "WhereWhen", "WhereWhile", "WhileIf", "WhereIf",
        "Shall", "ShallNot", "ActorSubj", "NPSubj", "Runs", "RunsOn", "IsRun", "Happens", "HappensI", "Undergoes",
        "CondOne", "CondAnd", "Holds", "HoldsA", "IsFree", "FeatGiven", "FeatAtom", "Do", "DoTo", "Print", "ExitOk",
        "ExitErr", "RefuseErr", "CommitPush", "ChangeNothing", "Hold", "HoldA", "HoldAtMost", "CodeNP", "QuotedNP",
        "Only", "OneNP", "MoreNP", "CodeLit", "CmdCode", "CmdActor", "QuotedLit", "CountNum", "CountCode"}
KIND_PARTS = {"An", "Every", "The", "No", "AtMostOne", "One", "Pl", "Its", "Named", "It", "toNP", "NumberOf"}
ATTR_PARTS = {"One", "More", "ThatIs", "ThatIsNot", "Whose", "WhoseNot", "Pre", "Is", "IsNot", "Becomes", "Set", "Of"}
COND_PARTS = {"Pre", "ThatIs", "ThatIsNot", "Is", "IsNot"}
AMOUNT = 3   # what a count named by a code (`workers`) stands for in a check


def _bare(text):
    return text.strip().strip("`")


class Vocab:
    """The ids of one lexicon's grammar, by category: kinds, attributes (with their kind and values), conditions,
    relations, events, actors and resources."""

    def __init__(self, lexicon):
        ids = lexicon.ids()
        self.kinds = {ids[t.key]: t.term for t in lexicon.of("kind")}
        by_term = {term: kid for kid, term in self.kinds.items()}
        self.events = {ids[t.key]: t.term for t in lexicon.of("event")}
        self.actors = {ids[t.key]: t.term for t in lexicon.of("actor")}
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
        self.conds, self.cond_terms, self.cond_entries = {}, {}, {}
        for t in lexicon.of("condition"):
            for kind in (k for k in t.kinds if k in by_term):
                cid = ids[t.key] if len(t.kinds) == 1 else "%s_%s" % (ids[t.key], by_term[kind])
                self.conds[cid], self.cond_terms[cid], self.cond_entries[cid] = by_term[kind], t.term, t
        self.rels, self.rel_kinds = {}, {}
        for t in lexicon.of("relation"):
            if len(t.kinds) == 2 and all(k in by_term for k in t.kinds):
                self.rels[ids[t.key]] = spec_lexicon.ident(t.term, "relation")
                self.rel_kinds[ids[t.key]] = t.kinds
        self.means = {cid: self._means(cid) for cid in self.conds}
        self.cond_attr = {cid: m[0] for cid, m in self.means.items() if m}

    def decode(self, fun):
        """(category, id of the lexicon entry, part) of a typed fun; (None, None, None) for any other."""
        if fun in self.value_text:
            return "value", fun, None
        for cat, names in (("kind", self.kinds), ("relation", self.rels), ("event", self.events),
                           ("actor", self.actors), ("resource", self.resources)):
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
        """True when the logic has a translation of the fun."""
        return fun in CORE or self.decode(fun)[0] is not None

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

    def _means(self, cid):
        """(attribute id, values one of which it is, values it is not) of a `Means: its <attribute> is …`, or None
        where the Means says something else."""
        found = re.match(r"^its (.+?) is (.+)$", self.cond_entries[cid].means.strip().rstrip("."))
        kid = self.conds[cid]
        tid = next((tid for tid, (k, t) in self.attrs.items() if found and k == kid and t.term == found.group(1)),
                   None)
        if tid is None:
            return None
        by_text = {_bare(self.value_text[v]): v for v in self.attr_values[tid]}
        pos, neg = [], []
        for clause in found.group(2).split(" and "):
            negated = clause.startswith("not ")
            words = re.split(r",\s*|\s+or\s+", clause[4:] if negated else clause)
            vids = [by_text.get(_bare(w)) for w in words if w.strip()]
            if not vids or None in vids:
                return None
            (neg if negated else pos).extend(vids)
        return tid, pos, neg


def means_values(vocab, cid):
    """(values one of which the condition's Means names, values it excludes), or None when it does not read."""
    found = vocab.means.get(cid)
    return (found[1], found[2]) if found else None


def facts(vocab):
    """The context's facts from its lexicon: values, resources, the event and kind names the background theory
    reads, and each condition's rule from its `Means:` (a free atom where it does not read)."""
    out = ["value(%s,%s,%s)." % (kid, tid, vid) for tid, (kid, _) in sorted(vocab.attrs.items())
           for vid in vocab.attr_values[tid]]
    out += ["attribute(%s,%s)." % (kid, tid) for tid, (kid, _) in sorted(vocab.attrs.items())]
    for sid, term in sorted(vocab.resources.items()):
        out += ["resource(%s)." % sid, "capacity(%s,%d)." % (sid, 1 if "exclusive" in term.resource else AMOUNT)]
    names = {"start": "start_event(%s).", "end": "end_event(%s)."}
    out += [names[term] % eid for eid, term in sorted(vocab.events.items()) if term in names]
    out += ["resource_kind(%s)." % kid for kid, term in sorted(vocab.kinds.items()) if term == "resource"]
    out += ["resource_relation(%s)." % vocab.rels[rid] for rid, (_, k2) in sorted(vocab.rel_kinds.items())
            if k2 == "resource"]
    for cid, kid in sorted(vocab.conds.items()):
        term = vocab.cond_terms[cid]
        if term == "free" and vocab.kinds.get(kid) == "resource":
            out.append("free_condition(%s)." % cid)
            continue
        read = means_values(vocab, cid)
        if read is None:
            out.append("{ cond(%s,X) } :- kind(X,%s)." % (cid, kid))
            continue
        pos, neg = read
        tid = vocab.cond_attr[cid]
        body = ["kind(X,%s)" % kid]
        if len(pos) == 1:
            body.append("attr(X,%s,%s)" % (tid, pos[0]))
        elif pos:
            out += ["vals(%s,%s)." % (cid, v) for v in pos]
            body += ["attr(X,%s,V)" % tid, "vals(%s,V)" % cid]
        body += ["not attr(X,%s,%s)" % (tid, v) for v in neg]
        out.append("cond(%s,X) :- %s." % (cid, ", ".join(body)))
    return {"always": out, "dynamic": [], "initial": []}
