"""The properties of an operation or an event of the domain model (b547, checking r66, r67; the contracts design's
C-1): what it promises beyond its outcomes, written on its model line and carried into the contract (contract_form).

An operation's line carries, after its parameters, any of `idempotent by <parameter>`, `compensated by <operation>`
(an operation of its own service, or `<service>.<operation>`) and `followed by <event>`, each ended by `;`, by the
next property or by `outcomes:`: `operation charge(order)  idempotent by order; compensated by refund`. An event's
line carries, after `raised by <service>.<operation>`, `; delivery: <text>` and `; when: <text>`.

`operation(text)` and `event(text)` give the line's text without its properties and the properties read, each a
`Property` whose `text` is how the line says it; `problems(model)` gives v_m8 of a property that refers to a
parameter, an operation or an event the model does not declare, as domain_model_check gives its own.
"""
import re
from dataclasses import dataclass

KEYS = ("idempotent by", "compensated by", "followed by")
EVENT_KEYS = ("delivery", "when")
_KEY = "|".join(k.replace(" ", r"\s+") for k in KEYS)
PROPERTY = re.compile(r"(?:^|(?<=[\s;)]))(?P<key>%s)\s+(?P<value>.+?)\s*(?=;|\s(?:%s)\s|\soutcomes:|$)"
                      % (_KEY, _KEY))


@dataclass(frozen=True)
class Property:
    key: str        # idempotent by, compensated by, followed by, delivery or when
    value: str

    @property
    def text(self):
        return "%s: %s" % (self.key, self.value) if self.key in EVENT_KEYS else "%s %s" % (self.key, self.value)


def operation(text):
    """(the operation's text with its properties taken out, its properties in order)."""
    found = [Property(" ".join(m.group("key").split()), m.group("value").strip()) for m in PROPERTY.finditer(text)]
    rest = PROPERTY.sub("", text)
    rest = re.sub(r"\s*;\s*(?=;|outcomes:|$)", " ", rest)
    rest = re.sub(r"\)\s*;", ")", rest)
    return " ".join(rest.split()), tuple(found)


def event(text):
    """(the event's `<phrase>: raised by <service>.<operation>`, its properties, each segment after `;` that is no
    property, which the reader refuses)."""
    head, *segments = [s.strip() for s in text.split(";")]
    props, stray = [], []
    for seg in (s for s in segments if s):
        key, sep, value = seg.partition(":")
        if sep and key.strip() in EVENT_KEYS and value.strip():
            props.append(Property(key.strip(), value.strip()))
        else:
            stray.append(seg)
    return head, tuple(props), tuple(stray)


def _operation_named(model, service, name):
    owner, _, op = name.rpartition(".")
    found = model.services.get(owner or service)
    return bool(found and found.operation(op))


def problems(model):
    """v_m8 of each property that refers to what the model does not declare, as (code, subject, message)."""
    events = {e.phrase for e in model.events}
    out = []
    for service in model.services.values():
        for op in service.operations:
            params = {name for name, _ in op.raw}
            for prop in op.properties:
                missing = {"idempotent by": lambda v: v not in params,
                           "compensated by": lambda v: not _operation_named(model, service.name, v),
                           "followed by": lambda v: v not in events}[prop.key](prop.value)
                if missing:
                    what = {"idempotent by": "a parameter of %s" % op.name, "compensated by": "an operation",
                            "followed by": "an event"}[prop.key]
                    out.append(("v_m8", "%s.%s %s" % (service.name, op.name, prop.text),
                                "%s: the property %s of %s.%s refers to %s, which is not %s the model declares"
                                % (op.where, prop.text, service.name, op.name, prop.value, what)))
    return out
