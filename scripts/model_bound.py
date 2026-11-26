"""The bound check's facts (b549, checking r95-r99; decisions 0116, 0126, 0127), for model_domain: what model.lp's
v_pb1-v_pb4 read, and v_m4 beside them, from the domain model (domain_model) and a parsed line's logical form (spec_lf).

Of the model (`model_facts`): `port_op(O)` of each operation of a service of a driven port (an area of kind `port`),
and `outcome(O, X, K)` of each outcome an operation declares, X its name (`stock.reserve done`, `stock.reserve
refused: no stock`: a refusal one outcome a reason) and K its kind (done, returned, passed, failed, refused), with
`outcome_reason(X, R)` of a refusal's reason R.

Of a line Q (`line_facts`): `port_line(Q)` when its capability's area is a driven port, else `core_line(Q)`;
`on_outcome(Q, K, Obj)` of each outcome kind K its trigger is on, the request pack's verb of a thing of the object Obj
("When the stock service completes a reservation": done and returned, model_domain_lines' `obj` of the reservation);
`on_reply(Q, K, O)` of each outcome kind K its trigger's reply is, to the request of O it names ("When the stock
service completes the request to reserve a note": reply-trigger, b724);
`denies(Q, O, K)` of each outcome kind K its response says the service never gives to the request of O its trigger
makes ("... shall not refuse the request": refused). model.lp joins them on the model's `op_object(O, Obj)`: a core
line on an outcome handles it, a core line on a reply of the outcome's kind to the request of its operation handles it
(a refusal each refusal reason), a port line that denies it excludes it.
"""
from spec_lf_core import Atom, Box, Ref

VERBS = {"complete": ("done", "returned"), "return": ("returned",), "refuse": ("refused",), "fail": ("failed",)}
KINDS = ("done", "returned", "passed", "failed", "refused")


def ported(model):
    """The names of the areas of kind `port`: the driven ports."""
    return {name for name, area in model.areas.items() if area.kind == "port"}


def model_facts(model):
    out, ports = [], ported(model)
    for op in model.operations():
        o = "%s.%s" % (op.service, op.name)
        service = model.services.get(op.service)
        if service is not None and service.area in ports:
            out.append(("port_op", o))
        for x in op.outcomes:
            if x.kind not in KINDS:
                continue
            if x.kind == "refused":
                for r in x.reasons:
                    name = "%s refused: %s" % (o, r)
                    out += [("outcome", o, name, "refused"), ("outcome_reason", name, r)]
            else:
                out.append(("outcome", o, "%s %s" % (o, x.kind), x.kind))
    return out


def _negated(items, under=False):
    """(atom, negated) of each atom of a response, a `not` box's atoms negated."""
    for x in items:
        if isinstance(x, Atom):
            yield x, under or (x.pred == "event" and x.args[2] == 0)
        elif isinstance(x, Box):
            inner = under or x.op == "not"
            yield from _negated(x.body, inner)
            if x.scope:
                yield from _negated(x.scope.body, inner)


def _replied(atom, ref):
    """True of the request atom a reply's object `ref` is (spec_lf_request's `replied`: its first argument the
    referent)."""
    return atom.pred == "request" and atom.args[0] == ref


def line_facts(lines, ident, form, port):
    """The facts of one parsed line: `lines` model_domain_lines' Lines (its `obj`), `port` whether its capability's
    area is a driven port."""
    out = [("port_line" if port else "core_line", ident)]
    trigger = next((p for p in form.parts if p.op in ("when", "if")), None)
    said = [a for a in (trigger.body if trigger else ()) if isinstance(a, Atom)]
    for a in said:
        if not lines.packed(a, VERBS):      # the request pack's sense, not a context's beside it (b847)
            continue
        for label, ref in a.args[3]:
            obj = lines.obj(getattr(ref, "kind", None)) if label != "subject" else None
            if obj:
                out += [("on_outcome", ident, k, obj) for k in VERBS[a.args[1]]]
        for role in a.args[3][1:]:     # a reply to the request of O (reply-trigger, b724)
            out += [("on_reply", ident, k, r.args[1]) for r in said if _replied(r, role[-1]) for k in VERBS[a.args[1]]]
    requested = [a.args[1] for a in said if a.pred == "request" and not isinstance(a.args[0], Ref)]
    response = [a for p in form.parts if p.op == "response" for a in _negated(p.body)]
    for a, negated in response:
        if negated and lines.packed(a, VERBS):
            out += [("denies", ident, o, k) for o in requested for k in VERBS[a.args[1]]]
    return out
