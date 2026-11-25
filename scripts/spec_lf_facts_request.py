"""A request and the request pack's responses as `grammar/check.lp`'s facts (the domain contract design, §5.2, §5.3),
beside spec_lf_facts, whose walk calls it in a context that imports the request pack.

- The trigger: a `request(e, O, ...)` atom (spec_lf_request) with its parameters is `trig(R, req, req(O, Ps), D, X)`,
  O the operation's id (spec_lf_ids: the verb's model element), Ps the parameters the line says, each `p(P, V)` in
  name order (V a value or a code as its string, `some` of "with a p", `on` of a flag, `no` of "without", `thing` of a
  thing), D the requester and X the object, with each thing a parameter names after it (`pair(X, T)`, so that two
  triggers are one only when those things unify too); a value of a parameter that is the word of an attribute, a
  code or another thing's value of it (param-of, b418), is `val` in Ps and its referent in X as a thing's is, so that
  "with the title `a`" and "with the title of another note" are one request when the unification keeps one value;
  and `param(R, I, P, V)`, `noparam(R, I, P)` of each, I the
  trigger's request. Two triggers are one request when their operation and parameter sets are equal: a parameter
  absent from one line and given in another makes two triggers, as two option sets of a run did.
- A response's request (response-request, b543): a `resp` by its doer, the requester, whose event is the request's
  key `req(O, Ps)` with its object, as a trigger's is (`keyed`, b545), so that "shall publish ... with the summary
  `s1`" and "shall not publish ... with the summary `s2`" are two acts, and the entailment check follows the
  request to the lines on its key (`act`). A response's act of a verb naming an operation with no parameters is a
  request too, of the key `req(O,())` (`operated`, b571), and each response's request says its operation, its object
  before its parameters' things, its parameters and their things (`asked`), by which check.lp forbids a request whose
  key a "shall not"'s covers (spec_entail_chain's `covers`): "shall not publish the design-decision" clashes with
  "shall publish the design-decision with the summary `s1`" on one trigger.
- The responses: the pack's verbs as the outcomes the check knows (`OUTCOMES`: refuse `refused`, return `returned`,
  complete `done`, fail `failed`, notify `notified`, keep `kept`, name `named`), each a `resp`, and a name also
  `names(R, I, X)`; any other verb is the context's (spec_lf_facts_atoms).
"""
import re

import spec_lf_modal
from spec_lf_core import Ref, const

OUTCOMES = {"refuse": "refused", "return": "returned", "complete": "done", "fail": "failed", "notify": "notified",
            "keep": "kept", "name": "named"}
ASKED = ("request", "param", "noparam")     # a response's request and its parameters' atoms (`act`)
VAL = "val"     # the key's value of a parameter whose value is a referent of its attribute (`valued`)
# outcomes that say how a request ended, which one response of one request has only one of (check.lp's `outcome`)
ENDS = ("refused", "returned", "done", "failed")


def requests(part):
    """The request atoms of a trigger part (spec_lf_request's), in order."""
    return [a for a in part.body if getattr(a, "pred", None) == "request"]


def attribute(walk, p):
    return any(e.term == p for _, e in walk.ids.v.attrs.values())


def valued(walk, p, v):
    """True of a value of parameter p that is a value of p's attribute (param-of, b418, design-decision 0110): a code
    of it or another thing's value of it, both of kind p (spec_lf_request's `value_kind`), or a value it lists."""
    if isinstance(v, Ref):
        return v.kind == p and attribute(walk, p)
    return v not in (None, "some", "on") and attribute(walk, p)


def _term(walk, p, v):
    """The check's term of a parameter's value: a referent's, or of a listed value one named after the parameter."""
    if isinstance(v, Ref):
        return walk.term(v)
    name = "pv_%s" % _slug(p)
    walk.emit("role", name, walk.ids.kind(p))
    walk.emit("named", name, const(str(v)))
    return name


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
    params = _params(part.body, atom.args[0])
    key, subject, obj = keyed(walk, atom, params)
    walk.emit("trig", "req", key, subject, obj)
    for p, v in params:
        if v is None:
            walk.emit("noparam", n, _slug(p))
        else:
            walk.emit("param", n, _slug(p), walk.term(v) if isinstance(v, Ref) else _value(walk, v))


def _params(body, e):
    """[(parameter, value or None)] of request e's `param` and `noparam` atoms in `body`, in name order."""
    return sorted((a.args[1], a.args[2] if a.pred == "param" else None) for a in body
                  if getattr(a, "pred", None) in ("param", "noparam") and a.args[0] == e)


def keyed(walk, atom, params):
    """(the key `req(O,Ps)`, the requester's term, the object) of a request atom with its parameters, a trigger's or
    a response's alike: two requests are one when their keys are, so that a response's request of one code and a
    line on the request of another are two (batch-80 review 1 f5)."""
    parts = _parts(walk, atom, params)
    return parts[0], parts[1], parts[2]


def _parts(walk, atom, params):
    """`keyed`'s key, requester and object, then the operation's id, the object before the parameters' things, each
    parameter's (name, the key's value) and each thing a parameter names (name, term)."""
    _, _, verb, sense, roles = atom.args
    subject, kinds, _ = walk.slots(roles)
    base = obj = walk.obj(kinds) if kinds else "none"
    things = [(_slug(p), _term(walk, p, v)) for p, v in params
              if isinstance(v, Ref) and v.origin not in ("constant", "parameter") or valued(walk, p, v)]
    for _, t in things:
        obj = "pair(%s,%s)" % (obj, t)
    said = [(_slug(p), VAL if valued(walk, p, v) else _value(walk, v)) for p, v in params]
    op = walk.ids.event(verb, sense)
    key = "req(%s,(%s))" % (op, ",".join("p(%s,%s)" % ps for ps in said) + ("," if len(said) == 1 else ""))
    return key, walk.term(subject), obj, op, base, said, things


def _slug(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "x"


def outcome(walk, verb):
    """The check's event of a verb of the request pack in a context that imports it, else None."""
    return OUTCOMES.get(verb) if walk.ids.request else None


def act(walk, atom, body, pos):
    """The facts of a response's request atom (`ASKED`'s first) with its parameters' atoms in `body`: a `resp` whose
    event is the request's key, as a trigger's (`keyed`), by its doer, the requester; a parameter's atom alone is read
    with its request."""
    if atom.pred == "request":
        asked(walk, pos, *_parts(walk, atom, _params(body, atom.args[0])))


def operated(walk, e):
    """True of the event id of a verb naming an operation in a context that imports the request pack: a response's
    act of it with no parameters is a request too, of the key `req(O,())` (b571), which spec_lf_facts reads by
    `asked`."""
    return bool(walk.ids.request) and e in getattr(walk.ids.v, "operations", ())


def asked(walk, pos, key, subject, obj, op, base, said=(), things=()):
    """A response's request: its `resp`, and what check.lp's covering clash reads of it (b571): `rqo(R,I,O,X)` its
    operation and its object before the parameters' things, `rqp(R,I,P,V)` each parameter the key names with its
    value there, `rqt(R,I,P,T)` each thing a parameter names."""
    walk.acts += 1
    walk.emit("resp", walk.acts, spec_lf_modal.polarity(walk, pos), key, subject, obj)
    walk.emit("rqo", walk.acts, op, base)
    for p, v in said:
        walk.emit("rqp", walk.acts, p, v)
    for p, t in things:
        walk.emit("rqt", walk.acts, p, t)
