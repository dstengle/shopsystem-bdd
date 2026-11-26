"""Handlers of features/product.feature's domain map (product r15-r21, b642), beside product_handlers.py, whose world,
Givens of instances, refusal and completion they share; each a `work_queue_world.local` tried before its. At the When
of `spec subdomain` or `spec context` the product the Givens describe is written into the product file with the id
`example.org` (the product's id i2 of a Given stands for it) and committed: before a subdomain is declared, each job
the Givens bring in, held unless a Given says this product does not hold it; before a bounded context is declared,
each subdomain, held unless a Given says not. The command is run with the values the instances stand for (`value`): a
subdomain type `core`, `central` when a Given says it does not conform to the subdomain type form; a bounded context's
id `example.org/<i>`, `other.org/<i>` when a Given says the product's id does not cover it; a subdomain's id `<i>`;
a shop `example.org/shop-<s>`; a subdomain known by its id when the When gives one. The Thens read the subdomain
(with its type and jobs) or the bounded context (with its subdomains and its shop, none for a provider) back from
the kept product file, and what a refusal names with its option."""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = sys.modules["shop_handlers_%s" % hashlib.sha256(str(HERE / "product_handlers.py").encode()).hexdigest()[:12]]
W = sys.modules["shop_work_queue_world"]
COMMANDS = ("`spec subdomain`", "`spec context`")
OPTIONS = {"subdomain type": "--type", "job": "--serves", "subdomain": "--addresses"}


def value(w, name):
    kind = w["kinds"].get(name)
    if kind == "subdomain type":
        return "central" if name in w["unformed"] else "core"
    if kind == "id" and name == w.get("product id"):
        return "example.org"
    if kind == "id" and w.get("context"):
        return "%s/%s" % ("other.org" if name in w.get("uncovered", ()) else "example.org", name)
    if kind == "shop":
        return "example.org/shop-%s" % name
    return name


def given_has(step):
    """`this product has the id i2`: the product's id, which the product file gives as `example.org`."""
    if not P.mine(step) or step.term != "has" or P.world(step)["kinds"].get(step.names[-1]) != "id":
        return False
    P.world(step)["product id"] = step.names[-1]


def given_not(step):
    """`the id i2 does not cover the id i1`: the bounded context's id i1 lies outside the product's."""
    if not P.mine(step) or step.term not in ("cover", "covers"):
        return False
    P.world(step).setdefault("uncovered", set()).add(step.names[-1])


def held(w, context):
    """The product file's product before the run: its id, and its jobs (a subdomain declared) or its subdomains (a
    bounded context declared)."""
    product = {"id": "example.org", "actors": [], "jobs": {}}
    for name, kind in w["kinds"].items():
        if name in w["outside"]:
            continue
        if kind == "job" and not context:
            product["jobs"][name] = {"actors": [], "statement": P.FORMED % name, "needs": []}
        if kind == "subdomain" and context:
            product.setdefault("subdomains", {})[name] = {"type": "core", "serves": []}
    return product


def runs(step):
    if not P.mine(step) or step.term not in COMMANDS:
        return False
    w, repo = P.world(step), step.repo
    w["context"] = step.term == "`spec context`"
    kinds = {w["kinds"].get(n): n for n in step.names}
    (repo / P.REL).parent.mkdir(parents=True, exist_ok=True)
    (repo / P.REL).write_text(P.scripts("product_store").render(held(w, w["context"])))
    step.context["head"] = W.init(repo)
    if w["context"]:
        ident = value(w, kinds["id"]) if "id" in kinds else "example.org/%s" % kinds["bounded context"]
        args = ["context", ident]
        args += ["--addresses", value(w, kinds["subdomain"])] if "subdomain" in kinds else []
        args += ["--shop", value(w, kinds["shop"])] if "shop" in kinds else []
    else:
        ident = value(w, kinds["id"]) if "id" in kinds else kinds["subdomain"]
        args = ["subdomain", ident, "--type", value(w, kinds["subdomain type"]) if "subdomain type" in kinds else "core"]
        args += ["--serves", value(w, kinds["job"])] if "job" in kinds else []
    w["key"], w["when"] = ident, kinds
    step.context["result"] = step.run("spec", *args)


def holds(step, w, name):
    """Whether the kept product holds the subdomain (its type and jobs as the When gave them) or the bounded context
    (its subdomains and its shop, none without one) of `name`."""
    product, kind, given = P.kept(step), w["kinds"].get(name), w["when"]
    if kind == "subdomain":
        want = {"type": value(w, given["subdomain type"]), "serves": [value(w, given["job"])]}
        return product.get("subdomains", {}).get(w["key"]) == want
    want = {"addresses": [value(w, given["subdomain"])]}
    want.update({"shop": value(w, given["shop"])} if "shop" in given else {})
    return product.get("contexts", {}).get(w["key"]) == want


def then(step):
    """This product holds x; `spec` writes x (one commit of the product file, x in it); `spec` names x (its value, and
    the option it is given by; the product's id, which the context's id lies outside)."""
    if not P.mine(step) or "when" not in P.world(step) or step.term not in ("holds", "write", "name"):
        return False
    w, done = P.world(step), step.context["result"]
    said, name = done.stdout + done.stderr, step.names[-1] if step.names else None
    if w["kinds"].get(name) not in ("subdomain", "bounded context", "subdomain type", "job", "id"):
        return False
    if step.term == "name":
        assert done.returncode != 0 and value(w, name) in said, said
        assert w["kinds"][name] == "id" or OPTIONS[w["kinds"][name]] in said, said
        return None
    if step.term == "write":
        assert done.returncode == 0, said
        assert P.git(step.repo, "show", "--name-only", "--format=", "HEAD").split() == [P.REL]
        assert P.git(step.repo, "rev-parse", "HEAD").strip() != step.context["head"]
    assert holds(step, w, name), P.kept(step)


W.local("GivenDoes")(given_has)
W.local("GivenDoesNot")(given_not)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then)
