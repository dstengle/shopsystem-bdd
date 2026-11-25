"""drafting's line that joins the item's group of the same title (drafting#r65, b583): in readiness_world's codified
spec, the item holding the world's passing line in a group of work-queue titled with the item's title, as a plain
`work line` titles the group it opens; a plain `work line <item> --into work-queue` drafts another line, and the Thens
read the item as committed: one group of work-queue, holding both lines. Each a `local` handler that takes a step of
r65's scenario (`mine`) and returns False on any other."""
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


def mine(step):
    """True when the step is of drafting's scenario of r65."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None and "r65" in found.tags


@local("GivenK")
def given_named(step):
    """a requirement group, a capability, an item, a group title, a requirement: what the item and its When make."""
    return None if mine(step) else False


@local("GivenDoes")
@local("GivenDoesNot")
def given_holds(step):
    """the item i1 holds the requirement group r1: the item given the world's passing line in a group of work-queue,
    titled with the item's title (readiness_world's `give_lines`); the rest is said by the item and the When."""
    if not mine(step):
        return False
    if step.term in ("holds", "hold") and step.text.startswith("the item"):
        R.give_lines(step, step.names[0], R.PASSING)
        step.context["drafted"] = step.names[0]
    return None


@local("WhenRuns")
@local("WhenRequests")
def draft(step):
    """`work line <item> --into work-queue <line>` with no `--group` and no `--in`."""
    if not mine(step):
        return False
    item = step.context["drafted"]
    B.write_item(step, item, status="shaped")
    B.run_work(step, "line", B.ident(item), "--into", R.CAPABILITY, R.LINE, **R.NO_INPUT)
    return None


@local("ThenDoesNot")
def one_group(step):
    """the drafting service does not keep the requirement group r3: `work` exited 0 and the item, as committed, holds
    one group of work-queue, titled with the item's title, holding the held line and the drafted one."""
    if not mine(step):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    item = step.context["drafted"]
    rel = step.context["items"][item]
    text = W.git(step.repo, "show", "HEAD:%s" % rel)
    groups = re.findall(r"(?m)^#### \[g\d+\] (.*)$", text)
    assert groups == [step.context["item_fields"][item]["title"]], text
    assert R.PASSING in text and R.LINE in text, text
    return None
