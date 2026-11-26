"""items#r66's and r67's Givens (b648), `local` handlers loaded after readiness_handlers_givens.py and so tried before
it: the item that meets the bar holds readiness_world's passing line as `work-queue#r5` in its group `g4`, and the
capability that holds its requirement id is the fixture's work-queue, given a line of its own under `g4` and `r5`
(another line, which the item's does not contradict), so the item's group and requirement ids collide with the
capability's, as a merged batch's would."""
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
R = shared("shop_readiness_world", "readiness_world.py")
# The capability's own group g4 and line r5, which a merged batch laid: of another While than the item's line.
HELD = ("### [g4] `work abandon` abandons a proposed initiative\n- [r5] While an initiative is `proposed`, when the "
        "person runs `work abandon` on the initiative, `work` shall set the status of the initiative to "
        "`abandoned`.\n\n")


def mine(step):
    """True when the step is of items' scenarios of r66 and r67."""
    requested = sys.modules["vocab"].vocab4.requested
    found = requested.scenario(step.request.node)
    return requested.capability(step.request.node) == "items" and found is not None \
        and bool({"r66", "r67"} & set(found.tags))


def _held(step):
    """The fixture's work-queue holding the group `g4` and the requirement `r5`, once."""
    R.codify(step)
    path = step.repo / "spec" / "capabilities" / ("%s.md" % R.CAPABILITY)
    text = path.read_text()
    if "[g4]" not in text:
        path.write_text(text.replace("## Not yet\n", HELD + "## Not yet\n", 1))


@W.local("GivenK")
def given_capability(step):
    """`a capability c1`: the fixture's work-queue, written when a Given says it holds the id."""
    if not mine(step) or step.kind != "capability":
        return False
    return None


@W.local("GivenDoes")
def given_holds(step):
    """the item i1 holds the requirement id r1: its passing line's `r5` (readiness_handlers_givens' meeting the bar
    gives it); the capability c1 holds the requirement id r1: work-queue's own `g4` and `r5` (`_held`)."""
    if not mine(step) or step.term not in ("holds", "hold") or not step.nps[0].startswith("the requirement id "):
        return False
    if step.subject.startswith("the capability "):
        _held(step)
    return None
