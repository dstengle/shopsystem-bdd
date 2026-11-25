"""Handlers of checking's adapter spec scenarios (r84-r87, b540), each a `work_queue_world.local` that takes only a step
of a scenario of one of its groups (`mine`). The world is the domain-model fixture (tests/scripts/fixtures/
domain-model/) as the parent bounded context, with the adapter spec a1 nested in it at `adapters/stock-inventory/`,
written at the When: its spec/index.md of `kind: adapter`, its id the parent's id followed by `/adapter/stock-inventory`
(another context's when a Given says it does not conform to the adapter spec id form), `realises:` the parent's
`notebook#r1` and the requirement id a Given names (`notebook#r99` when no requirement has it), `providers:` the
provider p1 `bounded-context/example.org/fixture/inventory` at `1.2.0`, its contract kept as `spec obtain` keeps it
under `provider/example.org/fixture/inventory/1.2.0/` when a Given says the adapter spec holds it, and each adapter
decision a file of its `adr/`.

The When runs `spec check` on the adapter spec (`--root adapters/stock-inventory`); the Thens read its exit and what
its output names each instance by."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g84", "g85", "g86", "g87"}
PARENT = "bounded-context/example.org/fixture/domain-model"
OTHER = "bounded-context/example.org/fixture/other"
NAME = "stock-inventory"
PROVIDER = "bounded-context/example.org/fixture/inventory"
VERSION = "1.2.0"
KINDS = ("id", "adapter spec", "requirement id", "provider", "contract", "adapter decision")

INDEX = """---
id: %s/adapter/%s
title: stock over inventory
kind: adapter
realises: [%s]
providers: [%s]
language: codified-2
imports: [request]
---

# stock over inventory

## Purpose

The adapter that realises the notes service's needs with inventory's operations.

## Composition
"""

DECISION = """---
id: design-decision/example.org/fixture/domain-model/adapter/stock-inventory/transport
summary: "The adapter reaches inventory over its published operations."
date: 2026-11-25
status: accepted
tier: judgement
---

# 0001. Transport

## Decision

The adapter reaches inventory over its published operations.
"""


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("adapter", {"kinds": {}, "parent": PARENT, "missing": False, "realises": False,
                                               "provider": False, "held": False, "decision": False})


def given_instance(step):
    if not mine(step) or step.kind not in KINDS:
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_state(step):
    """`the adapter spec a1 has the id i1`, `... has the provider p1`, `... realises the requirement id r1`, `... holds
    the adapter decision a2`, `... holds the contract c1`, `... holds no contract`, `the provider p1 has the contract
    c1` and `no requirement has the requirement id r1`."""
    if not mine(step) or step.term not in ("has", "holds", "realise"):
        return False
    w, said = world(step), " ".join(step.nps)
    if step.text.startswith("no requirement has"):
        w["missing"] = True
    elif step.term == "realise":
        w["realises"] = True
    elif "the provider" in said:
        w["provider"] = True
    elif step.term == "holds" and "the adapter decision" in said:
        w["decision"] = True
    elif step.term == "holds" and "the contract" in said:
        w["held"] = True


def given_unconforming(step):
    """`the id i1 does not conform to the adapter spec id form`: the id another context's."""
    if not mine(step) or step.term != "conform":
        return False
    world(step)["parent"] = OTHER


def build(step):
    """The parent context with the adapter spec nested in it, and what the output names each instance by."""
    w, repo = world(step), step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    adapter = repo / "adapters" / NAME
    (adapter / "spec").mkdir(parents=True)
    realised = "notebook#r99" if w["missing"] else "notebook#r1"
    realises = ["notebook#r1"] + (["notebook#r99"] if w["realises"] and w["missing"] else [])
    providers = ["%s@%s" % (PROVIDER, VERSION)] if w["provider"] else []
    (adapter / "spec" / "index.md").write_text(INDEX % (w["parent"], NAME, ", ".join(realises), ", ".join(providers)))
    if w["held"]:
        kept = adapter / "provider" / "example.org" / "fixture" / "inventory" / VERSION
        kept.mkdir(parents=True)
        (kept / "contract.toml").write_text('context = "%s"\nversion = "%s"\nstatus = "published"\n'
                                            % (PROVIDER, VERSION))
    if w["decision"]:
        (adapter / "adr").mkdir()
        (adapter / "adr" / "0001-transport.md").write_text(DECISION)
    says = {"id": "%s/adapter/%s" % (w["parent"], NAME), "requirement id": realised, "provider": PROVIDER}
    for name, kind in w["kinds"].items():
        if kind in says:
            step.context.setdefault("says", {})[name] = says[kind]


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "--root", "adapters/" + NAME, "check")


def then_completes(step):
    """`the specification service completes this request`: `spec check` finds nothing in the adapter spec."""
    if not mine(step) or "adapter" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr


def then_fails(step):
    """`the specification service fails this check`."""
    if not mine(step) or "adapter" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr


def then_names(step):
    """`the specification service names the id i1`: a line of `spec check`'s output names it."""
    if not mine(step) or "adapter" not in step.context or step.term != "name":
        return False
    done, said = step.context["result"], step.context["says"][step.names[0]]
    assert any(said in line for line in done.stdout.splitlines()), done.stdout + done.stderr


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_state)
W.local("GivenDoesNot")(given_unconforming)
W.local("WhenRuns")(runs)
W.local("ThenExitsOk")(then_completes)
W.local("ThenExitsErr")(then_fails)
W.local("ThenDoes")(then_names)
