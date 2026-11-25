"""A requirement group of an item that serves a job, laid by `work batch start` (batches r124, b641): the item, ready
and passing the bar with readiness_world's passing line in its group (the requirement group r1), holds the pair of that
group and the job j1 `start-work` under the `serves:` line of its block; the Thens read the capability work-queue (c1)
off the batch's branch after the command: the group r2 that holds the passing line, its `serves:` line naming the job,
and the capability in the lay's commit."""
import re
import sys

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
JOB = "start-work"
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's


def _r():
    return sys.modules["shop_readiness_world"]


def mine(step):
    """True when the step is of batches' scenario of r124."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and "r124" in found.tags


@four("GivenK", "requirement group", *BOTH)
@four("GivenK", "job", *BOTH)
def given_named(step):
    """a requirement group r1, a job j1: the item's group and `start-work`."""
    if not mine(step):
        return False
    step.context["serving"] = True


@four("GivenDoes", "serves", *BOTH)
@four("GivenDoes", "serve", *BOTH)
def given_serves(step):
    """the requirement group r1 serves the job j1: the pair the item's block holds."""
    if not mine(step):
        return False


@four("GivenDoes", "holds", *BOTH)
def holds(step):
    """the item i1 holds the requirement group r1: its block of readiness_world's passing line, `serves: [g4
    start-work]` before its group g4."""
    (k1, n1), (k2, _) = parts(step)
    if (k1, k2) != ("item", "requirement group") or not mine(step):
        return False
    R = _r()
    R.codify(step)
    title = step.context.get("item_fields", {}).get(n1, {}).get("title", "Title of %s" % n1)
    text = R.block(title, R.PASSING).replace("\n\n####", "\n\nserves: [g4 %s]\n\n####" % JOB, 1)
    B.write_item(step, n1, sections={"Requirements": text})


def _branch(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    return branches[0]


def _group(step):
    """The laid group's text on the batch's branch: the group of work-queue that holds the passing line."""
    rel = "spec/capabilities/%s.md" % _r().CAPABILITY
    text = T.git(step, "show", "%s:%s" % (_branch(step), rel))
    found = [g for g in re.split(r"(?m)^(?=### \[g)", text) if _r().PASSING in g]
    assert len(found) == 1, text
    return found[0]


@four("ThenDoes", "serves", *BOTH)
@four("ThenDoes", "serve", *BOTH)
def serves(step):
    """the requirement group r2 serves the job j1: the laid group's `serves:` line, right under its heading, names
    the job."""
    if not mine(step):
        return False
    lines = _group(step).split("\n")
    assert lines[1].startswith("serves:") and JOB in [j.strip() for j in lines[1][7:].split(",")], lines


@four("ThenDoes", "has", *BOTH)
def has_group(step):
    """the capability c1 has the requirement group r2: work-queue on the batch's branch holds the laid group."""
    if [k for k, _ in parts(step)] != ["capability", "requirement group"] or not mine(step):
        return False
    _group(step)


def keeps(step):
    """the batches service keeps the capability c1: work-queue's file in the lay's commit on the batch's branch."""
    if parts(step)[1][0] != "capability" or not mine(step):
        return False
    rel = "spec/capabilities/%s.md" % _r().CAPABILITY
    assert rel in T.git(step, "log", "--format=", "--name-only", "-1", _branch(step), "--", rel), rel


for _verb in KEEPS:       # each key requested.py tries in turn of "keeps", so no other one passes
    four("ThenDoes", _verb, *BOTH)(keeps)
