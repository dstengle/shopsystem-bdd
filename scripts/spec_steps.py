"""A group's requirements read into Gherkin steps (design-r3 §5): their facts (`spec_facts`), never a solve, read by
fixed rules into the Steps trees of Givens, a When and Thens.

`read(facts, logic, steps)` takes the facts of each requirement of one group, in order, as `spec_steps_facts` keeps
them (a split requirement's first way through; a defined condition without its definition's literals):
- Givens: `feat`, then the pre-state (`cond`, `ccond`, `crel`, `holds`, `free`) in fact order, then one contrast
  for each `every` role with a restriction. A `none` gives no Given.
- When: the `trig`.
- Thens: by conjunct, each `resp`, then its object's restrictions, then its `set`s (a positive set worded once);
  then each contrast's `does not`, after its requirement's Thens.
A later requirement's role is the first requirement's role of the same kind and rank; Givens and the When are the
first requirement's.

`Reader(logic, steps)` is the atom table: one atom (a clingo symbol: `attr`, `cond`, `rel`, `given`, `holds`, `over`,
`ran`, `ran_any`, `does`, `set_to`, over instances `o(K,V)`) as a Steps tree, with the instances named by
their kind's letter and a counter in order of first mention. `logic` is spec_logic_vocab's Vocab, `steps`
features_vocab's Vocab. An instance first mentioned in a Given is introduced by `<attribute>_Given` ("a work-item w1
that is `drafted`") or `<kind>_Given` ("a result r1").
"""
import spec_steps_facts as sf

LETTERS = {"initiative": "i", "work-item": "w", "capability-proposal": "p", "glossary-proposal": "p", "request": "q"}


class TraceError(Exception):
    """A group with no scenario: an atom with no step."""


class Reader:
    """One scenario read into steps: the instances' names, the Givens already introduced, and the step funs' types."""

    def __init__(self, logic, steps):
        self.logic, self.steps, self.names, self.counts, self.known = logic, steps, {}, {}, set()

    # --- terms ----------------------------------------------------------------------------------------------
    def name(self, sym):
        if sym not in self.names:
            term = self.logic.kinds.get(sym.arguments[0].name, "x")
            letter = LETTERS.get(term, term[0].lower())
            self.counts[letter] = self.counts.get(letter, 0) + 1
            self.names[sym] = "%s%d" % (letter, self.counts[letter])
        return self.names[sym]

    def mention(self, sym):
        """Name every instance of a term in order (its arguments' preorder)."""
        if is_instance(sym):
            self.name(sym)
        for arg in sym.arguments if name_of(sym) else ():
            self.mention(arg)

    def args(self, fun):
        return str(self.steps.gram.functionType(fun)).split(" -> ")[:-1]

    def typed(self, sym, cat):
        """An instance (or a named code) as the typed noun phrase `cat` (`k_initiative_NP`)."""
        kid = cat[:-3]
        if is_instance(sym):
            own = sym.arguments[0].name
            return (own if own + "_NP" == cat else kid) + "_Inst", ("NameLit", self.name(sym))
        if text_of(sym) is not None:
            return kid + "_Inst", ("NameLit", text_of(sym))
        raise TraceError("no noun phrase of %s for %s" % (kid, sym))

    def np(self, sym, cat="NP"):
        if cat != "NP":
            return self.typed(sym, cat)
        if is_instance(sym):
            kid = sym.arguments[0].name
            return kid + "_toNP", self.typed(sym, kid + "_NP")
        text = text_of(sym)
        if text is not None:
            return ("CodeNP", ("CodeLit", text)) if text.startswith("`") else ("QuotedNP", ("QuotedLit", '"%s"' % text))
        if name_of(sym) == "number" and len(sym.arguments) == 1:
            return sym.arguments[0].name + "_NumberOf", (sym.arguments[0].name,)
        if name_of(sym) == "value" and len(sym.arguments) == 2:
            fun = sym.arguments[0].name + "_Of"
            return fun, self.np(sym.arguments[1], self.args(fun)[0])
        if (name_of(sym) or "").startswith("n_") and not sym.arguments:
            return (sym.name,)
        raise TraceError("no noun phrase for %s" % sym)

    def subj(self, sym):
        if name_of(sym) in self.logic.actors and not sym.arguments:
            return "ActorSubj", (sym.name,)
        return "NPSubj", self.np(sym)

    def cmd(self, sym):
        text = text_of(sym)
        return ("CmdCode", ("CodeLit", text)) if text is not None else ("CmdActor", (sym.name,))

    def build(self, fun, *syms):
        """The atom fun applied to its terms, each fitted to the type the fun asks for."""
        return (fun,) + tuple(self.np(s, c) if not isinstance(s, tuple) else s for s, c in zip(syms, self.args(fun)))

    # --- atoms ----------------------------------------------------------------------------------------------
    def atom(self, sym, positive=True):
        """The Atom tree of a fluent (`attr`, `cond`, `rel`, `holds`, `over`), positive or negated."""
        a = sym.arguments
        if sym.name == "attr":
            return self.build(a[1].name + ("_Is" if positive else "_IsNot"), a[0], (a[2].name,))
        if sym.name == "cond":
            return self.build(a[0].name + ("_Is" if positive else "_IsNot"), a[1])
        if sym.name == "rel":
            return self.build(self.relation(a[0].name, a[1], a[2]) + ("_Atom" if positive else "_AtomNot"), a[1], a[2])
        if sym.name == "holds" and positive and is_instance(a[0]):
            exclusive = "exclusive" in getattr(self.logic.resources.get(a[1].name), "resource", "")
            return "Holds" if exclusive else "HoldsA", self.np(a[0]), (a[1].name,)
        if sym.name == "over" and not positive:
            return "IsFree", (a[0].name,)
        raise TraceError("no step for %s%s" % ("" if positive else "not ", sym))

    def relation(self, rid, x, y):
        k1, k2 = (s.arguments[0].name[2:] if is_instance(s) else None for s in (x, y))
        funs = sorted(f for f, r in self.logic.rels.items() if r == rid)
        exact = [f for f in funs if f.startswith("rel_%s_" % k1) and f.endswith("_%s" % k2)]
        if not (exact or funs):
            raise TraceError("no relation %s" % rid)
        return (exact or funs)[0]

    def given(self, sym, positive):
        """The Given steps of one state-0 atom; a thing it mentions first is introduced."""
        a = sym.arguments
        fresh = [s for s in things(sym) if s not in self.known]
        self.known.update(fresh)
        if positive and sym.name == "attr" and fresh and fresh[0] == a[0]:
            first = [(a[1].name + "_Given", ("NameLit", self.name(a[0])), (a[2].name,))]
            return first + [(s.arguments[0].name + "_Given", ("NameLit", self.name(s))) for s in fresh[1:]]
        if sym.name == "given":
            return [("SFeat", ("FeatGiven", ("CodeLit", text_of(a[0]))))]
        intro = [(s.arguments[0].name + "_Given", ("NameLit", self.name(s))) for s in fresh]
        return intro + [("SAtom", self.atom(sym, positive))]

    def when(self, sym):
        a = sym.arguments
        if sym.name == "ran":
            return "STrig", (("Runs", self.subj(a[0]), self.cmd(a[1])) if is_none(a[2]) else
                             ("RunsOn", self.subj(a[0]), self.cmd(a[1]), self.np(a[2])))
        if sym.name == "ran_any":
            return "STrig", ("IsRun", self.cmd(a[0]))
        if sym.name == "does":
            return "STrig", (("HappensI", self.subj(a[0]), (a[1].name,)) if is_none(a[2]) else
                             ("Happens", self.subj(a[0]), (a[1].name,), self.np(a[2])))
        if sym.name == "set_to":
            return "STrig", self.build(a[1].name + "_Becomes", a[0], (a[2].name,))
        raise TraceError("no When step for %s" % sym)

    def then(self, sym, positive=True):
        a = sym.arguments
        if sym.name != "does":
            return "SAtom", self.atom(sym, positive)
        s, event, x = self.subj(a[0]), a[1], a[2]
        if event.name == "set":
            return "SAtom", self.build(event.arguments[0].name + ("_Is" if positive else "_IsNot"), x,
                                       (event.arguments[1].name,))
        if event.name == "for":
            q = "QuotedFor", ("QuotedLit", '"%s"' % text_of(event.arguments[1])), self.np(x)
            return ("SDoes" if positive else "SDoesNot"), s, (event.arguments[0].name,), q
        if event.name == "print":
            return ("SPrints" if positive else "SPrintsNot"), s, ("OneNP", self.np(x))
        if positive and event.name in ("exit_ok", "change_nothing"):
            return ("SExitsOk" if event.name == "exit_ok" else "SChangesNothing"), s
        if positive and event.name == "exit_error":
            return "SExitsErr", s, self.np(x)
        if positive and name_of(x) == "pair":
            return "SDoesTo", s, (event.name,), self.np(x.arguments[0]), self.np(x.arguments[1])
        if not is_none(x):
            return ("SDoes" if positive else "SDoesNot"), s, (event.name,), self.np(x)
        if name_of(event) and not event.arguments:
            return ("SDoesI" if positive else "SDoesINot"), s, (event.name,)
        raise TraceError("no Then step for %s%s" % ("" if positive else "not ", sym))


def name_of(sym):
    """The name of a function symbol (a constant included), or None for a string or a number."""
    import clingo
    return sym.name if sym.type == clingo.SymbolType.Function else None


def is_instance(sym):
    return name_of(sym) == "o" and len(sym.arguments) == 2


def text_of(sym):
    import clingo
    return sym.string if sym.type == clingo.SymbolType.String else None


def is_none(sym):
    return name_of(sym) == "none" and not sym.arguments


def things(sym):
    out = [sym] if is_instance(sym) else []
    for arg in sym.arguments if name_of(sym) else ():
        out += [x for x in things(arg) if x not in out]
    return out


def read(facts, logic, steps):
    """[(keyword, Steps tree)] of one group: `facts` holds the facts of each of its requirements, in order."""
    shared, pre, when, thens, extra = {}, [], [], [], []
    for n, req in enumerate(facts):
        syms = sf.own(logic, req)
        inst = sf.instances(syms, n, shared)
        groups, pending, late = {}, [], []
        for sym in syms:
            name, a = sym.name, sym.arguments
            if name in sf.PRE and n == 0:
                pre.append(sf.fluent(sf.subst(sym, inst)))
            elif name == "trig" and n == 0:
                when.append(sf.trigger(sf.subst(sym, inst)))
            elif name in sf.OBJ:
                pending.append(sf.fluent(sf.subst(sym, inst)))
            elif name in ("resp", "set", "only"):
                resps, objs, sets = groups.setdefault(a[1].number, ([], [], []))
                if name == "set":
                    sets.append(sf.fluent(sf.subst(sym, inst)))
                    continue
                if name == "resp" and not (a[2].name == "pos" and name_of(a[3]) == "set"):
                    resps.append(sf.response(sf.subst(sym, inst)))
                # the restrictions of what a response does not do pick it out; they hold of nothing it makes
                objs.extend(pending if name == "resp" and a[2].name == "pos" else [])
                pending = []
            elif name == "every":
                found = sf.contrast(logic, syms, a[1].name, inst, n)
                if found:
                    extra.append(found[1])
                    late += [sf.response(sf.subst(s, inst), found[0]) for s in syms if s.name == "resp"
                             and s.arguments[2].name == "pos" and s.arguments[5] == a[1]]
        thens += [t for i in sorted(groups) for part in groups[i] for t in part] + late
    r, out = Reader(logic, steps), []
    pre.sort(key=lambda p: p[1].name != "given")
    for positive, sym in pre + extra:
        out += [("given", t) for t in r.given(sym, positive) if ("given", t) not in out]
    out += [("when", r.when(t)) for t in when]
    return out + list(dict.fromkeys(("then", r.then(sym, positive)) for positive, sym in thens))
