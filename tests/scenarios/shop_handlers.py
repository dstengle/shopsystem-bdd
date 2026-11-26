"""Handlers of features/shop.feature (shop r1-r5, b576), each a `work_queue_world.local` that takes only a step of a
scenario of the shop's feature (`mine`). The scenario's repository is a bounded context whose spec/index.md id is
`bounded-context/example.org/home/home`, so the shop's product id is `example.org/home` (`PRODUCT`). An id i1 is
`bounded-context/example.org/home/i1`, or, once a Given says the product id does not cover it,
`bounded-context/elsewhere.org/away/i1`; a bounded context is known by the id a Given or the When gives it, else
`bounded-context/example.org/home/<name>`. The bounded contexts the shop holds by the Givens are written into
`.shop/contexts.toml` (shop_contexts' `render`) and committed at the When, which runs `work context keep <id>` or
`work context list`. The Thens read what the run printed and the file and commit it kept."""
import subprocess
import sys
import tomllib
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
PRODUCT = "example.org/home"
THIS = "bounded-context/%s/home" % PRODUCT
REL = ".shop/contexts.toml"
INDEX = "---\nid: %s\nkind: bounded-context\nlanguage: codified-2\n---\n\n# home\n" % THIS


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "shop"


def world(step):
    return step.context.setdefault("shop", {"ids": {}, "contexts": {}, "held": [], "outside": set()})


def id_of(w, name):
    """The id an id instance i1 stands for, or the id a bounded context b1 is known by."""
    if name in w["contexts"] and w["contexts"][name]:
        return id_of(w, w["contexts"][name])
    if name in w["outside"]:
        return "bounded-context/elsewhere.org/away/%s" % name
    return "bounded-context/%s/%s" % (PRODUCT, name)


def given_instance(step):
    if not mine(step):
        return False
    w = world(step)
    if step.kind == "bounded context":
        w["contexts"].setdefault(step.names[0], None)
    elif step.kind == "id":
        w["ids"][step.names[0]] = True
    elif step.kind != "product id":
        return False


def given_does(step):
    """`this shop has the product id p1` (the repository's own), `the bounded context b1 has the id i1`, `this shop
    holds the bounded context b1`, `this shop holds no bounded context`."""
    if not mine(step) or step.term not in ("has", "holds"):
        return False
    w = world(step)
    if step.term == "has" and step.subject.startswith("the bounded context"):
        w["contexts"][step.names[0]] = step.names[1]
    elif step.term == "holds" and step.names:
        w["held"].append(step.names[0])


def given_not(step):
    """`the product id p1 does not cover the id i1`; `this shop does not hold the bounded context b3`."""
    if not mine(step) or step.term not in ("cover", "holds", "hold"):
        return False
    if step.term == "cover":
        world(step)["outside"].add(step.names[-1])


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True).stdout


def runs(step):
    if not mine(step) or step.term not in ("`work context keep`", "`work context list`"):
        return False
    w, repo = world(step), step.repo
    (repo / "spec").mkdir(parents=True, exist_ok=True)
    (repo / "spec" / "index.md").write_text(INDEX)
    if w["held"]:
        (repo / ".shop").mkdir(exist_ok=True)
        (repo / REL).write_text(scripts("shop_contexts").render([id_of(w, n) for n in w["held"]]))
    step.context["head"] = W.init(repo)
    if step.term == "`work context list`":
        step.context["result"] = step.run("work", "context", "list")
        return None
    context, ident = step.names[0], step.names[-1]
    w["contexts"][context] = w["contexts"].get(context) or ident
    step.context["result"] = step.run("work", "context", "keep", id_of(w, ident))


def scripts(name):
    import importlib
    if str(ROOT / "scripts") not in sys.path:
        sys.path.insert(0, str(ROOT / "scripts"))
    return importlib.import_module(name)


def kept_ids(step):
    path = step.repo / REL
    return tomllib.loads(path.read_text())["contexts"] if path.is_file() else []


def printed(step):
    done = step.context["result"]
    return done.stdout.split()


def then(step):
    """The shop holds b1 (in the kept file); `work` writes it (one commit of the file, a change from the head before
    the run); `work` refuses (an error exit); `work` names the id i1 (on stderr or stdout)."""
    if not mine(step) or "result" not in step.context:
        return False
    w, done = world(step), step.context["result"]
    if step.term == "holds":
        assert id_of(w, step.names[-1]) in kept_ids(step), (step.repo / REL).read_text()
    elif step.term == "write":
        assert done.returncode == 0, done.stdout + done.stderr
        assert git(step.repo, "show", "--name-only", "--format=", "HEAD").split() == [REL]
        assert git(step.repo, "rev-parse", "HEAD").strip() != step.context["head"]
        assert id_of(w, step.names[-1]) in kept_ids(step)
    elif step.term == "refuse":
        assert done.returncode != 0 and done.stderr.strip(), done.stdout + done.stderr
    elif step.term == "name":
        assert id_of(w, step.names[-1]) in (done.stdout + done.stderr).split(), done.stdout + done.stderr
    else:
        return False


def returned(step):
    """`work` returns the bounded context b1 (its id a line of what it printed), or this bounded context."""
    if not mine(step) or "result" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr
    want = THIS if not step.names else id_of(world(step), step.names[-1])
    assert want in printed(step), done.stdout


def not_returned(step):
    if not mine(step) or "result" not in step.context:
        return False
    assert id_of(world(step), step.names[-1]) not in printed(step), step.context["result"].stdout


def completes(step):
    if not mine(step) or "result" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_does)
W.local("GivenDoesNot")(given_not)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then)
W.local("ThenPrints")(returned)
W.local("ThenPrintsNot")(not_returned)
W.local("ThenExitsOk")(completes)
