"""The product a bounded context belongs to (b602, product r1-r7; decisions 0141, 0142): its id and purpose, its
actors and its jobs to be done, each job with its id, its actors, its job statement and the jobs it needs. A product
is a dict `{"id", "purpose", "actors": [...], "jobs": {id: {"actors", "statement", "needs"}}}`, read and kept by the
store the caller gives (product_store's). `declare` keeps the product's id and purpose, `declare_actor` an actor,
`declare_job` a job, a job declared again in place of the one of its id (its other keys kept, b673). A job is refused, naming the business
reference, when it has no product actor or one the product does not hold (checked first, b813), its statement is not of the job statement form (`conforms`, its form only), the product actor its
statement mentions is not the product's or not one of the job's actors (b798), an actor of it is not the product's, a need of it is no job the product holds, or a need depends on the job, directly or through the jobs
it needs (`depends`), so that needs never close a cycle."""
import re

from plumbing.shop_refused import Refused

# the job statement form: When <situation>, <actor> wants <motivation>, so they can <outcome>. The situation may hold
# commas (b674): the statement splits at the last ", <actor> wants" before ", so they can", an actor of no comma; a
# situation of one character is one too (b798).
FORM = re.compile(r"When (?P<situation>\S(?:(?:(?!, so they can ).)*\S)?), (?P<actor>\S[^,]*?) wants "
                  r"(?P<motivation>\S.*?), so they can (?P<outcome>\S.*)\.")
SAID = "When <situation>, <actor> wants <motivation>, so they can <outcome>."


def empty():
    return {"id": None, "purpose": None, "actors": [], "jobs": {}}


def conforms(statement):
    """Whether a job statement is of the job statement form."""
    return FORM.fullmatch(statement.strip()) is not None


def depends(jobs, need, job):
    """Whether the job `need` depends on `job`: it is the job, or needs it, directly or through the jobs it needs."""
    seen, todo = set(), [need]
    while todo:
        found = todo.pop()
        if found == job:
            return True
        if found not in seen:
            seen.add(found)
            todo.extend(jobs.get(found, {}).get("needs", []))
    return False


def declare(product, ident, purpose):
    """The product with its id and purpose; its actors and jobs kept."""
    return {**product, "id": ident, "purpose": purpose}


def declare_actor(product, actor):
    """The product with the actor among its actors (kept once)."""
    actors = product["actors"] if actor in product["actors"] else product["actors"] + [actor]
    return {**product, "actors": actors}


def declare_job(product, ident, actors, statement, needs):
    """The product with the job of `ident`; refused naming the job statement, an actor or a need as above, the
    product actor first: a job with none, or with one the product does not hold (b813)."""
    if not actors:
        raise Refused("a job is declared with its product actor: give {names}, an actor of the product",
                      reason="product actor outside the product", names=["parameter:product actor"])
    for actor in actors:
        if actor not in product["actors"]:
            raise Refused("{names} %r is no actor of the product" % actor, reason="product actor outside the product",
                          names=["parameter:product actor"])
    if not conforms(statement):
        raise Refused("{names} %r is not of the job statement form %s" % (statement, SAID),
                      reason="job statement not in the job statement form", names=["parameter:job statement"])
    said = FORM.fullmatch(statement.strip())["actor"]
    if said not in product["actors"]:
        raise Refused("the job statement mentions %r, no actor of the product: declare it with spec actor, then give it "
                      "as {names}" % said, reason="product actor outside the product", names=["parameter:product actor"])
    if said not in actors:
        raise Refused("{names} %r mentions the product actor %r, not the job's %s" % (
            statement.strip(), said, ", ".join(repr(a) for a in actors)),
            reason="job statement mentioning another product actor", names=["parameter:job statement"])
    for need in needs:
        if need not in product["jobs"]:
            raise Refused("{names} %s is no job of the product" % need, reason="need outside the product",
                          names=["parameter:need"])
    for need in needs:
        if depends(product["jobs"], need, ident):
            raise Refused("{names} %s depends on the job %s, so the needs would close a cycle" % (need, ident),
                          reason="need that depends on the job", names=["parameter:need"])
    job = {"actors": list(dict.fromkeys(actors)), "statement": statement.strip(), "needs": list(dict.fromkeys(needs))}
    return {**product, "jobs": {**product["jobs"], ident: {**product["jobs"].get(ident, {}), **job}}}
