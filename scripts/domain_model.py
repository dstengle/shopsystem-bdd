"""The domain model of a bounded context (the domain contract design, §4.1): every `spec/model/<area>.md` read once per
state of its files (`load`) into a `Model`: its areas (frontmatter `id`, `area`, `kind`, `imports`), objects,
services with their operations, events and actors, each block read by domain_model_parse. An operation acts on an
object (the one its first done or returned outcome names, else its first parameter naming an object), and each
parameter is typed: a flag when written `<name> (flag)`, by the values a parameter lists, else as an object when it
names one (or a kind of an imported pack that an object's relation, attribute or `kind of` names, b618) or a relation
of the operation's object, else by the attribute of that object it names, else text. `resolve` finds an element by its
qualified id (`object design-decision`, `attribute design-decision.tier`, `value design-decision.status accepted`,
`relation design-decision.supersedes`, `service decisions`, `operation decisions.enter`, `actor the person`,
`event <phrase>`), which spec_vocabulary's entries name. A context with no `spec/model/` has an empty Model.
"""
import re
from collections import namedtuple
from dataclasses import dataclass, field
from pathlib import Path

import domain_model_parse
from domain_model_parse import Parameter
from model_parse import frontmatter
from plumbing.shop_refused import Refused

Element = namedtuple("Element", "kind id area")
KINDS = ("object", "attribute", "value", "relation", "lifecycle", "service", "operation", "actor", "event")
FENCE = re.compile(r"^```model\s*$")
_CACHE = {}


@dataclass(frozen=True)
class Area:
    name: str
    kind: str = ""
    imports: tuple = ()
    id: str = ""
    path: str = ""


@dataclass
class Model:
    areas: dict = field(default_factory=dict)
    objects: dict = field(default_factory=dict)
    services: dict = field(default_factory=dict)
    events: list = field(default_factory=list)
    actors: dict = field(default_factory=dict)
    twice: list = field(default_factory=list)     # (kind, name, where) of an object, service or actor declared again
    asked: bool = False     # whether a parameter was looked up among the imported packs' kinds (b618)

    def operations(self):
        return [op for s in self.services.values() for op in s.operations]

    def resolve(self, ref):
        """The Element `ref` names (`<kind> <qualified id>`), or None."""
        kind, _, rest = " ".join(ref.split()).partition(" ")
        if kind == "object" and rest in self.objects:
            return Element(kind, rest, self.objects[rest].area)
        if kind in ("service", "actor"):
            found = (self.services if kind == "service" else self.actors).get(rest)
            return Element(kind, rest, found.area) if found else None
        if kind == "event":
            found = next((e for e in self.events if e.phrase == rest), None)
            return Element(kind, rest, found.area) if found else None
        if kind == "operation":
            service, _, name = rest.rpartition(".")
            found = self.services.get(service)
            return Element(kind, rest, found.area) if found and found.operation(name) else None
        return self._member(kind, rest)

    def _member(self, kind, rest):
        """An attribute, value, relation or lifecycle: `<object>.<name>`, a value's `<object>.<attribute> <value>`."""
        for name, obj in self.objects.items():
            if not rest.startswith(name + "."):
                continue
            tail = rest[len(name) + 1:]
            if kind == "relation" and obj.relation(tail):
                return Element(kind, rest, obj.area)
            if kind == "attribute" and obj.attribute(tail) or kind == "lifecycle" and any(
                    lc.attribute == tail for lc in obj.lifecycles):
                return Element(kind, rest, obj.area)
            if kind == "value":
                for a in obj.attributes:
                    if tail.startswith(a.name + " ") and tail[len(a.name) + 1:] in a.values:
                        return Element(kind, rest, obj.area)
        return None


def exists(root):
    """True when `root` has a domain model folder; looked once a held state (spec_held, b430)."""
    import spec_held
    return spec_held.memo(root, ("domain_model.exists",), lambda: (Path(root) / "spec" / "model").is_dir())


def _block(text):
    """(first line number, lines) of the file's ` ```model ` block; ([], 0) when it has none."""
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if FENCE.match(line)), None)
    if start is None:
        return 0, []
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("```")), len(lines))
    return start + 2, lines[start + 1:end]


def _area(path, where):
    text = path.read_text(encoding="utf-8")
    head, _ = frontmatter(text)
    name = str(head.get("area") or path.stem)
    imports = head.get("imports") or []
    area = Area(name, str(head.get("kind") or ""), tuple(imports) if isinstance(imports, list) else (str(imports),),
                str(head.get("id") or ""), where)
    first, lines = _block(text)
    return area, domain_model_parse.Reader(where, name).read(lines, first)


def _object_of(model, op):
    for o in op.outcomes:
        if o.kind in ("done", "returned"):
            head = re.sub(r"\s*\(.*\)$", "", re.sub(r"^(?:the|each|every|a|an)\s+", "", o.phrase)).strip()
            if head in model.objects:
                return head
    return next((name for name, _ in op.raw if name in model.objects), "")


def _parameter(model, obj, name, values, flags=(), packed=()):
    if name in flags:
        return Parameter(name, "flag")
    if values:
        return Parameter(name, "values", values)
    alternatives = tuple(a.strip() for a in name.split("|"))
    if all(a in model.objects or a in packed for a in alternatives):
        return Parameter(name, "object", targets=alternatives)
    rel = obj.relation(name) if obj else None
    if rel:
        return Parameter(name, "object", targets=rel.targets)
    attr = obj.attribute(name) if obj else None
    if attr and attr.type == "values":
        return Parameter(name, "values", attr.values)
    if attr and attr.type == "object":
        return Parameter(name, "object", targets=attr.targets)
    return Parameter(name, attr.type if attr else "text")


def _named(model):
    """What the model's objects name: each relation's and object attribute's targets and each `kind of`."""
    out = set()
    for obj in model.objects.values():
        out |= {t for rel in obj.relations for t in rel.targets} | {obj.kind_of}
        out |= {t for a in obj.attributes if a.type == "object" for t in a.targets}
    return out


def _resolve(model, packed=()):
    for op in model.operations():
        op.object = _object_of(model, op)
        obj = model.objects.get(op.object)
        op.parameters = tuple(_parameter(model, obj, name, values, op.flags, packed) for name, values in op.raw)


def read(root):
    """The Model of the context at `root`, unread (no cache)."""
    root = Path(root)
    model = Model()
    for path in sorted((root / "spec" / "model").glob("*.md")):
        area, reader = _area(path, path.relative_to(root).as_posix())
        if area.name in model.areas:
            raise Refused("%s: the area %s is declared again" % (area.path, area.name))
        model.areas[area.name] = area
        for kind, items, store in (("object", reader.objects, model.objects),
                                   ("service", reader.services, model.services),
                                   ("actor", reader.actors, model.actors)):
            for item in items:
                if item.name in store:
                    model.twice.append((kind, item.name, item.where))
                store.setdefault(item.name, item)
        model.events += reader.events
    names = {a.strip() for op in model.operations() for name, _ in op.raw for a in name.split("|")}
    wanted = names & _named(model) - set(model.objects)
    if wanted:      # only then the index read, so that a model of none stats no more (b430)
        import spec_packs  # here: spec_packs reads the lexicon, which reads this module
        model.asked, wanted = True, wanted & set(spec_packs.kinds(root))
    _resolve(model, wanted)
    return model


def _stamp(root, index=False):
    """The state of the model's files, and with `index` of `spec/index.md`, whose imports a model that asked reads."""
    out = []
    for p in ([Path(root) / "spec" / "index.md"] if index else []) + sorted((Path(root) / "spec" / "model").glob("*.md")):
        if not p.is_file():
            continue
        st = p.stat()
        out.append((p.name, st.st_mtime_ns, st.st_size))
    return tuple(out)


def load(root):
    """The Model of the context at `root`, read once per state of its `spec/model/` files (statted once a held state,
    spec_held, b430)."""
    import spec_held
    return spec_held.memo(root, ("domain_model",), lambda: _load(root))


def _load(root):
    key, stamp = str(Path(root).resolve()), _stamp(root)
    hit = _CACHE.get(key)
    if hit and hit[0] == stamp and (not hit[1].asked or hit[2] == _stamp(root, True)):
        return hit[1]
    model = read(root)
    _CACHE[key] = (stamp, model, _stamp(root, True) if model.asked else None)
    return model

