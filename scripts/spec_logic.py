"""Requirement trees as telingo program parts (design §12.1): one translation per core and typed fun.

A statement becomes one integrity constraint guarded by `on("<id>")`, so an unsatisfiable core names statements.
A trigger is read at the step before its response (`'` in a `dynamic` part); a statement with no trigger holds in
every state (`always`). Noun phrases are variables bound by their kind and modifiers, read universally, except an
existential object of a response (`write a question`), which is a new thing `n("<id>",k)`. A group's witness
(`witness`) makes its pre-state true at step 0 and its trigger at step 1 with things `w("<g>",k)`, two for a plural
or `every`. The atoms are those `grammar/background.lp` reads: `kind/2`, `attr/3`, `rel/3`, `cond/2`, `does/3`,
`ran/3`, `holds/2`, `given/1`.
"""
import re
from pathlib import Path

import spec_tree
from spec_logic_vocab import AMOUNT, Vocab, facts, means_values

BACKGROUND = Path(__file__).resolve().parent.parent / "grammar" / "background.lp"
ACTIONS = {"ExitOk": [("exit_ok", None)], "ExitErr": [("exit_error", 1)], "ChangeNothing": [("change_nothing", None)],
           "RefuseErr": [("exit_error", 1), ("change_nothing", None)], "CommitPush": [("commit", 1), ("push", 1)]}
__all__ = ["Vocab", "facts", "means_values", "program", "translate", "witness"]


def _const(text):
    return '"%s"' % str(text).replace("\\", "\\\\").replace('"', '\\"')


class Sentence:
    """One statement's translation. In "rule" mode a noun phrase is a variable; in "witness" mode it is a thing."""

    def __init__(self, vocab, ident, mode="rule"):
        self.v, self.ident, self.mode = vocab, ident, mode
        self.n, self.k, self.bound, self.facts, self.negated, self.skolem = 0, 0, {}, [], False, True

    def fresh(self):
        self.n += 1
        if self.mode == "rule":
            return "X%d" % self.n
        name = "w(%s,%d)" % (_const(self.ident), self.n)
        self.facts.append("thing(%s)." % name)
        return name

    def new_thing(self, kid):
        self.k += 1
        name = "n(%s,%d)" % (_const(self.ident), self.k)
        self.facts += ["thing(%s)." % name, "kind(%s,%s)." % (name, kid)]
        return name

    # --- noun phrases ------------------------------------------------------------------------------------------
    def np(self, t, skolem=False):
        """(terms, literals) of a noun phrase: one term, or two for a plural in a witness."""
        fun = t[0]
        if fun in ("Only",) or fun.endswith("_toNP"):
            return self.np(t[1], skolem)
        if fun in ("CodeNP", "QuotedNP"):
            return [_const(t[1][1])], []
        cat, base, part = self.v.decode(fun)
        if cat == "attribute" and part == "Of":
            terms, lits = self.np(t[1])
            return ["value(%s,%s)" % (base, terms[0])], lits
        if cat == "attribute_word":
            return [base], []
        if cat != "kind":
            return ["none"], []
        if part == "Named":
            name = _const(t[1][1])
            if self.mode == "witness":
                self.facts.append("thing(%s)." % name)
            self.bound[base] = name
            return [name], ["kind(%s,%s)" % (name, base)]
        if part == "NumberOf":
            return ["number(%s)" % base], []
        if part in ("It", "The", "Its") and base in self.bound:
            term = self.bound[base]
            return [term], (self.cn(t[1], [term], top=False) if part != "It" else [])
        if part == "No" and self.mode == "witness":
            return ["none"], []
        if part == "No" and skolem:
            self.negated = True
            skolem = False
        if skolem and part in ("An", "One", "AtMostOne"):
            return [self.new_thing(base)], []
        many = self.mode == "witness" and part in ("Pl", "Every")
        terms = [self.fresh() for _ in range(2 if many else 1)]
        self.bound[base] = terms[0]
        lits = self.cn(t[1], terms) if part != "It" else ["kind(%s,%s)" % (terms[0], base)]
        return terms, lits

    def cn(self, t, terms, top=True):
        """The literals a common noun gives each of its terms."""
        fun = t[0]
        cat, base, part = self.v.decode(fun)
        if cat == "kind" and part is None:
            return ["kind(%s,%s)" % (x, base) for x in terms] if top else []
        if cat == "relation":
            inner = self.cn(t[1], terms, top)
            others, lits = self.np(t[2])
            return inner + ["rel(%s,%s,%s)" % (self.v.rels[base], x, others[0]) for x in terms] + lits
        if cat == "attribute":
            kid = self.v.attrs[base][0]
            if part == "Pre":
                head = ["kind(%s,%s)" % (x, kid) for x in terms] if top else []
                return head + ["attr(%s,%s,%s)" % (x, base, self.v.value(t[1])) for x in terms]
            inner = self.cn(t[1], terms, top)
            return inner + [lit for x in terms for lit in self.values(x, base, t[2], part.endswith("Not"))]
        if cat == "condition":
            kid = self.v.conds[base]
            if part == "Pre":
                head = ["kind(%s,%s)" % (x, kid) for x in terms] if top else []
                return head + ["cond(%s,%s)" % (base, x) for x in terms]
            neg = "not " if part == "ThatIsNot" else ""
            return self.cn(t[1], terms, top) + ["%scond(%s,%s)" % (neg, base, x) for x in terms]
        return []

    def values(self, x, tid, t, negated):
        """`that is v`, `whose A is v1 or v2` (one of the values), and their negations (none of them)."""
        vals = [self.v.value(m) for m in self.v.members(t)]
        if negated:
            return ["not attr(%s,%s,%s)" % (x, tid, v) for v in vals]
        if len(vals) == 1:
            return ["attr(%s,%s,%s)" % (x, tid, vals[0])]
        key = "%s_%d" % (re.sub(r"\W", "_", self.ident).lower(), len(self.facts))
        self.facts += ["vals(%s,%s)." % (key, v) for v in vals]
        var = "V%s" % key
        return ["attr(%s,%s,%s)" % (x, tid, var) if self.mode == "rule" else "attr(%s,%s,%s)" % (
            x, tid, vals[0]), "vals(%s,%s)" % (key, var if self.mode == "rule" else vals[0])]

    # --- clauses -----------------------------------------------------------------------------------------------
    def subject(self, t):
        if t[0] == "ActorSubj":
            return t[1][0], []
        terms, lits = self.np(t[1])
        return terms[0], lits

    def command(self, t):
        return _const(t[1][1]) if t[0] == "CmdCode" else t[1][0]

    def trig(self, t):
        fun = t[0]
        if fun in ("Runs", "RunsOn"):
            subj, lits = self.subject(t[1])
            obj, more = self.np(t[3]) if fun == "RunsOn" else (["none"], [])
            return lits + more + ["ran(%s,%s,%s)" % (subj, self.command(t[2]), obj[0])]
        if fun == "IsRun":
            return ["ran(%s,%s,none)" % ("_" if self.mode == "rule" else "anyone", self.command(t[1]))]
        if fun in ("Happens", "HappensI"):
            subj, lits = self.subject(t[1])
            obj, more = self.np(t[3]) if fun == "Happens" else (["none"], [])
            return lits + more + ["does(%s,%s,%s)" % (subj, t[2][0], o) for o in obj]
        if fun == "Undergoes":
            obj, lits = self.np(t[1])
            who = "_" if self.mode == "rule" else "anyone"
            return lits + ["does(%s,%s,%s)" % (who, t[2][0], o) for o in obj]
        cat, base, part = self.v.decode(fun)
        if cat == "attribute" and part == "Becomes":
            terms, lits = self.np(t[1])
            return lits + ["attr(%s,%s,%s)" % (x, base, self.v.value(t[2])) for x in terms]
        return []

    def cond(self, t):
        fun = t[0]
        if fun == "CondOne":
            return self.atom(t[1])
        if fun == "CondAnd":
            return self.atom(t[1]) + self.cond(t[2])
        if fun == "FeatGiven":
            self.facts.append("feature(%s)." % _const(t[1][1]))
            return ["given(%s)" % _const(t[1][1])]
        if fun == "FeatAtom":
            return self.atom(t[1])
        return []

    def atom(self, t):
        fun = t[0]
        if fun in ("Holds", "HoldsA"):
            terms, lits = self.np(t[1])
            return lits + ["holds(%s,%s)" % (x, t[2][0]) for x in terms] + ["active(%s)" % x for x in terms]
        if fun == "IsFree":
            return ["not over(%s)" % t[1][0]]
        cat, base, part = self.v.decode(fun)
        terms, lits = self.np(t[1])
        if cat == "attribute":
            neg = "not " if part == "IsNot" else ""
            return lits + ["%sattr(%s,%s,%s)" % (neg, x, base, self.v.value(t[2])) for x in terms]
        if cat == "condition":
            neg = "not " if part == "IsNot" else ""
            return lits + ["%scond(%s,%s)" % (neg, base, x) for x in terms]
        return lits

    def vp(self, t, subj):
        """(heads, literals of the response's own noun phrases, count) of a verb phrase."""
        fun = t[0]
        if fun in ("Do", "DoTo"):
            objs, lits = self.np(t[2], skolem=self.skolem)
            if fun == "DoTo":
                more, extra = self.np(t[3], skolem=self.skolem)
                return ["does(%s,%s,%s)" % (subj, t[1][0], "pair(%s,%s)" % (objs[0], more[0]))], lits + extra, None
            return ["does(%s,%s,%s)" % (subj, t[1][0], objs[0])], lits, None
        if fun == "Print":
            heads, lits = [], []
            for member in self.v.members(t[1]):
                objs, more = self.np(member, skolem=self.skolem)
                heads.append("does(%s,print,%s)" % (subj, objs[0]))
                lits += more
            return heads, lits, None
        if fun in ACTIONS:
            objs, lits = self.np(t[1], skolem=self.skolem) if len(t) > 1 else (["none"], [])
            return ["does(%s,%s,%s)" % (subj, act, objs[0] if arg else "none") for act, arg in ACTIONS[fun]], lits, None
        if fun in ("Hold", "HoldA"):
            return ["holds(%s,%s)" % (subj, t[1][0])], [], None
        if fun == "HoldAtMost":
            count = t[1][1] if t[1][0] == "CountNum" else AMOUNT
            return [], [], "#count{ Y : holds(Y,%s), active(Y) } > %s" % (t[2][0], count)
        cat, base, part = self.v.decode(fun)
        if cat == "attribute" and part == "Set":
            terms, lits = self.np(t[1])
            vid = self.v.value(t[2])
            return ["attr(%s,%s,%s)" % (x, base, vid) for x in terms], lits, None
        return [], [], None


def _prime(lit):
    return lit[4:].join(("not '", "")) if lit.startswith("not ") else "'" + lit


CHOOSABLE = ("does(", "ran(", "holds(")


def translate(vocab, ident, tree):
    """{"always", "dynamic"}: the constraint of one statement guarded by on(ident), a choice of each response it
    asks for (so that only a constraint can refuse it), and the facts it needs."""
    s = Sentence(vocab, ident)
    parts = spec_tree.parts(tree)
    pre = s.cond(parts["feat"]) if parts["feat"] else []
    pre += s.cond(parts["cond"]) if parts["cond"] else []
    trig = s.trig(parts["trig"]) if parts["trig"] else []
    resp = parts["resp"]
    subj, slits = s.subject(resp[1])
    s.skolem = resp[0] == "Shall"
    heads, olits, count = s.vp(resp[2], subj)
    shall = resp[0] == "Shall" and not s.negated
    body = pre + trig + slits + (olits if shall else [])
    if parts["trig"]:
        body = [_prime(x) for x in body]
        olits = [_prime(x) for x in olits]
    guard = ":- on(%s)" % _const(ident)
    if count:
        rules = [", ".join([guard] + body + [count]) + "."] if shall else []
    elif shall:
        rules = [", ".join([guard] + body + ["not " + h]) + "." for h in heads]
        rules = ["{ %s }%s." % (h, " :- " + ", ".join(body) if body else "") for h in heads] + rules
    else:
        rules = [", ".join([guard] + body + heads + olits) + "."] if heads else []
    out = {"always": ["#external on(%s)." % _const(ident)] + s.facts, "dynamic": [], "initial": []}
    out["dynamic" if parts["trig"] else "always"] += rules
    return out


def witness(vocab, group, trees):
    """The parts that make a group's pre-state true at step 0 and its trigger at step 1 (its responses are then due
    at step 2): static facts for kinds and relations, a choice of each event it needs, and `wit(0)`/`wit(1)`."""
    s = Sentence(vocab, group, mode="witness")
    first = spec_tree.parts(trees[0]) if trees else dict.fromkeys(("feat", "cond", "trig", "resp"))
    pre = []
    for key in ("feat", "cond"):
        pre += s.cond(first[key]) if first[key] else []
    trig = s.trig(first["trig"]) if first["trig"] else []
    if trees and trees[0][0] == "Ubiq":
        pre += s.subject(first["resp"][1])[1]
    static = [x + "." for x in pre + trig if x.startswith(("kind(", "rel("))]
    pre, trig = ([x for x in lits if not x.startswith(("kind(", "rel(", "active("))] for lits in (pre, trig))
    out = {"always": list(dict.fromkeys(s.facts + static)), "initial": ["__w0.", ":- not wit(0)."],
           "dynamic": [":- '__w0, not wit(1)."]}
    out["always"] += ["{ %s }." % x for x in dict.fromkeys(pre + trig) if x.startswith(CHOOSABLE)]
    out["always"].append("wit(0)%s." % (" :- " + ", ".join(pre) if pre else ""))
    out["always"].append("wit(1)%s." % (" :- " + ", ".join(pre + trig) if pre + trig else ""))
    return out


def program(parts):
    """The telingo program text: the background theory, then each {part: rules} in order."""
    text = [BACKGROUND.read_text()]
    for name in ("always", "initial", "dynamic"):
        rules = [r for p in parts for r in p.get(name, [])]
        if rules:
            text.append("#program %s.\n%s\n" % (name, "\n".join(dict.fromkeys(rules))))
    return "\n".join(text)
