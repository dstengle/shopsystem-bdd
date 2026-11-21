"""items#r41's Givens (b477), `local` handlers loaded after readiness_handlers_givens.py and so tried before it, in a
context with a domain model (tests/scripts/fixtures/domain-model/'s spec: the service notes, its operation
`archive(note)`): the item's model line restates `archive` with a refusal reason no line states, which violates
v_m4, beside a requirement line of notebook that passes; what `work ready` names each by."""
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
MODEL = "service notes\n  operation archive(note)  outcomes: done | refused: retired note"
ELEMENT, RULE = "notes.archive", "v_m4"
LINE = "While a note is `active`, when the person archives the note, the notes service shall keep the note."
REQUIREMENTS = ("### notebook\n\n#### [g10] An active note archived is kept\n- [r10] %s\n\n### notes model\n\n```model\n%s\n```"
                % (LINE, MODEL))


def mine(step):
    """True when the step is of items' scenario of r41."""
    requested = sys.modules["vocab"].vocab4.requested
    found = requested.scenario(step.request.node)
    return requested.capability(step.request.node) == "items" and found is not None and "r41" in found.tags


def _says(step, name, text):
    step.context.setdefault("says", {})[name] = text


def _spec(step):
    """The fixture's spec over the repository's `spec/`, once, its index naming the context `ex.com/prod/ctx`."""
    if step.context.get("model_spec"):
        return
    shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
    index = step.repo / "spec" / "index.md"
    index.write_text(re.sub(r"(?m)^id: .*$", "id: bounded-context/ex.com/prod/ctx", index.read_text(), count=1))
    step.context["model_spec"] = True


@W.local("GivenK")
def given_named(step):
    """`a model line m1`: named by the operation it restates; `a rule r1`: the rule it violates."""
    if not mine(step) or step.kind not in ("model line", "rule"):
        return False
    _spec(step)
    _says(step, step.names[0], ELEMENT if step.kind == "model line" else RULE)
    return None


@W.local("GivenDoes")
def given_held(step):
    """`the item i1 holds the model line m1`: the item's requirements MODEL in its notes model block beside notebook's
    LINE; `the model line m1 violates the rule r1`: so MODEL does, its reason stated by no line."""
    if not mine(step) or not step.subject.startswith(("the item ", "the model line ")):
        return False
    if step.term in ("holds", "hold") and step.nps[0].startswith("the model line "):
        B.write_item(step, step.names[0], sections={"Requirements": REQUIREMENTS})
        return None
    return None if step.term in ("violates", "violate") else False
