"""The facts of a requirement line against the domain model (the domain contract design, §5.5), for model_domain: what
model.lp's v_m2-v_m7 read, from a parsed line's logical form (spec_lf) and from the model (domain_model).

Of the model (`model_facts`): `operation(O)`, `op_param(O, P)`, `valued(O, P)` and `param_value(O, P, V)` of a
parameter with values, `op_by(O, A)` of each actor or kind an operation's `by` list allows, `actor_kind(A, K)` of an
actor's `kind of`, `op_reason(O, R)` of each declared `refused:` reason, and `lifecycle(Obj, T)`, `transition(Obj, T,
From, To)` of each lifecycle, and `op_area(O, A)`, `obj_area(Obj, A)` of the area each operation's service and each
object is declared in (v_m9, b610). O is an operation's id (`notes.add`), Obj an object's name, T its attribute's.

Of a line Q (`line_facts`): `requester(Q, O, A)` of its trigger's request of O by the actor A (a kind's name when a K
requests it: Q governs O), `asks(Q, O, D)` of a response's request of O by its doer D (response-request, b543), and
of a response's act of a verb naming O with no parameters, which spec_lf_facts keys `req(O,())` (`acted`, b571, b604),
`req_param(Q, O, P)` of each parameter either names, `req_value(Q, O, P, V)` of each value it gives one; `on_refusal(Q,
Obj)` of a trigger's refusal of a thing of the object Obj (beside the model's `op_object(O, Obj)`, O's object: a line
on the refusal of what a response asks O for states O's reasons, v_m4); `states_reason(Q,
O, R)` of each declared reason of O its refusal states, read by the reason's first noun (session's call, §5.5): a
named parameter states the reason whose first noun is the parameter, a named thing the reason that names its kind;
`sets(Q, Obj, T, From, To)` of a set of a lifecycle's attribute from the value its pre-state says, and
`sets_from_any(Q, Obj, T, To)` of one whose pre-state says none.
"""
import re

from spec_lf_core import Atom, Box, Ref

STOP = {"no", "not", "a", "an", "the", "such", "already", "in", "or", "and", "of", "this", "its", "unmet"}


def _bare(v):
    return str(v).strip().strip("`")


def first_noun(reason):
    """The first word of a reason that is no article, negation or particle ("no text" -> text)."""
    return next((w for w in re.findall(r"[a-z0-9-]+", reason.lower()) if w not in STOP), "")


def model_facts(model):
    out = []
    for s in model.services.values():
        out += [("op_area", "%s.%s" % (s.name, op.name), s.area) for op in s.operations]
    for op in model.operations():
        o = "%s.%s" % (op.service, op.name)
        out.append(("operation", o))
        for p in op.parameters:
            out.append(("op_param", o, p.name))
            if p.type == "values":
                out.append(("valued", o, p.name))
                out += [("param_value", o, p.name, v) for v in p.values]
        out += [("op_by", o, a) for a in getattr(op, "by", ())]
        out += [("op_reason", o, r) for x in op.outcomes if x.kind == "refused" for r in x.reasons]
        if op.object:
            out.append(("op_object", o, op.object))
    for a in model.actors.values():
        if a.kind_of:
            out.append(("actor_kind", a.name, a.kind_of))
    for obj in model.objects.values():
        out.append(("obj_area", obj.name, obj.area))
        for lc in obj.lifecycles:
            out.append(("lifecycle", obj.name, lc.attribute))
            out += [("transition", obj.name, lc.attribute, a, b) for a, b in lc.transitions]
    return out


def _atoms(items):
    for x in items:
        if isinstance(x, Atom):
            yield x
        elif isinstance(x, Box):
            yield from _atoms(x.body)
            if x.scope:
                yield from _atoms(x.scope.body)


class Lines:
    """The facts of the lines of one context: its model and its lexicon's kinds and attributes by their elements."""

    def __init__(self, model, lexicon):
        self.model = model
        self.objects = {t.term: t.element.split(".", 1)[1] for t in lexicon.of("kind") if t.element}
        self.attrs = {(k, t.term): t.element.rsplit(".", 1)[1] for t in lexicon.of("attribute") if t.element
                      for k in t.kinds}
        self.operations = {}     # (verb, sense) -> the operation it names, senses numbered as spec_logic_vocab's
        for t in lexicon.of("event"):
            sense = 1 + sum(1 for k in self.operations if k[0] == t.term and k[1] is not None)
            self.operations[(t.term, sense)] = t.operation
            self.operations[(t.term, None)] = t.operation     # with no sense, the verb's last, as spec_lf_ids'

    def obj(self, kind):
        return self.objects.get(kind)

    def facts(self, ident, form):
        out = []
        trigger = next((p for p in form.parts if p.op in ("when", "if")), None)
        pre = [a for p in form.parts if p.op in ("while", "where", "when", "if") for a in p.body
               if isinstance(a, Atom)]     # what the pre-state says, not what a box in it says
        response = [a for p in form.parts if p.op == "response" for a in _atoms(p.body)]
        reqs = [a for a in _atoms(trigger.body if trigger else ()) if a.pred == "request"]
        for req in reqs:
            out += self.request(ident, "requester", req, pre)
            out += self.reasons(ident, req.args[1], response)
        for req in (a for a in response if a.pred == "request"):     # a response's request (b543)
            out += self.request(ident, "asks", req, response)
        out += self.acted(ident, response)
        out += [("on_refusal", ident, self.obj(x.kind)) for x in self.refused(trigger) if self.obj(x.kind)]
        out += self.sets(ident, pre, response)
        return out

    def request(self, ident, pred, req, said):
        """`requester` (a trigger's) or `asks` (a response's) of a request atom, and its parameters `said` names."""
        e, o, _, _, roles = req.args
        out = [(pred, ident, o, self.doer(roles[0][1]))]
        for a in said:
            if a.pred in ("param", "noparam") and a.args[0] == e:
                out.append(("req_param", ident, o, a.args[1]))
                if a.pred == "param" and isinstance(a.args[2], str) and a.args[2].startswith("`"):
                    out.append(("req_value", ident, o, a.args[1], _bare(a.args[2])))
        return out

    def doer(self, who):
        """The actor a request's subject names, or the object of its kind (a K requests it)."""
        return who.value if who.origin == "constant" else self.obj(who.kind) or who.kind

    def acted(self, ident, response):
        """`asks` of a response's act of a verb naming an operation with no parameters (b604)."""
        out = []
        for a in response:
            o = a.pred == "event" and self.operations.get((a.args[1], a.args[2]))
            if o:
                out.append(("asks", ident, o, self.doer(a.args[3][0][1])))
        return out

    @staticmethod
    def refused(trigger):
        """The things a trigger's refusal is of: "If the stock service refuses a reservation" (the request pack's
        refuse), each its object's referent."""
        return [r[1] for a in (trigger.body if trigger else ()) if isinstance(a, Atom) and a.pred == "event"
                and a.args[1] == "refuse" for r in a.args[3][1:] if len(r) == 2 and isinstance(r[1], Ref)]

    def reasons(self, ident, o, response):
        service, _, name = o.rpartition(".")
        op = self.model.services[service].operation(name) if service in self.model.services else None
        if op is None or not any(a.pred == "event" and a.args[1] == "refuse" for a in response):
            return []
        declared = [r for x in op.outcomes if x.kind == "refused" for r in x.reasons]
        out = []
        for a in response:
            if a.pred != "event" or a.args[1] != "name":
                continue
            x = next((r[1] for r in a.args[3][1:] if len(r) == 2 and isinstance(r[1], Ref)), None)
            if x is None:
                continue
            if x.kind == "parameter":
                out += [("states_reason", ident, o, r) for r in declared if first_noun(r) == _bare(x.value).lower()]
            else:
                kind = (self.obj(x.kind) or x.kind).lower()
                out += [("states_reason", ident, o, r) for r in declared if kind in r.lower()]
        return out

    def sets(self, ident, pre, response):
        out = []
        for a in response:
            if a.pred != "initiates":
                continue
            _, _, x, term, value = a.args
            obj, attr = self.obj(x.kind), self.attrs.get((x.kind, term))
            if not obj or not attr:
                continue
            was = next((_bare(c.args[2]) for c in pre if c.pred == "attr" and c.args[0] == x and c.args[1] == term
                        and not isinstance(c.args[2], Ref)), None)
            if was is None:
                out.append(("sets_from_any", ident, obj, attr, _bare(value)))
            else:
                out.append(("sets", ident, obj, attr, was, _bare(value)))
        return out
