"""drafting's port line drafted with the requirement ids it supports (drafting#r86, drafting#r87, b705), in
readiness_world's codified spec (the fixture's work-queue, live r1-r4). Each a `local` handler that takes a step of
r86's or r87's scenario (`mine`) and returns False on any other: the requirement id a live one of work-queue,
`work-queue#r1`, or, when no requirement has it, `work-queue#r99`; `work line <item> --into work-queue
--relied-on-by <id> <line>` drafts the item, written at the When with no lines; and the Thens read the item's block
as `work` committed it, the line with its `Relied on by:` line after it, or the refusal and the item left as it
was."""
import importlib.util
import re
import sys
from pathlib import Path


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
R = shared("shop_readiness_world", "readiness_world.py")
local = W.local
LIVE, NONE = "work-queue#r1", "work-queue#r99"


def mine(step):
    """True when the step is of drafting's scenario of r86 or r87."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return (sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None
            and bool({"r86", "r87"} & set(found.tags)))


def _world(step):
    return step.context.setdefault("relied", {"id": LIVE})


@local("GivenK")
def given_named(step):
    """a requirement, a requirement id, an item: what the When writes."""
    return None if mine(step) else False


@local("GivenDoes")
def given_does(step):
    """the requirement r1 supports the requirement id r2: the option the When gives; no requirement has the
    requirement id r2: the id `NONE`, which the fixture's work-queue does not hold."""
    if not mine(step):
        return False
    if step.term in ("has", "have"):
        _world(step)["id"] = NONE
    return None


@local("WhenRuns")
@local("WhenRequests")
def draft(step):
    """`work line <item> --into work-queue --relied-on-by <id> <line>` (the request re-keyed by the CLI contract)."""
    if not mine(step):
        return False
    world = _world(step)
    item = world["item"] = re.search(r"\bthe item (i\d+)", " ".join(W.scenario_texts(step))).group(1)
    R.codify(step)
    path = B.write_item(step, item, status="shaped")
    world["before"] = path.read_text()
    B.run_work(step, "line", B.ident(item), "--into", R.CAPABILITY, "--relied-on-by", world["id"], R.PASSING,
               **R.NO_INPUT)
    return None


@local("ThenDoes")
def then_does(step):
    """the item i1 holds the requirement r1, keeps the requirement r1: the item's block of work-queue, as committed,
    holds the line with `Relied on by: work-queue#r1` right after it; refuses this request; names the requirement id
    r2: its id in what `work` printed, the item left as it was."""
    if not mine(step):
        return False
    done, world = step.context["result"], _world(step)
    rel = step.context["items"][world["item"]]
    if step.term in ("refuses", "refuse"):
        assert done.returncode != 0 and "usage:" not in done.stderr, (done.stdout, done.stderr)    # no usage error
        assert (step.repo / rel).read_text() == world["before"], step.text
        return None
    if step.term in ("names", "name"):
        assert world["id"] in done.stderr + done.stdout, (done.stdout, done.stderr)
        return None
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    lines = W.git(step.repo, "show", "HEAD:%s" % rel).split("\n")
    at = next((k for k, line in enumerate(lines) if line.startswith("- [r") and line.endswith(R.PASSING)), None)
    assert at is not None, (step.text, lines)
    assert lines[at + 1] == "Relied on by: %s" % world["id"], (step.text, lines)
    return None
