"""Handlers of features/product.feature (product r1-r7, b602), each a `work_queue_world.local` that takes only a step of
a scenario of the product's feature (`mine`). The Givens are recorded; at the When of `spec job` the product they describe is
written into the product file (product_store's `render`) and committed, and `spec product`, `spec actor` or `spec job`
run with the values the instances stand for (`value`): a product actor p1 is `the p1 user`, held by the product unless
a Given says it is not; a need n1 is the job `n1`, held unless a Given says not, needing the job j1 when it depends on
it (so the product holds j1 too); a job statement j2 is of the job statement form unless a Given says it does not
conform, its text the given block's when it holds one (b674, r14), each product actor then standing for the actor
that text names (r44, b798); a statement of the form names the product actor a Given says it mentions, else the one
the When gives, else one named as the statement (`the j2 user`), and the product holds the actor it names unless a
Given says it does not hold that product actor (r42, r43, b798); an id i1 is `example.org/i1` of a product and `i1`
of a job, a job known by its id when the When gives one. A job the When declares with no statement is given one of
the form, so that only what the line says is wrong. A
product detail p1 is a table `[p1]` the product form does not name, written after the rendered product (b673, r8-r10);
a product that does not conform to the product form has `jobs = ["j1"]` (r11-r13). The Thens read what the run
printed, its exit (a refusal no traceback), and the product file and commit it kept; "this product" is named by the
product file's path."""
import re
import subprocess
import sys
import tomllib
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
REL = ".shop/product/product.toml"
FORMED = "When a change is wanted, the %s user wants it specified, so they can build it."
UNFORMED = "A change is wanted by the %s user."


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "product"


def world(step):
    return step.context.setdefault("product", {"kinds": {}, "outside": set(), "unformed": set(), "depends": {},
                                               "details": [], "texts": {}})


def detail(name):
    """The text of the product detail `name` in the product file: a table no part of the product form names."""
    return '\n[%s]\nsubdomains = ["s-%s"]\n' % (name, name)


def scripts(name):
    import importlib
    if str(ROOT / "scripts") not in sys.path:
        sys.path.insert(0, str(ROOT / "scripts"))
    return importlib.import_module(name)


def value(w, name, of=None):
    """What an instance stands for on the command line and in the product file."""
    kind = w["kinds"].get(name)
    if kind == "product actor":
        return w.get("spoken") or "the %s user" % name
    if kind == "job statement" and name in w["texts"]:
        return w["texts"][name]
    if kind == "job statement":
        return UNFORMED % name if name in w["unformed"] else FORMED % mentioned(w, name)
    if kind == "id":
        return "example.org/%s" % name if of == "product" else name
    if kind == "purpose":
        return "The purpose %s." % name
    return w.get("ids", {}).get(name, name)


def speaker(text):
    """The actor a job statement of the form names: `When <situation>, <actor> wants`."""
    found = re.match(r"When .*, (.+?) wants ", text)
    return found and found[1]


def mentioned(w, statement):
    """The name of the product actor the job statement `statement` mentions (`the <name> user`)."""
    return w.get("mentions", {}).get(statement) or w.get("when actor") or statement


def given_instance(step):
    if not mine(step):
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_text(step):
    """`the job statement `j2` holds "When ..."`: the group's given block, j2's text in place of FORMED (r14)."""
    if not mine(step):
        return False
    text = step.quoted[0][1:-1]
    world(step)["texts"][step.names[0].strip("`")] = text
    world(step)["spoken"] = speaker(text)


def given_does(step):
    """`the need n1 depends on the job j1`; `this product holds the product detail p1` (or the product actor p1)."""
    if not mine(step):
        return False
    w = world(step)
    if step.term in ("hold", "holds") and w["kinds"].get(step.names[-1]) == "product detail":
        w["details"].append(step.names[-1])
    elif step.term in ("hold", "holds") and w["kinds"].get(step.names[-1]) == "product actor" and not step.names[:-1]:
        w["outside"].discard(step.names[-1])      # this product holds the product actor p1: held, as by default
    elif step.term == "depend on":
        w["depends"][step.names[0]] = step.names[1]
    elif step.term in ("mention", "mentions"):
        w.setdefault("mentions", {})[step.names[0]] = step.names[1]
    else:
        return False


def given_not(step):
    """`this product does not hold the product actor p1`; `the job statement j2 does not conform to ...`; `this product
    does not conform to the product form` (its jobs a list, not a table of jobs)."""
    if not mine(step) or step.term not in ("holds", "hold", "conform"):
        return False
    w = world(step)
    if not step.names:
        w["unformed product"] = True
        return None
    (w["unformed"] if step.term == "conform" else w["outside"]).add(step.names[-1])


def held(w, job):
    """The product the Givens describe: before a job is declared, its actors and its jobs (each need, and what it
    depends on); before an actor or the product is declared, nothing."""
    if not job:
        return {"actors": [], "jobs": {}}
    actors = [value(w, n) for n, k in w["kinds"].items() if k == "product actor" and n not in w["outside"]]
    jobs = {}
    for name, kind in w["kinds"].items():
        if kind == "need" and name not in w["outside"]:
            needs = [w["depends"][name]] if name in w["depends"] else []
            jobs[name] = {"actors": actors[:1], "statement": FORMED % name, "needs": needs}
            for need in needs:
                jobs.setdefault(need, {"actors": actors[:1], "statement": FORMED % need, "needs": []})
    return {"actors": actors, "jobs": jobs}


def runs(step):
    if not mine(step) or step.term not in ("`spec product`", "`spec actor`", "`spec job`"):
        return False
    w, repo = world(step), step.repo
    kinds = {w["kinds"].get(n): n for n in step.names}
    if step.term == "`spec job`" and "id" in kinds:
        w["ids"] = {kinds["job"]: value(w, kinds["id"])}
    w["when actor"] = kinds.get("product actor")
    w["before"] = held(w, step.term == "`spec job`")
    if step.term == "`spec actor`":
        w["before"]["id"] = "example.org/notes"     # an actor is declared once the product has an id (r74, b827)
    if step.term == "`spec job`":
        statement = kinds.get("job statement")
        w["statement"] = value(w, statement) if statement else FORMED % mentioned(w, kinds["job"])
        said = speaker(w["statement"])
        if said and said not in w["before"]["actors"] and mentioned(w, statement or kinds["job"]) not in w["outside"]:
            w["before"]["actors"].append(said)
        w["supplied"] = None if "product actor" in kinds or "product actor" in step.context.get("absent", []) else (
            said or "the %s user" % mentioned(w, statement or kinds["job"]))    # a job is declared with an actor (r62)
        if w["supplied"] and w["supplied"] not in w["before"]["actors"] and mentioned(
                w, statement or kinds["job"]) not in w["outside"]:
            w["before"]["actors"].append(w["supplied"])
    text = scripts("product_store").render(w["before"]) + "".join(detail(name) for name in w["details"])
    if w.get("unformed product"):
        text = text.replace("actors = ", 'jobs = ["j1"]\nactors = ', 1)
    if any((w["before"]["actors"], w["before"]["jobs"], w["details"], w.get("unformed product"), w["before"].get("id"))):
        (repo / REL).parent.mkdir(parents=True, exist_ok=True)
        (repo / REL).write_text(text)
    step.context["head"] = W.init(repo)
    if step.term == "`spec product`":
        args = ["product", value(w, kinds["id"], "product"), "--purpose", value(w, kinds["purpose"])]
    elif step.term == "`spec actor`":
        args = ["actor", value(w, kinds["product actor"])]
    else:
        args = ["job", value(w, kinds["job"])]
        args += ["--actor", value(w, kinds["product actor"])] if "product actor" in kinds else []
        args += ["--actor", w["supplied"]] if w.get("supplied") else []
        args += ["--statement", w["statement"]]
        args += ["--needs", value(w, kinds["need"])] if "need" in kinds else []
    step.context["product_when"] = list(step.names)
    step.context["result"] = step.run("spec", *args)


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True).stdout


def kept(step):
    path = step.repo / REL
    return tomllib.loads(path.read_text()) if path.is_file() else {}


def holds(step, w, name):
    """Whether the kept product holds the instance `name`: a product actor among its actors, a job among its jobs
    (with the actor and the statement the When gave it)."""
    product, kind = kept(step), w["kinds"].get(name)
    if kind == "product actor":
        return value(w, name) in product.get("actors", [])
    if kind == "job":
        job = product.get("jobs", {}).get(value(w, name))
        given = {w["kinds"].get(n): n for n in step.context["product_when"]}
        return job is not None and all(job.get(field) == want for field, want in (
            ("actors", [value(w, given["product actor"])] if "product actor" in given else None),
            ("statement", value(w, given["job statement"]) if "job statement" in given else None)) if want)
    if kind == "product":
        given = {w["kinds"].get(n): n for n in step.context["product_when"]}
        return (product.get("id"), product.get("purpose")) == (value(w, given["id"], "product"),
                                                              value(w, given["purpose"]))
    if kind == "product detail":
        path = step.repo / REL
        return detail(name) in path.read_text() and product.get(name) == {"subdomains": ["s-%s" % name]}
    raise AssertionError("no product holds a %s" % kind)


def then(step):
    """This product holds x (in the kept file); `spec` writes x (one commit of the file, a change from the head before
    the run, x in it); `spec` refuses (an error exit, nothing changed); `spec` names x (its value, and its option)."""
    if not mine(step) or "result" not in step.context:
        return False
    w, done = world(step), step.context["result"]
    said = done.stdout + done.stderr
    if step.term == "holds":
        assert holds(step, w, step.names[-1]), kept(step)
    elif step.term == "write":
        assert done.returncode == 0, said
        assert git(step.repo, "show", "--name-only", "--format=", "HEAD").split() == [REL]
        assert git(step.repo, "rev-parse", "HEAD").strip() != step.context["head"]
        assert holds(step, w, step.names[-1]), kept(step)
    elif step.term == "refuse":
        assert done.returncode != 0 and done.stderr.strip() and "Traceback" not in said, said
        assert git(step.repo, "rev-parse", "HEAD").strip() == step.context["head"]
        assert not git(step.repo, "status", "--porcelain", "--", REL).strip()
    elif step.term == "name" and not step.names:
        assert REL in said, said           # this product: the product file
    elif step.term == "name":
        name = step.names[-1]
        option = {"job statement": "--statement", "product actor": "--actor", "need": "--needs"}[w["kinds"][name]]
        assert value(w, name) in said and option in said, said
    else:
        return False


def completes(step):
    if not mine(step) or "result" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr


W.local("GivenK")(given_instance)
sys.modules["vocab"].handler("GivenCode", "job statement")(given_text)     # a claim `features vocab --check` sees
W.local("GivenDoes")(given_does)
W.local("GivenDoesNot")(given_not)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then)
W.local("ThenExitsOk")(completes)
