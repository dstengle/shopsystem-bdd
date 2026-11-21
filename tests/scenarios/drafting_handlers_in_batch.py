"""drafting's lines of an in-batch item (r38-r40, b460): in readiness_world's codified spec, the item `in-batch`,
holding the world's passing line as `work-queue#r5` when a Given says it holds the requirement; `work line` run on it
(`--reword` to the world's other line, `--remove`, or a plain line into work-queue), and the Thens that read the item
as committed, still `in-batch`. Each a `local` handler that takes a step of those scenarios (`mine`) and returns
False on any other."""
import importlib.util
import re
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
TAGS = {"r38", "r39", "r40"}
OWN = "%s#r5" % R.CAPABILITY      # the id give_lines gives the item's line


def mine(step):
    """True when the step is of drafting's scenarios of r38-r40."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None and bool(
        TAGS & set(found.tags))


@local("GivenK")
def given_named(step):
    """a requirement r1: the line the item holds or is given; nothing yet."""
    return None if mine(step) and step.kind == "requirement" else False


@local("GivenDoes")
def given_holds(step):
    """the item i1 holds the requirement r1: the world's passing line, `work-queue#r5`."""
    if not mine(step) or step.term not in ("holds", "hold"):
        return False
    R.give_lines(step, step.names[0], R.PASSING)
    step.context["held"] = step.names[1]
    return None


@local("WhenRuns")
def run(step):
    """`work line` on the in-batch item: `--reword` its line to the world's other line, `--remove` it, or a plain
    line drafted into work-queue (the request re-keyed by the CLI contract)."""
    if not mine(step):
        return False
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    item = step.context["drafted"] = re.search(r"\bthe item (i\d+)", " ".join(W.scenario_texts(step))).group(1)
    R.codify(step)
    B.write_item(step, item, status="in-batch")
    if "--reword" in options:
        step.context["written"], step.context["gone"] = R.LINE, R.PASSING
        B.run_work(step, "line", B.ident(item), "--reword", OWN, R.LINE, **R.NO_INPUT)
    elif "--remove" in options:
        step.context["gone"] = R.PASSING
        B.run_work(step, "line", B.ident(item), "--remove", OWN, **R.NO_INPUT)
    else:
        step.context["written"] = R.LINE
        B.run_work(step, "line", B.ident(item), "--into", R.CAPABILITY, R.LINE, **R.NO_INPUT)
    return None


@local("ThenDoes")
@local("ThenDoesNot")
def kept(step):
    """the item i1 holds (does not hold) the requirement, the drafting service keeps (does not keep) it: `work`
    exited 0, the item, still `in-batch`, holds the written line and not the one taken out, as committed."""
    if not mine(step) or "requirement" not in step.text:
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    rel = step.context["items"][step.context["drafted"]]
    text = (step.repo / rel).read_text()
    assert W.field(step.repo / rel, "status") == "in-batch", (step.text, text)
    assert W.git(step.repo, "show", "HEAD:%s" % rel) == text, step.text
    if step.context.get("written"):
        assert step.context["written"] in text, (step.text, text)
    if step.context.get("gone"):
        assert step.context["gone"] not in text, (step.text, text)
    return None
