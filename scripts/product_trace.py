"""A job's trace (b644, product r26-r30; decisions 0140, 0142): what a job of the product rests on, derived and never
listed. Its requirements are the lines of the requirement groups that serve it (a group's `serves:` line naming the
job by its name or its id: `serving`), then every line a request of a line in the trace reaches, a line triggered on a
request its key covers (spec_entail_chain's `covers`), followed again up to spec_entail_chain's DEPTH hops
(`reached`); its adapter specs each adapter spec nested at `adapters/<name>/` whose `realises:` names a port line in
the trace (`realising`); and the traces of the jobs it needs (the product file's needs, product_store), joined,
each requirement and adapter spec once with why it is in the trace. A job no group serves is refused naming it.
Provider operations an adapter spec uses are not followed: the trace stops at the adapter spec."""
from pathlib import Path

import product_store
import spec_context
import spec_entail_chain
from model_parse import as_list, frontmatter
from shop_refused import Refused
from spec_entail_rules import Premises, parse


def name_of(job):
    """A job's name: the last part of its id `job/<path>/<name>`, else the name itself."""
    return str(job).strip().rpartition("/")[2]


def serving(ctx, job):
    """[(requirement id, text, group id)] of the lines of the groups that serve `job`, in file order."""
    out = []
    for cap_name, cap in sorted(ctx.caps.items()):
        for group in cap.groups:
            if any(name_of(j) == name_of(job) for j in group.serves):
                out += [("%s#%s" % (cap_name, r.id), r.text, "%s#%s" % (cap_name, group.id))
                        for r in group.requirements]
    return out


def texts(ctx):
    return {"%s#%s" % (name, r.id): r.text for name, cap in ctx.caps.items() for g in cap.groups
            for r in g.requirements}


def reached(ctx, starts):
    """{requirement id: the line whose request reaches it} of the lines `starts`' requests reach within DEPTH hops,
    none of `starts`' own: each a line triggered on a request its key covers."""
    facts = list(ctx.domain) + [f for s in ctx.statements for f in ctx.facts[s.id]]
    reqs, dom = parse(facts)
    P = Premises(reqs, dom)
    asks = {M: [e for _, p, e, _, _ in f["resp"] if p == "pos" and e.startswith("req(")] for M, f in reqs.items()}
    by_trig = spec_entail_chain.triggers(P)
    seen, out = set(starts), {}
    frontier = {M for M in reqs if P.base[M] in seen}
    for _ in range(spec_entail_chain.DEPTH):
        level = {}
        for M in sorted(frontier):
            for e in asks[M]:
                for N in spec_entail_chain.fired(by_trig, "req", e):
                    if P.base[N] not in seen and P.base[N] not in level:
                        level[P.base[N]] = P.base[M]
        if not level:
            break
        out.update(level)
        seen |= set(level)
        frontier = {M for M in reqs if P.base[M] in level}
    return out


def adapter_specs(root):
    """[(adapter spec id, [requirement id])] of each adapter spec nested at `adapters/<name>/` and what it realises."""
    out = []
    for index in sorted(Path(root).glob("adapters/*/spec/index.md")):
        data, _ = frontmatter(index.read_text(encoding="utf-8"))
        if str(data.get("kind", "")).strip() == "adapter" and data.get("id"):
            out.append((str(data["id"]), [str(i).strip() for i in as_list(data.get("realises"))]))
    return out


def own(root, ctx, job):
    """(requirements, adapter specs) of `job` alone, each [(id, text, why)] and [(id, why)]; None when no group
    serves it."""
    lines = serving(ctx, job)
    if not lines:
        return None
    reqs = [(rid, text, "served by %s" % gid) for rid, text, gid in lines]
    said = texts(ctx)
    reqs += [(rid, said.get(rid, ""), "governs the operation %s uses" % by)
             for rid, by in reached(ctx, [rid for rid, _, _ in lines]).items() if rid in said]
    held = {rid for rid, _, _ in reqs}
    specs = [(ident, "realises the port line %s" % rid) for ident, ids in adapter_specs(root)
             for rid in ids if rid in held]
    first = {}
    for ident, why in specs:
        first.setdefault(ident, (ident, why))
    return reqs, list(first.values())


def trace(root, job):
    """{"job", "requirements": [{"id", "text", "why"}], "adapter specs": [{"id", "why"}]} of `job` with the traces
    of the jobs it needs joined, each id once; refused naming the job when no requirement group serves it."""
    ctx = spec_context.load(root)
    first = own(root, ctx, job)
    if first is None:
        raise Refused("{names} %s is served by no requirement group" % job,
                      reason="job that no requirement group serves", names=["parameter:job"])
    jobs = product_store.read(root)["jobs"]
    reqs, specs = {r[0]: r for r in first[0]}, {s[0]: s for s in first[1]}
    todo, seen = list(needs(jobs, job)), {name_of(job)}
    while todo:
        need = todo.pop(0)
        if name_of(need) in seen:
            continue
        seen.add(name_of(need))
        todo += needs(jobs, need)
        found = own(root, ctx, need)
        for rid, text, why in found[0] if found else ():
            reqs.setdefault(rid, (rid, text, "needed job %s: %s" % (need, why)))
        for ident, why in found[1] if found else ():
            specs.setdefault(ident, (ident, "needed job %s: %s" % (need, why)))
    return {"job": job, "requirements": [{"id": i, "text": t, "why": w} for i, t, w in reqs.values()],
            "adapter specs": [{"id": i, "why": w} for i, w in specs.values()]}


def needs(jobs, job):
    """The jobs the product file says `job` needs, by its id or its name."""
    found = jobs.get(job) or next((j for i, j in jobs.items() if name_of(i) == name_of(job)), None)
    return list(found.get("needs", [])) if found else []
