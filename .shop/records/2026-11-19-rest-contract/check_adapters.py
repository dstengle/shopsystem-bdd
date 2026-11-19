"""Both interface contracts of the contract artifact checked against the domain model (2026-11-19-rest-contract).

The model is read with b348 and b42 laid (generate_schemas.laid_model). Checked, both ways, as `spec check` checks
spec/adapters/cli.toml (v_a1-v_a4):
- http-adapter.openapi.yaml: every operation of OPERATIONS has one path and method whose operationId is its id, and
  every operationId names an operation of the model; every path, query and body field is a parameter the operation
  declares, and every parameter the request carries has a field; x-actors are actors its `by` allows; each response's
  x-outcome is one of its outcomes (or broken); every declared refusal reason is carried by exactly one response's
  x-reasons, and none is carried that the model does not declare; each webhook's x-event is an event of the model;
  every $ref resolves to a file and a JSON pointer in it.
- cli-adapter.toml: every operation of OPERATIONS has a table, every table names an operation of the model, every
  parameter is one its operation declares.
Prints each problem; the exit is 1 when there is any.
"""
import json
import sys
import tomllib

import generate_schemas as gen
import yaml

HERE = gen.HERE
METHODS = ("get", "put", "post", "delete", "patch")


def pointer(doc, fragment):
    for part in [p for p in fragment.split("/") if p]:
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(doc, dict) or part not in doc:
            return False
        doc = doc[part]
    return True


def refs(node, at=""):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str):
                yield at, v
            else:
                yield from refs(v, "%s/%s" % (at, k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from refs(v, "%s/%d" % (at, i))


def check_refs(api, problems):
    for at, ref in refs(api):
        path, _, fragment = ref.partition("#")
        if not path:
            ok = pointer(api, fragment)
        else:
            target = HERE / path
            ok = target.is_file() and pointer(json.loads(target.read_text(encoding="utf-8")), fragment)
        if not ok:
            problems.append("openapi %s: the $ref %s resolves to nothing" % (at, ref))


def sent(op):
    """The parameters a request of `op` carries, by their schema names (generate_schemas.request's)."""
    o = "%s.%s" % (op.service, op.name)
    return {gen.snake(p.name) for p in op.parameters if p.name != op.object or (o, p.name) in gen.PASSED}


def fields(api, operation):
    out = {p["name"] for p in operation.get("parameters", [])}
    body = operation.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
    ref = body.get("$ref", "")
    if ref.endswith("/properties/parameters"):
        path, _, fragment = ref.partition("#")
        doc = json.loads((HERE / path).read_text(encoding="utf-8"))
        for part in [p for p in fragment.split("/") if p]:
            doc = doc[part]
        out |= set(doc.get("properties", {}))
    elif "/properties/parameters/properties/" in ref:
        out.add(ref.rsplit("/", 1)[1])
    return out


def check_http(model, ops, problems):
    api = yaml.safe_load((HERE / "http-adapter.openapi.yaml").read_text(encoding="utf-8"))
    check_refs(api, problems)
    seen = {}
    for path, item in api.get("paths", {}).items():
        for method in (m for m in METHODS if m in item):
            operation = item[method]
            o = operation.get("operationId", "")
            if o in seen:
                problems.append("openapi %s %s: %s is mapped again (first at %s)" % (method, path, o, seen[o]))
            seen[o] = "%s %s" % (method, path)
            op = ops.get(o)
            if op is None:
                problems.append("openapi %s %s: the operationId %s names no operation of the model" % (method, path, o))
                continue
            given = fields(api, operation)
            for f in sorted(given - sent(op)):
                problems.append("openapi %s: the field %s is no parameter of the operation" % (o, f))
            for f in sorted(sent(op) - given):
                problems.append("openapi %s: the parameter %s has no field" % (o, f))
            for a in operation.get("x-actors", []):
                if op.by and a not in op.by:
                    problems.append("openapi %s: the actor %s is not one the model allows (%s)" % (o, a, ", ".join(op.by)))
            kinds = {x.kind for x in op.outcomes} | {"broken"}
            declared = [r for x in op.outcomes if x.kind == "refused" for r in x.reasons]
            carried = []
            for status, response in operation.get("responses", {}).items():
                if "$ref" in response:
                    continue
                if response.get("x-outcome") not in kinds:
                    problems.append("openapi %s %s: the outcome %s is not one of the operation's"
                                    % (o, status, response.get("x-outcome")))
                carried += response.get("x-reasons", [])
            for r in declared:
                if carried.count(r) != 1:
                    problems.append("openapi %s: the reason %r is carried by %d responses, not one"
                                    % (o, r, carried.count(r)))
            for r in sorted(set(carried) - set(declared)):
                problems.append("openapi %s: the reason %r is not one the model declares" % (o, r))
    for o in gen.OPERATIONS:
        if o not in seen:
            problems.append("openapi: the operation %s has no path" % o)
    events = {e.phrase for e in model.events}
    for name, item in api.get("webhooks", {}).items():
        for method in (m for m in METHODS if m in item):
            if item[method].get("x-event") not in events:
                problems.append("openapi webhook %s: the event %s is not one of the model"
                                % (name, item[method].get("x-event")))


def check_cli(ops, problems):
    contract = tomllib.loads((HERE / "cli-adapter.toml").read_text(encoding="utf-8"))
    tables = contract.get("operations", {})
    for o, table in tables.items():
        op = ops.get(o)
        if op is None:
            problems.append("cli %s: names no operation of the model" % o)
            continue
        names = {p.name for p in op.parameters}
        for p in table.get("parameters", {}):
            if p not in names:
                problems.append("cli %s: the parameter %s is not one the operation declares" % (o, p))
    for o in gen.OPERATIONS:
        if o not in tables:
            problems.append("cli: the operation %s has no table" % o)


def main():
    model = gen.laid_model()
    ops = {"%s.%s" % (op.service, op.name): op for op in model.operations()}
    problems = []
    check_http(model, ops, problems)
    check_cli(ops, problems)
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
