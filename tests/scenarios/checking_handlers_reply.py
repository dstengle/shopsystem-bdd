"""Handlers of checking's scenario of a port outcome a reply trigger is on (r125, b724), each a
`work_queue_world.local` that takes only a step of a scenario of its group (`mine`). The world is the domain-model
fixture (tests/scripts/fixtures/domain-model/: the notes service, its CLI contract and the notebook capability's core
lines) with the driven port `stock` beside it, written at the When: its operation `stock.reserve`, whose outcomes are
`done → the reservation` and `refused: no stock`; the notes area importing it; the core line notebook#r10 that asks the
stock service to reserve a note (`response-request`), and the core lines that handle each outcome by a reply trigger
(`reply-trigger`): notebook#r11 triggered on the stock service's completion of the request to reserve a note, and
notebook#r12 on its refusal of it. Its features are written by `features generate`.

The Givens say only what the world is. The When runs `spec check` (v_pb2 finds no outcome unhandled, v_m4 no reason
unstated); the Then reads its exit."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g125"}

MODEL = """---
id: model/example.org/fixture/stock
area: stock
kind: port
imports: [notes]
---

# Stock

## Purpose

The stock the notes service reserves for a note through a driven port.

```model
object reservation kind of request
  relations: for → note (one)

service stock
  operation reserve(note, quantity)  outcomes: done → the reservation | refused: no stock
```
"""

VOCABULARY = """---
id: vocabulary/example.org/fixture/stock
area: stock
---

# The words of stock

## Terms

- **reservation** (noun) → object reservation. Stock set aside for a note.
- **reserve** (verb, action) → operation stock.reserve. Forms: reserves, reserved. Frame: <actor> reserves <note>.
- **the stock service** (proper noun) → service stock.
"""

LINES = """
### [g10] A person who starts has a note reserved
- [r10] When the person starts, the notes service shall reserve a note with the quantity `2`.

### [g11] A note whose reservation is completed is kept
- [r11] When the stock service completes the request to reserve a note, the notes service shall keep the note.

### [g12] A note whose reservation is refused is kept
- [r12] If the stock service refuses the request to reserve a note, then the notes service shall keep the note.
"""


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def given(step):
    """Each Given of the group: the world below says it."""
    if not mine(step):
        return False
    step.context["replied"] = True


def build(step):
    """The fixture copied into the repository, the port and the notebook's lines beside it, its features generated."""
    repo = step.repo
    if (repo / "spec" / "model" / "stock.md").is_file():     # the second When's: built by the first
        return
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    spec = repo / "spec"
    (spec / "model" / "stock.md").write_text(MODEL)
    (spec / "vocabulary" / "stock.md").write_text(VOCABULARY)
    notes = spec / "model" / "notes.md"
    assert "imports: []\n" in notes.read_text(), notes.read_text()
    notes.write_text(notes.read_text().replace("imports: []\n", "imports: [stock]\n"))
    notebook = spec / "capabilities" / "notebook.md"
    notebook.write_text(notebook.read_text() + LINES)
    index = spec / "index.md"
    row = "| notes | core | notebook |\n"
    assert row in index.read_text(), index.read_text()
    index.write_text(index.read_text().replace(row, row + "| stock | port | |\n"))
    step.context["generated"] = step.run("features", "generate")


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "check")


def then_completes(step):
    """`the specification service completes this request`: `spec check` finds nothing, the features written."""
    if not mine(step) or "replied" not in step.context:
        return False
    done, generated = step.context["result"], step.context["generated"]
    assert done.returncode == 0, done.stdout + done.stderr
    assert generated.returncode == 0, generated.stdout + generated.stderr


for _template in ("GivenK", "GivenDoes", "GivenDoesNot", "GivenNo", "GivenK_A"):
    W.local(_template)(given)
W.local("WhenRuns")(runs)
W.local("ThenExitsOk")(then_completes)
