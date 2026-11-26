"""The product check's facts in `spec`'s facts (`ProductReading`, b643, checking r114-r123; decisions 0140-0144): what
model.lp's v_job_elsewhere, v_need_cycle, w_unheld_job, w_untriggered_actor, w_unaddressed_sub, w_unreached_sub,
w_unserved_job and w_unserved_cap read, off the shop's product file (product_store's `.shop/product/product.toml`) and
the trace of each job this bounded context serves or holds (product_trace's `joined`, derived as `spec trace` derives
it). A job is named by its name (`name_of`), a bounded context by its id less `bounded-context/`.

Of the product: `pjob(J)`, `pjob_actor(J, P)` and `pneeds(J, N)` of each job; `held_by(J, B)` of each job a bounded
context's `jobs` hold and `here(B)` of this one (a job held here also a `job` node, which w_unserved_job reads);
`psub(S)` and `psub_serves(S, J)` of each subdomain; `addresses(B, S)` of each bounded context; `plays(P, A)` of each
product actor this bounded context maps to its actor A, and `triggers_as(P, Q)` of each requirement Q whose trigger's
request A makes (model_domain_lines' `requester`). Of this bounded context: `served_here(J)` of each job a requirement
group serves; `job_reaches(J, Q)` of each requirement of J's trace of its own (a provider's that an adapter spec's `uses:`
reaches left out, b637), and `job_reaches_context(J, B)` of this bounded
context when the trace holds a requirement and of each provider of an adapter spec in it (decision 0143).
A product file not of the product form `unformed_product(F, Why)` of its path and product_store's reason, which
w_unformed_product reads, so that the check names it and completes (r124, b695); nothing else read of it. The trace is derived only when a job has a serving group."""
import re
from pathlib import Path

import product_store
from model_parse import as_list, frontmatter
from plumbing.shop_refused import Refused

PROVIDER = re.compile(r"^(?:bounded-context/)?(?P<id>[^@\s]+)")


def name_of(job):
    """A job's name: the last part of its id, as product_trace's `name_of` reads it."""
    return str(job).strip().rpartition("/")[2]


def bare(context):
    """A bounded context's id less `bounded-context/`."""
    return str(context or "").strip().removeprefix("bounded-context/")


def said(actor):
    """An actor's term as compared: lowercased, its article left out."""
    return " ".join(str(actor).lower().removeprefix("the ").split())


def providers(root, ident):
    """The bounded contexts the adapter spec `ident` names under `providers:`."""
    for index in sorted(Path(root).glob("adapters/*/spec/index.md")):
        data, _ = frontmatter(index.read_text(encoding="utf-8"))
        if str(data.get("id", "")).strip() == ident:
            return [m.group("id") for m in (PROVIDER.match(str(p).strip()) for p in as_list(data.get("providers")))
                    if m]
    return []


class ProductReading:
    def read_product(self):
        try:
            product = product_store.read(self.root)
        except Refused as why:
            self.fact("unformed_product", product_store.REL, why.reason)
            return
        name = name_of
        here = bare(self.context)
        self.fact("here", here)
        for job, entry in product["jobs"].items():
            self.fact("pjob", name(job))
            for actor in entry.get("actors", []):
                self.fact("pjob_actor", name(job), actor)
            for need in entry.get("needs", []):
                self.fact("pneeds", name(job), name(need))
        held = set()
        for context, entry in product.get("contexts", {}).items():
            for job in entry.get("jobs", []):
                self.fact("held_by", name(job), bare(context))
                held |= {name(job)} if bare(context) == here else set()
            for subdomain in entry.get("addresses", []):
                self.fact("addresses", bare(context), subdomain)
        for subdomain, entry in product.get("subdomains", {}).items():
            self.fact("psub", subdomain)
            for job in entry.get("serves", []):
                self.fact("psub_serves", subdomain, name(job))
        for job in sorted(held):
            self.node(self.qualify(job, "job"), "job")
        self.read_actors(product.get("contexts", {}).get(here) or next(
            (e for c, e in product.get("contexts", {}).items() if bare(c) == here), {}))
        served = {name(j) for g in self.groups.values() for j in g.serves}
        for job in sorted(served):
            self.fact("served_here", job)
        if served:
            self.read_traces(product, sorted(served | held), here)

    def read_actors(self, entry):
        requested = [(args[0], args[2]) for pred, args in self.facts if pred == "requester"]
        for actor, called in entry.get("actors", {}).items():
            self.fact("plays", actor, called)
            for q, by in requested:
                if said(by) == said(called):
                    self.fact("triggers_as", actor, q)

    def read_traces(self, product, jobs, here):
        # here, not above: product_trace imports clingo, which `spec check` may have to run again to find
        import product_trace
        import spec_context
        ctx = spec_context.load(self.root)
        caps = {entry["name"]: cap for cap, entry in self.caps.items()}
        for job in jobs:
            found = product_trace.joined(self.root, ctx, job, product["jobs"])
            if found is None:
                continue
            reqs, specs = found
            for rid in reqs:
                if not product_trace.local(rid):    # a provider's requirement an adapter spec's uses: reaches (b637)
                    continue
                cap, _, n = rid.partition("#")
                self.fact("job_reaches", job, "%s#%s" % (caps.get(cap, cap), n))
            reached = ([here] if reqs else []) + [p for ident in specs for p in providers(self.root, ident)]
            for context in dict.fromkeys(reached):
                self.fact("job_reaches_context", job, bare(context))
