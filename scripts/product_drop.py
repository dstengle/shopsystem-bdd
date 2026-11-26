"""The product's declarations taken back (b795, product r45-r57): a job unassigned from the bounded context that holds
it (`unassign`), and a job, a product actor, a subdomain or a bounded context dropped from the product (`drop_job`,
`drop_actor`, `drop_subdomain`, `drop_context`), in the product dict of product_layer, kept by the store the caller
gives (product_store's). Nothing is dropped while something still refers to it: a job a job needs is refused naming
that job, one a bounded context holds naming the bounded context, one a subdomain serves naming the subdomain; a
product actor a job has (among its actors or in its job statement) naming the job, one a bounded context maps naming
the bounded context; a subdomain a bounded context addresses naming the bounded context; a bounded context that holds
a job naming the job. A job unassigned from a bounded context that does not hold it is refused naming the job, and a
declaration the product does not hold is refused naming it."""
from plumbing.shop_refused import Refused
from product_layer import FORM


def _held(product, part, ident, kind, names):
    if ident not in product.get(part, {}):
        raise Refused("{names} %s is no %s of the product" % (ident, kind), reason="%s outside the product" % kind,
                      names=[names])


def unassign(product, job, context):
    """The product with `job` out of the jobs of the bounded context `context`; refused naming the job when the
    bounded context does not hold it."""
    held = product.get("contexts", {})
    entry = held.get(context, {})
    if job not in entry.get("jobs", []):
        raise Refused("{names} %s is not assigned to the bounded context %s" % (job, context),
                      reason="job not assigned to the bounded context", names=["parameter:job"])
    jobs = [j for j in entry["jobs"] if j != job]
    entry = {k: v for k, v in entry.items() if k != "jobs"} | ({"jobs": jobs} if jobs else {})
    return {**product, "contexts": {**held, context: entry}}


def drop_job(product, job):
    """The product without the job `job`; refused as above."""
    _held(product, "jobs", job, "job", "parameter:job")
    for other, entry in product["jobs"].items():
        if job in entry.get("needs", []):
            raise Refused("the job %s needs %s: drop it first, or declare it again without the need; {names}" % (
                other, job), reason="job a job needs", names=["job:%s" % other])
    for context, entry in product.get("contexts", {}).items():
        if job in entry.get("jobs", []):
            raise Refused("the bounded context {names} holds the job %s: unassign it first" % job,
                          reason="job a bounded context holds", names=["bounded context:%s" % context])
    for subdomain, entry in product.get("subdomains", {}).items():
        if job in entry.get("serves", []):
            raise Refused("the subdomain {names} serves the job %s: declare it again without the job first" % job,
                          reason="job a subdomain serves", names=["subdomain:%s" % subdomain])
    return {**product, "jobs": {k: v for k, v in product["jobs"].items() if k != job}}


def _speaker(statement):
    found = FORM.fullmatch((statement or "").strip())
    return found and found["actor"]


def drop_actor(product, actor):
    """The product without the product actor `actor`; refused as above."""
    if actor not in product.get("actors", []):
        raise Refused("{names} %r is no actor of the product" % actor, reason="product actor outside the product",
                      names=["parameter:product actor"])
    for job, entry in product["jobs"].items():
        if actor in entry.get("actors", []) or _speaker(entry.get("statement")) == actor:
            raise Refused("the job {names} has the product actor %r: declare it again without it, or drop it first"
                          % actor, reason="product actor of a job", names=["job:%s" % job])
    for context, entry in product.get("contexts", {}).items():
        if actor in entry.get("actors", {}):
            raise Refused("the bounded context {names} maps the product actor %r" % actor,
                          reason="product actor a bounded context holds", names=["bounded context:%s" % context])
    return {**product, "actors": [a for a in product["actors"] if a != actor]}


def drop_subdomain(product, subdomain):
    """The product without the subdomain `subdomain`; refused as above."""
    _held(product, "subdomains", subdomain, "subdomain", "parameter:subdomain")
    for context, entry in product.get("contexts", {}).items():
        if subdomain in entry.get("addresses", []):
            raise Refused("the bounded context {names} addresses the subdomain %s: declare it again without it first"
                          % subdomain, reason="subdomain a bounded context addresses",
                          names=["bounded context:%s" % context])
    return {**product, "subdomains": {k: v for k, v in product["subdomains"].items() if k != subdomain}}


def drop_context(product, context):
    """The product without the bounded context `context`; refused as above."""
    _held(product, "contexts", context, "bounded context", "parameter:bounded context")
    jobs = product["contexts"][context].get("jobs", [])
    if jobs:
        raise Refused("the bounded context %s holds the job {names}: unassign it first" % context,
                      reason="bounded context that holds a job", names=["job:%s" % jobs[0]])
    return {**product, "contexts": {k: v for k, v in product["contexts"].items() if k != context}}
