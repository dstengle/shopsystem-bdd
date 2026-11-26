"""Handlers of laying's g5 (r5, b755), `work_queue_world.local`s tried before laying_handlers' own: two items that
retire the two lines of one group of readiness_world's codified spec (work-queue's g1, `r1` and `r2`), the item i1
retiring `r1` with readiness_world's PASSING line and another item, b2, retiring `r2` with a line of its own, both
laid in the workspace w1 (the second lay takes the group out whole) and the lay committed there; the When lifts i1,
a refusal of the lift kept as its reply.
The Thens read the reply (laying_handlers') and the workspace: its capability file not holding the line `r2`, which
b2 still retires, and holding `r1` again."""
import sys

L = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/laying_handlers.py"))   # loaded before this, by name
CAP, R, W, mine, world = L.CAP, L.R, L.W, L.mine, L.world

OTHER = ("While an initiative is `proposed`, when the person runs `work abandon` on the initiative, `work` shall set "
         "the status of the initiative to `abandoned`.")


def _block(retired, rid, gid, text):
    return ("### work-queue\n\nretired: [%s]\nretires: [%s %s]\n\n#### [%s] Retires %s\n- [%s] %s"
            % (retired, rid, retired, gid, retired, rid, text))


def given_instance(step):
    if not mine(step) or step.kind not in ("requirement group", "requirement id"):
        return False
    world(step)


def given_retires(step):
    """`the requirement r1 (r5) retires the requirement id r4 (r7)`: the world of two items retiring one group."""
    if not mine(step) or step.term != "retire" or not step.text.startswith("the requirement "):   # an item's: b746's
        return False
    world(step)["retiring"] = True


def requests(step):
    """`the batches service lifts the item i1 from the workspace w1`: b1 and b2 laid there and committed, then b1
    lifted; the laying service's reply kept."""
    if not mine(step) or step.template != "WhenRequests" or not world(step).get("retiring"):
        return False
    import backlog_items
    import laying
    from plumbing import domain_envelope
    from plumbing.shop_refused import Refused
    w = world(step)
    R().codify(step)
    B = sys.modules["shop_backlog_world"]
    B.write_item(step, "i1", status="in-batch", sections={"Requirements": _block("r1", "r5", "g4", R().PASSING)})
    B.write_item(step, "i2", status="in-batch", sections={"Requirements": _block("r2", "r6", "g5", OTHER)})
    W.init(step.repo)
    W.git(step.repo, "add", "-A")
    W.git(step.repo, "commit", "-q", "--allow-empty", "-m", "the world")
    tree = step.request.getfixturevalue("tmp_path_factory").mktemp("laying") / "w1"
    W.git(step.repo, "worktree", "add", "-q", "-b", "workspace", str(tree))
    first, second = (backlog_items.find(step.repo, b) for b in ("b1", "b2"))
    for item in (first, second):
        laid = laying.lay(item, tree)
        assert laid.outcome == "done", laid
    W.git(tree, "add", "-A")
    W.git(tree, "commit", "-q", "-m", "laid\n\nItem: b1\nItem: b2")
    w["tree"], w["item"] = tree, first
    try:
        w["response"] = laying.lift(first, tree)
    except Refused as why:                       # kept, so the Then that the lift kept the workspace says it
        w["response"] = domain_envelope.refused(why)


def then_held(step):
    """`the workspace w2 does not hold the requirement r6`: the capability file holds no line `r2`, which b2 still
    retires, and holds `r1` again, the lifted item's retired line."""
    if not mine(step) or not world(step).get("retiring") or step.term != "holds":
        return False
    text = (world(step)["tree"] / CAP).read_text()
    assert step.template.endswith("Not"), step.text
    assert "- [r2] " not in text and "- [r1] " in text, text


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_retires)
W.local("WhenRequests")(requests)
W.local("ThenDoesNot")(then_held)
