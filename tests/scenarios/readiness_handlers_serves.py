"""items#r74's Givens (b845), `local` handlers loaded after readiness_handlers_givens.py and so tried before it, in
readiness_world's codified spec: the requirement group r1 work-queue's live `g1` and the job j1 `start-work`; the
item's only line its block of work-queue's `serves: [g1 start-work]`, as `work line <item> --serves` writes it; it
holds no requirement and meets the bar."""
import importlib.util
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
GROUP, JOB = "g1", "start-work"


def mine(step):
    """True when the step is of items' scenario of r74."""
    requested = sys.modules["vocab"].vocab4.requested
    found = requested.scenario(step.request.node)
    return requested.capability(step.request.node) == "items" and found is not None and "r74" in found.tags


@W.local("GivenK")
def given_named(step):
    """`a requirement group r1`, `a job j1`: the codified spec laid; the item's block names them."""
    if not mine(step) or step.kind not in ("requirement group", "job"):
        return False
    R.codify(step)
    return None


@W.local("GivenDoes")
def given_does(step):
    """the requirement group r1 serves the job j1: noted; the item i1 holds the requirement group r1: its block of
    work-queue dedicating g1 to start-work, and nothing else; the item i1 holds no requirement, and meets this
    readiness bar: so the item as written does."""
    if not mine(step):
        return False
    if step.term in ("holds", "hold") and step.nps and step.nps[0].startswith("the requirement group "):
        R.codify(step)
        B.write_item(step, step.names[0],
                     sections={"Requirements": "### %s\n\nserves: [%s %s]" % (R.CAPABILITY, GROUP, JOB)})
    elif step.term not in ("serves", "serve", "holds", "hold", "meet", "meets", "pass"):
        return False
    return None
