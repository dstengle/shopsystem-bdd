"""Handlers of checking's coupling report scenarios (r144-r147, b612, b744), each a `work_queue_world.local` that takes only a
step of a scenario of one of its groups (`mine`). The world is the domain-model fixture (tests/scripts/fixtures/
domain-model/: the area notes, its vocabulary and the notebook capability's lines) with a second area beside it,
`binder`, written at the When: its model (`spec/model/binder.md`), whose object binder holds notes (an element that
refers to the notes word "note", r145) and whose attribute size has the value high, its words (`spec/vocabulary/
binder.md`: "high", a word notes defines too, r144; read before notes', so that notes holds the word's second entry),
and its capability `shelving`, whose line says the notes word "note" (r146); when a Given brings in a Python file
(r147), `src/notes_store.py`, `src/binder_shelf.py` that imports it and `.shop/modules.toml` declaring each area's
files.

The Givens keep what they say (`world`): each scenario's area a2 is notes, the area each coupling is of, and a1 is
binder; the word w1 is `high`, the element e2 `object note`, the requirement r1 `shelving#r1`, and the Python file p2 `src/notes_store.py`, named by the coupling returned as imported by
`src/binder_shelf.py`. The When runs `spec
coupling --json`; the Thens read the couplings of the envelope's content."""
import json
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g144", "g145", "g146", "g147"}
SAYS = {"word": "high", "element": "object note", "requirement": "shelving#r1"}
AREAS = {"a1": "binder", "a2": "notes"}
IMPORT = "src/binder_shelf.py -> src/notes_store.py"
MODULES = """[notes]
modules = ["src/notes_*.py"]

[binder]
modules = ["src/binder_*.py"]
"""

MODEL = """---
id: model/example.org/fixture/binder
area: binder
kind: supporting
imports: [notes]
---

# Binder

## Purpose

The binders a person keeps notes in.

```model
object binder
  attributes: size: low | high
  relations: holds → note (many)

service binder
  operation insert(note)  outcomes: done
```
"""

VOCABULARY = """---
id: vocabulary/example.org/fixture/binder
area: binder
---

# The words of binder

## Terms

- **binder** (noun) → object binder. A folder a person keeps notes in. Plural: binders.
- **size** (attribute) → attribute binder.size.
- **high** (adjective) → value binder.size high.
- **insert** (verb, action) → operation binder.insert. Forms: inserts, inserted. Frame: <actor> inserts <note>.
- **the binder service** (proper noun) → service binder.
"""

SHELVING = """---
id: capability/example.org/fixture/domain-model/shelving
title: Shelving
narrator: a person keeping notes
group: service
area: binder
specifies: service binder
language: codified-2
retired: []
unbuilt: []
---

# Shelving

## Purpose
A person keeps notes in a binder.

## Behaviour

### [g1] A note inserted is kept
- [r1] When the person inserts a note, the binder service shall keep the note.
"""


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("coupling", {"kinds": {}, "of": {}})


def given_instance(step):
    if not mine(step) or step.kind not in ("word", "term", "area", "element", "coupling", "capability",
                                           "requirement", "Python file"):
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_state(step):
    """`the area a2 has the coupling c1`: the coupling is of a2; the other states (has, holds, refers to, means,
    uses) are the world as written."""
    if not mine(step) or step.term not in ("has", "holds", "refer", "mean", "use", "import"):
        return False
    w = world(step)
    if step.term == "has" and w["kinds"].get(step.names[1]) == "coupling":
        w["of"][step.names[1]] = AREAS[step.names[0]]


def build(step):
    """The fixture copied into the repository with the area binder beside notes."""
    repo = step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    spec = repo / "spec"
    (spec / "model" / "binder.md").write_text(MODEL)
    (spec / "vocabulary" / "binder.md").write_text(VOCABULARY)
    (spec / "capabilities" / "shelving.md").write_text(SHELVING)
    index = spec / "index.md"
    row = "| notes | core | notebook |\n"
    assert row in index.read_text(), index.read_text()
    index.write_text(index.read_text().replace(row, row + "| binder | supporting | shelving |\n"))
    if "Python file" in world(step)["kinds"].values():
        code(repo)


def code(repo):
    """r147: binder's Python file imports notes', each area's files declared in `.shop/modules.toml`, committed (a
    Python file is a tracked one)."""
    (repo / "src").mkdir(exist_ok=True)
    (repo / "src" / "notes_store.py").write_text("NOTES = []\n")
    (repo / "src" / "binder_shelf.py").write_text("import notes_store\n")
    (repo / ".shop").mkdir(exist_ok=True)
    (repo / ".shop" / "modules.toml").write_text(MODULES)
    W.init(repo)


def runs(step):
    if not mine(step) or step.term != "`spec coupling`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "coupling", "--json")


def couplings(step):
    """The couplings `spec coupling --json` returned."""
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr
    envelope = json.loads(done.stdout)
    assert envelope["outcome"] == "returned", envelope
    return envelope["content"]["couplings"]


def coupling(step, name):
    """The coupling of the area the Givens say `name` is of, by the other area."""
    area = world(step)["of"][name]
    other = next(a for a in AREAS.values() if a != area)
    found = [c for c in couplings(step) if c["area"] == area and c["by"] == other]
    assert len(found) == 1, couplings(step)
    return found[0]


def then_returns(step):
    """`the specification service returns the coupling c1`."""
    if not mine(step) or "coupling" not in step.context:
        return False
    coupling(step, step.names[0])
    world(step)["returned"] = step.names[0]


def then_does(step):
    """`the coupling c1 holds the word w1`, `... the requirement r1`; `the specification service names the element
    e2`, `... the Python file p2`: the coupling it returned names it, a Python file in its imports."""
    if not mine(step) or "coupling" not in step.context or step.term not in ("holds", "name"):
        return False
    w = world(step)
    owner, thing = (step.names[0], step.names[1]) if step.term == "holds" else (w["returned"], step.names[0])
    kind = w["kinds"][thing]
    found = coupling(step, owner)
    if kind == "Python file":
        assert IMPORT in found.get("imports", []), found
        return
    assert SAYS[kind] in found[kind + "s"], found


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenPrints")(then_returns)
W.local("ThenDoes")(then_does)
