"""Handlers of checking's bound check scenarios (r95-r99, b549), each a `work_queue_world.local` that takes only a step
of a scenario of one of its groups (`mine`). The world is the domain-model fixture (tests/scripts/fixtures/domain-model/:
the notes service, its CLI contract and the notebook capability's core lines) with the driven port `stock` beside it,
written at the When: its operation `stock.reserve`, whose outcomes are `done → the reservation` and, where the group
says, `refused: no stock`; the notes area importing it; and of the lines that bound it those the group's world names
(`WORLDS`): the core line notebook#r10 that asks the stock service to reserve a note (`response-request`), the core
line notebook#r11 triggered on the stock service's completion of a reservation (it handles `done`), and the port line
stock-port#r1, triggered on the reservation, which says the stock service completes it or, where the group says, never
refuses it (it excludes the refusal), with its `Relied on by:` where the group says. Its features are written by
`features generate`.

The Givens say only what the world is; what the output names each instance by is `SAYS`. The When runs `spec check`;
the Thens read its exit and its output."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"

# group: (refusal declared, notebook#r10 asks, notebook#r11 handles done, the port line's response or None, relied on by)
WORLDS = {
    "g95": (False, False, True, "complete", None),
    "g96": (False, True, False, None, None),
    "g97": (False, True, True, "complete", "notebook#r2"),
    "g98": (False, True, True, "complete", None),
    "g99": (True, True, True, "not refuse", None),
}
SAYS = {"operation": "stock.reserve", "driven port": "stock", "port line": "stock-port#r1",
        "core line": "notebook#r10", "requirement id": "notebook#r2"}
OUTCOMES = {"g96": "stock.reserve done", "g99": "stock.reserve refused: no stock"}

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

HANDLING = """
### [g11] A reservation completed is kept
- [r11] When the stock service completes a reservation, the notes service shall keep the reservation.
"""

PORT = """---
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

### [g1] A note reserved is answered
- [r1] When the notes service reserves a note, the stock service shall %s the request.
%s"""


def group(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    if found is None or Path(found.feature.filename).stem != "checking":
        return None
    return next((g for g in WORLDS if g in found.tags), None)


def mine(step):
    return group(step) is not None


def given(step):
    """Each Given of the groups: the world below says it; an instance's name kept with what the output names it by."""
    if not mine(step):
        return False
    says = step.context.setdefault("says", {})
    for name in step.names:
        if step.kind == "operation outcome":
            says[name] = OUTCOMES.get(group(step), name)
        elif step.kind in SAYS:
            says[name] = SAYS[step.kind]
    step.context["bound"] = True


def build(step):
    """The fixture copied into the repository, the port and the lines of the group's world beside it, its features
    generated."""
    repo = step.repo
    refusal, asks, handles, port, relied = WORLDS[group(step)]
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    spec = repo / "spec"
    (spec / "model" / "stock.md").write_text(MODEL % (" | refused: no stock" if refusal else ""))
    (spec / "vocabulary" / "stock.md").write_text(VOCABULARY)
    notes = spec / "model" / "notes.md"
    assert "imports: []\n" in notes.read_text(), notes.read_text()
    notes.write_text(notes.read_text().replace("imports: []\n", "imports: [stock]\n"))
    notebook = spec / "capabilities" / "notebook.md"
    notebook.write_text(notebook.read_text() + (ASKING if asks else "") + (HANDLING if handles else ""))
    if port:
        (spec / "capabilities" / "stock-port.md").write_text(
            PORT % (port, "Relied on by: %s.\n" % relied if relied else ""))
    index = spec / "index.md"
    row = "| notes | core | notebook |\n"
    assert row in index.read_text(), index.read_text()
    index.write_text(index.read_text().replace(row, row + "| stock | port | %s |\n" % ("stock-port" if port else "")))
    generated = step.run("features", "generate")
    assert generated.returncode == 0, generated.stdout + generated.stderr


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "check")


def then_completes(step):
    """`the specification service completes this request`: `spec check` finds nothing."""
    if not mine(step) or "bound" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr


def then_fails(step):
    """`the specification service fails this check`."""
    if not mine(step) or "bound" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr


def then_names(step):
    """`the specification service names the operation o1`: a line of `spec check`'s output names it."""
    if not mine(step) or "bound" not in step.context or step.term != "name":
        return False
    done, said = step.context["result"], step.context["says"][step.names[0]]
    assert any(said in line for line in done.stdout.splitlines()), (said, done.stdout + done.stderr)


for _template in ("GivenK", "GivenDoes", "GivenDoesNot", "GivenNo", "GivenK_A"):
    W.local(_template)(given)
W.local("WhenRuns")(runs)
W.local("ThenExitsOk")(then_completes)
W.local("ThenExitsErr")(then_fails)
W.local("ThenDoes")(then_names)
