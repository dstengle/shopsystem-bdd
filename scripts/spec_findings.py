"""The words of `model logic`'s findings (design-r3 §6): an atom `grammar/check.lp` shows, written with the lexicon's
terms from the facts of the requirements it names (`spec_context`). A split requirement's id (`s#r5#2`) is written
as its requirement's (`spec_lf_core.split`)."""
from collections import defaultdict

import clingo
import spec_grammar4
import spec_meaning
from spec_lf_core import split

QUIET = {"print": "print", "exit_ok": "exit successfully", "exit_error": "exit with an error",
         "change_nothing": "change nothing"}
BOUNDS = {"least": "at least", "most": "at most", "exactly": "exactly", "more": "more than", "fewer": "fewer than"}


def article(word):
    return ("an " if word[:1] in "aeiou" else "a ") + word


def local(ident, other):
    """`r12` when the two ids are of one capability, else the whole id."""
    cap, _, rest = ident.rpartition("#")
    return rest if cap and cap == other.rpartition("#")[0] else ident


class Words:
    """The texts of one context's findings."""

    def __init__(self, root, ctx):
        self.root, self.v = root, ctx.vocab
        self.trees = {s.id: s.tree for s in ctx.statements}
        self.facts = defaultdict(list)
        for facts in ctx.facts.values():
            for fact in facts:
                sym = clingo.parse_term(fact[:-1])
                self.facts[sym.arguments[0].string].append((sym.name, sym.arguments[1:]))

    def of(self, rid, name):
        return [args for n, args in self.facts[rid] if n == name]

    def term(self, rid, x):
        """A term of a requirement in words: a role as its kind, an actor, a code, a value."""
        if x.type == clingo.SymbolType.String:
            return x.string
        if x.type == clingo.SymbolType.Number:
            return str(x.number)
        for var, kind in self.of(rid, "role"):
            if var == x:
                return article(self.v.kinds.get(kind.name, kind.name))
        if x.name == "pair":
            return " ".join(self.term(rid, a) for a in x.arguments)
        if x.name == "value":
            return self.v.value_text.get(x.arguments[1].name, str(x))
        if x.name == "any":
            return "anyone"
        return self.v.actors.get(x.name, str(x))

    def attr(self, t):
        kid, entry = self.v.attrs[t.name]
        return entry.term, article(self.v.kinds[kid])

    def value(self, v):
        if v.type == clingo.SymbolType.String:     # a code no entry lists, of an attribute ordered by number (b240)
            return v.string
        return self.v.value_text.get(v.name, v.name)

    def does(self, rid, e, d, x):
        """`<doer> to <event> <object>`."""
        who = self.term(rid, d)
        if e.type == clingo.SymbolType.String:
            return "%s to %s" % (who, e.string)
        if e.name == "set":
            term, kind = self.attr(e.arguments[0])
            return "%s to set the %s of %s to %s" % (who, term, kind, self.value(e.arguments[1]))
        if e.name == "hold":
            return "%s to hold the %s" % (who, self.v.resources[e.arguments[0].name].term)
        if e.name == "for":
            return '%s to %s "%s" for %s' % (who, self.v.events.get(e.arguments[0].name, e.arguments[0].name),
                                            e.arguments[1].string, self.term(rid, x))
        if e.name in QUIET:
            return "%s to %s" % (who, QUIET[e.name])
        obj = "" if x.type == clingo.SymbolType.Function and x.name == "none" else " " + self.term(rid, x)
        return "%s to %s%s" % (who, self.v.events.get(e.name, e.name), obj)

    def trigger(self, base):
        """The trigger of a requirement's grammar 4 tree (`When`, `If`: its second argument), as grammar 4 writes it."""
        tree = self.trees.get(base)
        if tree is None:
            return None
        read = spec_meaning.read(tree)
        if read[0] not in ("When", "If"):
            return None
        text = spec_grammar4.linearise(self.root, spec_meaning.write(read[2]))
        return text[0].lower() + text[1:] if text[:1].isupper() else text

    def pre(self, a, b, atoms):
        """The merged pre-state of a witness: its `pre(A,B,Z,Attr,Val,Pol)` and `prec(A,B,Z,C,Pol)` atoms, one phrase
        an instance."""
        inst = {}
        for atom in atoms:
            sym = clingo.parse_term(atom)
            if sym.name not in ("pre", "prec"):
                continue
            z, val, pol = sym.arguments[2], sym.arguments[-2], sym.arguments[-1]
            rid, var = (b, z.arguments[0]) if z.type == clingo.SymbolType.Function and z.name == "b" else (a, z)
            vals = inst.setdefault(str(z), (self.term(rid, var), []))[1]
            word = self.value(val) if sym.name == "pre" else self.v.cond_terms.get(val.name, val.name)
            text = ("is ", ("" if pol.name == "pos" else "not ") + word)
            if sym.name == "pre" and str(val) == "absent":       # "has no T" (b240)
                text = ("has ", "no " + self.attr(sym.arguments[3])[0])
            if text not in vals:
                vals.append(text)
        return ", ".join("%s that %s" % (who, said(vals)) for _, (who, vals) in sorted(inst.items()))

    def clash(self, x, y, whys, pre):
        """`<x> and #<y> clash: on "<trigger>" with <pre-state>, <why>`: x, y in the order they are reported."""
        bx, by = split(x), split(y)
        parts = []
        on = self.trigger(bx) or self.trigger(by)
        if on:
            parts.append('on "%s"' % on)
        if pre:
            parts.append("with %s" % pre)
        why = " and ".join(dict.fromkeys(self.why(x, y, w) for w in whys))
        where = " ".join(parts)
        return "%s and %s clash: %s" % (bx, "#" + local(by, bx) if local(by, bx) != by else by,
                                        "%s, %s" % (where, why) if where else why)

    def maybe(self, conds, clash):
        """An L6: `<x> and #<y>: possible clash, depends on the prose condition C; define it in the controlled
        language to decide: <the clash's text after "clash: ">`."""
        names = " and ".join(self.v.cond_terms.get(c.name, c.name) for c in conds)
        ids, _, rest = clash.partition(" clash: ")
        return "%s: possible clash, depends on the prose condition %s; define it in the controlled language to " \
               "decide: %s" % (ids, names, rest)

    def why(self, x, y, kind):
        lx, ly = local(split(x), split(y)), local(split(y), split(x))
        rx, ry = self.of(x, "resp"), self.of(y, "resp")
        if kind in ("pos_neg", "neg_pos"):
            for _, p, e, d, o in rx:
                if any(e == e2 and p != q for _, q, e2, _, _ in ry):
                    verbs = ("obliges", "forbids") if p.name == "pos" else ("forbids", "obliges")
                    return "%s %s and %s %s %s" % (lx, verbs[0], ly, verbs[1], self.does(x, e, d, o))
        if kind == "set":
            for _, _, t, v in self.of(x, "set"):
                for _, _, t2, w in self.of(y, "set"):
                    if t == t2 and v != w:
                        term, of = self.attr(t)
                        return "%s sets the %s of %s to %s and %s to %s" % (lx, term, of, self.value(v), ly,
                                                                            self.value(w))
        if kind == "exit":
            ok = any(r[2].name == "exit_ok" for r in rx if r[1].name == "pos")
            return ("%s exits successfully and %s with an error" if ok else
                    "%s exits with an error and %s successfully") % (lx, ly)
        if kind == "change":
            quiet = any(r[2].name == "change_nothing" for r in rx if r[1].name == "pos")
            rid, other = (y, ry) if quiet else (x, rx)
            what = next(self.does(rid, e, d, o) for _, p, e, d, o in other
                        if p.name == "pos" and e.name not in QUIET)
            return ("%s changes nothing and %s obliges %s" % (lx, ly, what) if quiet else
                    "%s obliges %s and %s changes nothing" % (lx, what, ly))
        if kind == "use":
            uses = self.of(x, "uses")
            d, o = (uses or self.of(x, "nouse"))[0]
            verbs = ("obliges", "forbids") if uses else ("forbids", "obliges")
            return "%s %s and %s %s %s to use %s" % (lx, verbs[0], ly, verbs[1], self.term(x, d), self.term(x, o))
        if kind == "only":
            rid, other, lo, lt = (x, y, lx, ly) if self.of(x, "only") else (y, x, ly, lx)
            _, e, d, o = self.of(rid, "only")[0]
            return "%s allows %s only within its restriction and %s obliges one outside it" % (
                lo, self.does(rid, e, d, o), lt)
        if kind == "count":
            for _, e, d, o, b, n in self.of(x, "count"):
                for _, e2, _, _, b2, n2 in self.of(y, "count"):
                    if e == e2:
                        act, obj = self.does(x, e, d, o), self.term(x, o)
                        act += "" if act.endswith(obj) else " " + obj
                        return "%s counts %s %s and %s %s %s (%s): no number meets both" % (
                            lx, BOUNDS[b.name], n, ly, BOUNDS[b2.name], n2, act)
        return "%s and %s demand opposite things" % (lx, ly)

    def bad_set(self, base, t, frm, to):
        term, kind = self.attr(t)
        start = "" if frm.name == "none" else " from %s" % self.value(frm)
        return "%s sets the %s of %s%s to %s, which no transition allows" % (base, term, kind, start, self.value(to))

    def unreachable(self, base, t, v):
        term, kind = self.attr(t)
        return "%s needs %s whose %s is %s, which no transition path reaches" % (base, kind, term, self.value(v))

    def forbid(self, a, b):
        """L7: the "shall not" of one side forbids what the "may" of the other permits."""
        may, nay = (a, b) if any(p.name == "may" for _, p, *_ in self.of(a, "resp")) else (b, a)
        _, _, e, d, o = next(r for r in self.of(may, "resp") if r[1].name == "may")
        return "%s forbids what %s permits: %s" % (split(nay), split(may),
                                                   self.does(may, e, d, o).replace(" to ", " may ", 1))

    def lint(self, raw, e, reactors):
        base = split(raw)
        d, o = next((d, o) for _, p, e2, d, o in self.of(raw, "resp") if e2 == e and p.name == "pos")
        text = "%s obliges %s in every state" % (base, self.does(raw, e, d, o))
        if reactors:
            text += "; %s %s to it" % (", ".join(reactors), "reacts" if len(reactors) == 1 else "react")
        return text


def said(vals):
    """[(verb, what)] as one predicate: "is `a` and not `b`", "has no status and is `a`" (a verb said once in a row)."""
    return " and ".join(("" if n and vals[n - 1][0] == verb else verb) + what for n, (verb, what) in enumerate(vals))
