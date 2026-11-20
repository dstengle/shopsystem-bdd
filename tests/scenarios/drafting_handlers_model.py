"""drafting's model line declared in an item that holds a capability new to the context (drafting#r26, b387), in a
fresh context: spec/index.md in the new language, an empty `spec/model/` (as `migrate init` founds it) and no
capability file. Each a `local` handler that takes a step of r26's scenario (`mine`) and returns False on any other:
the item holds the new capability's block, `work line --into <capability> --model` declares the model line, and the
Thens read the item's model block of the capability's area (its own name) and the commit that kept it."""
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
local = W.local

CAPABILITY = ("checklists", "a person keeping checklists", "Checklists of things to do, each ticked off in turn.")
MODEL = "object checklist kind of file\n  attributes: status: open | done"
INDEX = ("---\nid: bounded-context/ex.com/prod/ctx\ntitle: ctx\nlanguage: codified-2\nimports: [request]\n---\n\n"
         "# ctx\n")


def mine(step):
    """True when the step is of drafting's scenario of r26."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None and "r26" in found.tags


def _fresh(step):
    """A context founded as `migrate init` founds it: its index, an empty spec/model/ and spec/vocabulary/."""
    spec = step.repo / "spec"
    for folder in ("model", "vocabulary", "capabilities"):
        (spec / folder).mkdir(parents=True, exist_ok=True)
        (spec / folder / ".gitkeep").write_text("")
    (spec / "index.md").write_text(INDEX)


@local("GivenK")
def given_named(step):
    """a capability c1, a model line m1: what the When writes; an item: the backlog's."""
    return None if mine(step) and step.kind in ("capability", "model line") else False


@local("GivenDoesNot")
def given_absent(step):
    """the capability c1 does not exist: no spec/capabilities/<name>.md, as in a fresh context."""
    return None if mine(step) and step.term == "exist" else False


@local("GivenDoes")
def given_holds(step):
    """the item i1 holds the capability c1: the item, shaped, holding the new capability's block (b317's form)."""
    if not mine(step) or step.term != "holds" or not step.nps[0].startswith("the capability "):
        return False
    _fresh(step)
    name, narrator, purpose = CAPABILITY
    block = "### %s\n\nnarrator: %s\ngroup: service\npurpose: %s" % (name, narrator, purpose)
    B.write_item(step, step.names[0], status="shaped", sections={"Requirements": block})
    step.context.setdefault("says", {})[step.names[1]] = name
    return None


@local("WhenRuns")
def declare(step):
    """`work line <item> --into <capability> --model <lines>` (the request re-keyed by the CLI contract)."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    if not mine(step) or "--model" not in options:
        return False
    item = re.search(r"\bthe item (i\d+)", step.text).group(1)
    step.context["declared"] = item
    B.run_work(step, "line", B.ident(item), "--into", CAPABILITY[0], "--model", MODEL)
    return None


def _item_text(step):
    return (step.repo / step.context["items"][step.context["declared"]]).read_text()


def _block(text):
    """The model lines of the item's `### <area> model` block of the capability's area, or None."""
    found = re.search(r"(?ms)^### %s model\n+```model\n(.*?)^```" % re.escape(CAPABILITY[0]), text)
    return found.group(1) if found else None


@local("ThenDoes")
def kept(step):
    """the item i1 holds the model line m1: its model block of the area holds the lines; the drafting service keeps
    the model line m1: `work` exited 0 and committed the item with them."""
    if not mine(step) or "model line" not in step.text:
        return False
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    block = _block(_item_text(step))
    assert block is not None and MODEL in block, (step.text, _item_text(step))
    if step.term in ("holds", "hold"):
        return None
    rel = step.context["items"][step.context["declared"]]
    assert MODEL.splitlines()[0] in W.git(step.repo, "show", "HEAD:%s" % rel), step.text
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    return None
