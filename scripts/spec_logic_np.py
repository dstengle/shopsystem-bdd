"""The noun-phrase half of the translation (design-r2 §5.4) and the formulas both halves build.

A formula is a nested tuple: `("a", text)` an atom, `("~", f)`, `(">", f)` (strong next), `("&", [f...])` and
`("|", [f...])`. `tel` writes one as the body of a `&tel{}` atom, `asp` as plain ASP bodies (one for each
disjunct; for a definition and an auxiliary atom, which are not temporal), and `leaves` gives its atoms with their
polarity (for the labels of §5.7).

`Scope` holds one statement's (or witness's, or definition's) variables: a noun phrase of a kind is a variable
`X<n>` bound by `kind(X,K)`, an anaphor (`the`, `it`, `its`) the variable bound before for its kind, a name its
constant. A noun phrase under `no` becomes an auxiliary atom `some(Id,N,t(shared))` ("there is one"), negated.
"""
import itertools
import re
from collections import Counter, namedtuple

VAR = re.compile(r"\b[XC]\d+\b")
# one response conjunct: its atoms, the restrictions of its existential objects (`locals`), its conditions, the
# `every` object (variable, kind, restrictions), `no` (negated), an aggregate, its `Set`s and its effect signature
Conjunct = namedtuple("Conjunct", "heads mods locals pre universal negate count sets eff")


def plain(heads, pre=(), sets=(), eff=None, count=None):
    return Conjunct(list(heads), [], [], list(pre), None, False, count, list(sets), eff)


def const(text):
    return '"%s"' % str(text).replace("\\", "\\\\").replace('"', '\\"')


def atom(text):
    return ("a", text)


def neg(f):
    return ("~", f)


def conj(fs):
    fs = [f for f in fs if f]
    if not fs:
        return None
    return fs[0] if len(fs) == 1 else ("&", fs)


def tup(names):
    return "t(%s)" % ",".join(names) if names else "t"


def tel(f):
    """The formula as telingo writes it inside `&tel{ }`."""
    op = f[0]
    if op == "a":
        return f[1]
    if op in (">", "<"):
        return "%s (%s)" % (op, tel(f[1]))
    if op == "~":
        inner = tel(f[1])
        return "~ " + (inner if f[1][0] in ("a", ">", "<", "~") else "(%s)" % inner)
    sep = " & " if op == "&" else " | "
    return sep.join(tel(x) if x[0] in ("a", ">", "<", "~") else "(%s)" % tel(x) for x in f[1])


def asp(f):
    """The formula as plain ASP bodies, one list of literals for each disjunct. A negation is of an atom only."""
    op = f[0]
    if op == "a":
        return [[f[1]]]
    if op == "~":
        if f[1][0] != "a":
            raise ValueError("a negation in a rule body is of an atom: %s" % tel(f))
        return [["not " + f[1][1]]]
    if op == "&":
        return [[lit for part in combo for lit in part] for combo in itertools.product(*(asp(x) for x in f[1]))]
    if op == "|":
        return [body for x in f[1] for body in asp(x)]
    raise ValueError("no next in a rule body: %s" % tel(f))


def leaves(f):
    """(positive, atom text) of each atom of the formula, in order."""
    if f is None:
        return []
    op = f[0]
    if op == "a":
        return [(True, f[1])]
    if op == "~" and f[1][0] == "a":
        return [(False, f[1][1])]
    if op in ("~", ">", "<"):
        return leaves(f[1])
    return [x for g in f[1] for x in leaves(g)]


def subst(f, old, new):
    """The formula with the variable `old` renamed `new`."""
    pattern = re.compile(r"\b%s\b" % old)
    if f[0] == "a":
        return ("a", pattern.sub(new, f[1]))
    if f[0] in ("&", "|"):
        return (f[0], [subst(g, old, new) for g in f[1]])
    return (f[0], subst(f[1], old, new))


def varkey(name):
    return (name[0], int(name[1:]))


def variables(text):
    return sorted(set(VAR.findall(text)), key=varkey)


class Scope:
    """The variables, auxiliary rules and facts of one translation; `ident` names its auxiliary atoms."""

    def __init__(self, vocab, ident, bound=None):
        self.v, self.ident = vocab, ident
        self.n, self.naux, self.bound, self.kinds = 0, 0, dict(bound or {}), {}
        for kid, var in self.bound.items():
            self.kinds[var] = kid
        self.local, self.aux, self.facts, self.tests, self.named = set(), [], [], [], {}

    def fresh(self, kid):
        self.n += 1
        name = "X%d" % self.n
        self.kinds[name] = kid
        return name

    def created_since(self, mark):
        return ["X%d" % i for i in range(mark + 1, self.n + 1)]

    def used_kinds(self):
        """The kinds the translation's noun phrases bind, named ones included."""
        return sorted({k for k in self.kinds.values() if k} | set(self.named.values()))

    def counts(self):
        """The number of noun phrases of each kind (a pool's size less one)."""
        return Counter(k for k in self.kinds.values() if k)

    def who(self, term):
        """The doer of an event in a signature: the actor, or the kind of the noun phrase."""
        return term if term in self.v.actors else self.kind_of(term)

    def kind_of(self, term):
        """The kind id of a term of the translation, or `none`."""
        return self.kinds.get(term) or self.named.get(term) or "none"

    def binding(self, names):
        return ["kind(%s,%s)" % (x, self.kinds[x]) if self.kinds[x] else "thing(%s)" % x
                for x in sorted(set(names), key=varkey)]

    def define(self, name, formulas, locals_, label=None):
        """An auxiliary atom `<name>(Id,N,t(shared)[,t(locals)])` defined by the formulas (as ASP bodies); the
        variables of `locals_` are its own, the others are shared with the statement."""
        self.naux += 1
        bodies = asp(conj(formulas))
        shared = [x for x in variables(" ".join(" ".join(b) for b in bodies)) if x not in locals_]
        args = [const(self.ident), str(label or self.naux), tup(shared)] + ([tup(locals_)] if name == "obj" else [])
        head = "%s(%s)" % (name, ",".join(args))
        for body in bodies:
            self.aux.append("%s :- %s." % (head, ", ".join(self.binding(list(locals_) + shared) + body)))
        self.local.update(locals_)
        return head, shared

    # --- noun phrases ------------------------------------------------------------------------------------------
    @staticmethod
    def unwrap(t):
        while t[0] == "Only" or t[0].endswith("_toNP"):
            t = t[1]
        return t

    def np(self, t):
        """(term, formulas) of a noun phrase: its term, and the restrictions it puts on it."""
        t = self.unwrap(t)
        fun = t[0]
        if fun in ("CodeNP", "QuotedNP"):
            # a quoted text is its words: telingo's theory parser does not read an escaped quote as clingo does
            return const(t[1][1][1:-1] if fun == "QuotedNP" else t[1][1]), []
        cat, base, part = self.v.decode(fun)
        if cat == "attribute" and part == "Of":
            term, fs = self.np(t[1])
            return "value(%s,%s)" % (base, term), fs
        if cat == "attribute_word":
            return base, []
        if cat != "kind":
            return "none", []
        if part == "Named":
            name = const(t[1][1])
            self.facts.append("kind(%s,%s)." % (name, base))
            self.bound[base], self.named[name] = name, base
            return name, []
        if part == "NumberOf":
            return "number(%s)" % base, []
        if part in ("The", "It", "Its") and base in self.bound:
            term = self.bound[base]
            return term, (self.cn(t[1], term) if part != "It" else [])
        x = self.fresh(base)
        self.bound[base] = x
        return x, ([] if part == "It" else self.cn(t[1], x))

    def cn(self, t, x):
        """The restrictions a common noun puts on its variable."""
        cat, base, part = self.v.decode(t[0])
        if cat == "relation":
            return self.cn(t[1], x) + self.arg(t[2], lambda y: [atom("rel(%s,%s,%s)" % (base, x, y))])
        if cat == "attribute":
            if part == "Pre":
                return [self.test(x, base, [self.v.value(t[1])])]
            vals = [self.v.value(m) for m in self.v.members(t[2])]
            if part.endswith("Not"):
                return self.cn(t[1], x) + [neg(atom("attr(%s,%s,%s)" % (x, base, v))) for v in vals]
            return self.cn(t[1], x) + [self.test(x, base, vals)]
        if cat == "condition":
            if part == "Pre":
                return [atom("cond(%s,%s)" % (base, x))]
            one = atom("cond(%s,%s)" % (base, x))
            return self.cn(t[1], x) + [neg(one) if part == "ThatIsNot" else one]
        return []

    def test(self, x, tid, vals):
        """`attr(X,A,v)`, or a disjunction for `whose A is v1 or v2`; kept for L3's text (the values before)."""
        self.tests.append((x, tid, vals))
        alts = [atom("attr(%s,%s,%s)" % (x, tid, v)) for v in vals]
        return alts[0] if len(alts) == 1 else ("|", alts)

    def arg(self, t, build):
        """The formulas of an atom whose argument is a noun phrase: `build(term)` with the phrase's restrictions; under
        `no`, the negation of an auxiliary atom saying there is one."""
        u = self.unwrap(t)
        cat, base, part = self.v.decode(u[0])
        if cat == "kind" and part == "No":
            mark = self.n
            y = self.fresh(base)
            body = self.cn(u[1], y) + build(y)
            head, _ = self.define("some", body, self.created_since(mark))
            return [neg(atom(head))]
        term, fs = self.np(t)
        return fs + build(term)

    def objects(self, nps, build, eff):
        """A response's objects: `a`/`no` X is existential (local to the response's auxiliary atom), `every` X is
        bound with the condition, any other is the term it names."""
        terms, pre, mods, locals_, universal, negate = [], [], [], [], None, False
        for t in nps:
            u = self.unwrap(t)
            cat, base, part = self.v.decode(u[0])
            if t[0] == "Only" and cat == "kind" and part in ("An", "One"):
                # `only a K`: no such response to a thing that is not a K (a restriction, not an obligation)
                y = self.fresh(None)
                mods.append(neg(atom("kind(%s,%s)" % (y, base))))
                locals_.append(y)
                negate = True
                terms.append(y)
            elif cat == "kind" and (part in ("An", "One", "AtMostOne", "No") or (
                    part in ("The", "It", "Its") and base not in self.bound)):
                mark, saved = self.n, dict(self.bound)
                y = self.fresh(base)
                mods += self.cn(u[1], y)
                locals_ += self.created_since(mark)
                self.bound, negate = saved, negate or part == "No"
                terms.append(y)
            elif cat == "kind" and part in ("Every", "Pl"):
                y = self.fresh(base)
                self.bound[base] = y
                m = self.cn(u[1], y)
                pre += m
                universal = (y, base, m)
                terms.append(y)
            else:
                term, fs = self.np(t)
                pre += fs
                terms.append(term)
        return Conjunct(build(*terms), mods, locals_, pre, universal, negate, None, [], eff + (terms[0],))
