"""items#r68's and r69's Givens (b688), `local` handlers loaded after readiness_handlers_givens.py and so tried before
it, in a context with a domain model (tests/scripts/fixtures/domain-model/'s spec): the item's only lines its
`### imports` block, importing the plugin's pack `time` (r68), or its `### retirements` block, retiring notes' term
`low`, which no line says (r69); it holds no requirement and meets the bar. Of r70 (b694), the fixture's model holds an
object `text` (the base pack's noun, notes' term `text → object text` meaning it) and an object `page` kind of text;
the item imports the pack `base` and retires notes' `text` term, so that after the lay page's kind is base's text."""
import importlib.util
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
BLOCKS = {"pack": "### imports\n\n- pack `time`",
          "term": "### retirements\n\n- term `low → value note.priority low` in notes"}
SPELLED = "### imports\n\n- pack `base`\n\n### retirements\n\n- term `text → object text` in notes"
MODEL = "object text\n  attributes: body (text)\n\nobject page kind of text\n  attributes: title (text)\n\n"
TERMS = ("- **text** (noun) → object text. What a person writes.\n"
         "- **page** (noun) → object page. A text a note is written on.\n")


def mine(step):
    """True when the step is of items' scenarios of r68 and r69."""
    requested = sys.modules["vocab"].vocab4.requested
    found = requested.scenario(step.request.node)
    return requested.capability(step.request.node) == "items" and found is not None \
        and bool({"r68", "r69", "r70"} & set(found.tags))


def spelled(step):
    """True in r70's scenario."""
    return "r70" in sys.modules["vocab"].vocab4.requested.scenario(step.request.node).tags


def _spec(step):
    """The fixture's spec over the repository's `spec/`, once."""
    if not step.context.get("model_spec"):
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        step.context["model_spec"] = True
        if spelled(step):         # r70: an object text a notes term means, and page kind of it
            model = step.repo / "spec" / "model" / "notes.md"
            model.write_text(model.read_text().replace("service notes\n", MODEL + "service notes\n"))
            words = step.repo / "spec" / "vocabulary" / "notes.md"
            words.write_text(words.read_text().rstrip("\n") + "\n" + TERMS)


@W.local("GivenK")
def given_named(step):
    """`a pack p1`, `a term t1`: the world laid; the item's block names it."""
    if not mine(step) or step.kind not in ("pack", "term", "element"):
        return False
    _spec(step)
    return None


@W.local("GivenDoes")
def given_does(step):
    """the item i1 imports the pack p1: its imports block importing `time`; the item i1 retires the term t1: its
    retirements block retiring `low`; the item i1 holds no requirement, and meets this readiness bar: so the item as
    written does."""
    if not mine(step):
        return False
    kind = {"imports": "pack", "import": "pack", "retires": "term", "retire": "term"}.get(step.term)
    if kind is not None and step.subject.startswith("the item "):
        B.write_item(step, step.names[0], sections={"Requirements": SPELLED if spelled(step) else BLOCKS[kind]})
    elif step.term not in ("holds", "hold", "meet", "pass", "has", "have", "refers", "refer", "spells", "spell",
                           "means", "mean"):
        return False
    return None
