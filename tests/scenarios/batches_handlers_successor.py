"""The decision a laid retirement leaves unenforced, superseded on the batch branch (batches r173, r174, b741): beside
readiness_world's codified spec, spec/decisions/0001 accepted, of tier requirement, enforced by the live
`work-queue#r1` (the requirement r2, its requirement id r3), with the index current; the item i1's line `r5`
retires `work-queue#r1` (the requirement r1). r173: `work batch start`, and the Thens read the batch's branch (0001
superseded, a decision that supersedes it) and the output naming the successor. r174: the item laid in the batch,
and when the lay left 0001 accepted on the batch's branch, 0001 superseded there and a successor of the item's lay
written by hand (so the park, not the lay, is what the Thens see); `work batch park`, and the Thens read the batch's
branch: 0001 accepted and no decision superseding it. r177 (b750): 0001 enforced by `work-queue#r1` and
`work-queue#r3` (the requirement r4, its requirement id r5: a line of another group than
`work-queue#r1`'s, since backlog_retires' unlay of one retired line of a group both lines left puts the group back
whole), the item i2, `ready`, whose line `r6` retires
`work-queue#r3` (the requirement r6); `work batch start`, and the Thens read the one successor on the batch's branch,
enforced by i2's line as `work batch start` renumbered it. r178: the same decision, i1 and the item i2, both
`in-batch` in the batch the world lays (its lay superseding 0001 by one successor), i2 holding the requirement r6 that
retires `work-queue#r3`; `work batch park` of i1, and the Thens read the one successor on the batch's branch, still
enforced by i2's line. The handlers are put first in their keys' chains."""
import re
import sys

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


def first(template, term):
    """`four`, the handler put first in its key's chain."""
    def mark(fn):
        four(template, term, *BOTH)(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


def mine(step):
    """r173 or r174, the tag of the step's scenario, else None."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return next((t for t in ("r173", "r174", "r177", "r178") if found is not None and t in found.tags), None)


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
    """the requirement r1 retires the requirement id r3: the line `r5` of i1's block (`holds`); r6's, r177's i2's line
    `r6` (`holds`), and in r178, where no Given names the item that holds it, the item i2 written `in-batch` with it,
    so the world's batch holds it."""
    if not mine(step):
        return False
    if mine(step) == "r178" and parts(step)[0][1] == "r6":
        R = sys.modules["shop_readiness_world"]
        R.codify(step)
        B.write_item(step, "i2", status="in-batch", sections={"Requirements": OTHER % ("Title of i2", SECOND)})


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
    path.write_text(DECISION if mine(step) not in ("r177", "r178") else
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
    if n1 == "i2":      # r177: the other item, ready, retiring `work-queue#r3`
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


def superseded_by_hand(step, name):
    """r174: once the batch is made, when its lay left 0001 accepted, 0001 superseded on the batch's branch and a
    successor of the item's lay written beside it, as the lay of a batch that supersedes it writes them."""
    if mine(step) != "r174":
        return
    branch = T.batch_name(step, name)
    if _successors(_decisions(step, branch)):
        return
    item = B.ident("i1")
    tree = T.outside(step) / ("successor-%s" % branch)
    T.git(step, "worktree", "add", "-q", str(tree), branch)
    old = (tree / REL).read_text()
    (tree / REL).write_text(old.replace("status: accepted", "status: superseded", 1))
    new = old.replace(SLUG, "%s-%s" % (SLUG, item)).replace("# 0001.", "# 0002.").replace(
        "enforced_by: [work-queue#r1]", "enforced_by: [work-queue#r5]\nsupersedes: [%s]\n"
        "source: [item/ex.com/prod/ctx/%s]\nby: \"the lay of item/ex.com/prod/ctx/%s\"" % (IDENT, item, item))
    (tree / "spec" / "decisions" / ("0002-%s-%s.md" % (SLUG, item))).write_text(new)
    from model_report import render_decisions
    (tree / "spec" / "decisions" / "index.md").write_text(render_decisions(tree))
    T.git(step, "add", "-A", cwd=tree)
    T.git(step, "commit", "-q", "-m", "the successor of 0001\n\nItem: %s" % item, cwd=tree)
    T.git(step, "worktree", "remove", "--force", str(tree))


T.AFTER_BATCH.append(superseded_by_hand)


def _branch(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    return T.batch_name(step, "b1")


@first("ThenDoes", "set")
def sets(step):
    """the batches service sets the status of the design-decision d1 to `superseded` (r173) or `accepted` (r174):
    0001's status on the batch's branch."""
    if not mine(step):
        return False
    text = T.git(step, "show", "%s:%s" % (_branch(step), REL))
    assert re.search(r"(?m)^status: %s$" % B.bare(step.values[-1]), text), (text, step.context["result"].stdout)


def keeps(step):
    """the batches service keeps the design-decision d2, and the design-decision d2 supersedes the design-decision d1:
    one decision on the batch's branch names 0001 under `supersedes:`."""
    if not mine(step):
        return False
    found = _successors(_decisions(step, _branch(step)))
    assert len(found) == 1, found


for _verb in requested.KEEPS + ("supersede", "supersedes"):
    first("ThenDoes", _verb)(keeps)


def keeps_not(step):
    """the batches service does not keep the design-decision d2: no decision on the batch's branch supersedes 0001."""
    if not mine(step):
        return False
    found = _successors(_decisions(step, _branch(step)))
    assert found == [], found


for _verb in requested.KEEPS:
    first("ThenDoesNot", _verb)(keeps_not)


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
    """r177, r178: the requirement r6 enforces the design-decision d2: the one successor on the batch's branch names, under
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
