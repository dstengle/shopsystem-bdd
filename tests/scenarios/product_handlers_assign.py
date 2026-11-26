"""Handlers of features/product.feature's assignments and mappings (product r22-r25, b675), beside product_handlers.py,
whose world, Givens of instances and completion they share; each a `work_queue_world.local` tried before its. At the
When of `spec assign` or `spec plays` the product the Givens describe is written into the product file with the id
`example.org` and committed: each job the Givens bring in, each product actor unless a Given says this product does
not hold it, and each bounded context unless a Given says this product does not hold it, by its id (product_handlers_map's
`context_id`: `bounded-context/example.org/<b>`, or of the id a Given says it has), with the jobs a Given says it
holds. The command is run with the values the instances stand for: a job `<j>`, a product actor `the <p> user`, an
actor `the <a> person`, and of a parameter the When does not give its adapter example (a bounded context
`bounded-context/example.org/x`, an actor `the person`). Mapped with this bounded context (r40, b798), the scenario's
repository is the bounded context `bounded-context/example.org/here` with a domain model whose one actor is `the
person`, so an actor a Given says this domain model does not hold, `the <a> person`, is none of it. The
Thens read the job under the bounded context's `jobs`, or the product actor under its `actors` called by the actor,
back from the kept product file, the run committing only it; a refusal an error exit, nothing committed, the value
named."""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = sys.modules["shop_handlers_%s" % hashlib.sha256(str(HERE / "product_handlers.py").encode()).hexdigest()[:12]]
W = sys.modules["shop_work_queue_world"]
COMMANDS = ("`spec assign`", "`spec plays`")
HERE_ID = "bounded-context/example.org/here"
MODEL = "---\nid: model/example.org/here/people\narea: people\nkind: core\nimports: []\n---\n\n# People\n\n" \
        "```model\nactor the person kind of agent\n```\n"


def here(repo):
    """This bounded context: its index and a domain model holding the actor `the person` alone (r40)."""
    (repo / "spec" / "model").mkdir(parents=True, exist_ok=True)
    (repo / "spec" / "index.md").write_text("---\nid: %s\ntitle: Here\nlanguage: codified-2\n---\n\n# Here\n" % HERE_ID)
    (repo / "spec" / "model" / "people.md").write_text(MODEL)
    return HERE_ID


def context_id(w, name):
    """product_handlers_map's `context_id`, loaded after this module."""
    key = "shop_handlers_%s" % hashlib.sha256(str(HERE / "product_handlers_map.py").encode()).hexdigest()[:12]
    return sys.modules[key].context_id(w, name)


def value(w, name):
    kind = w["kinds"].get(name)
    if kind == "bounded context" and name in w.get("context ids", {}):
        return value(w, w["context ids"][name])
    if kind in ("bounded context", "id"):
        return context_id(w, name)
    if kind == "product actor":
        return "the %s user" % name
    if kind == "actor":
        return "the %s person" % name
    return name


def given_holds(step):
    """`the bounded context b1 holds the job j1`: the job assigned to it before the run."""
    if not P.mine(step) or step.term not in ("hold", "holds"):
        return False
    w = P.world(step)
    if w["kinds"].get(step.names[0]) != "bounded context":
        return False
    w.setdefault("assigned", {}).setdefault(step.names[0], []).append(step.names[-1])


def held(w):
    """The product file's product before the run: its id, actors, jobs and bounded contexts, each context's jobs."""
    kinds, outside = w["kinds"], w["outside"]
    product = {"id": "example.org", "actors": [value(w, n) for n, k in kinds.items()
                                               if k == "product actor" and n not in outside], "jobs": {}}
    for name, kind in kinds.items():
        if kind == "job":
            product["jobs"][name] = {"actors": [], "statement": P.FORMED % name, "needs": []}
        if kind == "bounded context" and name not in outside:
            jobs = w.get("assigned", {}).get(name, [])
            product.setdefault("contexts", {})[value(w, name)] = {"addresses": [], **({"jobs": jobs} if jobs else {})}
    return product


def runs(step):
    if not P.mine(step) or step.term not in COMMANDS:
        return False
    w, repo = P.world(step), step.repo
    kinds = {w["kinds"].get(n): n for n in step.names}
    (repo / P.REL).parent.mkdir(parents=True, exist_ok=True)
    (repo / P.REL).write_text(P.scripts("product_store").render(held(w)))
    context = value(w, kinds["bounded context"]) if "bounded context" in kinds else context_id(w, "x")
    context = here(repo) if ("bounded context", "this bounded context") in step.params else context
    step.context["head"] = W.init(repo)
    if step.term == "`spec assign`":
        args = ["assign", value(w, kinds["job"]), "--to", context]
    else:
        actor = value(w, kinds["actor"]) if "actor" in kinds else "the person"
        args = ["plays", value(w, kinds["product actor"]), "--in", context, "--as", actor]
    w["assign"] = kinds
    step.context["result"] = step.run("spec", *args)


def holds(step, w, context, name):
    """Whether the kept product's bounded context `context` holds the job, or the product actor called by the actor
    the When gave."""
    kept = P.kept(step).get("contexts", {}).get(value(w, context), {})
    if w["kinds"].get(name) == "job":
        return value(w, name) in kept.get("jobs", [])
    given = w["assign"]
    return kept.get("actors", {}).get(value(w, name)) == value(w, given["actor"])


def then(step):
    """The bounded context b1 holds x; the product service keeps x (one commit of the product file, x under the
    bounded context the When named); names x (an error exit, its value)."""
    if not P.mine(step) or "assign" not in P.world(step) or step.term not in ("holds", "hold", "write", "keep", "name"):
        return False
    w, done = P.world(step), step.context["result"]
    said, name = done.stdout + done.stderr, step.names[-1] if step.names else None
    if step.term == "name":
        assert done.returncode != 0 and value(w, name) in said, said
        return None
    if step.term in ("write", "keep"):
        assert done.returncode == 0, said
        assert P.git(step.repo, "show", "--name-only", "--format=", "HEAD").split() == [P.REL]
        assert P.git(step.repo, "rev-parse", "HEAD").strip() != step.context["head"]
        context = w["assign"]["bounded context"]
    else:
        context = step.names[0]
    assert holds(step, w, context, name), P.kept(step)


W.local("GivenDoes")(given_holds)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then)
