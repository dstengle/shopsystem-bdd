"""drafting's line drafted into one capability that retires a requirement of another (drafting#r113, b882), in
readiness_world's codified spec (the fixture's work-queue, live r1-r4, and review). Each a `local` handler that takes a
step of r113's scenario (`mine`) and returns False on any other: the capability c1 work-queue, its requirement r1 of
the id r2 `work-queue#r1`, the capability c2 review; the item, written at the When with a line of its own in
work-queue; `work line <item> --into review --retires work-queue#r1 <line>` run on it; and the Thens read the item as
committed: the line in its block of review, the id under its block of work-queue's `retired:` and the pair of the two
(`review#r<n> r1`) under its `retires:`."""
import re
import sys

W = sys.modules["shop_work_queue_world"]
B = sys.modules["shop_backlog_world"]
R = sys.modules["shop_readiness_world"]
four = sys.modules["shop_world_four"].four
local = W.local
IDENT = "work-queue#r1"
INTO = "review"
LINE = "When the person runs `work start` on an initiative, `work` shall give a brief to every stage."
OWN = "### work-queue\n\n#### [g9] Kept\n- [r9] " + R.PASSING


def mine(step):
    """True when the step is of drafting's scenario of r113."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return (sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None
            and "r113" in found.tags)


def _world(step):
    return step.context.setdefault("into_retiring", {})


@local("GivenK")
def given_named(step):
    """a requirement r1 (r3), a capability c1 (c2), a requirement id r2, an item i1 (i2): what the When writes."""
    return None if mine(step) and step.kind in ("requirement", "capability", "requirement id", "item") else False


@local("GivenDoes")
def given_has(step):
    """the capability c1 has the requirement r1, the requirement r1 has the requirement id r2: work-queue's r1."""
    return None if mine(step) and step.term in ("has", "have") else False


@local("WhenRuns")
@local("WhenRequests")
def draft(step):
    """`work line <item> --into review --retires work-queue#r1 <line>` (the request re-keyed by the CLI contract)."""
    if not mine(step):
        return False
    world = _world(step)
    item = world["item"] = re.search(r"\bthe item (i\d+)", step.text).group(1)
    R.codify(step)
    B.write_item(step, item, status="shaped", sections={"Requirements": OWN})
    B.run_work(step, "line", B.ident(item), "--into", INTO, "--retires", IDENT, LINE, **R.NO_INPUT)
    return None


def _committed(step):
    """The item as committed by the run, which exited 0 and left it clean."""
    done, rel = step.context["result"], step.context["items"][_world(step)["item"]]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    return W.git(step.repo, "show", "HEAD:%s" % rel)


def _block(text, capability):
    """The item's `### <capability>` block of its `## Requirements`, as committed."""
    found = re.search(r"(?ms)^### %s\n(.*?)(?=^### |^## |\Z)" % re.escape(capability), text)
    assert found, (capability, text)
    return found.group(1)


def _new_id(text):
    """The id of the item's line LINE in its block of review."""
    found = re.search(r"(?m)^- \[(r[1-9]\d*)\] %s$" % re.escape(LINE), _block(text, INTO))
    assert found, text
    return found.group(1)


@local("ThenDoes")
def then_does(step):
    """the capability c2 has the requirement r3, the item i2 holds it: the line in the item's block of review; the
    requirement r3 retires the requirement id r2: the block of work-queue retires r1, paired with `review#r<n>`; the
    drafting service keeps the item i2: the run committed it."""
    if not mine(step):
        return False
    text = _committed(step)
    if step.term in ("retire", "retires"):
        block = _block(text, "work-queue")
        assert re.search(r"(?m)^retired: \[(?:.*, )?r1(?:, .*)?\]$", block), block
        assert re.search(r"(?m)^retires: \[(?:.*, )?%s#%s r1(?:, .*)?\]$" % (INTO, _new_id(text)), block), block
        assert "- [r9] " + R.PASSING in block.split("\n"), block
        return None
    if step.term in ("has", "have", "hold", "holds"):
        _new_id(text)
    return None


for _verb in ("retire", "retires"):     # a chain of the key, which `features vocab` finds
    four("ThenDoes", _verb, "drafting")(then_does)
