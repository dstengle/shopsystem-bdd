"""drafting's model line that restates an operation, declared in an item (drafting r41, b463), in a context with a
domain model (tests/scripts/fixtures/domain-model/'s spec: the service notes, its operation `archive(note)`). Each a
`local` handler that takes a step of r41's scenario (`mine`) and returns False on any other: the model line notes'
`archive` with a parameter added and a refusal reason, `work line --into notebook --model` run on the item, and the
Thens read the item's model block of the area notes and the commit that kept it, the block laid over the model
declaring `archive` once, as the model line says it."""
import importlib.util
import re
import shutil
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
local = W.local
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
LINE = "  operation archive(note, reason)  outcomes: done | refused: retired note"
MODEL = "service notes\n" + LINE


def mine(step):
    """True when the step is of drafting's scenario of r41."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None and "r41" in found.tags


def _spec(step):
    if not step.context.get("restate_spec"):
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        step.context["restate_spec"] = True


@local("GivenK")
def given_named(step):
    """a model line m1 (notes' archive restated), an operation o1 (notes.archive): the fixture's spec."""
    if not mine(step) or step.kind not in ("model line", "operation"):
        return False
    _spec(step)
    return None


@local("GivenDoes")
def given_restates(step):
    """the model line m1 restates the operation o1: so MODEL says it, of the fixture's `archive(note)`."""
    return None if mine(step) and step.term in ("restates", "restate") else False


@local("WhenRuns")
def declare(step):
    """`work line <item> --into notebook --model <lines>` (the request re-keyed by the CLI contract)."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    if not mine(step) or "--model" not in options:
        return False
    item = re.search(r"\bthe item (i\d+)", step.text).group(1)
    step.context["declared"] = item
    B.write_item(step, item, status="shaped")
    B.run_work(step, "line", B.ident(item), "--into", "notebook", "--model", MODEL)
    return None


def _block(text):
    found = re.search(r"(?ms)^### notes model\n+```model\n(.*?)^```", text)
    return found.group(1).rstrip("\n").split("\n") if found else None


@local("ThenDoes")
def kept(step):
    """the item i1 holds the model line m1: its notes model block holds it, and laid over the model the block
    declares `archive` once, as the line says it; the drafting service keeps it: committed."""
    if not mine(step) or "model line" not in step.text:
        return False
    import backlog_model
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    rel = step.context["items"][step.context["declared"]]
    text = (step.repo / rel).read_text()
    block = _block(text)
    assert block is not None and LINE in block, (step.text, text)
    model = (step.repo / "spec" / "model" / "notes.md").read_text().split("\n")
    laid = backlog_model.merged(model, block)
    assert [x for x in laid if x.startswith("  operation archive(")] == [LINE], laid
    if step.term not in ("holds", "hold"):
        assert LINE in W.git(step.repo, "show", "HEAD:%s" % rel), step.text
        assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    return None
