"""The codified reading of scripts/model (design model v5; the GF conversion's design §7, §8, §10, §13.4): a part of
Model (model_facts).

A capability file with `language: codified-1` is read by spec_read into groups `<cap>#g<n>`, each requirement
`<cap>#r<n>` a member of one, and every requirement parsed in the context's grammar (spec_grammar): parsed(Q),
unparsed(Q, Why) or ambiguous(Q), its trigger and condition trees normalised as pre(Q, Key) (v15k), and logic_only(G)
from spec_tree; exemplified(Q, Literal) for a code or quoted string naming no declared constant
(spec_example, w_example); given_condition(G, Line) for a given line that is not example data (spec_read_given, v15m).
`spec/universal.md` gives the universal conditions, `spec/restated.json` the 0.29 ids a group may
restate, and a typed glossary (spec_lexicon) the terms with their categories. A scenario of a codified capability
names its group by `@g<n>`: generates(G, S)."""

import re
from collections import Counter

import spec_example
import spec_frames
import spec_lexicon
import spec_packs
import spec_read
import spec_read_given
import spec_tree

GRAMMAR_MISSING = object()


def term_word(t, shared=False):
    """The word a term's id is made of, as the 0.29 reader keyed it: a relation `<term> of <k1> to <k2>`, an attribute
    or condition entry with no gloss (it opens with a field), or a condition that is `shared` (another entry has its
    word), `<term> of <kind>`, any other the term."""
    word = t.term.replace("`", "").strip()
    if t.category == "relation" and len(t.kinds) == 2:
        return f"{word} of {t.kinds[0]} to {t.kinds[1]}"
    if t.category in ("attribute", "condition") and t.kinds and (shared and t.category == "condition" or not spec_lexicon.gloss(t.text)):
        return f"{word} of {', '.join(t.kinds)}"
    return word


def bare(value):
    return value.replace("`", "").strip()


class SpecReading:
    """The part of Model that reads codified files."""

    def read_lexicon(self):
        """The typed glossary: a term for each entry (a word given in a second category gets `-<category>`), and a term
        for each value of each kind's attribute, with category, value_of and linearises facts."""
        self.fact("typed", self.context)
        index = self.root / "spec" / "index.md"
        for n, bullet in enumerate(spec_lexicon._bullets(index.read_text(), "Glossary"), 1):
            if spec_lexicon.entry(bullet, "spec/index.md") is None:
                self.problems.append(f"spec/index.md: glossary bullet {n} is not '- **<term>** (<part of speech>): <text>'")
        lexicon = spec_lexicon.read(self.root)
        cats, n, terms = {}, 0, lexicon.terms
        words, known, kinds = Counter(t.term for t in terms), spec_frames.names(lexicon), lexicon.kind_names()
        overlapping = spec_frames.overlapping(lexicon)
        unmarked = spec_packs.unmarked(self.root, lexicon)     # v_t16, and v_t17 of an import of no pack
        for name in spec_packs.missing(self.root):
            self.fact("misimported", self.context, name)
        for n, t in enumerate(terms, 1):
            word = " ".join(term_word(t, words[t.term] > 1).lower().split())
            ident = self.term_id(word)
            if cats.get(ident, t.category) != t.category:
                word = f"{word} {t.category}"
                ident = self.term_id(word)
            cats[ident] = t.category
            self.term(word, n, [" ".join(w.lower().split()) for w in t.nots])
            if t.category:
                self.fact("category", ident, t.category)
            misread = t.category == "event" and spec_frames.misread(t, known)
            if misread:
                self.fact("misframed", ident, misread)
            elif t.category == "event" and spec_frames.frame(t, known) is None:
                self.fact("frameless", ident)
            if t.category == "event" and not t.aspect:
                self.fact("aspectless", ident)
            if t.category == "event" and words[t.term] > 1 and all(
                    u.category == "event" for u in terms if u.term == t.term):     # two senses of one verb
                self.fact("senses", ident)
                if t.term in overlapping:
                    self.fact("overlapping", ident)
            for name in unmarked.get((t.where, t.term), ()):
                self.fact("unmarked", ident, name)
            if t.category == "condition" and spec_frames.relational(t, kinds):
                self.fact("relational", ident)
            self.fact("linearises", ident, f"{t.category} {t.term} ({', '.join(t.kinds)})")
            if t.category == "attribute":
                for k in t.kinds:
                    for v in t.values:
                        vid = f"term/{self.path}/{re.sub(r'[^a-z0-9]+', '-', f'{bare(v)} of {k}'.lower()).strip('-')}"
                        self.node(vid, "term")
                        self.fact("term_of", vid, self.context)
                        self.fact("category", vid, "value")
                        self.fact("value_of", vid, self.term_id(k), ident)

    def read_restated(self):
        self.restated = spec_read.restated(self.root)
        for key in self.restated:
            self.fact("restated_id", f"{key}@0.29")

    def parsed(self, ident, text):
        """parsed, unparsed or ambiguous for one statement; its tree, or None."""
        if self._grammar is GRAMMAR_MISSING:
            return None
        import spec_grammar
        try:
            p = spec_grammar.parse(self.root, text)
        except (ImportError, spec_grammar.GrammarError) as err:      # no pgf, no gf, or gf refused the sources
            self._grammar = GRAMMAR_MISSING
            fix = "" if isinstance(err, spec_grammar.Unlabelled) else "; run `python3 scripts/tools install`"
            self.problems.append(f"the codified statements are not parsed: {err}{fix}")
            return None
        if p.tree is not None:
            self.fact("parsed", ident)
        elif p.trees:
            self.fact("ambiguous", ident)
        else:
            self.fact("unparsed", ident, p.refusal)
        return p.tree

    def given(self, gid, lines):
        """given_unparsed(G, Line) for a given line the typed Steps grammar (features_vocab) refuses as a Given."""
        import features_vocab
        import spec_grammar
        try:
            vocab = features_vocab.load(self.root)
        except (ImportError, spec_grammar.GrammarError):    # no tools: parsed() says which
            return
        for line, _ in lines:
            try:
                features_vocab.parse(vocab, "given", line)
            except features_vocab.StepError:
                self.fact("given_unparsed", gid, line)

    def read_codified(self, cap, path, entry):
        doc = spec_read.capability(path)
        where = self.rel(path)
        self.problems += [f"{where}: {p}" for p in doc.problems]
        self.fact("codified", cap)
        entry["codified"] = True
        for r in doc.retired:
            m = re.fullmatch(r"([rg])(\d+)", str(r))
            if not m:
                self.problems.append(f"{where}: retired {r!r} is not r<n> or g<n>")
            elif m.group(1) == "g":
                self.fact("retired_group", cap, int(m.group(2)))
            else:
                self.retired.add((cap, int(m.group(2))))
                self.fact("retired_id", cap, int(m.group(2)))
        for g in doc.groups:
            gid = f"{cap}#{g.id}"
            self.node(gid, "requirement-group")
            self.fact("group_id", gid, cap, int(g.id[1:]))
            self.fact("in", gid, cap)
            self.groups[gid] = g
            for name, n in g.restates:
                old = f"{name}#r{n}@0.29"
                self.fact("restates", gid, old)
                self.restated_by.setdefault(old, []).append(gid)
            trees = []
            for q in g.requirements:
                n = int(q.id[1:])
                qid = f"{cap}#{q.id}"
                self.node(qid, "requirement")
                self.fact("req_id", qid, cap, n)
                self.fact("member_of", qid, gid)
                entry["reqs"][n] = qid
                self.req_text[qid] = q.text
                self.group_of[qid] = gid
                tree = self.parsed(qid, q.text)
                for word in spec_example.parameters(q.text, self.example_constants()):     # w_example (I18)
                    self.fact("exemplified", qid, word)
                if tree is not None:
                    self.unmentioned.add(qid)       # a parsed statement uses lexicon words (C27)
                    trees.append(tree)
                    self.pre(qid, tree)
            if trees and len(trees) == len(g.requirements) and spec_tree.logic_only(trees):
                self.fact("logic_only", gid)
            for n, rid, text in g.odd:      # v15a with no id, v15b with an id used before
                qid = f"{cap}#line{n}" if rid is None else f"{cap}#{rid}~{n}"
                self.node(qid, "requirement")
                self.fact("member_of", qid, gid)
                if rid is not None:
                    self.fact("req_id", qid, cap, int(rid[1:]))
                self.req_text[qid] = text
            if g.given:
                self.given(gid, g.given)
            for line, block in g.given:     # v15m: a condition the statement has, not example data
                if not spec_read_given.example(line, block):
                    self.fact("given_condition", gid, line)

    def example_constants(self):
        """The declared constants a literal of a line may name (spec_example), read once."""
        if getattr(self, "_constants", None) is None:
            self._constants = spec_example.constants(spec_lexicon.read(self.root))
        return self._constants

    def pre(self, qid, tree):
        clauses = spec_tree.parts(spec_tree.normal(tree))
        if any(clauses[k] is not None for k in ("feat", "cond", "trig")):
            self.fact("pre", qid, " | ".join("-" if clauses[k] is None else spec_tree.show(clauses[k])
                                             for k in ("feat", "cond", "trig")))

    def read_universal(self):
        doc = spec_read.read_universal(self.root)
        if not doc.path.is_file():
            return
        if not spec_read.codified(doc.path):
            self.fact("uncodified", "spec/universal.md")
            return
        self.problems += [f"spec/universal.md: {p}" for p in doc.problems]
        for u in doc.conditions:
            uid = f"universal-condition/{self.path}/u{u.id[1:]}"
            self.node(uid, "universal-condition")
            self.fact("u_id", uid, int(u.id[1:]))
            self.req_text[uid] = u.text
            self.unmentioned.add(uid)
            self.parsed(uid, u.text)

    def codified_scenario(self, cap, key, title, tags, s):
        """generates(G, S) for each @g<n> tag naming a group of the capability."""
        self.unmentioned.add(s)
        for tag in tags:
            m = re.fullmatch(r"@(g\d+)", tag)
            if not m:
                continue
            gid = f"{cap}#{m.group(1)}"
            if self.nodes.get(gid) == "requirement-group":
                self.fact("generates", gid, s)
            else:
                self.dangling.append(f"{key}: scenario {title!r} names {gid}, which {cap} does not have")
