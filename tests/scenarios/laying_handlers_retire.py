"""Handlers of laying's g5 (r5, b755), `work_queue_world.local`s tried before laying_handlers' own: two items that
retire the two lines of one group of readiness_world's codified spec (work-queue's g1, `r1` and `r2`), the item i1
retiring `r1` with readiness_world's PASSING line and another item, b2, retiring `r2` with a line of its own, both
laid in the workspace w1 (the second lay takes the group out whole) and the lay committed there; the When lifts i1,
a refusal of the lift kept as its reply.
The Thens read the reply (laying_handlers') and the workspace: its capability file not holding the line `r2`, which
b2 still retires, and holding `r1` again. When a Given says r6 supports the requirement id r8 (r47, b761), `r2` carries
`Relied on by: batches#r1` (`SUPPORT`) in the world's spec, and the Thens read the put-back `r1` (r9) under its group
with no Relied on by line naming it."""
import re
import sys

L = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/laying_handlers.py"))   # loaded before this, by name
CAP, R, W, mine, world = L.CAP, L.R, L.W, L.mine, L.world

OTHER = ("While an initiative is `proposed`, when the person runs `work abandon` on the initiative, `work` shall set "
         "the status of the initiative to `abandoned`.")
SUPPORT = "Relied on by: batches#r1"


def _block(retired, rid, gid, text):
    return ("### work-queue\n\nretired: [%s]\nretires: [%s %s]\n\n#### [%s] Retires %s\n- [%s] %s"
            % (retired, rid, retired, gid, retired, rid, text))


def given_instance(step):
    if not mine(step) or step.kind not in ("requirement group", "requirement id"):
        return False
    world(step)


def given_retires(step):
    """`the requirement r1 (r5) retires the requirement id r4 (r7)`: the world of two items retiring one group;
    `the requirement r6 supports the requirement id r8`: `r2` carries `SUPPORT` (r47)."""
    if not mine(step) or step.term not in ("retire", "support") or not step.text.startswith("the requirement "):
        return False                                                                         # an item's: b746's
    world(step)["supporting" if step.term == "support" else "retiring"] = True


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
    if w.get("supporting"):
        path = step.repo / CAP
        text = path.read_text()
        found = re.search(r"(?m)^- \[r2\] .*$", text)
        path.write_text(text[:found.end()] + "\n" + SUPPORT + text[found.end():])
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


def _put_back(step):
    """The put-back line `r1` of the workspace's capability file with the lines after it up to the next line or group,
    under the group of `r2` (g1)."""
    text = (world(step)["tree"] / CAP).read_text()
    group = re.search(r"(?ms)^### \[g1\] .*?(?=^### |^## |\Z)", text)
    assert group is not None, text
    found = re.search(r"(?ms)^- \[r1\] .*?(?=^- \[r|^### |^## |\Z)", group.group(0))
    assert found is not None, group.group(0)
    return found.group(0)


def then_kept(step):
    """`the laying service keeps the requirement r9`: the lift done and `r1` back; `the requirement group r3 has the
    requirement r9`: `r1` back under g1 (r47)."""
    if not mine(step) or not world(step).get("supporting") or step.term not in ("keep", "has"):
        return False
    if step.term == "keep":
        assert world(step)["response"].outcome == "done", world(step)["response"]
    _put_back(step)


def then_held(step):
    """`the workspace w2 does not hold the requirement r6`: the capability file holds no line `r2`, which b2 still
    retires, and holds `r1` again, the lifted item's retired line; `the requirement r9 does not support the
    requirement id r8`: no `SUPPORT` with the put-back `r1` (r47)."""
    if not mine(step) or not world(step).get("retiring") or step.term not in ("holds", "support"):
        return False
    if step.term == "support":
        assert SUPPORT not in _put_back(step), _put_back(step)
        return
    text = (world(step)["tree"] / CAP).read_text()
    assert step.template.endswith("Not"), step.text
    assert "- [r2] " not in text and "- [r1] " in text, text


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_retires)
W.local("WhenRequests")(requests)
W.local("ThenDoes")(then_kept)
W.local("ThenDoesNot")(then_held)
