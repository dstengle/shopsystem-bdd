"""The entailment check's chain (b545, decision 0118, L-3 of the contracts design): a request a line states or a premise
forces fires the lines triggered by that request of the same requester (the lines that govern its operation), and
what they force fires the lines triggered on it, up to DEPTH hops. A chain starts at a request only: an outcome
fires a line of the chain only after a request has led to it.

`chained` gives the lines a query's chain may reach (each a premise of the stratum C, `useC(Q,M)`), read off the
triggers and the responses alone; `rules` writes such a line's premise rules (spec_entail_rules' `pairs`) at each
depth k, its trigger read off `evC(Q,k-1,E,D,X,S)` (an event forced at depth k-1 by S, or a request stated or forced
outside the chain at depth 0: grammar/entail.lp), its responses `rC(Q,k,...)`, and `via(Q,M,S)`, the premise S its
firing came by, which spec_entail follows back so that a finding names every line of the chain."""
import re
from collections import defaultdict

from spec_entail_rules import q

DEPTH = 3
REFUSALS = ("e_refuse", "refused")     # a line on a refusal is stratum B's (spec_entail_rules' `stage`)


def triggers(P):
    """{(kind, event): [M]} of the lines a chain may fire: on a request (`req`) or on another line's act (`does`)."""
    out = defaultdict(list)
    for M, t in sorted(P.trig.items()):
        if t[0] == "req" or t[0] == "does" and t[1] not in REFUSALS:
            out[(t[0], t[1])].append(M)
    return out


def requesting(gives, M):
    return any(p == "pos" and e.startswith("req(") for p, e in gives[M])


def chained(P, L, sources, gives, by_trig):
    """[M]: the lines a request of L or of its premises `sources` reaches within DEPTH hops, none of L's own."""
    events = {e for M in set(sources) | {L} for p, e in gives[M] if p == "pos" and e.startswith("req(")}
    seen = set()
    for k in range(DEPTH):
        level = {M for e in events for kind in (("req", "does") if k else ("req",)) for M in by_trig.get((kind, e), ())
                 if P.base[M] != P.base[L] and M not in seen}
        if not level:
            break
        seen |= level
        events = {e for M in level for p, e in gives[M] if p == "pos"}
    return sorted(seen)


def _body(x, k):
    if x.startswith("use(Q,"):
        return "useC(Q," + x[len("use(Q,"):]
    if x.startswith("ev(Q,"):     # the trigger: an event of the chain, `_` its kind (a request's key or an act)
        return re.sub(r"^ev\(Q,\w+,(.*)\)$", r"evC(Q,%d,\1,S)" % (k - 1), x)
    x = re.sub(r"^(isk|rel|prop)\(", r"\1all(", x)     # what the world, the strata A, B and the chain hold
    return re.sub(r"^(a|na)0\(", r"\g<1>1(", x)         # state 1, after the sets of stratum A


def rules(P, M):
    """M's premise rules in the stratum C at each depth 1..DEPTH, and `via(Q,M,S)`."""
    pairs, out = P.pairs(M), []
    if not pairs:
        return out
    for k in range(1, DEPTH + 1):
        for h, body in pairs:
            h = re.sub(r"^r\(Q,", "rC(Q,%d," % k, h)
            h = re.sub(r"^(isk|prop|rel|setv)\(", r"\1C(", h)
            out.append("%s :- %s." % (h, ", ".join(_body(x, k) for x in body)))
        out.append("via(Q,%s,S) :- %s." % (q(M), ", ".join(_body(x, k) for x in pairs[0][1])))
    return out


def premises(found, via):
    """{(L, I): {M}} of `found` with each premise's chain followed back through `via` ({(L, I): {(M, S)}}): every
    line a firing came by, L's own (`self`) left out."""
    out = {}
    for key, ms in found.items():
        back, todo = set(ms), list(ms)
        while todo:
            m = todo.pop()
            for m2, s in via.get(key, ()):
                if m2 == m and s != "self" and s not in back:
                    back.add(s)
                    todo.append(s)
        out[key] = back
    return out
