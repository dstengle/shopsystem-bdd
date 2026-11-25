"""items#r55's Givens (b581), `local` handlers loaded after readiness_handlers_givens.py and so tried before it: in
readiness_world's codified spec, the capability c1 its work-queue, the requirement group r1 its group g1 and the group
title g1 that group's title (`TITLE`); the item holds the requirement group r2, a group of work-queue of that title
holding readiness_world's PASSING; what `work ready` names the group title by."""
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
B = shared("shop_backlog_world", "backlog_world.py")

TITLE = "`work start` starts a proposed initiative"      # the title of the fixture's work-queue#g1


def mine(step):
    """True when the step is of items' scenario of r55."""
    requested = sys.modules["vocab"].vocab4.requested
    found = requested.scenario(step.request.node)
    return requested.capability(step.request.node) == "items" and found is not None and "r55" in found.tags


def _says(step, name, text):
    step.context.setdefault("says", {})[name] = text


@W.local("GivenK")
def given_named(step):
    """`a capability c1`: work-queue; `a requirement group r1`: its group; `a group title g1`: TITLE."""
    if not mine(step) or step.kind not in ("capability", "requirement group", "group title"):
        return False
    R.codify(step)
    if step.kind == "capability":
        _says(step, step.names[0], R.CAPABILITY)
    elif step.kind == "group title":
        _says(step, step.names[0], TITLE)
    return None


@W.local("GivenDoes")
def given_group(step):
    """`the capability c1 has the requirement group r1` and `the requirement group r1 has the group title g1`: so the
    fixture's work-queue#g1 does; the item's group is given it where the item holds it. `the item i1 holds the
    requirement group r2`: the item's block of work-queue, one group titled TITLE holding PASSING."""
    if not mine(step) or not step.subject.startswith(("the capability ", "the requirement group ", "the item ")):
        return False
    if step.subject.startswith("the item "):
        if step.term not in ("holds", "hold") or not step.nps[0].startswith("the requirement group "):
            return False
        R.codify(step)
        B.write_item(step, step.names[0], sections={"Requirements": R.block(TITLE, R.PASSING)})
        return None
    return None if step.term in ("has", "have") else False
