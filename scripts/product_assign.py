"""The product's domain map, its jobs and actors placed (b675, product r22-r25; decisions 0140, 0141): a job assigned
to the one bounded context whose capabilities serve it (`assign`), kept under the context's `jobs`, and a product
actor mapped to the actor a bounded context's model calls it by (`map_actor`), kept under the context's `actors` as
`{product actor: actor}`, in the product dict of product_layer (its `contexts`, product_map's), kept by the store the
caller gives (product_store's). A job is assigned once: one a bounded context holds already is refused naming the
job; a bounded context whose id is not of the context id form (product_map's `conformed`, b793) is refused naming the
id, and one the product does not hold naming the bounded context; a job the product does not declare is refused
naming the job (b809); a product actor the product does not hold is refused naming it,
and so is a mapping in a bounded context whose id is not of the context id form, naming the id, in one the product
does not hold, naming the bounded context (b824), or in this bounded
context to an actor its domain model does not hold, naming the actor (b798)."""
from plumbing.shop_refused import Refused
from product_map import conformed


def assign(product, job, context):
    """The product with `job` among the jobs of the bounded context `context`; refused naming the id when it is not of
    the context id form, the bounded context when the product does not hold it, and the job when it is
    no job of the product (b809) or a bounded context holds it already."""
    conformed(context, "parameter:bounded context")
    held = product.get("contexts", {})
    if context not in held:
        raise Refused("{names} %s is no bounded context of the product" % context,
                      reason="bounded context outside the product", names=["parameter:bounded context"])
    if job not in product.get("jobs", {}):
        raise Refused("{names} %s is no job of the product" % job, reason="job outside the product",
                      names=["parameter:job"])
    for ident, entry in held.items():
        if job in entry.get("jobs", []):
            raise Refused("{names} %s is assigned to the bounded context %s already" % (job, ident),
                          reason="job assigned already", names=["parameter:job"])
    entry = held.get(context, {})
    return {**product, "contexts": {**held, context: {**entry, "jobs": entry.get("jobs", []) + [job]}}}


def map_actor(product, actor, context, called, here=None):
    """The product with the product actor `actor` among the actors of the bounded context `context`, called `called`
    there; refused naming the id when it is not of the context id form, the product actor when the product does not
    hold it (before the actor, b813), the bounded context when the product does not hold it (b824), and the actor
    when `context` is this bounded context, `here` (its id, the actors its domain model holds), and its domain model
    does not hold it."""
    conformed(context, "parameter:bounded context")
    if actor not in product.get("actors", []):
        raise Refused("{names} %r is no actor of the product" % actor, reason="product actor outside the product",
                      names=["parameter:product actor"])
    held = product.get("contexts", {})
    if context not in held:
        raise Refused("{names} %s is no bounded context of the product" % context,
                      reason="bounded context outside the product", names=["parameter:bounded context"])
    if here and context == here[0] and called not in here[1]:
        raise Refused("{names} %r is no actor of the domain model of %s; it holds %s" % (
            called, context, ", ".join(repr(a) for a in sorted(here[1])) or "no actor"),
            reason="actor outside the domain model", names=["parameter:actor"])
    entry = held.get(context, {})
    return {**product, "contexts": {**held, context: {**entry, "actors": {**entry.get("actors", {}), actor: called}}}}
