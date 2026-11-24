"""Handlers of checking's scenarios of a response's request (r71, r72, b543), each a `work_queue_world.local` that
takes only a step of a scenario of one of its groups (`mine`). The world is the domain-model fixture
(tests/scripts/fixtures/domain-model/: the notes service, its CLI contract and the notebook capability's lines) with a
driven port beside it, written at the When: the area `stock` of kind `port`, whose operation `stock.reserve` no line's
trigger requests (no requirement governs it) and the CLI contract has no table of; the notes area importing it; and
r1, a notebook line whose response asks the stock service to reserve a note with a quantity (`response-request`). In
r72's group the operation declares the refusal reason `no stock`, and r2, a notebook line triggered on the stock
service's refusal of a reservation, the thing the operation makes. The features are written by `features generate`.

The Givens say only what the world is; the When runs `spec check`; the Then reads its exit: v_m7 counts r1's request
of `stock.reserve`, and v_m4 counts r2 as stating its reason."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g71", "g72"}

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
  operation reserve(note, quantity)  outcomes: done → the reservation%s
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

ASKING = """
### [g10] A person who starts has a note reserved
- [r10] When the person starts, the notes service shall reserve a note with the quantity `2`.
"""

REFUSED = """
### [g11] A reservation refused is kept
- [r11] If the stock service refuses a reservation, then the notes service shall keep the reservation.
"""


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def refusing(step):
    """True in r72's group: the operation declares a refusal reason and a line is triggered on its refusal."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return "g72" in found.tags


def given(step):
    """Each Given of the groups: the world below says it."""
    if not mine(step):
        return False
    step.context["asking"] = True


def build(step):
    """The fixture copied into the repository, the port beside it and the notebook's lines, its features generated."""
    repo, refused = step.repo, refusing(step)
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    spec = repo / "spec"
    (spec / "model" / "stock.md").write_text(MODEL % (" | refused: no stock" if refused else ""))
    (spec / "vocabulary" / "stock.md").write_text(VOCABULARY)
    notes = spec / "model" / "notes.md"
    assert "imports: []\n" in notes.read_text(), notes.read_text()
    notes.write_text(notes.read_text().replace("imports: []\n", "imports: [stock]\n"))
    notebook = spec / "capabilities" / "notebook.md"
    notebook.write_text(notebook.read_text() + ASKING + (REFUSED if refused else ""))
    index = spec / "index.md"
    row = "| notes | core | notebook |\n"
    assert row in index.read_text(), index.read_text()
    index.write_text(index.read_text().replace(row, row + "| stock | port | |\n"))
    generated = step.run("features", "generate")
    assert generated.returncode == 0, generated.stdout + generated.stderr


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "check")


def then_completes(step):
    """`the specification service completes this request`: `spec check` finds nothing."""
    if not mine(step) or "asking" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr


for _template in ("GivenK", "GivenDoes", "GivenDoesNot", "GivenNo", "GivenK_A"):
    W.local(_template)(given)
W.local("WhenRuns")(runs)
W.local("ThenExitsOk")(then_completes)
