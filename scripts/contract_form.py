"""The contract form (b547, checking r64-r66; the contracts design's C-1, decision 0117): what a bounded context
publishes at a version in its own words, `contract.toml`, prepared by `spec prepare --contract <version>` from its
domain model and requirements and printed, nothing written.

The form: `context` (the id of `spec/index.md`) and `version` at the top; a table `[objects."<object>"]` of each
object (`area`, `kind_of`, `attributes`, `lifecycles`, `relations`, each written as the model block writes it); a
table `[operations."<service>.<operation>"]` of each operation (`parameters`, each `<name> (<type>)`; `outcomes`, each
`<kind> → <phrase>`; `reasons`, its refusal's; `requirements`, the requirements that govern it as `spec annotate`
gathers them, `<capability>#r<n>: <line>`; `properties`, domain_model_props'); a table `[events."<phrase>"]` of each
event (`raised_by`, `properties`). Every value but the top's and `area`, `kind_of` and `raised_by` is a list of
strings. `render(root, version)` gives the contract's text, `problems(text)` what keeps a text from conforming.
"""
import json
import tomllib
from pathlib import Path

TOP = {"context": str, "version": str}
TABLES = {"objects": {"area": str, "kind_of": str, "attributes": list, "lifecycles": list, "relations": list},
          "operations": {"parameters": list, "outcomes": list, "reasons": list, "requirements": list,
                         "properties": list},
          "events": {"raised_by": str, "properties": list}}


def _string(value):
    return json.dumps(value, ensure_ascii=False)


def _table(header, entries):
    out = ["", "[%s]" % header]
    for key, value in entries:
        if isinstance(value, str):
            out.append("%s = %s" % (key, _string(value)))
        elif value:
            out += ["%s = [" % key] + ["  %s," % _string(v) for v in value] + ["]"]
    return out


def _attribute(a):
    if a.type == "values":
        return "%s: %s" % (a.name, (" < " if a.ordered else " | ").join(a.values))
    if a.type == "object":
        return "%s → %s" % (a.name, " | ".join(a.targets))
    return "%s (%s)" % (a.name, a.type)


def _object(obj):
    return _table("objects.%s" % _string(obj.name), [
        ("area", obj.area or []), ("kind_of", obj.kind_of or []),
        ("attributes", [_attribute(a) for a in obj.attributes]),
        ("lifecycles", ["%s: %s" % (lc.attribute, "; ".join("%s → %s" % t for t in lc.transitions))
                        for lc in obj.lifecycles]),
        ("relations", ["%s → %s (%s)" % (r.phrase, " | ".join(r.targets), r.card) for r in obj.relations])])


def _parameter(p):
    if p.type == "values":
        return "%s (values: %s)" % (p.name, " | ".join(p.values))
    if p.type == "object":
        return "%s (object: %s)" % (p.name, " | ".join(p.targets))
    return "%s (%s)" % (p.name, p.type)


def _operation(service, op, governs):
    ident = "%s.%s" % (service, op.name)
    return _table("operations.%s" % _string(ident), [
        ("parameters", [_parameter(p) for p in op.parameters]),
        ("outcomes", [o.kind + (" → %s" % o.phrase if o.phrase else "") for o in op.outcomes]),
        ("reasons", [r for o in op.outcomes for r in o.reasons]),
        ("requirements", ["%s: %s" % pair for pair in governs.get(ident, [])]),
        ("properties", [p.text for p in op.properties])])


def _event(event):
    return _table("events.%s" % _string(event.phrase), [
        ("raised_by", "%s.%s" % (event.service, event.operation)),
        ("properties", [p.text for p in event.properties])])


def render(root, version):
    """The contract of the context at `root` at `version`, in the contract form."""
    import adapter_annotate
    import domain_model
    from model_parse import frontmatter
    model = domain_model.load(root)
    head, _ = frontmatter((Path(root) / "spec" / "index.md").read_text(encoding="utf-8"))
    governs = adapter_annotate.governing(root)
    out = ["context = %s" % _string(str(head.get("id", ""))), "version = %s" % _string(version)]
    for name in sorted(model.objects):
        out += _object(model.objects[name])
    for name in sorted(model.services):
        for op in model.services[name].operations:
            out += _operation(name, op, governs)
    for event in model.events:
        out += _event(event)
    return "\n".join(out) + "\n"


def _typed(where, data, keys):
    for key, value in data.items():
        want = keys.get(key)
        if want is None:
            yield "%s: %s is no key of the contract form" % (where, key)
        elif not isinstance(value, want) or want is list and not all(isinstance(v, str) for v in value):
            yield "%s: %s is not %s" % (where, key, "a string" if want is str else "a list of strings")


def problems(text):
    """What keeps `text` from conforming to the contract form, each a sentence; none of a contract that conforms."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as e:
        return ["the contract does not read as TOML: %s" % e]
    out = ["the contract has no %s" % key for key in TOP if not isinstance(data.get(key), str)]
    out += list(_typed("the contract", {k: v for k, v in data.items() if k not in TABLES}, TOP))
    for section, keys in TABLES.items():
        found = data.get(section, {})
        if not isinstance(found, dict):
            out.append("%s is not a table" % section)
            continue
        for name, table in found.items():
            if not isinstance(table, dict):
                out.append("%s.%s is not a table" % (section, name))
            else:
                out += list(_typed("%s.%s" % (section, name), table, keys))
    return out


def prepare(root, version):
    """`spec prepare`: the contract printed, nothing written."""
    print(render(root, version), end="")
    return 0
