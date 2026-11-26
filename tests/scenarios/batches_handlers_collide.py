"""An item whose ids collide with its capability's, so that `work batch start`'s pick renumbers them (batches r126,
r127, b660): over the worlds of batches_handlers_adapter (an operation table) and batches_handlers_move (a moved term),
the item's group and requirement ids made `g1` and `r1`, which its capability in `spec/` holds already (work-queue's
of readiness_world's codified spec, notebook's of the domain-model fixture); an item that holds no group given
readiness_world's passing line under those ids. Loaded before batches_handlers_corpus, whose handler
of "the item holds the requirement id" would take these steps."""
import re
import sys

B, F = sys.modules["shop_backlog_world"], sys.modules["shop_world_four"]
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
TAGS = {"r126", "r127"}


def mine(step):
    """True when the step is of batches' scenarios of r126 and r127."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and bool(TAGS & set(found.tags))


@four("GivenK", "requirement id", *BOTH)
@four("GivenK", "capability", *BOTH)
def given_named(step):
    """a requirement id r1, a capability c1: the ids `g1` and `r1` of the item's capability."""
    if not mine(step):
        return False


def colliding(text, passing):
    """The item's `## Requirements` text with its first group and requirement ids `g1` and `r1`, or, with no group,
    `passing` (a capability block of one group) under them before it."""
    if "#### [g" not in text:
        text = passing + "\n\n" + text
    text = re.sub(r"(?m)^#### \[g\d+\]", "#### [g1]", text, count=1)
    return re.sub(r"(?m)^- \[r\d+\]", "- [r1]", text, count=1)


@four("GivenDoes", "holds", *BOTH)
def holds(step):
    """the item i1 holds the requirement id r1: the item as the world wrote it, its ids colliding; the capability c1
    holds the requirement id r1: its capability in `spec/` holds `g1` and `r1` already."""
    (k1, n1), (k2, _) = parts(step)
    if k2 != "requirement id" or k1 not in ("item", "capability") or not mine(step):
        return False
    if k1 == "capability":
        return None
    R = sys.modules["shop_readiness_world"]
    R.codify(step)
    sections = dict(step.context["item_fields"][n1]["sections"])
    sections["Requirements"] = colliding(sections.get("Requirements", ""), R.block("Title of %s" % n1, R.PASSING))
    B.write_item(step, n1, sections=sections)
