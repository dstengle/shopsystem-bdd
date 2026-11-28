"""The decision an applied retirement leaves unenforced, superseded in the workspace it is applied to (batches r173,
r177, b741, b750; reviews r18, r19, b874): beside readiness_world's codified spec, spec/decisions/0001 accepted, of
tier requirement, enforced by the live `work-queue#r1` (the requirement r2, its requirement id r3), with the index
current; the item i1's line `r5` retires `work-queue#r1` (the requirement r1). r173: `work batch start`, and the Thens
read i1's task branch (0001 superseded, a decision that supersedes it) and the output naming the successor. r177:
0001 enforced by `work-queue#r1` and `work-queue#r3` (the requirement r4, its requirement id r5), the item i2,
`ready`, whose line `r6` retires `work-queue#r3`; `work batch start`, and the Thens read the one successor on i2's task
branch, enforced by i2's line as `work batch start` renumbered it. reviews r18: i1 parked in the batch the world makes
(its own task branch superseding 0001); `work batch review`, and the Thens read the batch's branch, rebuilt from the
base with no parked item applied: no decision superseding 0001. reviews r19: beside it the item i2 `in-batch`, whose
line `r6` retires `work-queue#r1` too; the batch's branch holds the one successor of i2's retirement. The handlers are
put first in their keys' chains."""
import re
import sys
from pathlib import Path

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
requested = sys.modules["vocab"].vocab4.requested     # KEEPS: the spellings of keep
SLUG = "the-queue-is-worked-in-order"
IDENT = "design-decision/ex.com/prod/ctx/%s" % SLUG
REL = "spec/decisions/0001-%s.md" % SLUG
DECISION = ("---\nid: %s\nsummary: \"The queue is worked in order.\"\ndate: 2026-11-20\nstatus: accepted\n"
            "tier: requirement\nenforced_by: [work-queue#r1]\n---\n\n# 0001. The queue is worked in order\n\n"
            "## Decision\n\nA proposed initiative is started by `work start`.\n" % IDENT)
BLOCK = "### work-queue\n\nretired: [r1]\nretires: [r5 r1]\n\n#### [g4] %s\n- [r5] %s"
SECOND = ("While an initiative is `proposed`, when the person runs `work abandon` on the initiative, `work` shall set "
          "the status of the initiative to `abandoned`.")      # passes beside R.PASSING (readiness_world's DIFFERING)
OTHER = "### work-queue\n\nretired: [r3]\nretires: [r6 r3]\n\n#### [g5] %s\n- [r6] %s"     # r177's i2
SAME = "### work-queue\n\nretired: [r1]\nretires: [r6 r1]\n\n#### [g5] %s\n- [r6] %s"      # reviews r19's i2
TAGS = {"batches": ("r173", "r177"), "reviews": ("r18", "r19")}


def first(template, term):
    """`four`, the handler put first in its key's chain."""
    def mark(fn):
        four(template, term, *BOTH)(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


def mine(step):
    """r173, r177 (batches) or r18, r19 (reviews), the tag of the step's scenario, else None."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    if found is None:
        return None
    tags = TAGS.get(Path(found.feature.filename).stem, ())
    return next((t for t in tags if t in found.tags), None)


@first("GivenK", "design-decision")
@first("GivenK", "requirement")
@first("GivenK", "requirement id")
@first("GivenK_A", "design-decision")
@first("GivenDoes", "has")
@first("GivenDoes", "supersede")
@first("GivenDoes", "supersedes")
def noted(step):
    """What the decision and the item's block below say: the decision's status on the batch's branch is the lay's
    (accepted on main), the requirement r2 is `work-queue#r1`, its id r3 the one the item's line retires."""
    return None if mine(step) else False


@first("GivenDoes", "retire")
@first("GivenDoes", "retires")
def retires(step):
    """the requirement r1 retires the requirement id r3: the line `r5` of i1's block (`holds`); r6's (r4's), i2's line
    `r6` (`holds`)."""
    if not mine(step):
        return False


@first("GivenDoes", "enforce")
@first("GivenDoes", "enforces")
def enforces(step):
    """the requirement r2 enforces the design-decision d1: 0001 on main, accepted, and the decisions index."""
    if not mine(step):
        return False
    from model_report import render_decisions
    R = sys.modules["shop_readiness_world"]
    R.codify(step)
    path = step.repo / REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(DECISION if mine(step) != "r177" else
                    DECISION.replace("[work-queue#r1]", "[work-queue#r1, work-queue#r3]"))
    (path.parent / "index.md").write_text(render_decisions(step.repo))


@first("GivenDoes", "holds")
@first("GivenDoes", "hold")
def holds(step):
    """the item i1 holds the requirement r1: its block retiring `work-queue#r1` by its line `r5`."""
    (k1, n1), (k2, _) = parts(step)
    if not mine(step) or (k1, k2) != ("item", "requirement"):
        return False
    R = sys.modules["shop_readiness_world"]
    R.codify(step)
    title = step.context.get("item_fields", {}).get(n1, {}).get("title", "Title of %s" % n1)
    if n1 == "i2" and mine(step) == "r19":      # the other item, in-batch, retiring `work-queue#r1` too
        B.write_item(step, n1, sections={"Requirements": SAME % (title, SECOND)})
    elif n1 == "i2":      # r177: the other item, ready, retiring `work-queue#r3`
        B.write_item(step, n1, status="ready", sections={"Requirements": OTHER % (title, SECOND)})
    else:
        B.write_item(step, n1, sections={"Requirements": BLOCK % (title, R.PASSING)})


def _decisions(step, branch):
    """{path: text} of the decisions on `branch`, the index left out."""
    names = T.git(step, "ls-tree", "--name-only", branch, "spec/decisions/").split()
    return {n: T.git(step, "show", "%s:%s" % (branch, n)) for n in names if not n.endswith("/index.md")}


def _successors(found):
    return [p for p, text in found.items()
            if re.search(r"(?m)^supersedes: \[(.*, )?%s(, .*)?\]$" % re.escape(IDENT), text)]


def _branch(step):
    """The branch of the workspace the Thens read: of r173 i1's task, of r177 i2's, of a submit the batch's."""
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    batch = T.batch_name(step, "b1")
    return {"r173": "%s-%s" % (batch, B.ident("i1")), "r177": "%s-%s" % (batch, B.ident("i2"))}.get(mine(step), batch)


@first("ThenDoes", "set")
def sets(step):
    """the batches service sets the status of the design-decision d1 to `superseded` (r173): 0001's status on the
    task's branch."""
    if not mine(step):
        return False
    text = T.git(step, "show", "%s:%s" % (_branch(step), REL))
    assert re.search(r"(?m)^status: %s$" % B.bare(step.values[-1]), text), (text, step.context["result"].stdout)


def keeps(step):
    """the batches service keeps the design-decision d2, and the design-decision d2 supersedes the design-decision d1:
    one decision on the workspace's branch names 0001 under `supersedes:`; `keeps the workspace w1`: of a submit, the
    batch's branch (`workspace`)."""
    if not mine(step):
        return False
    if parts(step)[-1][0] == "worktree":
        return workspace(step)
    found = _successors(_decisions(step, _branch(step)))
    assert len(found) == 1, found


for _verb in requested.KEEPS + ("supersede", "supersedes"):
    first("ThenDoes", _verb)(keeps)


def keeps_not(step):
    """the batches service does not keep the design-decision d2: no decision on the workspace's branch supersedes
    0001."""
    if not mine(step):
        return False
    found = _successors(_decisions(step, _branch(step)))
    assert found == [], found


for _verb in requested.KEEPS:
    first("ThenDoesNot", _verb)(keeps_not)


@first("ThenDoes", "has")
def workspace(step):
    """`the batch b1 has the workspace w1`, `keeps the workspace w1`: the submit exited 0, the batch's branch its
    workspace."""
    if not mine(step) or {k for k, _ in parts(step)} - {"batch", "worktree", "batches service"}:
        return False
    _branch(step)


@first("ThenDoes", "holds")
def holds_decision(step):
    """`the workspace w1 holds the design-decision d2`: one decision on the batch's branch supersedes 0001."""
    if not mine(step) or [k for k, _ in parts(step)] != ["worktree", "design-decision"]:
        return False
    assert len(_successors(_decisions(step, _branch(step)))) == 1, step.text


@first("ThenDoesNot", "holds")
def holds_no_decision(step):
    """`the workspace w1 does not hold the design-decision d2`: no decision on the batch's branch supersedes 0001."""
    if not mine(step) or [k for k, _ in parts(step)] != ["worktree", "design-decision"]:
        return False
    found = _decisions(step, _branch(step))
    assert _successors(found) == [], step.text
    assert re.search(r"(?m)^status: accepted$", found[REL]), found[REL]


@first("ThenDoes", "name")
def names(step):
    """the batches service names the design-decision d2: what `work batch start` printed names the successor's file."""
    if not mine(step):
        return False
    found = _successors(_decisions(step, _branch(step)))
    out = step.context["result"].stdout
    assert found and all(p in out for p in found), (found, out)


@first("ThenDoes", "enforce")
@first("ThenDoes", "enforces")
def enforced(step):
    """r177: the requirement r6 enforces the design-decision d2: the one successor on i2's task branch names, under
    `enforced_by`, i2's line as `work batch start` renumbered it on main, and no longer `work-queue#r3`."""
    if not mine(step):
        return False
    branch = _branch(step)
    found = _decisions(step, branch)
    successors = _successors(found)
    assert len(successors) == 1, successors
    line = re.search(r"(?m)^retires: \[(r\d+) r3\]$", T.git(step, "show", "main:.shop/backlog/%s.md" % B.ident("i2")))
    enforcers = re.search(r"(?m)^enforced_by: \[(.*)\]$", found[successors[0]]).group(1).split(", ")
    assert line and "work-queue#%s" % line.group(1) in enforcers and "work-queue#r3" not in enforcers, (
        enforcers, step.context["result"].stdout)
