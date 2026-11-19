"""A request and the request pack's responses as `grammar/check.lp`'s facts (the domain contract design, §5.2, §5.3),
beside spec_lf_facts, whose walk calls it in a context that imports the request pack.

- The trigger: a `request(e, O, ...)` atom (spec_lf_request) with its parameters is `trig(R, req, req(O, Ps), D, X)`,
  O the operation's id (spec_lf_ids: the verb's model element), Ps the parameters the line says, each `p(P, V)` in
  name order (V a value or a code as its string, `some` of "with a p", `on` of a flag, `no` of "without", `thing` of a
  thing), D the requester and X the object, with each thing a parameter names after it (`pair(X, T)`, so that two
  triggers are one only when those things unify too); and `param(R, I, P, V)`, `noparam(R, I, P)` of each, I the
  trigger's request. Two triggers are one request when their operation and parameter sets are equal: a parameter
  absent from one line and given in another makes two triggers, as two option sets of a run did.
- The responses: the pack's verbs as the outcomes the check knows (`OUTCOMES`: refuse `refused`, return `returned`,
  complete `done`, fail `failed`, notify `notified`, keep `kept`, name `named`), each a `resp`, and a name also
  `names(R, I, X)`; any other verb is the context's (spec_lf_facts_atoms).
"""
import re

from spec_lf_core import Ref, const

OUTCOMES = {"refuse": "refused", "return": "returned", "complete": "done", "fail": "failed", "notify": "notified",
            "keep": "kept", "name": "named"}
# outcomes that say how a request ended, which one response of one request has only one of (check.lp's `outcome`)
ENDS = ("refused", "returned", "done", "failed")


def requests(part):
    """The request atoms of a trigger part (spec_lf_request's), in order."""
    return [a for a in part.body if getattr(a, "pred", None) == "request"]


def _value(walk, v):
    if v is None:
        return "no"
    if isinstance(v, Ref):
        return "thing" if v.origin not in ("constant", "parameter") else const(v.value)
    if v in ("some", "on"):
        return v
    return const(str(v).strip("`"))


def trigger(walk, part):
    """The facts of a trigger part with one request in it, or one request on each of "two Ks" (one operation, one
    requester: a `trig` of each, as spec_lf_distinct's `one_act` reads events); each other atom the pre-state's, as
    spec_lf_facts reads it."""
    found = requests(part)
    if len(found) != 1 and len({(a.args[1], a.args[4][0]) for a in found}) != 1:
        raise ValueError("no translation of a trigger with %d requests" % len(found))
    for n, atom in enumerate(found, 1):
        _request(walk, part, atom, n)
    for item in part.body:
        if item not in found and getattr(item, "pred", None) not in ("param", "noparam"):
            walk.literal(item)


def _request(walk, part, atom, n):
    e, _, verb, sense, roles = atom.args
    params = sorted((a.args[1], a.args[2] if a.pred == "param" else None) for a in part.body
                    if getattr(a, "pred", None) in ("param", "noparam") and a.args[0] == e)
    subject, kinds, _ = walk.slots(roles)
    things = [v for _, v in params if isinstance(v, Ref) and v.origin not in ("constant", "parameter")]
    obj = walk.obj(kinds) if kinds else "none"
    for t in things:
        obj = "pair(%s,%s)" % (obj, walk.term(t))
    said = ["p(%s,%s)" % (_slug(p), _value(walk, v)) for p, v in params]
    key = "req(%s,(%s))" % (walk.ids.event(verb, sense), ",".join(said) + ("," if len(said) == 1 else ""))
    walk.emit("trig", "req", key, walk.term(subject), obj)
    for p, v in params:
        if v is None:
            walk.emit("noparam", n, _slug(p))
        else:
            walk.emit("param", n, _slug(p), walk.term(v) if isinstance(v, Ref) else _value(walk, v))


def _slug(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "x"


def outcome(walk, verb):
    """The check's event of a verb of the request pack in a context that imports it, else None."""
    return OUTCOMES.get(verb) if walk.ids.request else None
