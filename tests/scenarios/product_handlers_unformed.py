"""Handlers of features/product.feature's declarations checked for their form and order (product r70-r74, b827),
beside product_handlers.py, whose Givens of instances and of what does not conform they share; each a
`work_queue_world.local` tried before the other product handlers', taking only a step of a scenario of r70-r74
(`ours`). The Givens are kept: this product's id (`this product has the id i1`, `example.org/i1`), this product with
no id, an id this product does not have. At the When of `spec product`, `spec actor` or `spec subdomain` the product
they describe is written into the product file and committed (its id `example.org` unless a Given gives it one or
says it has none), and the command run with the values the instances stand for (`value`): a product's id
`example.org/<i>`, `garden-<i>` (no dotted domain) when a Given says it does not conform to the product id form; a
product actor `the <p> user`, `<p> user` (no `the`) when it does not conform to the product actor form; a
subdomain's id `<i>`, `Watering_<i>` when it does not conform to the subdomain id form. The Thens read the refusal (an
error exit, no traceback, nothing committed) and what it names: the value, or this product's file."""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = sys.modules["shop_handlers_%s" % hashlib.sha256(str(HERE / "product_handlers.py").encode()).hexdigest()[:12]]
W = sys.modules["shop_work_queue_world"]
TAGS = {"r70", "r71", "r72", "r73", "r74"}
COMMANDS = {"`spec product`": "product", "`spec actor`": "actor", "`spec subdomain`": "subdomain"}


def ours(step):
    return P.mine(step) and bool(TAGS & {m.name for m in step.request.node.iter_markers()})


def world(step):
    return step.context.setdefault("unformed", {"id": "example.org"})


def value(step, name, command=None):
    w, p = world(step), P.world(step)
    kind, unformed = p["kinds"].get(name), name in p["unformed"]
    if kind == "product actor":
        return ("%s user" if unformed else "the %s user") % name
    if kind == "id" and command == "subdomain":
        return "Watering_%s" % name if unformed else name
    if kind == "id":
        return "garden-%s" % name if unformed else "example.org/%s" % name
    return w.get("values", {}).get(name, name)


def given_has(step):
    """`this product has the id i1`: the product file's id `example.org/i1`; `this product has no id`: none."""
    if not ours(step) or step.term not in ("has", "have"):
        return False
    world(step)["id"] = value(step, step.names[-1]) if step.names else None


def given_not(step):
    """`this product does not have the id i2`: the id the When gives is another than the product's."""
    if not ours(step) or step.term not in ("has", "have"):
        return False


def runs(step):
    if not ours(step) or step.term not in COMMANDS:
        return False
    w, repo, command = world(step), step.repo, COMMANDS[step.term]
    kinds = {P.world(step)["kinds"].get(n): n for n in step.names}
    (repo / P.REL).parent.mkdir(parents=True, exist_ok=True)
    (repo / P.REL).write_text(P.scripts("product_store").render({"id": w["id"], "actors": [], "jobs": {}}))
    step.context["head"] = W.init(repo)
    if command == "product":
        args = ["product", value(step, kinds["id"]), "--purpose", "The purpose of the product."]
    elif command == "actor":
        args = ["actor", value(step, kinds["product actor"])]
    else:
        args = ["subdomain", value(step, kinds["id"], command), "--type", "core"]
    w["command"] = command
    step.context["result"] = step.run("spec", *args)


def then(step):
    """`the product service refuses this request`; `... names the id i2` (its value), `... names this product` (the
    product file)."""
    if not ours(step) or "command" not in world(step) or step.term not in ("refuse", "name"):
        return False
    done = step.context["result"]
    said = done.stdout + done.stderr
    assert done.returncode != 0 and done.stderr.strip() and "Traceback" not in said, said
    if step.term == "refuse":
        assert P.git(step.repo, "rev-parse", "HEAD").strip() == step.context["head"]
        assert not P.git(step.repo, "status", "--porcelain", "--", P.REL).strip()
    elif step.names:
        assert value(step, step.names[-1], world(step)["command"]) in said, said
    else:
        assert P.REL in said, said


W.local("GivenDoes")(given_has)
W.local("GivenDoesNot")(given_not)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then)
