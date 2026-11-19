"""The facts of a requirement line against the domain model (the domain contract design, §5.5), for model_domain: what
model.lp's v_m2-v_m7 read, from a parsed line's logical form (spec_lf) and from the model (domain_model).

Of the model (`model_facts`): `operation(O)`, `op_param(O, P)`, `valued(O, P)` and `param_value(O, P, V)` of a
parameter with values, `op_by(O, A)` of each actor or kind an operation's `by` list allows, `actor_kind(A, K)` of an
actor's `kind of`, `op_reason(O, R)` of each declared `refused:` reason, and `lifecycle(Obj, T)`, `transition(Obj, T,
From, To)` of each lifecycle. O is an operation's id (`notes.add`), Obj an object's name, T its attribute's.

Of a line Q (`line_facts`): `requester(Q, O, A)` of a request of O by the actor A (a kind's name when a K requests it),
`req_param(Q, O, P)` of each parameter it names, `req_value(Q, O, P, V)` of each value it gives one; `states_reason(Q,
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
    for a in model.actors.values():
        if a.kind_of:
            out.append(("actor_kind", a.name, a.kind_of))
    for obj in model.objects.values():
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
            e, o, _, _, roles = req.args
            who = roles[0][1]
            out.append(("requester", ident, o, who.value if who.origin == "constant" else self.obj(who.kind) or who.kind))
            for a in pre:
                if a.pred in ("param", "noparam") and a.args[0] == e:
                    out.append(("req_param", ident, o, a.args[1]))
                    if a.pred == "param" and isinstance(a.args[2], str) and a.args[2].startswith("`"):
                        out.append(("req_value", ident, o, a.args[1], _bare(a.args[2])))
            out += self.reasons(ident, o, response)
        out += self.sets(ident, pre, response)
        return out

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
