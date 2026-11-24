"""The entailment check's chain (b545, decision 0118, L-3 of the contracts design): a request a line states or a premise
forces fires the lines triggered on a request of its operation of the same requester (the lines that govern the operation,
each parameter a line's key names given the same value in the request's, a line of fewer parameters or none firing
too: `covers`, f1 of batch-81's review 1), and
what they force fires the lines triggered on it, up to DEPTH hops. A chain starts at a request only: an outcome
fires a line of the chain only after a request has led to it.

`chained` gives the lines a query's chain may reach (each a premise of the stratum C, `useC(Q,M)`), read off the
triggers and the responses alone; `rules` writes such a line's premise rules (spec_entail_rules' `pairs`) at each
depth k, its trigger read off `evC(Q,k-1,E,D,X,S)` (a request's key E its own key covers, `covers(Key,E)` of
`cover_facts`, or the act it is on; an event forced at depth k-1 by S, or a request stated or forced
outside the chain at depth 0: grammar/entail.lp), its responses `rC(Q,k,...)`, and `via(Q,M,S)`, the premise S its
firing came by, which spec_entail follows back so that a finding names every line of the chain."""
import re
from collections import defaultdict
from functools import cache

import clingo
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


@cache
def _key(e):
    """(the operation, {(parameter, value)}) of a request's key `req(O,Ps)`, else None."""
    try:
        t = clingo.parse_term(e)
    except RuntimeError:
        return None
    if t.name != "req" or len(t.arguments) != 2:
        return None
    return str(t.arguments[0]), frozenset((str(a.arguments[0]), str(a.arguments[1])) for a in t.arguments[1].arguments)


def covers(line, request):
    """Whether a line triggered on the key `line` governs the request of the key `request`: one operation, and each
    parameter the line's key names given the same value in the request's (a line of none covering every request)."""
    a, b = _key(line), _key(request)
    return a is not None and b is not None and a[0] == b[0] and a[1] <= b[1]


def fired(by_trig, kind, e):
    """[M] of the lines on event e: on a request, every line whose key covers it; on an act, the lines on it."""
    if kind != "req":
        return by_trig.get((kind, e), ())
    return [M for (k, key), ms in by_trig.items() if k == "req" and covers(key, e) for M in ms]


def cover_facts(P, lines):
    """`covers(Key,E)` of each request key E a line of P states and the key of each chain line in `lines` on a
    request that covers it, for the stratum C's join (`rules`)."""
    keys = {a[2] for f in P.reqs.values() for a in f["resp"] if a[1] == "pos" and a[2].startswith("req(")}
    own = {P.trig[M][1] for M in lines if M in P.trig and P.trig[M][0] == "req"}
    return ["covers(%s,%s)." % (q(k), q(e)) for k in sorted(own) for e in sorted(keys) if covers(k, e)]


def requesting(gives, M):
    return any(p == "pos" and e.startswith("req(") for p, e in gives[M])


def chained(P, L, sources, gives, by_trig):
    """[M]: the lines a request of L or of its premises `sources` reaches within DEPTH hops, none of L's own."""
    events = {e for M in set(sources) | {L} for p, e in gives[M] if p == "pos" and e.startswith("req(")}
    seen = set()
    for k in range(DEPTH):
        level = {M for e in events for kind in (("req", "does") if k else ("req",)) for M in fired(by_trig, kind, e)
                 if P.base[M] != P.base[L] and M not in seen}
        if not level:
            break
        seen |= level
        events = {e for M in level for p, e in gives[M] if p == "pos"}
    return sorted(seen)


def _body(x, k, key=None):
    if x.startswith("use(Q,"):
        return "useC(Q," + x[len("use(Q,"):]
    if key and x.startswith("ev(Q,req,%s," % key):     # a request its key covers (`covers`)
        return "evC(Q,%d,Ereq,%s,S), covers(%s,Ereq)" % (k - 1, x[len("ev(Q,req,%s," % key):-1], key)
    if x.startswith("ev(Q,"):     # the trigger: an event of the chain, `_` its kind (a request's key or an act)
        return re.sub(r"^ev\(Q,\w+,(.*)\)$", r"evC(Q,%d,\1,S)" % (k - 1), x)
    x = re.sub(r"^(isk|rel|prop)\(", r"\1all(", x)     # what the world, the strata A, B and the chain hold
    return re.sub(r"^(a|na)0\(", r"\g<1>1(", x)         # state 1, after the sets of stratum A


def rules(P, M):
    """M's premise rules in the stratum C at each depth 1..DEPTH, and `via(Q,M,S)`."""
    pairs, out = P.pairs(M), []
    if not pairs:
        return out
    key = q(P.trig[M][1]) if M in P.trig and P.trig[M][0] == "req" else None
    for k in range(1, DEPTH + 1):
        for h, body in pairs:
            h = re.sub(r"^r\(Q,", "rC(Q,%d," % k, h)
            h = re.sub(r"^(isk|prop|rel|setv)\(", r"\1C(", h)
            out.append("%s :- %s." % (h, ", ".join(_body(x, k, key) for x in body)))
        out.append("via(Q,%s,S) :- %s." % (q(M), ", ".join(_body(x, k, key) for x in pairs[0][1])))
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
