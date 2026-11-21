"""drafting's retirement list applied to an item (drafting#r29, drafting#r30, b461), in readiness_world's codified
spec (the fixture's work-queue, live r1-r4). Each a `local` handler that takes a step of r29's or r30's scenario
(`mine`) and returns False on any other: each requirement the list holds a pair of a live id of work-queue and a new
line, a requirement id no requirement has `work-queue#r9`; `work line <item> --retirement-list <file>` applies it,
and the Thens read the item's block as `work` committed it, or the refusal and the item left as it was."""
import importlib.util
import sys
from pathlib import Path


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
R = shared("shop_readiness_world", "readiness_world.py")
local = W.local

LIVE = ["work-queue#r1", "work-queue#r2", "work-queue#r3"]
NONE = "work-queue#r9"
LINES = ["When the person runs `work list`, `work` shall print every work-item.",
         "When the person runs `work list`, `work` shall exit successfully.",
         "When the person runs `work start` on an initiative, `work` shall commit the initiative."]


def mine(step):
    """True when the step is of drafting's scenario of r29 or r30."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return (sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None
            and bool({"r29", "r30"} & set(found.tags)))


def _world(step):
    """The scenario's requirements, each (the id it retires, its line), by name; the names the list holds."""
    return step.context.setdefault("retirements", {"pairs": {}, "held": []})


@local("GivenK")
def given_named(step):
    """a retirement list r1, a requirement r2, a requirement id r2: what the list file holds; an item: shaped."""
    if not mine(step) or step.kind not in ("retirement list", "requirement", "requirement id", "item"):
        return False
    R.codify(step)
    pairs = _world(step)["pairs"]
    if step.kind == "item":
        B.write_item(step, step.names[0], status="shaped")
    elif step.kind == "requirement":
        k = len(pairs)
        pairs[step.names[0]] = (LIVE[k], LINES[k])
    elif step.kind == "requirement id":
        pairs[step.names[0]] = (NONE, LINES[0])
    return None


@local("GivenDoes")
def given_holds(step):
    """the retirement list r1 holds the requirement r2 (or the requirement id r2): that pair in the file; no
    requirement has the requirement id r2: its id `NONE`, which the fixture's work-queue does not hold."""
    if not mine(step) or step.term not in ("holds", "hold", "has", "have"):
        return False
    if step.term in ("has", "have"):
        return None
    _world(step)["held"].append(step.names[1])
    return None


@local("GivenDoesNot")
def given_not(step):
    """the retirement list r1 does not hold the requirement r4: its pair left out of the file."""
    return None if mine(step) and step.term in ("hold", "holds") else False


@local("WhenRuns")
def apply(step):
    """`work line <item> --retirement-list <file>`, the file one pair a line: `<id> <line>`."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    if not mine(step) or "--retirement-list" not in options:
        return False
    world = _world(step)
    listed = step.repo.parent / "retirements.txt"
    listed.write_text("".join("%s %s\n" % world["pairs"][n] for n in world["held"]))
    item = next(iter(step.context["items"]))
    world["item"] = item
    B.run_work(step, "line", B.ident(item), "--retirement-list", str(listed))
    return None


def _kept(step):
    rel = step.context["items"][_world(step)["item"]]
    return W.git(step.repo, "show", "HEAD:%s" % rel)


@local("ThenDoes")
def then_does(step):
    """keeps the item i1 (exit 0, committed); keeps the requirement r2 (its line in the item, its id retired);
    refuses this request; names the requirement id r2."""
    if not mine(step):
        return False
    done = step.context["result"]
    pairs = _world(step)["pairs"]
    if step.term in ("refuses", "refuse"):
        assert done.returncode != 0, (done.stdout, done.stderr)
        return None
    if step.term in ("names", "name"):
        assert pairs[step.names[0]][0] in done.stderr + done.stdout, (done.stdout, done.stderr)
        return None
    assert done.returncode == 0, (done.stdout, done.stderr)
    rel = step.context["items"][_world(step)["item"]]
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    if "requirement" in step.text:
        ident, line = pairs[step.names[0]]
        kept = _kept(step)
        assert line in kept and ident.split("#")[1] in kept.split("retired:")[1].splitlines()[0], kept
    return None


@local("ThenDoesNot")
def then_does_not(step):
    """does not keep the requirement r4 (its line not in the item); does not keep the item i1 (no commit)."""
    if not mine(step):
        return False
    if "requirement" in step.text:
        assert pairs_line(step) not in _kept(step), _kept(step)
        return None
    assert W.git(step.repo, "rev-parse", "HEAD").strip() == step.context["head"], step.text
    return None


def pairs_line(step):
    return _world(step)["pairs"][step.names[0]][1]
