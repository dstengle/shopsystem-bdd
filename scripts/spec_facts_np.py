"""The noun-phrase half of the facts (design-r3 §3): the roles of one requirement and the restrictions its noun phrases
put on them.

A noun phrase of a kind is a role `v<n>` (`role(R,V,K)`), numbered in order of mention; an anaphor (`the`, `it`,
`its`) is the role bound before for its kind, a `Named` code a role with `named(R,V,C)`; a `the`/`its` with nothing
bound before is a fresh role marked `the(R,V)`, the one thing of its kind (check.lp). A restriction is a literal
on the role: in the pre-state (`cond`, `ccond`, `crel`) or, for a response's object, on the object (`oattr`, `orel`,
and `onot`, `ocond` for a negated value and a condition). A noun phrase under `no` in a clause is no role: it gives
`none(R,K,A,Val)`, `cnone(R,K,C)` or `rnone(R,Rel,X,Y)` (its side of the relation written `kind(K)`), read over the
whole pre-state (§3.3); the restrictions of its own noun are left out, which only strengthens the `none`.

A value list (`whose A is v1 or v2`) and a condition's `or` are choices (`Scope.pick`): `spec_facts.translate`
walks the tree once for each way through them. A defined condition (`Vocab.def_lits`) is followed, when it is
positive, by its definition's literals on the same role, the definition's other noun phrases fresh roles.

`every K` as a clause's subject is no role either: a universal `u<n>` (`uall(R,U,K)`), its noun's
restrictions `uattr(R,U,A,Val)`, `urel(R,Rel,U,W)`, and what the clause says of it `ucond(R,U,A,Val,Pol)` or
`uccond(R,U,C,Pol)`; a restriction the check cannot match (negated, a condition) or a value list gives no conclusion.
"""


def const(text):
    """A clingo string."""
    return '"%s"' % str(text).replace("\\", "\\\\").replace('"', '\\"')


def unwrap(t):
    while t[0] == "Only" or t[0].endswith("_toNP"):
        t = t[1]
    return t


class Scope:
    """One walk of one requirement: its facts (`out`), roles, bindings and the choices it took."""

    def __init__(self, vocab, rid, choices=()):
        self.v, self.rid = vocab, const(rid)
        self.n, self.bound, self.out = 0, {}, []
        self.choices, self.taken, self.options, self.expanding = list(choices), [], [], set()
        self.univ, self.ubad = set(), set()

    def emit(self, pred, *args):
        fact = "%s(%s)." % (pred, ",".join((self.rid,) + tuple(str(a) for a in args)))
        if fact not in self.out:
            self.out.append(fact)

    def pick(self, n):
        """The alternative (0 … n-1) this walk takes at the next choice point."""
        i = len(self.taken)
        c = self.choices[i] if i < len(self.choices) else 0
        self.taken.append(c)
        self.options.append(n)
        return c

    def fresh(self, kid):
        self.n += 1
        name = "v%d" % self.n
        self.emit("role", name, kid)
        return name

    def decode(self, fun, what):
        found = self.v.decode(fun)
        if found[0] is None:
            raise ValueError("no translation of the %s %s" % (what, fun))
        return found

    # --- literals ----------------------------------------------------------------------------------------------
    def attr(self, x, tid, val, pos, obj):
        if x in self.univ:
            self.emit("uattr", x, tid, val) if pos else self.ubad.add(x)
        elif obj:
            self.emit("oattr" if pos else "onot", x, tid, val)
        else:
            self.emit("cond", x, tid, val, "pos" if pos else "neg")

    def values(self, x, tid, vals, pos, obj):
        """`is v`, `whose A is v1 or v2` (a choice of one), `whose A is not v1 or v2` (each negated)."""
        if pos:
            self.attr(x, tid, vals[self.pick(len(vals))] if len(vals) > 1 else vals[0], True, obj)
        else:
            for val in vals:
                self.attr(x, tid, val, False, obj)

    def rel(self, rid, x, y, obj, pos=True):
        if not pos:
            if obj or x in self.univ or y in self.univ:
                raise ValueError("no translation of a negated relation %s there" % rid)
            self.emit("crel", rid, x, y, "neg")
        elif x in self.univ:
            self.emit("urel", rid, x, y)
        elif y in self.univ:
            self.ubad.add(y)
        elif obj:
            self.emit("orel", rid, x, y)
        else:
            self.emit("crel", rid, x, y, "pos")

    def ccond(self, x, cid, pos, obj):
        if x in self.univ:
            self.ubad.add(x)
            return
        self.emit("ocond" if obj else "ccond", x, cid, "pos" if pos else "neg")
        if pos and cid in self.v.def_lits and cid not in self.expanding:
            kid, clause = self.v.def_lits[cid]
            saved, self.bound = self.bound, {kid: x}
            self.expanding.add(cid)
            self.clause(clause, obj)
            self.expanding.discard(cid)
            self.bound = saved

    def clause(self, t, obj=False):
        raise NotImplementedError

    # --- noun phrases ------------------------------------------------------------------------------------------
    def np(self, t, obj=False):
        """The term of a noun phrase, its restrictions emitted."""
        t = unwrap(t)
        fun = t[0]
        if fun == "CodeNP":
            return const(t[1][1])
        if fun == "QuotedNP":
            return const(t[1][1][1:-1])
        cat, base, part = self.decode(fun, "noun phrase")
        if cat == "attribute" and part == "Of":
            return "value(%s,%s)" % (base, self.np(t[1], obj))
        if cat == "attribute_word":
            return base
        if cat != "kind" or part is None:
            raise ValueError("no translation of the noun phrase %s" % fun)
        if part == "Named":
            x = self.fresh(base)
            self.emit("named", x, const(t[1][1]))
            self.bound[base] = x
            return x
        if part == "NumberOf":
            return "number(%s)" % base
        if part in ("The", "It", "Its") and base in self.bound:
            x = self.bound[base]
            if part != "It":
                self.cn(t[1], x, obj)
            return x
        x = self.fresh(base)
        self.bound[base] = x
        if part in ("The", "Its"):
            self.emit("the", x)             # no antecedent: the one thing of its kind
        if part != "It":
            self.cn(t[1], x, obj)
        return x

    def cn(self, t, x, obj):
        """The restrictions a common noun puts on its role."""
        cat, base, part = self.decode(t[0], "common noun")
        if cat == "kind" and part is None:
            return
        if cat == "relation" and part is None:
            self.cn(t[1], x, obj)
            y, kid = self.arg(t[2], obj)
            if kid:
                self.emit("rnone", base, x, "kind(%s)" % kid)
            else:
                self.rel(base, x, y, obj)
            return
        if cat == "attribute" and part in ("Pre", "ThatIs", "ThatIsNot", "Whose", "WhoseNot"):
            if part == "Pre":
                self.attr(x, base, self.v.value(t[1]), True, obj)
                return
            self.cn(t[1], x, obj)
            self.values(x, base, [self.v.value(m) for m in self.v.members(t[2])], not part.endswith("Not"), obj)
            return
        if cat == "condition" and part in ("Pre", "ThatIs", "ThatIsNot"):
            if part != "Pre":
                self.cn(t[1], x, obj)
            self.ccond(x, base, part != "ThatIsNot", obj)
            return
        raise ValueError("no translation of the common noun %s" % t[0])

    def every(self, t, obj):
        """The universal `u<n>` of an `every K` argument of a clause, its restrictions emitted (`uall`, `uattr`,
        `urel`); None for any other argument (a plural stays a role), or under an object."""
        u = unwrap(t)
        cat, base, part = self.v.decode(u[0])
        if obj or cat != "kind" or part != "Every":
            return None
        x = "u%d" % (len(self.univ) + 1)
        self.univ.add(x)
        self.emit("uall", x, base)
        self.cn(u[1], x, obj)
        return x

    def universal_atom(self, t, cat, base, part, obj):
        """`every K ... is v` / `is C` (and `is not`): `ucond`, `uccond` on the universal; True when it was one. A
        value list or a restriction the check cannot match (a negated one, a condition) gives no conclusion."""
        u = self.every(t[1], obj)
        if u is None:
            return False
        pol = "pos" if part == "Is" else "neg"
        if cat == "condition" and u not in self.ubad:
            self.emit("uccond", u, base, pol)
        elif cat == "attribute" and u not in self.ubad and len(self.v.members(t[2])) == 1:
            self.emit("ucond", u, base, self.v.value(t[2]), pol)
        return True

    def arg(self, t, obj=False):
        """(term, None) of an atom's argument, or (None, kind) for a noun phrase under `no`."""
        u = unwrap(t)
        cat, base, part = self.v.decode(u[0])
        if cat == "kind" and part == "No":
            return None, base
        return self.np(t, obj), None
