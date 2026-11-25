"""drafting's requirement group dedicated to a job (r71, b641): in readiness_world's codified spec, the requirement
group r1 work-queue's live `g1` and the job j1 `start-work`; `work line <item> --serves work-queue#g1 start-work` run
on the item, written at the When with no lines; and the Thens read the item as committed: its block of work-queue
holding the pair under its `serves:` line. Each a `local` handler that takes a step of r71's scenario (`mine`) and
returns False on any other."""
import re
import sys

W = sys.modules["shop_work_queue_world"]
B = sys.modules["shop_backlog_world"]
R = sys.modules["shop_readiness_world"]
local = W.local
GROUP, JOB = "g1", "start-work"
PAIR = "serves: [%s %s]" % (GROUP, JOB)


def mine(step):
    """True when the step is of drafting's scenario of r71."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None and "r71" in found.tags


@local("GivenK")
def given_named(step):
    """a requirement group, a job, an item: what the When writes."""
    return None if mine(step) else False


@local("WhenRuns")
@local("WhenRequests")
def dedicate(step):
    """`work line <item> --serves work-queue#g1 start-work` (the request re-keyed by the CLI contract)."""
    if not mine(step):
        return False
    item = step.context["dedicated"] = re.search(r"\bthe item (i\d+)", " ".join(W.scenario_texts(step))).group(1)
    R.codify(step)
    B.write_item(step, item, status="shaped")
    B.run_work(step, "line", B.ident(item), "--serves", "%s#%s" % (R.CAPABILITY, GROUP), JOB, **R.NO_INPUT)
    return None


def _block(step):
    """The item's block of work-queue as committed, after `work` exited 0 and left the item clean."""
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    rel = step.context["items"][step.context["dedicated"]]
    text = W.git(step.repo, "show", "HEAD:%s" % rel)
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    found = re.search(r"(?ms)^### %s\n(.*?)(?=^### |\Z)" % re.escape(R.CAPABILITY), text)
    assert found is not None, (step.text, text)
    return found.group(1)


@local("ThenDoes")
def kept(step):
    """the requirement group r1 serves the job j1, the item i1 holds the requirement group r1, the drafting service
    keeps the item i1: the item's block of work-queue, as committed, says the pair."""
    if not mine(step):
        return False
    block = _block(step)
    assert PAIR in block.split("\n"), (step.text, block)
    return None
