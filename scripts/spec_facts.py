"""Requirement trees as ground facts (design-r3 §3): one translation per fun, the only reading of a requirement's
meaning in the plugin. `model logic` reads the facts with `grammar/check.lp`, `features generate` reads them into
steps.

`translate(vocab, ident, tree)` walks the tree once and gives its facts in a fixed order: `form`, then the feature,
the condition, the trigger and each response conjunct `I` in spoken order, each with the roles it first mentions.

- the pre-state: `feat(R,F)`, `cond(R,V,A,Val,Pol)`, `ccond(R,V,C,Pol)`, `crel(R,Rel,V,W,Pol)` (Rel a relation's
  id, or a verb's for "a session does not write a file"), `holds(R,V,Res)`,
  `free(R,Res)`, `none`, `cnone`, `rnone` for a noun phrase under `no`, `uall` and its kin for one under `every`,
  `the(R,V)` for a definite with no antecedent (spec_facts_np);
- the trigger: `trig(R,P,E,D,V)`, P one of `does`, `ran`, `becomes`; D an actor, a role or `any`;
- each response: `resp(R,I,Pol,E,D,V)`, E `for(E0,Q)` and V the role X for `E0 "q" for X`; a positive `Set`
  also `set(R,I,V,A,Val)`; the object's restrictions `oattr`, `orel` (`onot`, `ocond`); `every(R,V)` for an
  `every` object or subject; `only(R,I,K)` for `only a K` (no `resp`); `count(R,Res,N)` for `hold at most`;
  `uses(R,D,X)` and `nouse(R,D,X)` for a ubiquitous `use`.

A choice (a condition's `or`, a value list `whose A is v1 or v2`) splits the requirement: one walk for each way
through, ids `R#1`, `R#2`, … with `disj(R#k,R)` naming the requirement each comes from (`split`). A fun with no
translation raises `ValueError` naming it; no partial facts are given.
"""
import spec_tree
from spec_facts_np import Scope, const, unwrap

FORMS = {"Ubiq": "ubiq", "When": "when", "While": "while", "Where": "where", "IfThen": "if",
         "WhileWhen": "while_when", "WhereWhen": "where_when", "WhereWhile": "where_while", "WhileIf": "while_if",
         "WhereIf": "where_if"}
__all__ = ["def_facts", "define", "split", "translate"]


class Walk(Scope):
    """The clause, trigger and verb-phrase funs over the noun phrases of `Scope`."""

    def run(self, tree):
        if tree[0] not in FORMS:
            raise ValueError("no translation of the requirement %s" % tree[0])
        self.emit("form", FORMS[tree[0]])
        p = spec_tree.parts(tree)
        if p["feat"]:
            self.feature(p["feat"])
        if p["cond"]:
            self.clause(p["cond"])
        if p["trig"]:
            self.trigger(p["trig"])
        i = 0
        for polarity, subj, vp in p["resp"]:
            d = self.subject(subj, every=True)
            i = self.vp(vp, i, polarity == "Shall", d, tree[0] == "Ubiq")
        return self.out

    def subject(self, t, every=False):
        if t[0] == "ActorSubj":
            return t[1][0]
        if t[0] != "NPSubj":
            raise ValueError("no translation of the subject %s" % t[0])
        u = unwrap(t[1])
        cat, base, part = self.v.decode(u[0])
        if every and cat == "kind" and part in ("Every", "Pl"):
            return self.universal(u, base)
        return self.np(t[1])

    def universal(self, u, base):
        x = self.fresh(base)
        self.bound[base] = x
        self.emit("every", x)
        self.cn(u[1], x, False)
        return x

    @staticmethod
    def command(t):
        if t[0] == "CmdCode":
            return const(t[1][1])
        if t[0] == "CmdActor":
            return t[1][0]
        raise ValueError("no translation of the command %s" % t[0])

    def trigger(self, t):
        fun = t[0]
        if fun in ("Runs", "RunsOn"):
            d = self.subject(t[1])
            cmd = self.command(t[2])
            self.emit("trig", "ran", cmd, d, self.np(t[3]) if fun == "RunsOn" else "none")
        elif fun == "IsRun":
            self.emit("trig", "ran", self.command(t[1]), "any", "none")
        elif fun in ("Happens", "HappensI"):
            d = self.subject(t[1])
            self.emit("trig", "does", t[2][0], d, self.np(t[3]) if fun == "Happens" else "none")
        else:
            cat, base, part = self.decode(fun, "trigger")
            if cat != "attribute" or part != "Becomes":
                raise ValueError("no translation of the trigger %s" % fun)
            x = self.np(t[1])
            self.emit("trig", "becomes", "set(%s,%s)" % (base, self.v.value(t[2])), "any", x)

    def feature(self, t):
        if t[0] == "FeatGiven":
            self.emit("feat", const(t[1][1]))
        elif t[0] == "FeatAtom":
            self.atom(t[1])
        else:
            raise ValueError("no translation of the feature %s" % t[0])

    def clause(self, t, obj=False):
        fun = t[0]
        if fun == "CondOne":
            self.atom(t[1], obj)
        elif fun == "CondAnd":
            self.atom(t[1], obj)
            self.clause(t[2], obj)
        elif fun == "CondOr":
            if self.pick(2) == 0:
                self.atom(t[1], obj)
            else:
                self.clause(t[2], obj)
        else:
            raise ValueError("no translation of the condition %s" % fun)

    def atom(self, t, obj=False):
        fun = t[0]
        if fun in ("Holds", "HoldsA"):
            x, kid = self.arg(t[1], obj)
            if kid:
                raise ValueError("no translation of %s under %s" % (t[1][0], fun))
            self.emit("holds", x, t[2][0])
            return
        if fun == "IsFree":
            self.emit("free", t[1][0])
            return
        if fun in ("Does", "DoesNot"):     # a verb between two kinds: a relation named by its verb (b85)
            self.rel(t[2][0], self.subject(t[1]), self.np(t[3], obj), obj, fun == "Does")
            return
        cat, base, part = self.decode(fun, "clause")
        if cat in ("attribute", "condition") and part in ("Is", "IsNot") and self.universal_atom(t, cat, base, part,
                                                                                               obj):
            return
        if cat == "attribute" and part in ("Is", "IsNot"):
            x, kid = self.arg(t[1], obj)
            if kid and part == "Is":
                self.emit("none", kid, base, self.v.value(t[2]))
            elif kid:
                raise ValueError("no translation of %s under %s" % (t[1][0], fun))
            else:
                self.attr(x, base, self.v.value(t[2]), part == "Is", obj)
        elif cat == "condition" and part in ("Is", "IsNot"):
            x, kid = self.arg(t[1], obj)
            if kid and part == "Is":
                self.emit("cnone", kid, base)
            elif kid:
                raise ValueError("no translation of %s under %s" % (t[1][0], fun))
            else:
                self.ccond(x, base, part == "Is", obj)
        elif cat == "relation" and part in ("Atom", "AtomNot"):
            (x, kx), (y, ky) = self.arg(t[1], obj), self.arg(t[2], obj)
            if (kx or ky) and part == "Atom":
                self.emit("rnone", base, x or "kind(%s)" % kx, y or "kind(%s)" % ky)
            elif kx or ky:
                raise ValueError("no translation of `no` under %s" % fun)
            else:
                self.rel(base, x, y, obj, part == "Atom")
        else:
            raise ValueError("no translation of the clause %s" % fun)

    # --- responses ---------------------------------------------------------------------------------------------
    def vp(self, t, i, shall, d, ubiq):
        """Emit one verb phrase's conjuncts after the i-th; the number of the last."""
        fun = t[0]
        if fun == "Print":
            for m in self.v.members(t[1]):
                i += 1
                self.respond(i, shall, "print", d, [m])
            return i
        i += 1
        if fun == "Do" and ubiq and self.v.events.get(t[1][0]) == "use":
            self.emit("uses" if shall else "nouse", d, self.np(t[2]))
        elif fun == "Do" and unwrap(t[2])[0] == "QuotedFor":
            q = unwrap(t[2])
            terms, negate, _ = self.objects([q[2]])
            event = "for(%s,%s)" % (t[1][0], const(q[1][1][1:-1]))
            self.emit("resp", i, "pos" if shall != negate else "neg", event, d, terms[0])
        elif fun == "Do":
            self.respond(i, shall, t[1][0], d, [t[2]])
        elif fun == "DoTo":
            self.respond(i, shall, t[1][0], d, [t[2], t[3]])
        elif fun == "DoI":
            self.emit("resp", i, "pos" if shall else "neg", t[1][0], d, "none")
        elif fun == "ExitErr":
            self.respond(i, shall, "exit_error", d, [t[1]])
        elif fun in ("ExitOk", "ChangeNothing"):
            self.emit("resp", i, "pos" if shall else "neg", "exit_ok" if fun == "ExitOk" else "change_nothing", d,
                      "none")
        elif fun in ("Hold", "HoldA"):
            self.emit("resp", i, "pos" if shall else "neg", "hold(%s)" % t[1][0], d, "none")
        elif fun == "HoldAtMost":
            n = t[1][1] if t[1][0] == "CountNum" else const(t[1][1][1])
            self.emit("count", t[2][0], n)
        else:
            cat, base, part = self.decode(fun, "verb phrase")
            if cat != "attribute" or part != "Set":
                raise ValueError("no translation of the verb phrase %s" % fun)
            x, val = self.np(t[1]), self.v.value(t[2])
            if shall:
                self.emit("set", i, x, base, val)
            self.emit("resp", i, "pos" if shall else "neg", "set(%s,%s)" % (base, val), d, x)
        return i

    def respond(self, i, shall, event, d, nps):
        terms, negate, only = self.objects(nps)
        if only:
            self.emit("only", i, only)
            return
        pos = shall != negate
        obj = terms[0] if len(terms) == 1 else "pair(%s,%s)" % tuple(terms)
        self.emit("resp", i, "pos" if pos else "neg", event, d, obj)

    def objects(self, nps):
        """(terms, negated by `no`, the kind of `only a K`) of a response's objects: `a`/`no` X is an object with its
        own restrictions, `every` X a universal role, any other the term it names."""
        terms, negate, only = [], False, None
        for t in nps:
            u = unwrap(t)
            cat, base, part = self.v.decode(u[0])
            if cat == "kind" and part in ("Every", "Pl"):
                terms.append(self.universal(u, base))
            elif cat == "kind" and (part in ("An", "One", "AtMostOne", "No") or (
                    part in ("The", "It", "Its") and base not in self.bound)):
                saved = dict(self.bound)
                y = self.fresh(base)
                if part in ("The", "Its"):
                    self.emit("the", y)
                if part != "It":
                    self.cn(u[1], y, True)
                self.bound = saved
                if part != "No":
                    self.bound[base] = y          # a later "the K" is this object (S10)
                negate = negate or part == "No"
                only = base if t[0] == "Only" and part in ("An", "One") else only
                terms.append(y)
            else:
                terms.append(self.np(t))
        return terms, negate, only


def _next(taken, options):
    """The choices of the next walk after one that took `taken`, or None after the last."""
    for j in range(len(taken) - 1, -1, -1):
        if taken[j] + 1 < options[j]:
            return taken[:j] + [taken[j] + 1]
    return None


def translate(vocab, ident, tree):
    """The facts of one requirement (of each of its splits, in order)."""
    first = Walk(vocab, ident)
    out = first.run(tree)
    if not first.options:
        return out
    out, seq, k = [], [], 0
    while seq is not None:
        k += 1
        sid = "%s#%d" % (ident, k)
        w = Walk(vocab, sid, seq)
        out += ["disj(%s,%s)." % (const(sid), const(ident))] + w.run(tree)
        seq = _next(w.taken, w.options)
    return out


def split(ident):
    """The requirement a split comes from: `s#r5#2` -> `s#r5`; any other id as it is."""
    head, sep, tail = ident.rpartition("#")
    return head if sep and tail.isdigit() else ident


def def_facts(vocab):
    """The domain facts of the defined conditions for `grammar/check.lp`: `prose(C)` for a condition with no `Def`;
    for a `Def` whose every way through is attribute literals on its own subject, `dalt(C,N)` for its N-th way and
    `dlit(C,N,Attr,Val,Pol)` for each literal (a `Def` with any other fact is neither: it is followed where positive)."""
    out = ["prose(%s)." % c for c in sorted(vocab.conds) if c not in vocab.def_lits]
    for cid, (kid, clause) in sorted(vocab.def_lits.items()):
        ways, seq = [], []
        while seq is not None:
            w = Walk(vocab, "d", seq)
            w.bound, w.expanding = {kid: "s"}, {cid}
            w.clause(clause)
            ways.append(w.out)
            seq = _next(w.taken, w.options)
        if all(f.startswith('cond("d",s,') for way in ways for f in way):
            for n, way in enumerate(ways, 1):
                out.append("dalt(%s,%d)." % (cid, n))
                out += ["dlit(%s,%d,%s" % (cid, n, f[len('cond("d",s,'):]) for f in way]
    return out


def define(vocab, tree):
    """Record a condition's `Def` tree: its clause, followed on the role of a positive mention (spec_facts_np)."""
    cid, kid = vocab.def_funs[tree[0]]
    vocab.def_lits[cid] = (kid, tree[1])
    vocab.define(cid)
