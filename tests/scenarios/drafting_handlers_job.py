"""drafting's requirement group dedicated to a job the product does not hold, and a line drafted for a job (r92,
r93, b799), in readiness_world's codified spec. Each a `local` handler that takes a step of r92's or r93's scenario
(`mine`) and returns False on any other. r92: this product kept in its product file holding the job `keep-notes`
alone, the job j1 `no-such-job`, `work line <item> --serves work-queue#g1 no-such-job` run, and the Thens of the
refusal (no usage error, the item left as it was, nothing committed) and the job it names. r93: no product file, the
job j1 `start-work`, `work line <item> --into work-queue <line> --serves start-work` run, and the Thens of the item as
committed holding the line and of what `work` printed: the requirement's id with its line, the group and the job."""
import re
import sys

W = sys.modules["shop_work_queue_world"]
B = sys.modules["shop_backlog_world"]
R = sys.modules["shop_readiness_world"]
local = W.local
HELD, OUTSIDE, SERVED = "keep-notes", "no-such-job", "start-work"
PRODUCT = ".shop/product/product.toml"


def mine(step):
    """True when the step is of drafting's scenario of r92 or r93."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return (sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None
            and bool({"r92", "r93"} & set(found.tags)))


def _world(step):
    return step.context.setdefault("job", {})


@local("GivenK")
@local("GivenDoes")
@local("GivenDoesNot")
def given(step):
    """this product, a job, a requirement group, an item, a requirement, and that this product does not hold the
    job: what the When writes."""
    if not mine(step):
        return False
    if "product" in step.text:
        _world(step)["product"] = True
    return None


def _product(step):
    """The product file holding the job `HELD` alone, which `work` commits with the repository before its run."""
    path = step.repo / PRODUCT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('id = "example.org"\npurpose = "Notes kept."\nactors = []\n\n[jobs."%s"]\nactors = []\n'
                    'statement = "When I note, I want to keep it, so I can find it."\nneeds = []\n' % HELD)


@local("WhenRuns")
@local("WhenRequests")
def dedicate(step):
    """`work line <item> --serves work-queue#g1 no-such-job` (r92), `work line <item> --into work-queue <line>
    --serves start-work` (r93); the request re-keyed by the CLI contract."""
    if not mine(step):
        return False
    world = _world(step)
    item = world["item"] = re.search(r"\bthe item (i\d+)", " ".join(W.scenario_texts(step))).group(1)
    R.codify(step)
    if world.get("product"):
        _product(step)
    path = B.write_item(step, item, status="shaped")
    world["before"] = path.read_text()
    if world.get("product"):
        world["job"] = OUTSIDE
        B.run_work(step, "line", B.ident(item), "--serves", "%s#g1" % R.CAPABILITY, OUTSIDE, **R.NO_INPUT)
    else:
        world["job"] = SERVED
        B.run_work(step, "line", B.ident(item), "--into", R.CAPABILITY, R.PASSING, "--serves", SERVED, **R.NO_INPUT)
    return None


def _line(step, world):
    """The item's line of `R.PASSING` as committed: its id and its group's id."""
    text = W.git(step.repo, "show", "HEAD:%s" % step.context["items"][world["item"]])
    group = rid = None
    for line in text.split("\n"):
        found = re.match(r"#### \[(g\d+)\] ", line)
        group = found.group(1) if found else group
        if line.startswith("- [r") and line.endswith(R.PASSING):
            rid = line[3:line.index("]")]
            break
    assert rid is not None, (step.text, text)
    return rid, group


@local("ThenDoes")
def then_does(step):
    """r92: refuses this request (an error exit, no usage error, the item as it was, nothing committed), names the job
    j1. r93: the item i1 holds the requirement r2 and the drafting service keeps it (the item's line as committed,
    clean); names the requirement r2 (its id and its line), the requirement group r1 (its id), the job j1."""
    if not mine(step):
        return False
    done, world = step.context["result"], _world(step)
    said = done.stdout + done.stderr
    rel = step.context["items"][world["item"]]
    if step.term in ("refuses", "refuse"):
        assert done.returncode != 0 and "usage:" not in done.stderr, (done.stdout, done.stderr)
        assert (step.repo / rel).read_text() == world["before"], step.text
        assert W.git(step.repo, "rev-parse", "HEAD").strip() == step.context["head"], step.text
        return None
    if step.term in ("names", "name") and "job" in step.text:
        assert world["job"] in said, (step.text, said)
        return None
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    rid, group = _line(step, world)
    if step.term in ("names", "name") and "requirement group" in step.text:
        assert "%s#%s" % (R.CAPABILITY, group) in done.stdout, (step.text, done.stdout)
    elif step.term in ("names", "name"):
        assert "%s#%s" % (R.CAPABILITY, rid) in done.stdout and R.PASSING in done.stdout, (step.text, done.stdout)
    return None
