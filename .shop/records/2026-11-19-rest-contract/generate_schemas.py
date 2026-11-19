"""The data schemas of the contract artifact, made from the domain model (2026-11-19-rest-contract, README.md).

Lays items b348 and b42 over a copy of `spec/` (backlog_lines.lay_onto), reads the domain model (domain_model.read)
and writes JSON Schema 2020-12 files under `schemas/` beside this file: the model's objects (`model.schema.json`),
the response envelope (`envelope.schema.json`), each operation's request and response (`operations.schema.json`) and
each event's notification (`events.schema.json`). With `--check` nothing is written: each file is made again and
compared, and every schema is checked against the 2020-12 meta-schema; either way each example of `examples.json`
is validated against the schema it names. The exit is 1 on a difference or an example that does not validate.

Rules (the README's "From the model to the schemas"):
- an object is a JSON object with its `reference`, its `text` when it is a kind of text or of file, and its attributes; a kind of another object extends it (allOf);
- an attribute of values is an enum, text a string, number a number, time a date-time string;
- a relation `holds` or `has` embeds its targets, a property each named by its kind (an object of no structure that is a kind of text as a string,
  any other as {reference, text}); any other relation names its target by reference;
- a parameter naming the operation's own object is not sent unless it is passed (PASSED); another object parameter
  is a reference, a version a string;
- a response is the envelope with the content an outcome phrase names and the refusal reasons the model declares.
"""
import dataclasses
import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import backlog_items
import backlog_lines
import domain_envelope
import domain_model

ITEMS = ("b348", "b42")
OPERATIONS = ("contracts.publish", "contracts.fetch", "contracts.obtain", "context requests.suggest")
EVENTS = ("contract published",)
OBJECTS = ("contract", "term proposal", "request line")
PASSED = {("context requests.suggest", "term proposal")}     # a parameter whose data the request carries
EMBED = ("holds", "has")
META = "https://json-schema.org/draft/2020-12/schema"
BASE = "https://shopsystem.missingmass.io/shopsystem-bdd/contract/"
VERSION = {"type": "string", "pattern": r"^\d+\.\d+\.\d+$", "description": "A version, <major>.<minor>.<patch>."}
REFERENCE = {"type": "string", "pattern": r"^[a-z][a-z -]*:\S.*$",
             "description": "A business reference `<kind>:<id>`, as `parameter:version` or `bounded context:<id>`."}


def snake(words):
    return words.strip().replace(" ", "_").replace("-", "_").replace(".", "_")


def model_ref(name):
    return {"$ref": "model.schema.json#/$defs/%s" % snake(name)}


def laid_model():
    copy = Path(tempfile.mkdtemp(prefix="contract-schemas-"))
    try:
        shutil.copytree(ROOT / "spec", copy / "spec")
        for name in ITEMS:
            backlog_lines.lay_onto(copy, backlog_items.find(str(ROOT), name))
        return domain_model.read(copy)
    finally:
        shutil.rmtree(copy, ignore_errors=True)


def bare(model, name):
    """Whether an object has no attribute and no relation of its own."""
    obj = model.objects.get(name)
    return obj is None or not (obj.attributes or obj.relations or obj.kind_of in model.objects)


def textlike(model, name):
    obj = model.objects.get(name)
    return name == "version" or (obj is not None and bare(model, name) and obj.kind_of == "text")


def target(model, name, embed):
    if name == "version":
        return dict(VERSION)
    if not embed:
        return {"$ref": "#/$defs/reference"} if name in OBJECTS else dict(REFERENCE, title=name)
    if name in OBJECTS:
        return {"$ref": "#/$defs/%s" % snake(name)}
    if textlike(model, name):
        return {"type": "string", "title": name}
    return {"type": "object", "title": name, "required": ["reference", "text"], "additionalProperties": False,
            "properties": {"reference": {"$ref": "#/$defs/reference"}, "text": {"type": "string"}}}


def attribute(attr):
    if attr.type == "values":
        return {"enum": list(attr.values)}
    if attr.type == "object":
        return {"$ref": "#/$defs/reference"}
    return {"number": {"type": "number"}, "time": {"type": "string", "format": "date-time"},
            "version": dict(VERSION)}.get(attr.type, {"type": "string"})


def relation(model, rel):
    embed = rel.phrase in EMBED
    one = [target(model, t, embed) for t in rel.targets]
    if rel.card.startswith("one"):
        return one[0] if len(one) == 1 else {"oneOf": one}
    if len(one) == 1:
        return {"type": "array", "items": one[0]}
    return {"type": "object", "additionalProperties": False,
            "properties": {snake(t): {"type": "array", "items": s} for t, s in zip(rel.targets, one)}}


def object_schema(model, name):
    obj = model.objects[name]
    props = {} if obj.kind_of in OBJECTS else {"reference": {"$ref": "#/$defs/reference"}}
    if obj.kind_of in ("text", "file"):                     # a text, or a file of text: what it says
        props["text"] = {"type": "string"}
    props.update({snake(a.name): attribute(a) for a in obj.attributes})
    for r in obj.relations:
        if r.phrase in EMBED:      # a held thing's property named by its kind
            props.update({snake(t): relation(model, dataclasses.replace(r, targets=(t,))) for t in r.targets})
        else:
            props[snake(r.phrase)] = relation(model, r)
    out = {"title": name, "type": "object", "properties": props}
    if not any(model.objects[o].kind_of == name for o in OBJECTS):   # a kind that others extend stays open
        out["unevaluatedProperties"] = False
    if obj.kind_of in OBJECTS:
        out["allOf"] = [{"$ref": "#/$defs/%s" % snake(obj.kind_of)}]
    return out


def content(model, phrase):
    words = phrase.split()
    many = bool(words) and words[0] in ("every", "each")
    head = " ".join(w for w in words if w not in ("the", "every", "each", "a", "an"))
    one = model_ref(head) if head in OBJECTS else dict(REFERENCE, title=head) if head else {}
    return {"type": "array", "items": one} if many else one


def request(model, op):
    o = "%s.%s" % (op.service, op.name)
    params = {}
    for p in op.parameters:
        if p.name == op.object and (o, p.name) not in PASSED:
            continue
        if (o, p.name) in PASSED:
            params[snake(p.name)] = model_ref(p.name)
        elif p.type == "values":
            params[snake(p.name)] = {"enum": list(p.values)}
        elif p.type == "flag":
            params[snake(p.name)] = {"type": "boolean"}
        elif p.name == "version" or "version" in p.targets:
            params[snake(p.name)] = dict(VERSION)
        else:
            params[snake(p.name)] = {"$ref": "envelope.schema.json#/$defs/reference"}
    return {"title": "the request of %s" % o, "type": "object", "required": ["operation", "parameters"],
            "additionalProperties": False,
            "properties": {"operation": {"const": o},
                           "parameters": {"type": "object", "properties": params, "additionalProperties": False}}}


def response(model, op):
    o = "%s.%s" % (op.service, op.name)
    cases = []
    for x in op.outcomes:
        if x.kind == "refused":
            error = {"allOf": [{"$ref": "envelope.schema.json#/$defs/error"}],
                     "properties": {"reason": {"enum": list(x.reasons)}}}
            cases.append({"properties": {"outcome": {"const": "refused"}, "content": {"type": "null"},
                                         "errors": {"type": "array", "minItems": 1, "items": error}}})
        else:
            kind = {"notifies": "done"}.get(x.kind, x.kind)
            cases.append({"properties": {"outcome": {"const": kind}, "content": content(model, x.phrase) or {}}})
    cases.append({"properties": {"outcome": {"const": "broken"}}})
    return {"title": "the response of %s" % o, "allOf": [{"$ref": "envelope.schema.json"}], "oneOf": cases}


def envelope():
    entry = {"type": "object", "required": ["reason", "names"], "additionalProperties": False,
             "properties": {"reason": {"type": "string"},
                            "names": {"type": "array", "items": {"$ref": "#/$defs/reference"}}}}
    return {"$schema": META, "$id": BASE + "envelope.schema.json", "title": "the response envelope",
            "description": domain_envelope.__doc__.split("\n\n")[0].replace("\n", " "),
            "type": "object", "required": ["outcome", "content", "errors", "notices"], "additionalProperties": False,
            "properties": {"outcome": {"enum": list(domain_envelope.OUTCOMES)}, "content": {},
                           "errors": {"type": "array", "items": {"$ref": "#/$defs/error"}},
                           "notices": {"type": "array", "items": {"$ref": "#/$defs/notice"}}},
            "allOf": [{"if": {"properties": {"outcome": {"enum": list(domain_envelope.ERRING)}}},
                       "then": {"properties": {"errors": {"minItems": 1}}},
                       "else": {"properties": {"errors": {"maxItems": 0}}}}],
            "$defs": {"reference": REFERENCE, "error": entry, "notice": entry}}


def schemas():
    model = laid_model()
    ops = {"%s.%s" % (op.service, op.name): op for op in model.operations()}
    defs = {snake(n): object_schema(model, n) for n in OBJECTS}
    defs["reference"] = REFERENCE
    files = {"envelope.schema.json": envelope(),
             "model.schema.json": {"$schema": META, "$id": BASE + "model.schema.json",
                                   "title": "the objects of the contract's operations", "$defs": defs}}
    odefs = {}
    for o in OPERATIONS:
        odefs[snake(o) + "_request"] = request(model, ops[o])
        odefs[snake(o) + "_response"] = response(model, ops[o])
    files["operations.schema.json"] = {"$schema": META, "$id": BASE + "operations.schema.json",
                                       "title": "the requests and responses of the contract's operations",
                                       "$defs": odefs}
    edefs = {}
    for e in (e for e in model.events if e.phrase in EVENTS):
        raised = ops["%s.%s" % (e.service, e.operation)]
        done = next(x for x in raised.outcomes if x.kind == "done")
        edefs[snake(e.phrase)] = {"title": "the notification of %s" % e.phrase, "type": "object",
                                  "required": ["event", "content"], "additionalProperties": False,
                                  "properties": {"event": {"const": e.phrase}, "content": content(model, done.phrase)}}
    files["events.schema.json"] = {"$schema": META, "$id": BASE + "events.schema.json",
                                   "title": "the notifications of the contract's events", "$defs": edefs}
    return files


def examples(files):
    """Each example of `examples.json` validated against the schema it names; the problems, each a line."""
    import jsonschema
    from referencing import Registry, Resource
    registry = Registry().with_resources((BASE + n, Resource.from_contents(s)) for n, s in files.items())
    out = []
    for ex in json.loads((HERE / "examples.json").read_text(encoding="utf-8")):
        validator = jsonschema.Draft202012Validator({"$ref": BASE + ex["schema"]}, registry=registry)
        errors = ["%s: %s" % (ex["name"], e.message[:200]) for e in validator.iter_errors(ex["instance"])]
        if ex.get("expect") == "invalid":
            errors = [] if errors else ["%s: it validates" % ex["name"]]
        out += errors
    return out


def main(argv):
    import jsonschema
    out = HERE / "schemas"
    differ = []
    files = schemas()
    for name in examples(files):
        differ.append("an example that does not validate: %s" % name)
    for name, schema in files.items():
        jsonschema.Draft202012Validator.check_schema(schema)
        text = json.dumps(schema, indent=2, ensure_ascii=False) + "\n"
        path = out / name
        if "--check" in argv:
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                differ.append(name)
        else:
            out.mkdir(exist_ok=True)
            path.write_text(text, encoding="utf-8")
    for name in differ:
        print(name if name.startswith("an example") else "stale: schemas/%s" % name)
    return 1 if differ else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
