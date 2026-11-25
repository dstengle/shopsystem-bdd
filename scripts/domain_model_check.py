"""The domain model's own rules (the domain contract design, §5.5), read with no line: v_m8, a relation or an
attribute to an undeclared object (a kind of an imported pack declared, b609), a transition over a value its attribute does not declare, two operations of one
name in a service, an event raised by no operation, an object, service or actor declared twice, and a property
that refers to a parameter, an operation or an event the model does not declare (domain_model_props); each as
(code, subject, message), which `model check` reports among its violations (model_spec's facts).
"""
from collections import Counter

import domain_model_props


def _declared(model, kinds=()):
    """What a relation or an attribute may name: the model's objects, actors and services, and `kinds`, the kinds of
    the packs the index imports (b609)."""
    return set(model.objects) | set(model.actors) | set(model.services) | set(kinds)


def _objects(model, kinds=()):
    known = _declared(model, kinds)
    for obj in model.objects.values():
        for rel in obj.relations:
            for t in (t for t in rel.targets if t not in known):
                yield ("v_m8", "%s.%s" % (obj.name, rel.phrase), "%s: the relation %s of %s names %s, which the model "
                       "does not declare" % (obj.where, rel.phrase, obj.name, t))
        for attr in (a for a in obj.attributes if a.type == "object"):
            for t in (t for t in attr.targets if t not in known):
                yield ("v_m8", "%s.%s" % (obj.name, attr.name), "%s: the attribute %s of %s names %s, which the "
                       "model does not declare" % (obj.where, attr.name, obj.name, t))
        for lc in obj.lifecycles:
            values = obj.attribute(lc.attribute).values
            stray = sorted({v for step in lc.transitions for v in step if v not in values})
            if stray:
                yield ("v_m8", "%s.%s" % (obj.name, lc.attribute), "%s: the lifecycle %s of %s goes through %s, "
                       "which its values do not declare" % (obj.where, lc.attribute, obj.name, ", ".join(stray)))


def _services(model):
    for service in model.services.values():
        for name, n in Counter(op.name for op in service.operations).items():
            if n > 1:
                yield ("v_m8", "%s.%s" % (service.name, name), "%s: the service %s declares the operation %s %d "
                       "times" % (service.where, service.name, name, n))
    for event in model.events:
        service = model.services.get(event.service)
        if not service or not service.operation(event.operation):
            yield ("v_m8", event.phrase, "%s: the event %s is raised by %s.%s, which is no operation of the "
                   "model" % (event.where, event.phrase, event.service, event.operation))


def problems(model, kinds=()):
    """v_m8 of `model`, as (code, subject, message) sorted; `kinds` the imported packs' kinds (spec_packs' `kinds`),
    declared objects for the model."""
    twice = [("v_m8", name, "%s: the %s %s is declared again" % (where, kind, name))
             for kind, name, where in model.twice]
    return sorted(set(list(_objects(model, kinds)) + list(_services(model)) + twice +
                       domain_model_props.problems(model)))
