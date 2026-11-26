"""Handlers of features/product.feature's declarations taken back (product r45-r57, b795), beside product_handlers.py,
whose world, Givens of instances, refusal and completion they share; each a `work_queue_world.local` tried before its,
taking only a step of a scenario whose When unassigns or drops (`ours`). The Givens are kept as relations: a bounded
context that holds a job (assigned to it) or a product actor (mapped to `the person`), that addresses a subdomain, a
subdomain that serves a job, a job that needs a need, a job that has a product actor. At the When of `spec unassign`
or `spec drop` the product they describe is written into the product file with the id `example.org` and committed:
each job and need (a job `<j>`), each product actor (`the <p> user`), each subdomain (`<s>`, of type `core`) and each
bounded context (`bounded-context/example.org/<b>`) the Givens bring in, with those relations; a job unassigned from
a bounded context no Given says does not hold it is held by it (r50's world: r51's If takes precedence where it does
not hold the job). The command is run
with the values the instances stand for: `spec unassign <job> --from <bounded context>`, `spec drop job|actor|
subdomain|context <it>`. The Thens read the kept product file: the bounded context, or this product, not holding the
thing; the product service not keeping it (one commit of the product file, the thing out of the bounded context or
the product); what a refusal names (an error exit, the value)."""
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = sys.modules["shop_handlers_%s" % hashlib.sha256(str(HERE / "product_handlers.py").encode()).hexdigest()[:12]]
W = sys.modules["shop_work_queue_world"]
WHEN = re.compile(r"When the person (unassigns|drops) ")
STATEMENT = "When a change is wanted, %s wants it specified, so they can build it."
DROPPED = {"job": "job", "need": "job", "product actor": "actor", "subdomain": "subdomain", "bounded context": "context"}


def ours(step):
    if not P.mine(step):
        return False
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and any(s.type == "when" and WHEN.match("When " + s.name) for s in found.steps)


def world(step):
    return step.context.setdefault("drop", {"rels": []})


def value(w, name):
    kind = w["kinds"].get(name)
    if kind == "product actor":
        return "the %s user" % name
    if kind == "bounded context":
        return "bounded-context/example.org/%s" % name
    return name


def given_rel(step):
    """`the bounded context b1 holds the job j1`, `... addresses the subdomain s1`, `the subdomain s1 serves the job
    j1`, `the job j1 needs the need n1`, `the job j1 has the product actor p1`: kept as (verb, a, b)."""
    if not ours(step) or step.term not in ("hold", "holds", "address", "serve", "need", "has", "have"):
        return False
    verb = {"holds": "hold", "addresses": "address", "serves": "serve", "needs": "need", "has": "have"}
    world(step)["rels"].append((verb.get(step.term, step.term), *step.names[:2]))


def given_not(step):
    """`the bounded context b1 does not hold the job j1`: the job not assigned to it."""
    if not ours(step) or step.term not in ("hold", "holds"):
        return False
    world(step).setdefault("unheld", []).append(tuple(step.names[:2]))


def held(w):
    """The product the Givens describe."""
    kinds, rels = w["kinds"], w["rels"]
    product = {"id": "example.org", "actors": [], "jobs": {}, "subdomains": {}, "contexts": {}}
    for name, kind in kinds.items():
        if kind == "product actor":
            product["actors"].append(value(w, name))
    for name, kind in kinds.items():
        if kind in ("job", "need"):
            actors = [value(w, b) for v, a, b in rels if v == "have" and a == name]
            needs = [b for v, a, b in rels if v == "need" and a == name]
            speaker = actors[0] if actors else "the developer"
            product["jobs"][name] = {"actors": actors, "statement": STATEMENT % speaker,
                                     "needs": needs}
        if kind == "subdomain":
            product["subdomains"][name] = {"type": "core", "serves": [b for v, a, b in rels if v == "serve" and a == name]}
        if kind == "bounded context":
            entry = {"addresses": [b for v, a, b in rels if v == "address" and a == name]}
            jobs = [b for v, a, b in rels if v == "hold" and a == name and kinds.get(b) in ("job", "need")]
            actors = {value(w, b): "the person" for v, a, b in rels if v == "hold" and a == name
                      and kinds.get(b) == "product actor"}
            entry.update({"jobs": jobs} if jobs else {})
            entry.update({"actors": actors} if actors else {})
            product["contexts"][value(w, name)] = entry
    if "the developer" not in product["actors"] and any(not j["actors"] for j in product["jobs"].values()):
        product["actors"].append("the developer")
    return product


def runs(step):
    if not ours(step) or not step.term.startswith(("`spec unassign", "`spec drop")):
        return False
    w = world(step)
    w["kinds"] = P.world(step)["kinds"]
    repo, kinds = step.repo, {w["kinds"].get(n): n for n in step.names}
    if step.term.startswith("`spec unassign"):
        pair = (kinds["bounded context"], kinds["job"])
        if pair not in w.get("unheld", []) and ("hold", *pair) not in w["rels"]:
            w["rels"].append(("hold", *pair))     # r51's If takes precedence where it does not hold the job
        args = ["unassign", value(w, kinds["job"]), "--from", value(w, kinds["bounded context"])]
    else:
        name = step.names[-1]
        args = ["drop", DROPPED[w["kinds"][name]], value(w, name)]
    (repo / P.REL).parent.mkdir(parents=True, exist_ok=True)
    (repo / P.REL).write_text(P.scripts("product_store").render(held(w)))
    step.context["head"] = W.init(repo)
    w["when"], w["unassign"] = list(step.names), args[0] == "unassign"
    step.context["result"] = step.run("spec", *args)


def holds(step, w, owner, name):
    """Whether the kept product (owner None: this product) or its bounded context `owner` holds `name`."""
    kept, kind, it = P.kept(step), w["kinds"].get(name), value(w, name)
    if owner is not None:
        entry = kept.get("contexts", {}).get(value(w, owner), {})
        return it in entry.get("jobs", []) or it in entry.get("actors", {})
    part = {"job": "jobs", "need": "jobs", "subdomain": "subdomains", "bounded context": "contexts"}.get(kind)
    return it in kept.get("actors", []) if kind == "product actor" else it in kept.get(part, {})


def then_not(step):
    """The bounded context b1 (this product) does not hold x; the product service does not keep x (one commit of the
    product file, x out of the bounded context the When named, or out of the product)."""
    if not ours(step) or "when" not in world(step) or step.term not in ("hold", "holds", "write"):
        return False
    w, done = world(step), step.context["result"]
    said, name = done.stdout + done.stderr, step.names[-1]
    if step.term == "write":
        assert done.returncode == 0, said
        assert P.git(step.repo, "show", "--name-only", "--format=", "HEAD").split() == [P.REL]
        assert P.git(step.repo, "rev-parse", "HEAD").strip() != step.context["head"]
        owner = next((n for n in w["when"] if w["kinds"].get(n) == "bounded context"), None) if w["unassign"] else None
        if owner is not None:
            assert value(w, owner) in P.kept(step).get("contexts", {}), P.kept(step)
        assert not holds(step, w, owner, name), P.kept(step)
        return None
    owner = step.names[0] if len(step.names) > 1 else None
    assert not holds(step, w, owner, name), P.kept(step)


def then_names(step):
    """The product service names x: an error exit, x's value in what it said."""
    if not ours(step) or "when" not in world(step) or step.term != "name" or not step.names:
        return False
    done = step.context["result"]
    said = done.stdout + done.stderr
    assert done.returncode != 0 and value(world(step), step.names[-1]) in said, said


W.local("GivenDoes")(given_rel)
W.local("GivenDoesNot")(given_not)
W.local("WhenRuns")(runs)
W.local("ThenDoesNot")(then_not)
W.local("ThenDoes")(then_names)
