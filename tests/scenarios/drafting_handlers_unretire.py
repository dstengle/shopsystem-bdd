"""drafting's requirement id reinstated in an item (drafting#r89-r91, b760, b768), in readiness_world's codified
spec (the fixture's work-queue, live r1-r4). Each a `local` handler that takes a step of r89's, r90's or r91's
scenario (`mine`) and returns False on any other: the item, written at the When, its block of work-queue holding
`retired: [r1]` and no line, as `work line --retires work-queue#r1 --no-line` writes it, unless a Given says it does
not hold the requirement id (then a block with a line of its own and nothing retired), or, of r91, its own line r9
that retires r1 (`retires: [r9 r1]`, as `work line --retires work-queue#r1` writes it) beside r2 retired with no line,
so that `retired:` is not left empty, which would hide the pair; `work line <item> --remove
work-queue#r1` run on it; and the Thens read the item back, as committed, or the refusal and what it names."""
import re
import sys

W = sys.modules["shop_work_queue_world"]
B = sys.modules["shop_backlog_world"]
R = sys.modules["shop_readiness_world"]
four = sys.modules["shop_world_four"].four
local = W.local
IDENT = "work-queue#r1"
RETIRING = "### work-queue\n\nretired: [r1]"
UNRETIRING = "### work-queue\n\n#### [g9] Kept\n- [r9] " + R.PASSING
OWN = "### work-queue\n\nretired: [r1, r2]\nretires: [r9 r1]\n\n#### [g9] Kept\n- [r9] " + R.PASSING


def mine(step):
    """True when the step is of drafting's scenario of r89, r90 or r91."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return (sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None
            and bool({"r89", "r90", "r91"} & set(found.tags)))


def _world(step):
    return step.context.setdefault("unretiring", {"holds": True, "own": False})


@local("GivenK")
def given_named(step):
    """a requirement id r1, an item i1, a requirement r2 (r3): what the When writes."""
    return None if mine(step) and step.kind in ("requirement id", "item", "requirement") else False


@local("GivenDoes")
def given_retiring(step):
    """the requirement r2 retires the requirement id r1, the item i1 holds the requirement r2: the item's own line
    retires r1; the requirement r3 retires the requirement id r1: a requirement the item must not hold after."""
    if not mine(step) or step.term not in ("retire", "retires", "hold", "holds"):
        return False
    if step.term in ("hold", "holds"):
        _world(step)["own"] = True
    return None


@local("GivenDoesNot")
def given_absent(step):
    """the item i1 does not hold the requirement id r1: the item's block retires nothing."""
    if not mine(step) or step.term not in ("hold", "holds"):
        return False
    _world(step)["holds"] = False
    return None


@local("WhenRuns")
@local("WhenRequests")
def reinstate(step):
    """`work line <item> --remove work-queue#r1` (the request re-keyed by the CLI contract)."""
    if not mine(step):
        return False
    world = _world(step)
    item = world["item"] = re.search(r"\bthe item (i\d+)", step.text).group(1)
    R.codify(step)
    text = OWN if world["own"] else RETIRING if world["holds"] else UNRETIRING
    path = B.write_item(step, item, status="shaped", sections={"Requirements": text})
    world["before"] = path.read_text()
    B.run_work(step, "line", B.ident(item), "--remove", IDENT, **R.NO_INPUT)
    return None


def _committed(step):
    """The item as committed by the run, which exited 0 and left it clean."""
    done, rel = step.context["result"], step.context["items"][_world(step)["item"]]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    return W.git(step.repo, "show", "HEAD:%s" % rel)


@local("ThenDoes")
def then_does(step):
    """refuses this request: an error exit that is no usage error, the item as it was; names the requirement id r1:
    `work-queue#r1` in what `work` printed, with the reason that the item does not retire it; keeps the item i2: the
    run committed it."""
    if not mine(step):
        return False
    done, world = step.context["result"], _world(step)
    out = done.stdout + done.stderr
    if step.term in ("refuse", "refuses"):
        assert done.returncode != 0 and "usage:" not in done.stderr, (done.stdout, done.stderr)
        assert (step.repo / step.context["items"][world["item"]]).read_text() == world["before"], step.text
        return None
    if step.term in ("name", "names"):
        assert IDENT in out and "not retired by" in out, out
        return None
    _committed(step)
    return None


def not_held(step):
    """the item i2 does not hold the requirement id r1: no `retired:` of the item as committed names r1; does not
    hold the requirement r3 (a requirement that retires r1): no `retires:` pair of it names r1, its own line r9 kept."""
    if not mine(step):
        return False
    text = _committed(step)
    if re.search(r"\bthe requirement r\d+$", step.text):
        assert not re.search(r"^retires: \[.*\br\d+ r1\b", text, re.MULTILINE), (step.text, text)
        assert "- [r9] " + R.PASSING in text.split("\n"), (step.text, text)
        return None
    assert not re.search(r"^retired: \[.*\br1\b", text, re.MULTILINE), (step.text, text)
    return None


for _verb in ("hold", "holds"):     # a chain of the key, which `features vocab` finds
    four("ThenDoesNot", _verb, "drafting")(not_held)
