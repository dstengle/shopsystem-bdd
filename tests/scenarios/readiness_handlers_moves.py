"""items#r64's and r65's Givens (b654), `local` handlers loaded after readiness_handlers_givens.py and so tried before
it, in a context with a domain model (tests/scripts/fixtures/domain-model/'s spec, beside it an area `labels` with an
empty model): the item's only lines its `### moves` block, which moves notes' `object tag` to labels (r64) or shared's
term `the person` to notes, the area that declares the actor (r65); it holds no requirement and meets the bar."""
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
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
LABELS = "---\nid: model/example.org/fixture/labels\narea: labels\nkind: core\nimports: []\n---\n\n# Labels\n\n" \
         "## Purpose\n\nThe labels notes carry.\n\n```model\n```\n"
MOVES = {"model line": "- model line `object tag` from notes to labels",
         "term": "- term `the person → actor the person` from shared to notes"}


def mine(step):
    """True when the step is of items' scenarios of r64 and r65."""
    requested = sys.modules["vocab"].vocab4.requested
    found = requested.scenario(step.request.node)
    return requested.capability(step.request.node) == "items" and found is not None \
        and bool({"r64", "r65"} & set(found.tags))


def _spec(step):
    """The fixture's spec over the repository's `spec/`, once, its index naming the context `ex.com/prod/ctx`, and
    the area labels."""
    if step.context.get("model_spec"):
        return
    shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
    index = step.repo / "spec" / "index.md"
    index.write_text(re.sub(r"(?m)^id: .*$", "id: bounded-context/ex.com/prod/ctx", index.read_text(), count=1))
    (step.repo / "spec" / "model" / "labels.md").write_text(LABELS)
    step.context["model_spec"] = True


def _moves(step, name, kind):
    """The item `name` holding only its moves block, moving the model line or the term."""
    B.write_item(step, name, sections={"Requirements": "### moves\n\n%s" % MOVES[kind]})


@W.local("GivenK")
def given_named(step):
    """`a model line m1`, `an area a1`, `a term t1`: the world laid; the item's block names each."""
    if not mine(step) or step.kind not in ("model line", "area", "term"):
        return False
    _spec(step)
    return None


@W.local("GivenDoes")
def given_does(step):
    """the model line m1 moves to the area a1: noted; the item i1 holds the model line m1: its moves block moving
    `object tag` to labels; the item i1 moves the term t1: its moves block moving the person into notes; the item i1
    holds no requirement, and meets (passes) this readiness bar: so the item as written does."""
    if not mine(step):
        return False
    if step.term in ("moves", "move") and step.subject.startswith("the item "):
        _moves(step, step.names[0], "term")
    elif step.term in ("holds", "hold") and step.nps[0].startswith("the model line "):
        _moves(step, step.names[0], "model line")
    elif step.term not in ("moves", "move", "holds", "hold", "meet", "pass"):
        return False
    return None
