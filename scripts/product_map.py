"""The product's domain map (b642, product r15-r21; decisions 0128, 0143): its subdomains, each by its id with its
subdomain type and the jobs it serves, and the bounded contexts that address them, each by its id with the subdomains
it addresses and the shop that keeps it, none for a third-party provider. In the product dict of product_layer,
`subdomains: {id: {"type", "serves"}}` and `contexts: {id: {"addresses", "shop"?}}`, kept by the store the caller
gives (product_store's). `declare_subdomain` keeps a subdomain and `declare_context` a bounded context, each declared
again in place of the one of its id (its other keys kept). A subdomain is refused, naming the parameter, when its type
is not of the subdomain type form (`TYPES`) or a job it serves is no job of the product; a bounded context when its id
lies outside the product's id (`covers`) or a subdomain it addresses is no subdomain of the product."""
from shop_refused import Refused

# the subdomain type form: the types of subdomain decision 0128 names
TYPES = ("core", "supporting", "generic")


def covers(product_id, ident):
    """Whether the product's id covers `ident`: its path opens with the product's id and goes on under it."""
    ident = ident.removeprefix("bounded-context/")
    return bool(product_id) and ident.startswith(product_id.rstrip("/") + "/") and len(ident) > len(product_id) + 1


def declare_subdomain(product, ident, kind, jobs):
    """The product with the subdomain of `ident`; refused naming the subdomain type or a job as above."""
    if kind not in TYPES:
        raise Refused("{names} %r is not of the subdomain type form: %s" % (kind, ", ".join(TYPES)),
                      reason="subdomain type not in the subdomain type form", names=["parameter:subdomain type"])
    for job in jobs:
        if job not in product["jobs"]:
            raise Refused("{names} %s is no job of the product" % job, reason="job outside the product",
                          names=["parameter:job"])
    held = product.get("subdomains", {})
    subdomain = {**held.get(ident, {}), "type": kind, "serves": list(dict.fromkeys(jobs))}
    return {**product, "subdomains": {**held, ident: subdomain}}


def declare_context(product, ident, subdomains, shop):
    """The product with the bounded context of `ident`, kept by `shop` or, with none, a third-party provider; refused
    naming the id or a subdomain as above."""
    if not covers(product.get("id"), ident):
        raise Refused("{names} %s lies outside the product's id %s" % (ident, product.get("id") or "(none declared)"),
                      reason="id outside the product", names=["parameter:id"])
    for subdomain in subdomains:
        if subdomain not in product.get("subdomains", {}):
            raise Refused("{names} %s is no subdomain of the product" % subdomain,
                          reason="subdomain outside the product", names=["parameter:subdomain"])
    held = product.get("contexts", {})
    context = {k: v for k, v in held.get(ident, {}).items() if k != "shop"}
    context["addresses"] = list(dict.fromkeys(subdomains))
    context.update({"shop": shop} if shop else {})
    return {**product, "contexts": {**held, ident: context}}
