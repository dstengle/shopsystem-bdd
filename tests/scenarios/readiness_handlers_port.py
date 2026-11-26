"""items#r71's Givens (b705), `local` handlers loaded after readiness_handlers_givens.py and so tried before it, in a
context with a domain model and a driven port: tests/scripts/fixtures/domain-model/'s spec with checking_handlers_port's
area `stock` of kind `port` beside it (its model, its words, the notes model importing it) and its capability
`stock-port` holding no line yet. The item holds a core line of notebook, whose response asks the stock service to
reserve a note, and the port line of stock-port that governs that request; the port line supports the core line's
requirement id when its `Relied on by:` names it, as `work line --relied-on-by` keeps it. Both lines' ids are `r1`,
which collides with notebook's own r1, so the bar's renumbered copy carries the id under `Relied on by:` too."""
import hashlib
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


def handlers(file):
    """A handler module vocab's glob loaded already, by the name it gave it."""
    path = Path(__file__).with_name(file).resolve()
    return sys.modules["shop_handlers_%s" % hashlib.sha256(str(path).encode()).hexdigest()[:12]]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
P = handlers("checking_handlers_port.py")
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
CAPABILITY = """---
id: capability/example.org/fixture/domain-model/stock-port
title: Stock port
narrator: the notes service
group: service
area: stock
specifies: service stock
language: codified-2
retired: []
unbuilt: []
---

# Stock port

## Purpose
What the notes service needs of the stock it reaches.

## Behaviour
"""
CORE = ("### notebook\n\n#### [g1] A person who starts has a note reserved\n- [r1] When the person starts, the notes "
        "service shall reserve a note with the quantity `2`.")
PORT = ("### stock-port\n\n#### [g1] A note reserved is reserved\n- [r1] When the notes service reserves a note, the "
        "stock service shall complete the request.")
RELIED = "Relied on by: notebook#r1"


def mine(step):
    """True when the step is of items' scenario of r71."""
    requested = sys.modules["vocab"].vocab4.requested
    found = requested.scenario(step.request.node)
    return requested.capability(step.request.node) == "items" and found is not None and "r71" in found.tags


def _world(step):
    return step.context.setdefault("ported", {"held": [], "supports": False})


def _spec(step):
    """The fixture's spec over the repository's `spec/` with the driven port beside it, once."""
    if step.context.get("model_spec"):
        return
    spec = step.repo / "spec"
    shutil.copytree(FIXTURE, spec, dirs_exist_ok=True)
    index = spec / "index.md"
    text = index.read_text()        # its id the fixture's, which its capabilities' ids and `Relied on by:` are read in
    row = "| notes | core | notebook |\n"
    assert row in text, text
    index.write_text(text.replace(row, row + "| stock | port | stock-port |\n"))
    (spec / "model" / "stock.md").write_text(P.MODEL % "port")
    (spec / "vocabulary" / "stock.md").write_text(P.VOCABULARY)
    (spec / "capabilities" / "stock-port.md").write_text(CAPABILITY)
    notes = spec / "model" / "notes.md"
    notes.write_text(notes.read_text().replace("imports: []\n", "imports: [stock]\n"))
    step.context["model_spec"] = True


def _write(step):
    """The item with the lines it holds, the port line's `Relied on by:` after it when it supports the core line."""
    world = _world(step)
    blocks = [CORE] if "core" in world["held"] else []
    if "port" in world["held"]:
        blocks.append(PORT + ("\n" + RELIED if world["supports"] else ""))
    B.write_item(step, world["item"], sections={"Requirements": "\n\n".join(blocks)})


@W.local("GivenK")
def given_named(step):
    """`a port line p1`, `a core line c1`, `a requirement id r1`: the spec they are read in."""
    if not mine(step) or step.kind not in ("port line", "core line", "requirement id"):
        return False
    _spec(step)
    return None


@W.local("GivenDoes")
def given_held(step):
    """`the item i1 holds the port line p1` (the core line c1): the item's block of it; `the core line c1 has the
    requirement id r1`: its id; `the port line p1 supports the requirement id r1`: its `Relied on by:` names it."""
    if not mine(step) or step.term not in ("holds", "hold", "has", "have", "supports", "support"):
        return False
    world = _world(step)
    if step.term in ("holds", "hold"):
        world["item"] = step.names[0]
        world["held"].append("port" if step.nps[0].startswith("the port line") else "core")
    elif step.term in ("supports", "support"):
        world["supports"] = True
    if "item" in world:
        _write(step)
    return None
