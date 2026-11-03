"""Requirement trees as telingo `&tel` formulas (design-r2 §5): one translation per fun, the only reading of a
requirement's meaning in the plugin.

`translate(vocab, ident, tree)` gives a statement's constraints, one for each response conjunct, guarded by
`on(<id>)`: `When T, S shall R` is `:- on(id), B, &tel{ T & ~ > (R) }` (the response at the next state), a statement
with no trigger is `&tel{ C & ~ R }` in the same state, `shall not` drops the `~`. Beside them it gives a choice of
each trigger and response pattern, the labels of its responses (`lab(Id, resp(i)|mod(i,j)|no(i), Atom)`, fired
by the statement) and its signature facts (`trig/4`, `eff/4`, `uses/2`, `untriggered/1`, read by `grammar/cone.lp`).
`witness(vocab, gid, tree, sid)` makes a group's features, condition and trigger hold at state 0 for bound instances
(`bind/3`), labels them (`feat(i)`, `cond(i)`, `trig`, and `mod(0,j)` for the trigger's and the subject's
restrictions), and asks for a contrast of each `every … that …` response object. `definition(vocab, tree)` is a
condition's rule from its `Def` sentence. `program(parts)` puts `grammar/background.lp` first.
"""
import re
from collections import Counter, namedtuple
from pathlib import Path

import spec_logic_np as lnp
import spec_tree
from spec_logic_np import Scope, atom, conj, const, neg, tel
from spec_logic_vocab import AMOUNT, Vocab, facts, pools

BACKGROUND = Path(__file__).resolve().parent.parent / "grammar" / "background.lp"
MINIMAL = "% --- the minimal trace"
AUX = ("some(", "resp(", "obj(")
Rules = namedtuple("Rules", "always initial dynamic sigs pools l3")
__all__ = ["Rules", "Vocab", "definition", "facts", "pool_sizes", "program", "translate", "witness"]


class Translation(Scope):
    """The clause and verb-phrase funs (§5.3, §5.5) over the noun phrases of `Scope`."""

    def subject(self, t):
        return (t[1][0], []) if t[0] == "ActorSubj" else self.np(t[1])

    @staticmethod
    def command(t):
        return const(t[1][1]) if t[0] == "CmdCode" else t[1][0]

    def trigger(self, t):
        """(formulas, the trigger's atom, its signature (P, E, term), the atom its choice is of)."""
        fun = t[0]
        if fun in ("Runs", "RunsOn"):
            s, fs = self.subject(t[1])
            x, gs = self.np(t[3]) if fun == "RunsOn" else ("none", [])
            main = "ran(%s,%s,%s)" % (s, self.command(t[2]), x)
            return fs + gs + [atom(main)], main, ("ran", self.command(t[2]), x), main
        if fun == "IsRun":
            c = self.command(t[1])
            return [atom("ran_any(%s,none)" % c)], "ran_any(%s,none)" % c, ("ran", c, "none"), "ran(anyone,%s,none)" % c
        if fun in ("Happens", "HappensI"):
            s, fs = self.subject(t[1])
            x, gs = self.np(t[3]) if fun == "Happens" else ("none", [])
            main = "does(%s,%s,%s)" % (s, t[2][0], x)
            return fs + gs + [atom(main)], main, ("does(%s)" % self.who(s), t[2][0], x), main
        if fun == "Undergoes":
            x, gs = self.np(t[1])
            main = "done_to(%s,%s)" % (t[2][0], x)
            return gs + [atom(main)], main, ("does(anyone)", t[2][0], x), "does(anyone,%s,%s)" % (t[2][0], x)
        cat, base, part = self.v.decode(fun)
        if cat == "attribute" and part == "Becomes":
            x, gs = self.np(t[1])
            event = "set(%s,%s)" % (base, self.v.value(t[2]))
            main = "set_to(%s,%s,%s)" % (x, base, self.v.value(t[2]))
            return gs + [atom(main)], main, ("does(anyone)", event, x), "does(anyone,%s,%s)" % (event, x)
        raise ValueError("no translation of the trigger %s" % fun)

    def feature(self, t):
        if t[0] == "FeatGiven":
            self.facts.append("feature(%s)." % const(t[1][1]))
            return [[atom("given(%s)" % const(t[1][1]))]]
        return [self.atom_(t[1])]

    def clause(self, t):
        """The items of a condition, one for each atom of its `and` (an `or` is one item)."""
        if t[0] == "CondOne":
            return [self.atom_(t[1])]
        if t[0] == "CondAnd":
            return [self.atom_(t[1])] + self.clause(t[2])
        rest = self.clause(t[2])
        return [[("|", [conj(self.atom_(t[1])), conj([f for item in rest for f in item])])]]

    def atom_(self, t):
        fun = t[0]
        if fun in ("Holds", "HoldsA"):
            return self.arg(t[1], lambda x: [atom("holds(%s,%s)" % (x, t[2][0])), atom("active(%s)" % x)])
        if fun == "IsFree":
            return [neg(atom("over(%s)" % t[1][0]))]
        cat, base, part = self.v.decode(fun)
        if cat == "attribute":
            v = self.v.value(t[2])
            return self.arg(t[1], lambda x: [neg(atom("attr(%s,%s,%s)" % (x, base, v))) if part == "IsNot"
                                             else self.test(x, base, [v])])
        if cat == "condition":
            return self.arg(t[1], lambda x: [(neg if part == "IsNot" else lambda f: f)(
                atom("cond(%s,%s)" % (base, x)))])
        if cat == "relation":
            return self.arg(t[1], lambda x: self.arg(t[2], lambda y: [atom("rel(%s,%s,%s)" % (base, x, y))]))
        raise ValueError("no translation of the clause %s" % fun)

    def vp(self, t, s):
        """The conjuncts of one verb phrase (`print X and Y` is one for each member). An effect's signature names
        its doer (an actor, or the kind of the noun phrase), as a trigger's does: two never meet otherwise."""
        fun, d = t[0], "does(%s)" % self.who(s)
        if fun == "Do":
            return [self.objects([t[2]], lambda x: ["does(%s,%s,%s)" % (s, t[1][0], x)], (d, t[1][0]))]
        if fun == "DoTo":
            return [self.objects([t[2], t[3]], lambda x, y: ["does(%s,%s,pair(%s,%s))" % (s, t[1][0], x, y)],
                                 (d, t[1][0]))]
        if fun == "Print":
            return [self.objects([m], lambda x: ["does(%s,print,%s)" % (s, x)], (d, "print"))
                    for m in self.v.members(t[1])]
        if fun == "ExitErr":
            return [self.objects([t[1]], lambda x: ["does(%s,exit_error,%s)" % (s, x)], (d, "exit_error"))]
        if fun in ("ExitOk", "ChangeNothing"):
            event = "exit_ok" if fun == "ExitOk" else "change_nothing"
            return [lnp.plain(["does(%s,%s,none)" % (s, event)], eff=(d, event, "none"))]
        if fun in ("Hold", "HoldA"):
            return [lnp.plain(["holds(%s,%s)" % (s, t[1][0])], eff=("holds", t[1][0], self.who(s)))]
        if fun == "HoldAtMost":
            n = t[1][1] if t[1][0] == "CountNum" else AMOUNT
            return [lnp.plain([], count="#count{ Y : holds(Y,%s), active(Y) } > %s" % (t[2][0], n))]
        cat, base, part = self.v.decode(fun)
        if cat == "attribute" and part == "Set":
            x, fs = self.np(t[1])
            v = self.v.value(t[2])
            return [lnp.plain(["does(%s,set(%s,%s),%s)" % (s, base, v, x)], fs, [(base, v, x)],
                           (d, "set(%s,%s)" % (base, v), x))]
        raise ValueError("no translation of the verb phrase %s" % fun)


def _choice(text, kinds):
    """`{ atom : kind(V1,K1), … }.` with the atom's lnp.variables renamed in order, so equal patterns are one rule."""
    order = sorted(lnp.variables(text), key=lambda x: re.search(r"\b%s\b" % x, text).start())
    out = re.sub(r"\b[XC]\d+\b", lambda m: "V%d" % (order.index(m.group()) + 1), text)
    bound = ["kind(V%d,%s)" % (i, kinds[x]) if kinds[x] else "thing(V%d)" % i for i, x in enumerate(order, 1)]
    return "{ %s%s }." % (out, " : " + ", ".join(bound) if bound else "")


def _read(s, tree):
    """(feature items, condition items, trigger or None, [(polarity, subject term, its restrictions, conjunct)])."""
    p = spec_tree.parts(tree)
    feat = s.feature(p["feat"]) if p["feat"] else []
    cond = s.clause(p["cond"]) if p["cond"] else []
    trig = s.trigger(p["trig"]) if p["trig"] else None
    out = []
    for polarity, subj, vp in p["resp"]:
        term, smods = s.subject(subj)
        out += [(polarity, term, smods, c) for c in s.vp(vp, term)]
    return feat, cond, trig, out


def _flat(items):
    return [f for item in items for f in item]


def translate(vocab, ident, tree):
    """The Rules of one statement: its constraints, choices, response labels, signature and pool counts."""
    s = Translation(vocab, ident)
    feat, cond, trig, conjuncts = _read(s, tree)
    tf, lid = (trig[0] if trig else []), const(ident)
    always, sigs, l3 = ["#external on(%s)." % lid], [], []
    if trig:
        always.append(_choice(trig[3], s.kinds))
        sigs.append("trig(%s,%s,%s,%s)." % (lid, trig[2][0], trig[2][1], s.kind_of(trig[2][2])))
    else:
        sigs.append("untriggered(%s)." % lid)
    for i, (polarity, subj, smods, c) in enumerate(conjuncts, 1):
        positive = (polarity == "Shall") != c.negate
        pre = _flat(feat) + _flat(cond) + smods + c.pre
        used = ["used(%s)" % subj] if tree[0] == "Ubiq" and subj in s.kinds else []
        if c.count:
            always += [", ".join([":- on(%s)" % lid] + used + [c.count]) + "."] if positive else []
            continue
        if c.locals:
            head, shared = s.define("obj", [atom(h) for h in c.heads] + c.mods, c.locals, label=i)
            resp = atom("resp(%s,%d,%s)" % (lid, i, lnp.tup(shared)))
        else:
            head, resp = None, conj([atom(h) for h in c.heads])
        core = (">", resp) if trig else resp
        formula = conj(pre + tf + [neg(core) if positive else core])
        bound = s.binding(x for x in lnp.variables(tel(formula)) if x not in s.local)
        always.append(", ".join([":- on(%s)" % lid] + bound + used + ["&tel{ %s }" % tel(formula)]) + ".")
        always += [_choice(h, s.kinds) for h in c.heads]
        always += _labels(s, lid, i, c, positive, conj(pre + tf), bool(trig), used, head)
        if c.eff:
            sigs.append("eff(%s,%s,%s,%s)." % (lid, c.eff[0], c.eff[1], s.kind_of(c.eff[2])))
        for tid, v, x in c.sets:
            l3.append((tid, v, sorted({w for y, t2, vals in s.tests if y == x and t2 == tid for w in vals})))
    sigs += ["uses(%s,%s)." % (lid, k) for k in s.used_kinds()]
    return Rules(always + s.aux + s.facts, [], [], sigs, s.counts(), l3)


def _labels(s, lid, i, c, positive, fire, trig, used, head):
    """The label rules of one response conjunct, fired when the statement fires (at the next state for a trigger)."""
    firing = ["not &tel{ %s }" % tel(neg(("<", fire) if trig else fire))] if fire else []
    fvars = [x for x in lnp.variables(tel(fire)) if x not in s.local] if fire else []
    if head:
        if not positive:
            return []
        body = ", ".join([head] + s.binding(x for x in fvars if x not in lnp.variables(head)) + used + firing)
        out = ["lab(%s,resp(%d),%s) :- %s." % (lid, i, h, body) for h in c.heads]
        mods = [x for x in lnp.leaves(conj(c.mods)) if not x[1].startswith(AUX)]
        return out + ["lab(%s,mod(%d,%d),%s) :- %s." % (lid, i, j, a if pos else "neg(%s)" % a, body)
                      for j, (pos, a) in enumerate(mods, 1)]
    part = "resp" if positive else "no"
    sign = "" if positive else "not "
    return ["lab(%s,%s(%d),%s) :- %s." % (lid, part, i, h, ", ".join(
        s.binding(set(fvars) | set(lnp.variables(h))) + used + [sign + h] + firing)) for h in c.heads]


def witness(vocab, gid, tree, sid=None):
    """The Rules that make a group's clauses hold at state 0 for bound instances, with their labels and the contrast
    of each `every … that …` object; `sid` is the statement whose `no(i)` labels the contrasts give."""
    s = Translation(vocab, gid)
    feat, cond, trig, conjuncts = _read(s, tree)
    g = const(gid)
    extra = [f for _, _, smods, c in conjuncts for f in smods + c.pre]
    whole = conj(_flat(feat) + _flat(cond) + extra + (trig[0] if trig else []))
    subjects = [subj for _, subj, _, _ in conjuncts if subj in s.kinds] if not trig else []
    names = sorted(set((lnp.variables(tel(whole)) if whole else []) + subjects) - s.local, key=lnp.varkey)

    def binds(xs):
        return ["bind(%s,%s,%s)" % (g, const(x), x) for x in sorted(set(xs), key=lnp.varkey)]
    init = ["1 { bind(%s,%s,V) : kind(V,%s) } 1." % (g, const(x), s.kinds[x]) for x in names]
    init += [":- %s." % ", ".join(binds(names) + ["not &tel{ %s }" % tel(whole)])] if whole else []
    init += [":- %s, not used(%s)." % (binds([x])[0], x) for x in subjects]
    items = [("feat(%d)" % n, item) for n, item in enumerate(feat, 1)]
    items += [("cond(%d)" % n, item) for n, item in enumerate(cond, 1)]
    items += [("trig", [atom(trig[1])])] if trig else []
    mods = [x for f in (trig[0][:-1] if trig else []) + extra for x in lnp.leaves(f) if not x[1].startswith(AUX)]
    labelled = [(part, x) for part, item in items for x in lnp.leaves(conj(item)) if not x[1].startswith(AUX)]
    labelled += [("mod(0,%d)" % n, x) for n, x in enumerate(mods, 1)]
    for part, (pos, a) in labelled:
        init.append("lab(%s,%s,%s) :- %s." % (g, part, a if pos else "neg(%s)" % a,
                                             ", ".join(binds(lnp.variables(a)) + [a if pos else "not " + a])))
    dynamic, counts = [], s.counts()
    for i, (_, _, _, c) in enumerate(conjuncts, 1):
        if c.universal and c.universal[2]:
            counts[c.universal[1]] += 1
            out = _contrast(s, g, const(sid or gid), i, c, names, binds, bool(trig))
            init += out[0]
            dynamic += out[1]
    sigs = ["uses(%s,%s)." % (g, k) for k in s.used_kinds()]
    if trig:
        sigs.append("trig(%s,%s,%s,%s)." % (g, trig[2][0], trig[2][1], s.kind_of(trig[2][2])))
        s.aux.append(_choice(trig[3], s.kinds))
    return Rules(s.aux + s.facts, init, dynamic, sigs, counts, [])


def _contrast(s, g, lid, i, c, names, binds, trig):
    """(initial, dynamic) rules of one contrast: an instance of the object's kind that fails its restriction at state
    0, and the `no(i)` label of the response it is not given (design-r2 §5.7's `not(i)`; `not` is clingo's)."""
    y, kid, restriction = c.universal
    name = "C%d" % i
    fails = lnp.subst(conj(restriction), y, name)
    others = [x for x in lnp.variables(tel(fails)) if x != name]
    init = ["1 { bind(%s,%s,V) : kind(V,%s) } 1." % (g, const(name), kid),
            ":- bind(%s,%s,V), bind(%s,%s,V)." % (g, const(name), g, const(y)),
            ":- %s, &tel{ %s }." % (", ".join(binds([name] + [x for x in others if x in names])
                                             + s.binding(x for x in others if x not in names)), tel(fails)),
            "contrast(%s,%d,%s) :- bind(%s,%s,%s)." % (g, i, name, g, const(name), name)]
    prime = "'" if trig else ""
    labels = []
    for h in (lnp.subst(atom(h), y, name)[1] for h in c.heads):
        labels.append("lab(%s,no(%d),%s) :- %s." % (lid, i, h, ", ".join(
            ["%scontrast(%s,%d,%s)" % (prime, g, i, name)]
            + [prime + b for b in binds(x for x in lnp.variables(h) if x in names)] + ["not " + h])))
    return (init, labels) if trig else (init + labels, [])


def definition(vocab, tree):
    """The rule of a condition defined by its `Def` sentence: `cond(c,X0) :- kind(X0,K), <the sentence's body>.`"""
    cid, kid = vocab.def_funs[tree[0]]
    s = Translation(vocab, "def:" + cid, bound={kid: "X0"})
    out = []
    for body in lnp.asp(conj(_flat(s.clause(tree[1])))):
        names = [x for x in lnp.variables(" ".join(body)) if x not in s.local]
        out.append("cond(%s,X0) :- %s." % (cid, ", ".join(s.binding(["X0"] + names) + body)))
    return Rules(out + s.aux + s.facts, [], [], [], Counter(), [])


def program(parts, optimise=False):
    """The telingo program text: the background theory (its minimisation only when `optimise`), then each part."""
    background = BACKGROUND.read_text()
    text = [background if optimise else background.split(MINIMAL)[0]]
    for name in ("always", "initial", "dynamic"):
        rules = [r for p in parts for r in (getattr(p, name) if isinstance(p, Rules) else p.get(name, []))]
        if rules:
            text.append("#program %s.\n%s\n" % (name, "\n".join(dict.fromkeys(rules))))
    return "\n".join(text)


def pool_sizes(parts):
    """The pool of each kind for a program of these parts (spec_logic_vocab.pools): the most noun phrases of the kind
    in any one part, so a cone of many statements does not multiply its instances (spec_engine retries larger)."""
    return pools(Counter({k: max(p.pools[k] for p in parts if isinstance(p, Rules)) for k in
                          {k for p in parts if isinstance(p, Rules) for k in p.pools}}))
