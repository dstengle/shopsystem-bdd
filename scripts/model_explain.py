"""`model explain <cap>#r<n>` (the CNL 4 design, I13b; call 12): a requirement's line, then what it also means and
what takes precedence over it.

"which also means:" lists each response the other requirements force where the line's trigger, state and responses
hold (spec_entail_rules' world of the line with every premise as a rule over it, grammar/entail.lp their background),
a response the line states itself left out, each with its premise: a universal condition (U11, a refusal changes
nothing) or a requirement, and the definition of refuse of an imported pack (spec_entail's bridge: an error exit on a
run is a refusal of its command, and a refusal an error exit). A refusal the line states fires the premises on a
refusal as the bridge's does. "taking precedence over it" lists each If requirement of the line's trigger, when the
line is of another form (call 12: where the If line's state holds its response replaces the line's); a universal
condition takes no precedence. An id no capability holds is refused, naming it, and nothing is written."""
import sys
from pathlib import Path

import clingo
import spec_context
import spec_entail
import spec_facts
import spec_packs
from spec_entail_rules import Premises, parse, q
from spec_findings import Words

EXC = {"if", "while_if", "where_if"}
EXTRA = """
evB(Q,does,e_refuse,D,C) :- r(Q,pos,e_refuse,D,C,self).
own(Q,P,E,D,X) :- r(Q,P,E,D,X,self).
cons(P,E,D,X,M) :- rA(Q,P,E,D,X,M), not own(Q,P,E,D,X).
cons(P,E,D,X,M) :- rB(Q,P,E,D,X,M), not own(Q,P,E,D,X).
#show cons/5.
"""


def held(ctx, ident):
    """The text of the requirement `ident` of a codified capability, or None when no capability holds it."""
    cap, _, rid = ident.rpartition("#")
    found = ctx.caps.get(cap)
    for group in found.groups if found else ():
        for r in group.requirements:
            if r.id == rid:
                return r.text
    return None


def refuse_pack(root):
    """The name of the imported pack whose `## Definitions` define refuse by an error exit, or None."""
    for name in spec_packs.imports(root):
        path = spec_packs.path_of(root, name)
        if path is not None and spec_entail.REFUSE.search(Path(path).read_text()):
            return name
    return None


class Explain:
    def __init__(self, root, ctx):
        self.root, self.words = root, Words(root, ctx)
        facts = list(ctx.domain) + [f for s in ctx.statements for f in ctx.facts[s.id]]
        self.reqs, self.dom = parse(facts)
        self.domain = [f for f in facts if f.split("(")[0] in ("kind", "sub", "val", "dalt", "dlit")]
        self.P = Premises(self.reqs, self.dom)
        self.pack = refuse_pack(root)

    def parts(self, ident):
        return sorted(r for r in self.reqs if spec_facts.split(r) == ident)

    def term(self, L, x):
        if x.type == clingo.SymbolType.Function and x.name == "t" and len(x.arguments) == 1:
            x = x.arguments[0]
            for y, c in self.words.of(L, "named"):
                if y == x:
                    return c.string
        return self.words.term(L, x)

    def says(self, L, p, e, d, x):
        """`<doer> shall [not] <event> <object>` in the lexicon's words."""
        who = self.term(L, d)
        rest = self.words.does(L, e, d, x)[len(self.words.term(L, d)) + len(" to "):]
        if x.type == clingo.SymbolType.Function and x.name == "t":
            rest = rest.replace(self.words.term(L, x.arguments[0]), self.term(L, x))
        return "%s shall %s%s" % (who, "" if p == "pos" else "not ", rest)

    def consequences(self, L):
        """[(what L also means, its premise)], the definition of refuse's first."""
        out, f, P = [], self.reqs[L], self.P
        trig = P.trig.get(L)
        if self.pack:
            by = "the definition of refuse in the pack %s" % self.pack
            for _, p, e, d, x in f["resp"]:
                if p == "pos" and e == "e_refuse":
                    out.append(("%s shall exit with an error" % self.term(L, clingo.parse_term(d)), by))
                if p == "pos" and e == "exit_error" and trig and trig[0] == "ran":
                    out.append(("%s shall refuse %s" % (self.term(L, clingo.parse_term(d)), trig[1]), by))
        Q = "q(%s,0)" % q(L)
        prog = list(P.world(L, "0", Q, bool(self.pack)))
        prog += self.domain
        for M in sorted(self.reqs):
            if P.base[M] != P.base[L] and spec_facts.split(M) != spec_facts.split(L) and spec_facts.split(L) not in self.precedence(M):
                prog += ["use(%s,%s)." % (Q, q(M))] + P.rule(M)
        ctl = clingo.Control(["--warn=none", "-t", "1"])
        ctl.add("base", [], "\n".join(prog + [spec_entail.ENTAIL.read_text(), EXTRA]))
        ctl.ground([("base", [])])
        found = []
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                found = sorted(model.symbols(shown=True), key=str)
        own = {self.says(L, p, *(clingo.parse_term(a) for a in (e, d, x))) for _, p, e, d, x in f["resp"]}
        for s in found:
            p, e, d, x, m = s.arguments
            said = self.says(L, p.name, e, d, x)
            if said not in own:     # a response the line states itself, which a premise forces too, is no news
                out.append((said, spec_facts.split(m.string)))
        return list(dict.fromkeys(out))

    def precedence(self, L):
        """The If requirements of L's trigger that take precedence over L (none when L is an If line)."""
        forms = {a[0] for a in self.reqs[L]["form"]}
        trig = self.P.trig.get(L)
        if forms & EXC or trig is None:
            return []
        return [spec_facts.split(M) for M, f in sorted(self.reqs.items())
                if "#" in M and spec_facts.split(M) != spec_facts.split(L) and {a[0] for a in f["form"]} & EXC
                and self.P.trig.get(M, [None, None])[:2] == trig[:2]]


def explain(root, ident):
    """Print the explanation of `ident` and return 0, or refuse an id no capability holds and return 1."""
    ctx = spec_context.load(root)
    text = held(ctx, ident)
    if text is None:
        print("model explain: refused: %s: no capability holds the requirement %s" % (ident, ident), file=sys.stderr)
        return 1
    print("%s  %s" % (ident, text))
    ex = Explain(root, ctx)
    parts = ex.parts(ident)
    means = list(dict.fromkeys(c for L in parts for c in ex.consequences(L)))
    if means:
        print("which also means:")
        for what, by in means:
            print("  %s (by %s)" % (what, by))
    over = list(dict.fromkeys(M for L in parts for M in ex.precedence(L)))
    if over:
        print("taking precedence over it, where its state holds:")
        for M in over:
            print("  %s  %s" % (M, held(ctx, M)))
    return 0

