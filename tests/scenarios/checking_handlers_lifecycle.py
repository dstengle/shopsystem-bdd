"""Handlers of checking's scenario of a lifecycle transition another area's operation performs (r101, b610), each a
`work_queue_world.local` that takes only a step of a scenario of its group (`mine`). The world is the domain-model
fixture (tests/scripts/fixtures/domain-model/: the notes area, whose note has the lifecycle of its status, its CLI
contract and the notebook capability's lines) with a second area beside it, written at the When: the area `desk`
(`spec/model/desk.md`, importing notes), whose service holds the operation `desk.publish`, unexposed in the CLI
contract; its words (`spec/vocabulary/desk.md`); and its capability `desk`, whose one line requests the operation and
sets the status of the note from `draft` to `active`, so that the operation performs the transition `draft → active`
of the notes area's lifecycle. The features are written by `features generate`.

The Givens keep what they say (`world`): the lifecycle l1 is note's status, the area a1 `notes`, a2 `desk`, the
transition t1 `draft → active` (named in `spec check`'s rows as `note, status, draft, active`), the operation o1
`desk.publish`. The When runs `spec check`; the Thens read its exit and its output."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g101"}
SAYS = {"lifecycle": "note, status", "area": None, "transition": "note, status, draft, active",
        "operation": "desk.publish"}

MODEL = """---
id: model/example.org/fixture/desk
area: desk
kind: core
imports: [notes]
---

# Desk

## Purpose

The desk a person publishes notes from.

```model
service desk
  operation publish(note)  outcomes: done
```
"""

VOCABULARY = """---
id: vocabulary/example.org/fixture/desk
area: desk
---

# The words of desk

## Terms

- **publish** (verb, action) → operation desk.publish. Forms: publishes, published. Frame: <actor> publishes <note>.
- **the desk service** (proper noun) → service desk.
"""

CAPABILITY = """---
id: capability/example.org/fixture/domain-model/desk
title: Desk
narrator: a person keeping notes
group: service
area: desk
specifies: service desk
language: codified-2
retired: []
unbuilt: []
---

# Desk

## Purpose
A person publishes notes from the desk.

## Behaviour

### [g1] A draft note published becomes active
- [r1] While a note is `draft`, when the person publishes the note, the desk service shall set the status of the note
  to `active`.
"""


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("lifecycle", {"kinds": {}})


def given_instance(step):
    if not mine(step) or step.kind not in SAYS:
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_state(step):
    """`the area a1 holds the lifecycle l1`, `the lifecycle l1 has the transition t1`, `the operation o1 performs the
    transition t1` and `the area a2 holds the operation o1`: the world as written."""
    if not mine(step) or step.term not in ("holds", "has", "perform"):
        return False
    world(step)


def build(step):
    """The fixture copied into the repository with the desk area beside it, and what the output names each instance
    by."""
    repo = step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    spec = repo / "spec"
    (spec / "model" / "desk.md").write_text(MODEL)
    (spec / "vocabulary" / "desk.md").write_text(VOCABULARY)
    (spec / "capabilities" / "desk.md").write_text(CAPABILITY)
    contract = spec / "adapters" / "cli.toml"
    contract.write_text(contract.read_text() + '\n[unexposed]\noperations = ["desk.publish"]\n')
    index = spec / "index.md"
    row = "| notes | core | notebook |\n"
    assert row in index.read_text(), index.read_text()
    index.write_text(index.read_text().replace(row, row + "| desk | core | desk |\n"))
    for name, kind in world(step)["kinds"].items():
        if SAYS[kind]:
            step.context.setdefault("says", {})[name] = SAYS[kind]
    generated = step.run("features", "generate")
    assert generated.returncode == 0, generated.stdout + generated.stderr


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "check")


def then_fails(step):
    """`the specification service fails this check`."""
    if not mine(step) or "lifecycle" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr


def then_names(step):
    """`the specification service names the transition t1`: a row of `spec check`'s output names it."""
    if not mine(step) or "lifecycle" not in step.context or step.term != "name":
        return False
    done, said = step.context["result"], step.context["says"][step.names[0]]
    assert any(line.strip() == said for line in done.stdout.splitlines()), done.stdout + done.stderr


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenExitsErr")(then_fails)
W.local("ThenDoes")(then_names)
