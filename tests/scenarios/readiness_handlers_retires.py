"""Handlers of features/readiness.feature for `work line --retires` (b128, r13-r14): a new line that replaces a live
requirement of the fixture's capability `work-queue`, written onto an item with the old id under its block's
`retired:`, or refused when the requirement it retires is nonexistent. The flag is the one `GivenFeat` keeps
(world_run); each handler returns False when it is not given, so the step goes on to the other handlers."""
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

FLAG = "--retires"
ITEM = "i1"
LIVE = "work-queue#r1"              # a live requirement of the fixture's work-queue
NONEXISTENT = "work-queue#r99"      # an id work-queue does not hold
LINE = ("When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to "
        "`started` and commit the initiative.")


def retiring(step):
    return FLAG in step.context.get("flags", [])


@local("GivenK", "requirement")
def given_requirement(step):
    """`a requirement r1`: the requirement the run retires, a live one until a Given makes it nonexistent."""
    if not retiring(step):
        return False
    step.context.setdefault("retires", {})[step.names[0]] = LIVE


@local("GivenK_C", "requirement")
def given_nonexistent(step):
    if not retiring(step) or not step.text.endswith(" is nonexistent"):
        return False
    step.context.setdefault("retires", {})[step.names[0]] = NONEXISTENT
    step.context.setdefault("says", {})[step.names[0]] = NONEXISTENT


def work_line(step):
    """`work line --retires <id> <line>` on the item i1 (shaped, no lines yet): the id a Given kept for the
    requirement the step names, else a live one."""
    if not retiring(step):
        return False
    R.codify(step)
    item = step.names[0] if step.kind == "item" else ITEM
    B.write_item(step, item, status="shaped")
    retired = step.context.get("retires", {}).get(step.names[0], LIVE)
    step.context["retiring"] = retired
    B.run_work(step, "line", B.ident(item), FLAG, retired, LINE, **R.NO_INPUT)


local("WhenRuns", "item")(work_line)
local("WhenRuns", "requirement")(work_line)


@local("ThenDoes", "requirement")
def writes_requirement(step):
    """The run exited 0 and wrote the line onto the item under a fresh id of work-queue, its block's `retired:`
    holding the id it retires, and printing the new id."""
    if not retiring(step) or step.term != "write":
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    rel = B.bind_written(step, ITEM)
    held = (step.repo / rel).read_text().split("\n## Requirements\n", 1)[1]
    cap, old = step.context["retiring"].split("#")
    block = held.split("### %s\n" % cap, 1)[1]
    assert re.search(r"(?m)^retired: \[%s\]$" % old, block), block
    found = re.search(r"(?m)^- \[(r[1-9]\d*)\] %s$" % re.escape(LINE), block)
    assert found and found.group(1) != old, block
    assert "%s#%s" % (cap, found.group(1)) in done.stdout, done.stdout
