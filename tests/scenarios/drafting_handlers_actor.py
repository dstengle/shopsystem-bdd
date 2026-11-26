"""drafting's term that violates v_t6 kept and the rule named (r94, b801; reworded, r112, b848), in readiness_world's
codified spec. Each a `local` handler that takes a step of r94's or r112's scenario (`mine`) and returns False on any other: the term t1 the actor
`the initiative`, which reads as the fixture's kind initiative; the item, written at the When, `shaped` with no
requirement lines (of r112 holding the term `the planner`); `work line <item> --into work-queue --term <t1>` run on
it (of r112 `--reword-term "the planner" <t1>`); and the Thens of the item as
committed holding the term, the run's exit and `v_t6` in what it printed."""
import re
import sys

W, B, R = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_readiness_world"))
local = W.local
T1 = "- **the initiative** (proper noun): the initiative the person works on. Kind of: agent."
OLD = "- **the planner** (proper noun): the planner the person works with. Kind of: agent."


def mine(step):
    """True when the step is of drafting's scenario of r94 or r112."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None \
        and bool({"r94", "r112"} & set(found.tags))


def reworded(step):
    """True when the step is of r112's scenario, whose When rewords a term of the item."""
    return "r112" in sys.modules["vocab"].vocab4.requested.scenario(step.request.node).tags


@local("GivenK")
@local("GivenDoes")
def given(step):
    """a term t1, that it violates `v_t6`, an item i1: what the When writes."""
    return None if mine(step) else False


@local("WhenRuns")
@local("WhenRequests")
def write(step):
    """`work line <item> --into work-queue --term <t1>` (the request re-keyed by the CLI contract); of r112 the item
    holding OLD, reworded to t1 by `--reword-term`."""
    if not mine(step):
        return False
    item = step.context["termed"] = re.search(r"\bthe item (i\d+)", step.text).group(1)
    R.codify(step)
    if reworded(step):
        B.write_item(step, item, status="shaped", sections={"Notes": B.NOTE, "Requirements": "### %s\n\n%s" % (R.CAPABILITY, OLD)})
        B.run_work(step, "line", B.ident(item), "--into", R.CAPABILITY, "--reword-term", "the planner", T1,
                   **R.NO_INPUT)
        return None
    B.write_item(step, item, status="shaped")
    B.run_work(step, "line", B.ident(item), "--into", R.CAPABILITY, "--term", T1, **R.NO_INPUT)
    return None


@local("ThenDoes")
def then_does(step):
    """holds and keeps the term t1: the item as committed holds it, its file clean; names `v_t6`: in what `work`
    printed; completes this request: an exit 0."""
    if not mine(step):
        return False
    done = step.context["result"]
    said = done.stdout + done.stderr
    if step.term in ("names", "name"):
        assert "v_t6" in said and "the initiative" in said, (step.text, said)
        return None
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    if step.term in ("completes", "complete"):
        return None
    rel = step.context["items"][step.context["termed"]]
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    assert T1 in W.git(step.repo, "show", "HEAD:%s" % rel), step.text
    return None
