"""drafting's removal of the last requirement of a capability new to an item (drafting#r27, b448), in a fresh context
as drafting_handlers_model founds it: spec/index.md in the new language and no capability file. Each a `local`
handler that takes a step of r27's scenario (`mine`) and returns False on any other: the item holds the new
capability's block with one group of one line, `work line --remove <capability>#r<n>` takes the line out, and the
Thens read the item's block of the capability (its narrator, group and purpose) and the commit that kept it."""
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
INDEX = ("---\nid: bounded-context/ex.com/prod/ctx\ntitle: ctx\nlanguage: codified-2\nimports: [request]\n---\n\n"
         "# ctx\n")
LINE = "When the person ticks a checklist, the checklists service shall keep the checklist."


def mine(step):
    """True when the step is of drafting's scenario of r27."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None and "r27" in found.tags


def _fresh(step):
    """A context founded as `migrate init` founds it: its index and empty spec folders."""
    spec = step.repo / "spec"
    for folder in ("model", "vocabulary", "capabilities"):
        (spec / folder).mkdir(parents=True, exist_ok=True)
        (spec / folder / ".gitkeep").write_text("")
    (spec / "index.md").write_text(INDEX)


def _declared():
    name, narrator, purpose = CAPABILITY
    return "### %s\n\nnarrator: %s\ngroup: service\npurpose: %s" % (name, narrator, purpose)


@local("GivenK")
def given_named(step):
    """a capability c1, a requirement r1: what the item's block holds; an item: the backlog's."""
    return None if mine(step) and step.kind in ("capability", "requirement") else False


@local("GivenDoesNot")
def given_absent(step):
    """the capability c1 does not exist: no spec/capabilities/<name>.md, as in a fresh context."""
    return None if mine(step) and step.term == "exist" else False


@local("GivenDoes")
def given_holds(step):
    """the item i1 holds the capability c1: the item, shaped, holding the new capability's block (b317's form); the
    capability c1 has the requirement r1: the block given one group of that one line."""
    if not mine(step) or step.term not in ("holds", "has"):
        return False
    if step.term == "holds":
        _fresh(step)
        step.context["declared"] = step.names[0]
        B.write_item(step, step.names[0], status="shaped", sections={"Requirements": _declared()})
        return None
    block = _declared() + "\n\n#### [g1] Ticking a checklist keeps it\n- [r1] %s" % LINE
    B.write_item(step, step.context["declared"], status="shaped", sections={"Requirements": block})
    return None


@local("WhenRuns")
def remove(step):
    """`work line <item> --remove <capability>#r1` (the request re-keyed by the CLI contract)."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    if not mine(step) or "--remove" not in options:
        return False
    B.run_work(step, "line", B.ident(step.context["declared"]), "--remove", "%s#r1" % CAPABILITY[0])
    return None


def _item_text(step):
    return (step.repo / step.context["items"][step.context["declared"]]).read_text()


@local("ThenDoes")
def kept(step):
    """the item i1 holds the capability c1: its block of the capability keeps its narrator, group and purpose, and
    the line is gone; the drafting service keeps the capability c1: `work` exited 0 and committed the item so."""
    if not mine(step) or "capability" not in step.text:
        return False
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    text = _item_text(step)
    assert _declared() in text and LINE not in text, text
    if step.term in ("holds", "hold"):
        return None
    rel = step.context["items"][step.context["declared"]]
    assert re.search(r"(?m)^### %s$" % CAPABILITY[0], W.git(step.repo, "show", "HEAD:%s" % rel)), step.text
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    return None
