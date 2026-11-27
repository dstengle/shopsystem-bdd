"""items#r73's world (b731), whose BLOCK and DESK checking's r166 reads too (checking_handlers_brings, b871): an item
whose core line performs another area's lifecycle transition. The domain-model fixture's whole spec, with a second area
`desk` (DESK) whose service's `stamp` the notes area imports; the area `notes` holds the lifecycle `note.status` and its transition `draft → active`; the item holds
notebook's core line requesting `desk.stamp` and setting the status of the note to `active` (BLOCK), so the lay brings
v_m9 of the transition. What `work ready` names the core line by is its requirement's id."""
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
LINE = "notebook#r10"
BLOCK = """### notebook

#### [g10] A note stamped is active
- [r10] When the person stamps a note, the desk service shall set the status of the note to `active`."""
DESK = {"model/desk.md": """---
id: model/example.org/fixture/desk
area: desk
kind: core
imports: [notes]
---

# Desk

## Purpose

The desk where notes are stamped.

```model
service desk
  operation stamp(note)  outcomes: done
```
""", "vocabulary/desk.md": """---
id: vocabulary/example.org/fixture/desk
area: desk
---

# The words of desk

## Terms

- **stamp** (verb, action) → operation desk.stamp. Forms: stamps, stamped. Frame: <actor> stamps <note>.
- **the desk service** (proper noun) → service desk.
"""}
KINDS = ("lifecycle", "area", "transition", "operation", "core line")
TERMS = ("holds", "hold", "has", "have", "performs", "perform", "uses", "use")


def _tag(step):
    """"items" when the step is of items' scenario of r73, else None."""
    requested = sys.modules["vocab"].vocab4.requested
    found = requested.scenario(step.request.node)
    if found is None:
        return None
    return "items" if requested.capability(step.request.node) == "items" and "r73" in found.tags else None


def _spec(step):
    """The world's spec, once: the fixture's and DESK."""
    if step.context.get("lifecycle_spec"):
        return
    spec = step.repo / "spec"
    shutil.copytree(FIXTURE, spec, dirs_exist_ok=True)
    notes = spec / "model" / "notes.md"
    notes.write_text(notes.read_text().replace("imports: []", "imports: [desk]", 1))
    for rel, text in DESK.items():
        (spec / rel).write_text(text)
    step.context["lifecycle_spec"] = True


def given_named(step):
    """`a lifecycle l1`, `an area a1`, `a transition t1`, `an operation o1`, `a core line c1`: the spec they are read
    in; the core line named by its requirement's id."""
    tag = _tag(step)
    if tag is None or step.kind not in KINDS:
        return False
    _spec(step)
    if step.kind == "core line":
        step.context.setdefault("says", {})[step.names[0]] = LINE
    return None


def given_held(step):
    """`the item i1 holds the core line c1`: the item's BLOCK; the areas, the lifecycle, its transition and the
    operation that performs it: so the spec and BLOCK say."""
    tag = _tag(step)
    if tag is None or step.term not in TERMS:
        return False
    if step.term in ("holds", "hold") and step.subject.startswith("the item "):
        B.write_item(step, step.names[0], sections={"Requirements": BLOCK})
    return None


W.local("GivenK")(given_named)
W.local("GivenDoes")(given_held)
