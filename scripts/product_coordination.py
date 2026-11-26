"""A job's coordination (b680, product r31-r33; decision 0134): how its trace coordinates the requests it makes of
other bounded contexts, derived from the trace's lines and the domain model, never declared. Each line's requests
are model_domain_lines' `requester` and `asks` of it, read off its logical form; a port operation is one a port line
governs (model_bound's driven port: a line of a capability whose area is of kind `port` that requests it) or one of a
service of a driven port. Of the trace's operations:

- a saga: two port operations or more it uses, each with a property that refers to an operation (`compensated by`);
- a long-running process: a port operation it uses whose outcome a line handles (model_bound's `on_outcome` of the
  operation's object) and that line uses an operation that performs a transition (a line triggered on a request of
  it sets an attribute of a lifecycle: model_domain_lines' `sets`, `sets_from_any`);
- a port request: an operation it uses that a port line governs, that has no property that refers to an operation
  (`compensated by`, `REFERS`) and whose outcomes no line handles (r31 as reworded by f1, so that a saga's operations
  are no port request).

A saga is a long-running process too and is said first; a trace of no port operation has none (None)."""
from pathlib import Path

import domain_model
import model_bound
import model_domain_lines
import spec_grammar4
import spec_lexicon
import spec_lf
from model_parse import frontmatter

SAGA, PROCESS, REQUEST = "saga", "long-running process", "port request"
REFERS = ("compensated by",)     # the properties of domain_model_props that refer to an operation


def _facts(root, ctx):
    """{line id: [fact]} of each parsed line of the context, and the model."""
    model = domain_model.load(root)
    rgl, ports = spec_grammar4.load(root)[0], model_bound.ported(model)
    lines = model_domain_lines.Lines(model, spec_lexicon.read(root), rgl.verbs)
    areas = {}
    for name in ctx.caps:
        path = root / "spec" / "capabilities" / ("%s.md" % name)
        areas[name] = str(frontmatter(path.read_text())[0].get("area", "")) if path.is_file() else ""
    out = {}
    for s in ctx.statements:
        form = spec_lf.form(rgl, s.tree)
        port = areas.get(s.capability or "", "") in ports
        out[s.id] = lines.facts(s.id, form) + model_bound.line_facts(lines, s.id, form, port)
    return out, model


def coordination(root, ctx, traced):
    """The coordination of a job whose trace holds the requirement ids `traced`, or None."""
    if not domain_model.exists(root):
        return None
    facts, model = _facts(Path(root), ctx)
    uses = {q: {f[2] for f in fs if f[0] in ("requester", "asks")} for q, fs in facts.items()}
    port_lines = {q for q, fs in facts.items() if ("port_line", q) in fs}
    ops = {"%s.%s" % (op.service, op.name): op for op in model.operations()}
    ported = model_bound.ported(model)
    governed = {f[2] for q in port_lines for f in facts[q] if f[0] == "requester"}
    port_ops = governed | {o for o, op in ops.items() if getattr(model.services.get(op.service), "area", None) in ported}
    used = {o for q in traced for o in uses.get(q, ())} & port_ops
    if not used:
        return None
    compensated = {o for o in used if any(p.key in REFERS for p in ops[o].properties)}
    if len(compensated) >= 2:
        return SAGA
    transitions = {f[2] for fs in facts.values() for f in fs if f[0] == "requester"
                   and any(g[0] in ("sets", "sets_from_any") for g in fs)}
    handlers = {o: {q for q, fs in facts.items() for f in fs if f[0] == "on_outcome" and f[3] == ops[o].object}
                for o in used if ops[o].object}
    if any(uses[q] & transitions for hs in handlers.values() for q in hs):
        return PROCESS
    return REQUEST if any(not handlers.get(o) for o in (used & governed) - compensated) else None
