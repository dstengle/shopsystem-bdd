"""A ready item whose line retires a requirement of another capability, not reopened when its scenario passes on the
lay (batches r193, b882): beside readiness_world's codified spec, the item i1's line `r5` of work-queue (the capability
c1, the requirement r1, its id r2) retires review's `r1` (the capability c2, the requirement r3, its id r4), its
block of review holding `retired: [r1]` and the pair `work-queue#r5 r1`, as `work line --into work-queue --retires
review#r1` writes them; the scenario s1 of the line passes in the batch's worktree (batches_handlers_xpass); `work
batch start`, and batches_handlers_tracking's Then reads the item's status as other than `shaped`. The handlers are
put first in their keys' chains and take only what the other handlers of r109's steps leave."""
import sys

B, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
BLOCK = "### work-queue\n\n#### [g4] %s\n- [r5] %s\n\n### review\n\nretired: [r1]\nretires: [work-queue#r5 r1]"


def first(template, term):
    """`four`, the handler put first in its key's chain."""
    def mark(fn):
        four(template, term, *BOTH)(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and "r193" in found.tags


def _world(step):
    return step.context.setdefault("cross_retiring", {"other": set()})


@first("GivenK", "capability")
def given_capability(step):
    """a capability c1 (c2): work-queue (review), which the item's block names."""
    return None if mine(step) else False


@first("GivenDoes", "has")
def has(step):
    """the capability c1 (c2) has the requirement r1 (r3): work-queue's line of the item (review's r1); the requirement
    r3 has the requirement id r4: review#r1. Any other `has` left to its chain."""
    if not mine(step):
        return False
    (k1, n1), (_, n2) = parts(step)
    if k1 == "capability":
        named = _world(step).setdefault("capabilities", [])
        named.append(n1)
        if len(named) > 1:      # the second capability named, review
            _world(step)["other"].add(n2)
        return None
    return None if k1 == "requirement" and n1 in _world(step)["other"] else False


@first("GivenDoes", "holds")
@first("GivenDoes", "hold")
def holds(step):
    """the item i1 holds the requirement r1: the item the retiring line is written into."""
    (k1, n1), (k2, n2) = parts(step)
    if not mine(step) or (k1, k2) != ("item", "requirement"):
        return False
    _world(step).setdefault("held", {})[n2] = n1
    return None


@first("GivenDoes", "retire")
@first("GivenDoes", "retires")
def retires(step):
    """the requirement r1 retires the requirement id r4: the item holding r1 written with BLOCK."""
    if not mine(step):
        return False
    R = sys.modules["shop_readiness_world"]
    R.codify(step)
    item = _world(step)["held"][parts(step)[0][1]]
    title = step.context.get("item_fields", {}).get(item, {}).get("title", "Title of %s" % item)
    B.write_item(step, item, sections={"Requirements": BLOCK % (title, R.PASSING)})
    return None
