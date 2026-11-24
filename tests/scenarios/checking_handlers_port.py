"""Handlers of checking's driven port scenarios (r69, r70, b548), each a `work_queue_world.local` that takes only a step
of a scenario of one of its groups (`mine`). The world is the domain-model fixture (tests/scripts/fixtures/domain-model/:
the notes service, its CLI contract and the notebook capability's lines) with a driven port beside it, written at the
When: the area `stock` of kind `port` (`spec/model/stock.md`), whose service holds the operation `stock.reserve`, which
the CLI contract has no table of; its words (`spec/vocabulary/stock.md`); and its port contract `stock-port`, whose one
line requests the operation, so that v_m7 counts it, with its scenario as `features generate` writes it.

The Givens keep what they say (`world`): the area a1 is `stock`, the operation o1 `stock.reserve`, the requirement r1
`stock-port#r1`; a requirement id no requirement has is `notebook#r99`, which r1 then supports under its
`Relied on by:`. The When runs `spec check`; the Thens read its exit and its output."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g69", "g70"}
MISSING = "notebook#r99"
SAYS = {"area": "stock", "operation": "stock.reserve", "requirement": "stock-port#r1", "requirement id": MISSING}

MODEL = """---
id: model/example.org/fixture/stock
area: stock
kind: %s
imports: [notes]
---

# Stock

## Purpose

The stock the notes service reaches through a driven port.

```model
service stock
  operation reserve(note)  outcomes: done
```
"""

VOCABULARY = """---
id: vocabulary/example.org/fixture/stock
area: stock
---

# The words of stock

## Terms

- **reserve** (verb, action) → operation stock.reserve. Forms: reserves, reserved. Frame: <actor> reserves <note>.
- **the stock service** (proper noun) → service stock.
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

### [g1] A note reserved is reserved
- [r1] When the notes service reserves a note, the stock service shall complete the request.
%s"""

FEATURE = """# generated from spec/capabilities/stock-port.md by features generate; do not edit
Feature: Stock port
  Narrator: the notes service

  @g1 @r1
  Scenario: A note reserved is reserved
    Given a note n1
    When the notes service reserves the note n1
    Then the stock service completes this request
"""


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("port", {"kinds": {}, "kind": "port", "supports": False})


def given_instance(step):
    if not mine(step) or step.kind not in SAYS:
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_kind(step):
    """`the kind of the area a1 is `port``."""
    if not mine(step) or step.attribute != "kind":
        return False
    world(step)["kind"] = step.values[0].strip("`")


def given_state(step):
    """`the area a1 holds the operation o1`, `the operation o1 has no operation table` and `no requirement has the
    requirement id r2`: the world as written; `the requirement r1 supports the requirement id r2`: r1's
    `Relied on by:` names it."""
    if not mine(step) or step.term not in ("holds", "has", "support"):
        return False
    if step.term == "support":
        world(step)["supports"] = True


def build(step):
    """The fixture copied into the repository with the port beside it, and what the output names each instance by."""
    w, repo = world(step), step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    spec = repo / "spec"
    (spec / "model" / "stock.md").write_text(MODEL % w["kind"])
    (spec / "vocabulary" / "stock.md").write_text(VOCABULARY)
    (spec / "capabilities" / "stock-port.md").write_text(PORT % ("Relied on by: %s.\n" % MISSING
                                                                 if w["supports"] else ""))
    (repo / "features" / "stock-port.feature").write_text(FEATURE)
    index = spec / "index.md"
    row = "| notes | core | notebook |\n"
    assert row in index.read_text(), index.read_text()
    index.write_text(index.read_text().replace(row, row + "| stock | %s | stock-port |\n" % w["kind"]))
    for name, kind in w["kinds"].items():
        step.context.setdefault("says", {})[name] = SAYS[kind]


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "check")


def then_completes(step):
    """`the specification service completes this request`: `spec check` finds nothing."""
    if not mine(step) or "port" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr


def then_fails(step):
    """`the specification service fails this check`."""
    if not mine(step) or "port" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr


def then_names(step):
    """`the specification service names the requirement id r2`: a line of `spec check`'s output names it."""
    if not mine(step) or "port" not in step.context or step.term != "name":
        return False
    done, said = step.context["result"], step.context["says"][step.names[0]]
    assert any(said in line for line in done.stdout.splitlines()), done.stdout + done.stderr


W.local("GivenK")(given_instance)
W.local("GivenK_A")(given_kind)
W.local("GivenDoes")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenExitsOk")(then_completes)
W.local("ThenExitsErr")(then_fails)
W.local("ThenDoes")(then_names)
