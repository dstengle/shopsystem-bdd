"""The rules of the entailment check (the CNL 4 design, I13a; its study's comp.py and cex.py, ported): a context's
check facts read per requirement (`parse`), the world of a query q(L,I) as facts (`Premises.world`) and each premise M
as Datalog rules over a query variable Q (`Premises.rule`), in its stratum (`stage`); grammar/entail.lp is their
background. A codified-1 line's facts (spec_facts) and a codified-2 line's (spec_lf_facts) are read alike: an `each`
object is an `every` one."""
import re
from collections import defaultdict

import clingo

DOMAIN = ("kind", "sub", "actor", "fun", "val", "trans", "initial", "prose", "dalt", "dlit", "akind", "vkey", "dense")


def parse(facts):
    """({requirement: {predicate: [args]}}, {domain predicate: [args]}) of check facts (strings)."""
    reqs, dom = defaultdict(lambda: defaultdict(list)), defaultdict(list)
    for f in facts:
        t = clingo.parse_term(f.rstrip("."))
        args = [a.string if a.type == clingo.SymbolType.String else str(a) for a in t.arguments]
        if t.name in DOMAIN:
            dom[t.name].append(args)
        elif args:
            reqs[args[0]][t.name].append(args[1:])
    return reqs, dom


def q(s):
    """A term of the program: a symbol or a compound as it is, anything else quoted."""
    if re.fullmatch(r"[a-z][A-Za-z0-9_]*", s) or re.fullmatch(r"(value|number|kind|set)\(.*\)", s):
        return s
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"')


def _quiet(x):
    return x.startswith(("value(", "number("))


class Premises:
    def __init__(self, reqs, dom):
        self.reqs, self.dom = reqs, dom
        self.sup = defaultdict(set)
        for k, k2 in dom["sub"]:
            self.sup[k].add(k2)
        self.base = {r: (f["disj"][0][0] if f["disj"] else r) for r, f in reqs.items()}
        self.trig = {r: f["trig"][0] for r, f in reqs.items() if f["trig"]}

    def supers(self, k):
        out, todo = {k}, [k]
        while todo:
            for s in self.sup[todo.pop()]:
                if s not in out:
                    out.add(s)
                    todo.append(s)
        return out

    def canon(self, r):
        """Each role of r to the first role named by the same code (one thing), or to itself."""
        f, first, out = self.reqs[r], {}, {}
        for y, c in sorted(f["named"]):
            first.setdefault(c, y)
        for y, _ in f["role"]:
            c = next((c for yy, c in f["named"] if yy == y), None)
            out[y] = first[c] if c else y
        return out

    def every(self, r):
        f = self.reqs[r]
        return {y for (y,) in f["every"] + f["each"]}

    def ante_roles(self, r):
        f = self.reqs[r]
        out = {a[0] for a in f["cond"] + f["ccond"]} | {a[1] for a in f["crel"]} | {a[2] for a in f["crel"]}
        out |= {a[0] for a in f["named"]} | {a[3] for a in f["resp"]}
        if r in self.trig:
            out |= {self.trig[r][2], self.trig[r][3]}
        return out

    def existentials(self, r):
        """The roles of r's responses only (no code, not in its antecedent, not a doer): things r says are made."""
        can = self.canon(r)
        return {y for y in can if can[y] == y and y not in self.ante_roles(r) and y not in self.every(r)}

    def neguniv(self, r):
        """A role only in r's negative responses ("shall not ask a question"): no such thing, read as every."""
        f, ante = self.reqs[r], self.ante_roles(r)
        neg = {a[4] for a in f["resp"] if a[1] == "neg"}
        pos = {a[4] for a in f["resp"] if a[1] == "pos"}
        return {y for y, _ in f["role"] if y in neg and y not in pos and y not in ante}

    # ---- the world of a query ------------------------------------------------------------------------------------
    def world(self, L, I, Q, bridge):
        """The facts of query Q: L's terms (and the actors it names), its antecedent, trigger and other responses."""
        f, can, ex = self.reqs[L], self.canon(L), self.existentials(L)
        tm = lambda x: "t(%s)" % can[x] if x in can else q(x)
        terms, out = {}, []
        for y, k in f["role"]:
            if can[y] == y and y not in ex:
                terms[tm(y)] = k
        akind = dict(self.dom["akind"])
        for a in {a[2] for a in f["trig"]} | {a[3] for a in f["resp"]}:
            if a in akind:
                terms[a] = akind[a]
        if L in self.trig and self.trig[L][0] == "ran":
            terms[q(self.trig[L][1])] = "k_command"
        for z, k in terms.items():
            out += ["isk(%s,%s,%s)." % (Q, z, s) for s in self.supers(k)]
        out += ["code(%s,%s,%s)." % (Q, tm(y), q(c)) for y, c in f["named"]]
        out += ["%s(%s,%s,%s,%s)." % ("a0" if p == "pos" else "na0", Q, tm(y), t, v) for y, t, v, p in f["cond"]]
        out += ["a0(%s,%s,%s,%s)." % (Q, tm(y), t, v) for y, t, v in f["oattr"] if y not in ex]
        out += ["%s(%s,%s,%s)." % ("k" if p == "pos" else "nk", Q, tm(y), c) for y, c, p in f["ccond"]]
        out += ["%s(%s,%s,%s,%s)." % ("rel" if p == "pos" else "nrel", Q, qq, tm(a), tm(b)) for qq, a, b, p in f["crel"]]
        out += ["rel(%s,%s,%s,%s)." % (Q, qq, tm(a), tm(b)) for qq, a, b in f["orel"] if a not in ex]
        out += ["feat(%s,%s)." % (Q, q(ft)) for (ft,) in f["feat"]]
        out += ["lnone(%s,%s,%s,%s)." % (Q, kk, t, v) for kk, t, v in f["none"]]
        out += ["lcnone(%s,%s,%s)." % (Q, kk, c) for kk, c in f["cnone"]]
        side = lambda x: x if x.startswith("kind(") else tm(x)
        out += ["lrnone(%s,%s,%s,%s)." % (Q, qq, side(a), side(b)) for qq, a, b in f["rnone"]]
        if L in self.trig:
            p, e, d, x = self.trig[L]
            out.append("ev(%s,%s,%s,%s,%s)." % (Q, p, q(e), tm(d), tm(x)))
            if bridge and p == "ran":
                out.append("bridgecmd(%s,%s)." % (Q, q(e)))
        kinds = dict(f["role"])
        for j, p, e, d, x in f["resp"]:
            o = tm(x) if x in can and x not in ex else (x if _quiet(x) else ("x(%s)" % x if x in ex else q(x)))
            if j != str(I):
                out.append("r(%s,%s,%s,%s,%s,self)." % (Q, p, e, tm(d), o))
            elif x in ex and p == "neg":     # "shall not E a K": E is done to no K; the witness is any K
                out += ["isk(%s,x(%s),%s)." % (Q, x, s) for s in self.supers(kinds[x])]
                out.append("tq(%s,%s,%s,%s,x(%s))." % (Q, p, e, tm(d), x))
                out += ["rel(%s,%s,x(%s),%s)." % (Q, qq, x, tm(b)) for qq, a, b in f["orel"] if a == x]
                out += ["a0(%s,x(%s),%s,%s)." % (Q, x, t, v) for y, t, v in f["oattr"] if y == x]
            elif x in ex:     # something of its kind with its restrictions and L's other responses on it
                cs = ["iskall(%s,Y,%s)" % (Q, kinds[x])]
                cs += ["propall(%s,Y,%s,%s)" % (Q, t, v) for y, t, v in f["oattr"] if y == x]
                cs += ["relall(%s,%s,Y,%s)" % (Q, qq, tm(b)) for qq, a, b in f["orel"] if a == x]
                cs += ["rall(%s,%s,%s,%s,Y,_)" % (Q, p2, e2, tm(d2)) for j2, p2, e2, d2, x2 in f["resp"]
                       if x2 == x and j2 != j]
                out.append("hit(%s,M) :- rall(%s,%s,%s,%s,Y,M), Y != x(%s), %s." % (Q, Q, p, e, tm(d), x, ", ".join(cs)))
            else:
                out.append("tq(%s,%s,%s,%s,%s)." % (Q, p, e, tm(d), o))
        for j, p, e, d, x in f["resp"]:     # L's own made things and sets, as terms of the world
            if x in ex and j != str(I):
                out += ["prop(%s,x(%s),%s,%s)." % (Q, x, t, v) for y, t, v in f["oattr"] if y == x]
            if j != str(I) and e.startswith("set("):
                t, v = e[4:-1].split(",")
                out.append("setv(%s,%s,%s,%s)." % (Q, tm(x), t, v))
        return out

    # ---- a premise as rules --------------------------------------------------------------------------------------
    def rule(self, M):
        """M as Datalog over a query variable Q: `use(Q,M)` and its antecedent force its responses (tagged M)."""
        f, can = self.reqs[M], self.canon(M)
        if f["only"] or f["holds"] or f["free"] or f["uall"] or f["ccount"] or f["onattr"] or f["ccmp"]:
            return []     # never forced: an `every` or a count over the pre-state, a negated restriction, a comparison
        kinds, mq = dict(f["role"]), q(M)
        every = {can[y] for y in self.every(M)} | {can[y] for y in self.neguniv(M)}
        ante = {can[y] for y in self.ante_roles(M) if y in can} | every
        V = lambda y: "V_%s" % can[y] if y in can else ("none" if y == "none" else q(y))
        a, na = ("a0", "na0") if M in self.trig else ("a1", "na1")
        body = ["use(Q,%s)" % mq]
        if M in self.trig:
            p, e, d, x = self.trig[M]
            body.append("ev(Q,%s,%s,%s,%s)" % (p, q(e), "_" if d == "any" else V(d), V(x)))
        body += ["%s(Q,%s,%s,%s)" % (a if p == "pos" else na, V(y), t, v) for y, t, v, p in f["cond"]]
        body += ["%s(Q,%s,%s,%s)" % (a, V(y), t, v) for y, t, v in f["oattr"] if can.get(y) in ante]
        body += ["%s(Q,%s,%s)" % ("k" if p == "pos" else "nk", V(y), c) for y, c, p in f["ccond"]]
        body += ["%s(Q,%s,%s,%s)" % ("rel" if p == "pos" else "nrel", qq, V(y1), V(y2)) for qq, y1, y2, p in f["crel"]]
        body += ["rel(Q,%s,%s,%s)" % (qq, V(y1), V(y2)) for qq, y1, y2 in f["orel"] if can.get(y1) in ante]
        body += ["feat(Q,%s)" % q(ft) for (ft,) in f["feat"]]
        body += ["lnone2(Q,%s,%s,%s)" % (kk, t, v) for kk, t, v in f["none"]]
        body += ["lcnone2(Q,%s,%s)" % (kk, c) for kk, c in f["cnone"]]     # forced only when L states it as wide
        side = lambda x: x if x.startswith("kind(") else V(x)
        body += ["lrnone2(Q,%s,%s,%s)" % (qq, side(x1), side(x2)) for qq, x1, x2 in f["rnone"]]
        body += ["code(Q,%s,%s)" % (V(y), q(c)) for y, c in f["named"]]
        body += ["isk(Q,%s,%s)" % (V(y), kinds[y]) for y in sorted(ante)]

        def deps(z):
            return sorted({can[e] for qq, a1, a2 in f["orel"] for e in (a1, a2) if z in (a1, a2) and can.get(e) in every})

        def obj(z):
            if z in can and can[z] not in ante:
                return "f(%s,%s%s)" % (mq, can[z], "".join(",V_%s" % e for e in deps(z)))
            return V(z) if z in can or z == "none" else (z if _quiet(z) else q(z))
        heads = []
        for j, p, e, d, x in f["resp"]:
            heads.append("r(Q,%s,%s,%s,%s,%s)" % (p, e, obj(d), obj(x), mq))
            if e.startswith("set("):
                t, v = e[4:-1].split(",")
                heads.append("setv(Q,%s,%s,%s)" % (obj(x), t, v))
        for z in can:
            if can[z] == z and z not in ante:
                heads += ["isk(Q,%s,%s)" % (obj(z), s) for s in self.supers(kinds[z])]
                heads += ["prop(Q,%s,%s,%s)" % (obj(z), t, v) for y, t, v in f["oattr"] if y == z]
                heads += ["rel(Q,%s,%s,%s)" % (qq, obj(z), obj(y2)) for qq, y1, y2 in f["orel"] if y1 == z]
        men = lambda txt: {y for y in every if re.search(r"\bV_%s\b" % y, txt)}
        body0 = [b for b in body if not men(b)]
        # an `every` role is read per response, with its own restrictions
        return self.stage(M, [(h, body0 + [b for b in body if men(b) and men(b) <= men(h)]) for h in heads])

    def stage(self, M, rules):
        """M's rules in their stratum, so that no premise rule is recursive: A, the premises on L's own trigger, over
        the world's facts; B, the untriggered premises (over state 1, after A's sets) and those on the bridge's event.
        A chain longer than that (a stage-B premise firing another) is not followed."""
        t = self.trig.get(M)
        b = t is None or t[:2] == ["does", "e_refuse"]
        sfx, out = "B" if b else "A", []
        for h, body in rules:
            h = re.sub(r"^(r|isk|prop|rel|setv)\(", lambda m: m.group(1) + sfx + "(", h)
            if b:
                body = [re.sub(r"^(isk|rel|prop)\(", lambda m: m.group(1) + "2(", x) for x in body]
                body = [re.sub(r"^ev\(Q,does,e_refuse", "evB(Q,does,e_refuse", x) for x in body]
            out.append("%s :- %s." % (h, ", ".join(body)))
        return out
