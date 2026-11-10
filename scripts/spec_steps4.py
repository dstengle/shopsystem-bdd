"""A codified-2 group's requirements as Gherkin steps, read off their logical forms (the CNL 4 design, section 7.4;
I14a), the one meaning `model logic` reads (spec_lf), in the step grammar 4's trees (spec_rgl_steps).

- Givens: what the While and Where parts say, then what the trigger says of its referents besides its event, each a
  condition (`SCond`), a referent brought in at its first mention (`K_Given`, "a stage s1"); a `not` with no
  referents of its own is its condition negated.
- When: the trigger's event (`STrig`).
- Thens: each act of the response in the present (`S_Does`; setting an attribute spec_lf_set's), its polarity kept: "change nothing" is "changes nothing",
  a `not` over an act on a referent of its own "does not V a K"; a condition of the response a condition.
  An act a universal condition entails (`entailed`, by the act's number as spec_lf_facts numbers it: each act in
  order, "change nothing" one) is left out, a comment `# entailed: <premise>` in its place.
Givens and the When are the first requirement's; a later one's While and trigger referent of a kind is the first
one's of that kind and rank. A referent is named by its kind's first letter and a count, in order of first mention;
an actor by its fun, a code by the slot's `K_Code`, the run's own thing by `K_This`. A construct with no step
(`every`, `only`, a count, `or`, a relation row's atom, a negated restriction, a line of "may", "always" or
"never") is a TraceError naming it.
"""
import spec_lf
import spec_lf_set
import spec_rgl
from spec_lf_core import Atom, Box

kid = spec_rgl.kid


class TraceError(Exception):
    """A group with no scenario: a construct of its form with no step."""


class Reader:
    """One scenario read into step trees: the referents' names and the words' funs."""

    def __init__(self, vocab):
        self.vocab, self.names, self.counts, self.shared, self.known = vocab, {}, {}, {}, set()
        self.actors = {t: ("a_%s_%d" % (spec_rgl.slug(t), n + 1), k) for n, (t, k) in enumerate(vocab.actors)}

    # --- referents ---------------------------------------------------------------------------------------------
    def bind(self, refs, n):
        """Name a requirement's While and trigger referents, a later requirement's as the first's of its kind and
        rank; `n` is the requirement's place in its group."""
        rank = {}
        for r in refs:
            if r.origin not in ("while", "trigger"):
                continue
            rank[r.kind] = rank.get(r.kind, 0) + 1
            key = (r.kind, rank[r.kind])
            if n and key in self.shared:
                self.names[r] = self.shared[key]
            else:
                self.shared.setdefault(key, self.name(r))

    def name(self, ref):
        if ref not in self.names:
            letter = ref.kind[0].lower()
            self.counts[letter] = self.counts.get(letter, 0) + 1
            self.names[ref] = "%s%d" % (letter, self.counts[letter])
        return self.names[ref]

    def np0(self, ref):
        """(kind, the K_NP0 tree) of a referent that is no code."""
        if ref.origin == "constant" and ref.value in self.actors:
            fun, k = self.actors[ref.value]
            return k, (fun,)
        K = kid(ref.kind)
        if ref.origin == "indexical":
            return ref.kind, (K + "_This", (K + "_n",))
        return ref.kind, (K + "_Inst", (K + "_n",), ("NameLit", self.name(ref)))

    def np(self, ref, slot, a=False):
        """The `K_NP` tree of a referent in a slot of kind `slot`; with `a`, "a K" of its kind."""
        S = kid(slot)
        if not a and ref.origin in ("constant", "parameter") and ref.value not in self.actors:
            return (S + "_Code", ("CodeLit", ref.value))
        k, tree = (ref.kind, (kid(ref.kind) + "_Det", ("DetA",), (kid(ref.kind) + "_UseN", (kid(ref.kind) + "_n",)))) \
            if a else self.np0(ref)
        if slot not in self.vocab.ancestors(k):
            raise TraceError("no step of a %s in a slot of %s" % (k, slot))
        return (S + "_Simple", tree) if k == slot else ("%s_Up_%s" % (kid(k), S), tree)

    def arg(self, ref, slot, a=False):
        return (kid(slot) + "_One", self.np(ref, slot, a))

    # --- atoms -------------------------------------------------------------------------------------------------
    def frame(self, verb, sense, roles):
        """(fun, subject kind, the slot kinds) of the frame an atom's roles read."""
        seen = 0
        for n, v in enumerate(self.vocab.verbs, 1):
            seen += v.term.term == verb
            if v.term.term != verb or seen != sense:
                continue
            for m, (subject, pieces) in enumerate(v.frames, 1):
                labels = [(" ".join(w) or "object") if k is not None else " ".join(w) for w, k in pieces]
                if labels == [r[0] for r in roles[1:]]:
                    return ("e_%s_%s_%d_%d" % (spec_rgl.slug(verb), v.aspect, n, m), subject,
                            [k for _, k in pieces if k is not None])
        raise TraceError("no frame of %s" % verb)

    def clause(self, atom, a=()):
        """(subject kind, the subject's argument, the verb phrase) of an event or state atom; the referents in `a`
        said "a K"."""
        verb, sense, roles = atom.args[-3:]
        fun, subject, slots = self.frame(verb, sense, roles)
        refs = [r[1] for r in roles[1:] if len(r) == 2]
        if any(r.kind == "thing" and r in a for r in refs) and verb == "change" and len(refs) == 1:
            vp = (fun, ("k_thing_One", ("k_thing_Nothing",)))
        else:
            vp = (fun,) + tuple(self.arg(r, k, r in a) for r, k in zip(refs, slots))
        return subject, self.arg(roles[0][1], subject), vp

    def cond(self, item, pos=True):
        """The `Cond` tree of a state or attribute atom."""
        pol = ("PPos",) if pos else ("PNeg",)
        if item.pred == "state":
            subject, s, vp = self.clause(item)
            return (kid(subject) + "_Holds", pol, s, vp)
        if item.pred == "attr" and not hasattr(item.args[2], "kind"):
            x, term, value = item.args
            for n, (t, kinds) in enumerate(self.vocab.attributes, 1):
                k = next((k for k in kinds if k in self.vocab.ancestors(x.kind)), None)
                if t.term == term and k is not None:
                    T = "t_%s_%d" % (spec_rgl.slug(term), n)
                    return ("%s_%s_Is" % (T, kid(k)), pol, self.np(x, k), "%s_v_%s" % (T, spec_rgl.slug(value)))
        raise TraceError("no step of %s" % spec_lf.atom(item))

    def given(self, item, pos=True):
        """The Given steps of a condition, each referent it mentions first brought in."""
        if isinstance(item, Box):
            if item.op != "not" or item.refs:
                raise TraceError("no Given of %s" % item.op)
            return [s for sub in item.body for s in self.given(sub, not pos)]
        cond = self.cond(item, pos)
        out = []
        for r in mentioned(item):
            if r not in self.known and r.origin in ("while", "trigger"):
                self.known.add(r)
                out.append((kid(r.kind) + "_Given", (kid(r.kind) + "_n",), ("NameLit", self.name(r))))
        return out + [("SCond", cond)]

    def acts(self, body, pos=True):
        """[(act number or None, Then tree)] of a response's items, numbered as spec_lf_facts numbers its acts."""
        out = []
        for item in body:
            if isinstance(item, Atom) and item.pred in ("event", spec_lf_set.PRED):
                out.append((True, self.does(item, pos)))
            elif isinstance(item, Atom):
                out.append((None, ("SCond", self.cond(item, pos))))
            elif item.op == "not" and len(item.body) == 1 and isinstance(item.body[0], Atom) and \
                    item.body[0].pred in ("event", spec_lf_set.PRED):
                out.append((True, self.does(item.body[0], not pos, set(item.refs))))
            elif item.op == "not" and not item.refs:
                out += self.acts(item.body, not pos)
            else:
                raise TraceError("no Then of %s" % item.op)
        return out

    def does(self, atom, pos, a=()):
        if atom.pred == spec_lf_set.PRED:     # "`work` sets the status of the stage s2 to `done`" (b216)
            found = spec_lf_set.then(self, atom, pos)
            if found is None:
                raise TraceError("no step of %s" % spec_lf.atom(atom))
            return found
        subject, s, vp = self.clause(atom, a)
        nothing = vp[1:] == (("k_thing_One", ("k_thing_Nothing",)),)
        return (kid(subject) + "_Does", ("PPos",) if pos or nothing else ("PNeg",), s, vp)


def mentioned(item):
    out = []
    for x in item.args:
        for r in (x if isinstance(x, tuple) else (x,)):
            r = r[1] if isinstance(r, tuple) and len(r) == 2 else r
            if hasattr(r, "origin") and r not in out:
                out.append(r)
    return out


def read(vocab, forms, entailed=None):
    """[(keyword, tree)] of one group, `forms` the (requirement id, Form) of each of its requirements in order;
    `entailed` gives {requirement id: {act number: the comment's premise}}, an act left out with ("#", comment)."""
    r, givens, when, thens = Reader(vocab), [], [], []
    for n, (ident, form) in enumerate(forms):
        if form.modality != "shall":     # a permission obliges nothing, a necessity has no trigger (I17)
            raise TraceError("no step of a line that says %s" % form.modality)
        r.bind([x for p in form.parts for x in p.refs], n)
        number, gone = 0, (entailed or {}).get(ident, {})
        for part in form.parts:
            if part.op in ("while", "where") and n == 0:
                givens += [g for item in part.body for g in r.given(item)]
            elif part.op in ("when", "if") and n == 0:
                events = [i for i in part.body if isinstance(i, Atom) and i.pred == "event"]
                givens += [g for item in part.body if item not in events for g in r.given(item)]
                subject, s, vp = r.clause(events[0])
                when.append(("STrig", (kid(subject) + "_Event", s, vp)))
            elif part.op == "response":
                for act, tree in r.acts(part.body):
                    number += bool(act)
                    thens.append(("#", "entailed: %s" % gone[number]) if act and number in gone else ("then", tree))
            elif part.op not in ("while", "where", "when", "if"):
                raise TraceError("no step of %s" % part.op)
    out = [("given", g) for g in dict.fromkeys(givens)] + [("when", w) for w in when]
    return out + list(dict.fromkeys(thens))
