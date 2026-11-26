"""Handlers of features/product.feature's domain map (product r15-r21, b642), beside product_handlers.py, whose world,
Givens of instances, refusal and completion they share; each a `work_queue_world.local` tried before its. At the When
of `spec subdomain` or `spec context` the product the Givens describe is written into the product file with the id
`example.org` (the product's id i2 of a Given stands for it) and committed: before a subdomain is declared, each job
the Givens bring in, held unless a Given says this product does not hold it (`the bounded context b1 has the id i1`
kept as b1's id, which product_handlers_assign reads); before a bounded context is declared,
each subdomain, held unless a Given says not. The command is run with the values the instances stand for (`value`): a
subdomain type `core`, `central` when a Given says it does not conform to the subdomain type form; a bounded context's
id `bounded-context/example.org/<i>`, `bounded-context/other.org/<i>` when a Given says the product's id does not cover
it, without `bounded-context/` when a Given says it does not conform to the context id form (b793); a subdomain's id `<i>`;
a shop `example.org/shop-<s>`; a subdomain known by its id when the When gives one. The Thens read the subdomain
(with its type and jobs) or the bounded context (with its subdomains and its shop, none for a provider) back from
the kept product file, the product of a Given's shop (its id covering the shop's, b706), and what a
refusal names with its option."""
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
        return context_id(w, name, "other.org" if name in w.get("uncovered", ()) else "example.org")
    if kind == "shop":
        return "%s/shop-%s" % ("example.org" if name in w.get("products", {}) else "other.org", name)
    return name


def context_id(w, name, domain="example.org"):
    """A bounded context's id `bounded-context/<domain>/<i>` of the context id form, `<domain>/<i>` when a Given says
    it does not conform to the context id form (r37, r38, b793)."""
    return "%s/%s" % (domain, name) if name in w["unformed"] else "bounded-context/%s/%s" % (domain, name)


def given_has(step):
    """`this product has the id i2`: the product's id, which the product file gives as `example.org`; `the shop s1 has
    the product p1`: p1 is the shop's product, the shop's id one the product's id covers (b706, r34)."""
    if not P.mine(step) or step.term != "has":
        return False
    w = P.world(step)
    kinds = [w["kinds"].get(n) for n in step.names]
    if kinds == ["bounded context", "id"]:
        w.setdefault("context ids", {})[step.names[0]] = step.names[1]
    elif kinds[-1:] == ["id"]:
        w["product id"] = step.names[-1]
    elif len(step.names) == 2 and [w["kinds"].get(n) for n in step.names] == ["shop", "product"]:
        w.setdefault("products", {})[step.names[0]] = step.names[1]
    else:
        return False


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
        ident = value(w, kinds["id"]) if "id" in kinds else context_id(w, kinds["bounded context"])
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


def the_shops(step, w):
    """The product p1 is the product the shop that has it has (`given_has`): the kept product's id covers that shop's
    id, which the kept bounded context names as its shop (b706, r34)."""
    product, shops = P.kept(step), [s for s, p in w.get("products", {}).items() if p == step.names[0]]
    assert shops, "no shop has the product %s" % step.names[0]
    assert P.scripts("product_map").covers(product.get("id"), value(w, shops[0])), product
    assert product.get("contexts", {}).get(w["key"], {}).get("shop") == value(w, shops[0]), product


def then(step):
    """The product p1 holds x, p1 the shop's product (`the_shops`); this product holds x; `spec` writes x (one commit of the product file, x in it); `spec` names x (its value, and
    the option it is given by; the product's id, which the context's id lies outside)."""
    if not P.mine(step) or "when" not in P.world(step) or step.term not in ("holds", "write", "name"):
        return False
    w, done = P.world(step), step.context["result"]
    if step.term == "holds" and w["kinds"].get(step.names[0]) == "product":
        the_shops(step, w)
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
