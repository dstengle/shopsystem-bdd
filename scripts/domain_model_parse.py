"""The domain model's block read (the domain contract design, §4.1): the ` ```model ` block of a `spec/model/<area>.md`
file parsed line by line into its elements (objects with attributes, lifecycles and relations; services with
operations, parameters and outcomes; events; actors), each a frozen record; a line that does not read refused through
`shop_refused.Refused` naming the file and the line. A logical line is an element's header (no indentation), a member
(two spaces: `attributes:`, `lifecycle`, `relations:`, `operation`) or `outcomes:` (four); a line indented deeper
continues the one before; `#` to the end of a line is a comment. domain_model gathers the files into a Model and gives
a parameter its type.
"""
import re
from dataclasses import dataclass, field

import domain_model_props
from shop_refused import Refused

TYPES = ("text", "number", "time", "version")
CARDS = ("one", "many", "one, optional")
OUTCOMES = ("done", "returned", "passed", "failed", "notifies")
MEMBERS = ("attributes:", "lifecycle ", "relations:", "operation ")
ARROW = re.compile(r"\s*(?:→|->)\s*")


@dataclass(frozen=True)
class Attribute:
    name: str
    values: tuple = ()      # in order: an ordered attribute's order
    type: str = ""          # text, number, time, version; "values" with values; "object" with a target
    targets: tuple = ()     # the objects an `area → area` attribute names
    ordered: bool = False   # its values written `a < b < c`: ordered as listed (by number when each is a version)


@dataclass(frozen=True)
class Lifecycle:
    attribute: str
    transitions: tuple      # (from, to) in order


@dataclass(frozen=True)
class Relation:
    phrase: str
    targets: tuple
    card: str


@dataclass
class Object:
    name: str
    area: str = ""
    where: str = ""
    kind_of: str = ""       # the kind it is a kind of (`object session kind of agent`): an object or a pack's kind
    attributes: list = field(default_factory=list)
    lifecycles: list = field(default_factory=list)
    relations: list = field(default_factory=list)

    def attribute(self, name):
        return next((a for a in self.attributes if a.name == name), None)

    def relation(self, phrase):
        return next((r for r in self.relations if r.phrase == phrase), None)


@dataclass(frozen=True)
class Parameter:
    name: str
    type: str = "text"      # values, object, flag, text, number, time or version (domain_model's resolution)
    values: tuple = ()
    targets: tuple = ()


@dataclass(frozen=True)
class Outcome:
    kind: str               # done, returned, passed, failed, notifies or refused
    phrase: str = ""        # what follows `→`
    reasons: tuple = ()     # a refusal's reasons, each a short business phrase


@dataclass
class Operation:
    service: str
    name: str
    raw: tuple = ()         # the parameters as written: (name, values)
    where: str = ""
    outcomes: list = field(default_factory=list)
    flags: tuple = ()       # the boolean parameters, written `<name> (flag)`
    by: tuple = ()          # the actors (or kinds of actor) that may request it, written `by <actor>, ...`; none: any
    parameters: tuple = ()  # resolved by domain_model
    object: str = ""        # the object it acts on (domain_model)
    properties: tuple = ()  # what it promises beyond its outcomes (domain_model_props)


@dataclass
class Service:
    name: str
    area: str = ""
    where: str = ""
    operations: list = field(default_factory=list)

    def operation(self, name):
        return next((o for o in self.operations if o.name == name), None)


@dataclass(frozen=True)
class Event:
    phrase: str
    service: str
    operation: str
    area: str = ""
    where: str = ""
    properties: tuple = ()  # its delivery and when (domain_model_props)


@dataclass(frozen=True)
class Actor:
    name: str
    kind_of: str = ""
    area: str = ""
    where: str = ""


def logical(lines, first):
    """(line number, indent, text) of each logical line of a block whose first line is `first`, continuations
    joined; a member line at two spaces that names no member refused by the caller."""
    out = []
    for n, raw in enumerate(lines, first):
        text = raw.split("#", 1)[0].rstrip()
        if not text.strip():
            continue
        indent = len(text) - len(text.lstrip(" "))
        body = text.strip()
        starts = indent == 0 or indent == 2 or indent == 4 and body.startswith("outcomes:")
        if starts or not out:
            out.append([n, indent, body])
        else:
            out[-1][2] += " " + body
    return out


class Reader:
    """The elements of one block, read in order; `where` is the file's path as the refusal names it."""

    def __init__(self, path, area):
        self.path, self.area = path, area
        self.objects, self.services, self.events, self.actors = [], [], [], []
        self.current = None

    def refuse(self, n, why):
        raise Refused("%s:%d: %s" % (self.path, n, why))

    def read(self, lines, first):
        for n, indent, body in logical(lines, first):
            self.where = "%s:%d" % (self.path, n)
            if indent == 0:
                self.header(n, body)
            elif indent == 2 and isinstance(self.current, list) and body.startswith(MEMBERS[:3]):
                self.member(n, body)
            elif indent == 2 and isinstance(self.current, Service) and body.startswith("operation "):
                self.operation(n, body[len("operation "):])
            elif indent == 4 and isinstance(self.current, Service) and self.current.operations:
                self.outcomes(n, self.current.operations[-1], body[len("outcomes:"):])
            else:
                self.refuse(n, "not a member of %s: %s" % ("an object" if isinstance(self.current, list)
                                                            else "a service" if self.current else "any element",
                                                            body))
        return self

    def header(self, n, body):
        word, _, rest = body.partition(" ")
        rest = rest.strip()
        if word == "object" and rest:
            names, _, kind = rest.partition(" kind of ")
            self.current = [Object(name.strip(), self.area, self.where, kind.strip()) for name in names.split(",")]
            self.objects += self.current
        elif word == "service" and rest:
            self.current = Service(rest, self.area, self.where)
            self.services.append(self.current)
        elif word == "event" and ":" in rest:
            self.event(n, rest)
        elif word == "actor" and rest:
            name, _, kind = rest.partition(" kind of ")
            self.actors.append(Actor(name.strip(), kind.strip(), self.area, self.where))
            self.current = None
        else:
            self.refuse(n, "not an object, a service, an event or an actor: %s" % body)

    def event(self, n, rest):
        rest, props, stray = domain_model_props.event(rest)
        if stray:
            self.refuse(n, "an event's property is `delivery: <text>` or `when: <text>`: %s" % stray[0])
        phrase, _, raised = rest.rpartition(":")
        raised = raised.strip()
        if not raised.startswith("raised by ") or "." not in raised:
            self.refuse(n, "an event is `event <phrase>: raised by <service>.<operation>`")
        service, _, op = raised[len("raised by "):].rpartition(".")
        self.events.append(Event(phrase.strip(), service.strip(), op.strip(), self.area, self.where, props))
        self.current = None

    def member(self, n, body):
        if len(self.current) > 1:
            self.refuse(n, "members follow an object declared alone")
        obj = self.current[0]
        if body.startswith("attributes:"):
            obj.attributes += self.attributes(n, body[len("attributes:"):])
        elif body.startswith("relations:"):
            obj.relations += [self.relation(n, seg) for seg in body[len("relations:"):].split(";") if seg.strip()]
        else:
            self.lifecycle(n, obj, body[len("lifecycle "):])

    def attributes(self, n, text):
        out = []
        for segment in text.split(";"):
            pending = []
            for item in (i.strip() for i in segment.split(",")):
                typed = re.match(r"^(.+?)\s*\((\w+)\)$", item)
                if typed and typed.group(2) in TYPES:
                    out += [Attribute(name, type=typed.group(2)) for name in pending + [typed.group(1)]]
                    pending = []
                elif ":" in item:
                    name, _, values = item.partition(":")
                    ordered = "<" in values
                    values = tuple(v.strip() for v in re.split(r"[|<]", values) if v.strip())
                    if not values:
                        self.refuse(n, "the attribute %s gives no values" % name.strip())
                    out += [Attribute(p, type="text") for p in pending] + [
                        Attribute(name.strip(), values, "values", ordered=ordered)]
                    pending = []
                elif ARROW.search(item):
                    name, target = ARROW.split(item, 1)
                    out.append(Attribute(name, type="object", targets=tuple(t.strip() for t in target.split("|"))))
                elif item:
                    pending.append(item)
            out += [Attribute(p, type="text") for p in pending]
        return out

    def relation(self, n, segment):
        found = re.match(r"^(.+?)\s*(?:→|->)\s*(.+?)\s*\(([^)]*)\)$", segment.strip())
        if not found or " ".join(found.group(3).split()) not in CARDS:
            self.refuse(n, "a relation is `<phrase> → <object> (one | many | one, optional)`: %s" % segment.strip())
        targets = tuple(t.strip() for t in found.group(2).split("|"))
        return Relation(found.group(1).strip(), targets, " ".join(found.group(3).split()))

    def lifecycle(self, n, obj, text):
        name, sep, rest = text.partition(":")
        steps = [ARROW.split(s.strip(), 1) for s in rest.split(";") if s.strip()]
        if not sep or not steps or any(len(s) != 2 or not all(s) for s in steps):
            self.refuse(n, "a lifecycle is `lifecycle <attribute>: <value> → <value>; ...`")
        transitions = tuple((a.strip(), b.strip()) for a, b in steps)
        states = tuple(dict.fromkeys(v for t in transitions for v in t))
        name = name.strip()
        if not obj.attribute(name):     # declared with its values, the lifecycle's states are checked (v_m8)
            obj.attributes.append(Attribute(name, states, "values"))
        obj.lifecycles.append(Lifecycle(name, transitions))

    def operation(self, n, text):
        text, props = domain_model_props.operation(text)
        found = re.match(r"^([^(]+)\((.*?)\)\s*(?:by\s+(.*?))?\s*(?:outcomes:(.*))?$", text)
        if not found:
            self.refuse(n, "an operation is `operation <name>(<parameter>, ...)`: %s" % text)
        raw = []
        flags = []
        for p in (p.strip() for p in found.group(2).split(",") if p.strip()):
            flag = re.match(r"^(.+?)\s*\(flag\)$", p)     # a boolean parameter: "with the X", "without the X"
            if flag:
                flags.append(flag.group(1).strip())
                raw.append((flag.group(1).strip(), ()))
                continue
            name, _, values = p.partition(":")
            raw.append((name.strip(), tuple(v.strip() for v in values.split("|") if v.strip())))
        by = tuple(a.strip() for a in (found.group(3) or "").split(",") if a.strip())
        op = Operation(self.current.name, found.group(1).strip(), tuple(raw), self.where, flags=tuple(flags), by=by,
                       properties=props)
        self.current.operations.append(op)
        if found.group(4):
            self.outcomes(n, op, found.group(4))

    def outcomes(self, n, op, text):
        for part in (p.strip() for p in text.split("|")):
            kind, phrase = _split(part)
            if kind == "refused":
                op.outcomes.append(Outcome("refused", reasons=tuple(r.strip() for r in phrase.split(",") if r.strip())))
            elif kind in OUTCOMES:
                op.outcomes.append(Outcome(kind, phrase))
            else:
                self.refuse(n, "an outcome is one of %s or refused: %s" % (", ".join(OUTCOMES), part))


def _split(part):
    """(kind, phrase) of an outcome: `done → the item`, `refused: no tier, id taken`, `passed`."""
    refused = re.match(r"^refused\s*(?::\s*(.*))?$", part)
    if refused:
        return "refused", refused.group(1) or ""
    kind, *phrase = ARROW.split(part, 1)
    return kind.strip(), (phrase[0].strip() if phrase else "")
