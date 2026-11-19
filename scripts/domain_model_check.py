"""The domain model's own rules (the domain contract design, §5.5), read with no line: v_m8, a relation or an
attribute to an undeclared object, a transition over a value its attribute does not declare, two operations of one
name in a service, an event raised by no operation, and an object, service or actor declared twice; each as
(code, subject, message), which `model check` reports among its violations (model_spec's facts).
"""
from collections import Counter


def _declared(model):
    return set(model.objects) | set(model.actors) | set(model.services)


def _objects(model):
    known = _declared(model)
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


def problems(model):
    """v_m8 of `model`, as (code, subject, message) sorted."""
    twice = [("v_m8", name, "%s: the %s %s is declared again" % (where, kind, name))
             for kind, name, where in model.twice]
    return sorted(set(list(_objects(model)) + list(_services(model)) + twice))
