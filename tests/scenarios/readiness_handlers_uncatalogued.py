"""items#r40's Givens (b444), `local` handlers loaded after readiness_handlers_givens.py and so tried before it: a
construct with no catalogue entry, the plugin's construct catalogue written into the scenario's `grammar/` with the
entry of `set-attribute` left out, and a requirement of the item that uses it, readiness_world's PASSING (which sets
an attribute); what `work ready` names each by."""
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
R = shared("shop_readiness_world", "readiness_world.py")

CATALOGUE = Path(__file__).resolve().parents[2] / "grammar" / "constructs.md"
UNCATALOGUED = "set-attribute"


def _says(step, name, text):
    step.context.setdefault("says", {})[name] = text


def _uncatalogued(step):
    """The plugin's construct catalogue in the scenario's repository, less the entry of UNCATALOGUED."""
    text = re.sub(r"^## %s\n.*?(?=^## )" % re.escape(UNCATALOGUED), "", CATALOGUE.read_text(),
                  flags=re.MULTILINE | re.DOTALL)
    assert "## %s\n" % UNCATALOGUED not in text
    path = step.repo / "grammar" / "constructs.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


@W.local("GivenK")
def given_construct(step):
    """`a construct c1`: what `work ready` names it by, the construct the catalogue lacks."""
    if not R.mine(step) or step.kind != "construct":
        return False
    _says(step, step.names[0], UNCATALOGUED)
    return None


@W.local("GivenDoes")
def given_uncatalogued(step):
    """`the construct c1 has no catalogue entry`: the catalogue less its entry; `the requirement r1 uses the construct
    c1`: the requirement the item's one line (`<capability>#r5`), which uses it."""
    if not R.mine(step) or not step.subject.startswith(("the construct ", "the requirement ")):
        return False
    if step.term == "has" and step.subject.startswith("the construct ") and step.nps == ["no catalogue entry"]:
        _uncatalogued(step)
        return None
    if step.term in ("use", "uses") and step.nps[0].startswith("the construct "):
        owner = step.context.get("owner", {}).get(step.names[0], ("item", step.context.get("item", "i1")))
        R.give_lines(step, owner[1], R.PASSING)
        _says(step, step.names[0], "%s#r5" % R.CAPABILITY)
        return None
    return False
