"""drafting's requirement group dedicated to a job while the product is not of the product form, and to a job given by
its id (r96, r97, b803), in readiness_world's codified spec. Each a `local` handler that takes a step of r96's or r97's
scenario (`mine`) and returns False on any other. r96: this product's file kept with its actors no list of texts, the
job j1 `start-work`; r97: this product's file holding the job `start-work`, the job j1 given by its id
`job/example.org/start-work`. `work line <item> --serves work-queue#g1 <job>` run, and the Thens of the item as
committed, its block of work-queue holding the pair, and, of r96, what `work` printed naming the product file."""
import re
import sys

W = sys.modules["shop_work_queue_world"]
B = sys.modules["shop_backlog_world"]
R = sys.modules["shop_readiness_world"]
local = W.local
NAME, IDENT = "start-work", "job/example.org/start-work"
PRODUCT = ".shop/product/product.toml"
STATEMENT = "When I start, I want to pick work, so I can build it."


def mine(step):
    """True when the step is of drafting's scenario of r96 or r97."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return (sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None
            and bool({"r96", "r97"} & set(found.tags)))


def _world(step):
    return step.context.setdefault("product job", {})


@local("GivenK")
@local("GivenDoes")
@local("GivenDoesNot")
def given(step):
    """this product (not of the product form, or holding the job), a job with its id, a requirement group, an item:
    what the When writes."""
    if not mine(step):
        return False
    if "conform" in step.text:
        _world(step)["unformed"] = True
    return None


def _product(step, unformed):
    """The product file: its actors no list of texts (r96), else holding the job `NAME` (r97)."""
    path = step.repo / PRODUCT
    path.parent.mkdir(parents=True, exist_ok=True)
    actors = '"the person"' if unformed else '["the person"]'
    path.write_text('id = "example.org"\npurpose = "Work picked."\nactors = %s\n\n[jobs."%s"]\nactors = '
                    '["the person"]\nstatement = "%s"\nneeds = []\n' % (actors, NAME, STATEMENT))


@local("WhenRuns")
@local("WhenRequests")
def dedicate(step):
    """`work line <item> --serves work-queue#g1 <job>`, the job by its name (r96) or its id (r97)."""
    if not mine(step):
        return False
    world = _world(step)
    item = world["item"] = re.search(r"\bthe item (i\d+)", " ".join(W.scenario_texts(step))).group(1)
    R.codify(step)
    _product(step, world.get("unformed", False))
    B.write_item(step, item, status="shaped")
    world["job"] = NAME if world.get("unformed") else IDENT
    B.run_work(step, "line", B.ident(item), "--serves", "%s#g1" % R.CAPABILITY, world["job"], **R.NO_INPUT)
    return None


@local("ThenDoes")
def then_does(step):
    """the requirement group r1 serves the job j1, the item holds it, the drafting service keeps the item: its block
    of work-queue, as committed and clean, says the pair; names this product: what `work` printed names its file."""
    if not mine(step):
        return False
    done, world = step.context["result"], _world(step)
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    if step.term in ("names", "name"):
        assert PRODUCT in done.stdout + done.stderr, (step.text, done.stdout, done.stderr)
        return None
    rel = step.context["items"][world["item"]]
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    text = W.git(step.repo, "show", "HEAD:%s" % rel)
    found = re.search(r"(?ms)^### %s\n(.*?)(?=^### |\Z)" % re.escape(R.CAPABILITY), text)
    assert found is not None, (step.text, text)
    assert "serves: [g1 %s]" % world["job"] in found.group(1).split("\n"), (step.text, found.group(1))
    return None
