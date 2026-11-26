"""A job's trace (b644, product r26-r30; decisions 0140, 0142): what a job of the product rests on, derived and never
listed. Its requirements are the lines of the requirement groups that serve it (a group's `serves:` line naming the
job by its name or its id: `serving`), then every line a request of a line in the trace reaches, a line triggered on a
request its key covers (spec_entail_chain's `covers`), followed again up to spec_entail_chain's DEPTH hops
(`reached`); its adapter specs each adapter spec nested at `adapters/<name>/` whose `realises:` names a port line in
the trace (`realising`); and the traces of the jobs it needs (the product file's needs, product_store), joined,
each requirement and adapter spec once with why it is in the trace. A job no group serves is refused naming it, and
naming each open item one of whose groups serves it (`holders`, b814), so that the person traces it with that item.
An adapter spec in the trace is followed into its providers (b637, product r35; decision 0138): for each port
operation a port line in the trace governs, each provider operation its `uses:` names, the requirements the held
contract lists under it (adapter_uses' `governed`), each with the provider, its version and the operation
(`governed`), keyed by its provider and its id (`key`, b738), so that it is never taken for a line of this context
(`local`)."""
from pathlib import Path

import adapter_annotate
import adapter_uses
import product_coordination
import product_store
import spec_context
import spec_entail_chain
from model_parse import as_list, frontmatter
from plumbing.shop_refused import Refused
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
    """[(adapter spec id, [requirement id], its folder)] of each adapter spec nested at `adapters/<name>/` and what it
    realises."""
    out = []
    for index in sorted(Path(root).glob("adapters/*/spec/index.md")):
        data, _ = frontmatter(index.read_text(encoding="utf-8"))
        if str(data.get("kind", "")).strip() == "adapter" and data.get("id"):
            out.append((str(data["id"]), [str(i).strip() for i in as_list(data.get("realises"))], index.parent.parent))
    return out


def governed(root, specs, held):
    """[(provider id, requirement id, text, why)] of the requirements each held contract of an adapter spec in the
    trace lists under a provider operation it uses for a port operation a port line in the trace (`held`) governs."""
    specs = [(ident, folder) for ident, ids, folder in specs if held & set(ids)]
    if not specs:
        return []
    governing, out = adapter_annotate.governing(root), []
    for ident, folder in specs:
        for port, lines in sorted(adapter_uses.realised(folder, governing).items()):
            if not held & set(lines):
                continue
            for req, provider, version, used in adapter_uses.governed(folder, port):
                rid, _, text = str(req).partition(":")
                out.append((provider, rid.strip(), text.strip(), "governs the operation %s of %s@%s, which %s uses "
                            "for %s" % (used, provider, version, ident, port)))
    return out


def provided(root, specs, held):
    """[(requirement id, text, why)] of `governed`'s requirements, each by its provider's own id."""
    return [(rid, text, why) for _, rid, text, why in governed(root, specs, held)]


def key(provider, rid):
    """A provider's requirement keyed by its provider (b738): `<provider id less bounded-context/>:<id>`, so that
    an id equal to a requirement of this context, or of another provider, is neither dropped nor folded into it."""
    return "%s:%s" % (str(provider).strip().removeprefix("bounded-context/"), rid)


def local(rid):
    """Whether a trace's requirement id is this context's own, not a provider's `key`."""
    return ":" not in rid


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
    held, found = {rid for rid, _, _ in reqs}, adapter_specs(root)
    specs = [(ident, "realises the port line %s" % rid) for ident, ids, _ in found for rid in ids if rid in held]
    reqs += [(key(provider, rid), text, why) for provider, rid, text, why in governed(root, found, held)]
    first = {}
    for ident, why in specs:
        first.setdefault(ident, (ident, why))
    return reqs, list(first.values())


def joined(root, ctx, job, jobs):
    """(requirements, adapter specs) of `job` with those of the jobs it needs joined, each {id: (id, ..., why)} once,
    the needs read off the product's `jobs` (product_store's); None when no requirement group serves `job`."""
    first = own(root, ctx, job)
    if first is None:
        return None
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
    return reqs, specs


def trace(root, job):
    """{"job", "requirements": [{"id", "text", "why"}], "adapter specs": [{"id", "why"}]} of `job` with the traces
    of the jobs it needs joined, each id once; refused naming the job when no requirement group serves it, and each open item whose groups
    serve it (`holders`)."""
    ctx = spec_context.load(root)
    found = joined(root, ctx, job, product_store.read(root)["jobs"])
    if found is None:
        held = holders(root, job)
        said = "{names} %s is served by no requirement group" % job
        if held:    # b814: each open item whose groups serve it, so that the person traces it with the item
            said = "job %s is served by no requirement group; the item %s holds one that serves it: trace it " \
                   "with --item %s" % (job, ", ".join(held), held[0])
        raise Refused(said, reason="job that no requirement group serves",
                      names=["parameter:job"] + ["item:%s" % i for i in held])
    reqs, specs = found
    return {"job": job, "coordination": product_coordination.coordination(root, ctx, [r for r in reqs if local(r)]),
            "requirements": [{"id": i, "text": t, "why": w} for i, t, w in reqs.values()],
            "adapter specs": [{"id": i, "why": w} for i, w in specs.values()]}


def needs(jobs, job):
    """The jobs the product file says `job` needs, by its id or its name."""
    found = jobs.get(job) or next((j for i, j in jobs.items() if name_of(i) == name_of(job)), None)
    return list(found.get("needs", [])) if found else []


def holders(root, job):
    """The `b<n>` of each open item (not delivered, refused or withdrawn) whose `## Requirements` dedicates a group
    to `job` by its name or its id (backlog_section's `serves:` pairs); an item that does not read is passed over."""
    from backlog_items import items
    from backlog_retract import GONE
    from backlog_section import read
    out = []
    for item in items(root) if (Path(root) / ".shop" / "backlog").is_dir() else ():
        try:
            blocks = read(item, "the item %s" % item.name)
        except Refused:
            continue
        if item.status not in GONE and any(name_of(j) == name_of(job) for b in blocks for _, j in b.serves):
            out.append(item.name)
    return out
