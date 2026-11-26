"""Handlers of checking's provider operations an adapter spec uses (r135, r136, b637), each a `work_queue_world.local`
that takes only a step of a scenario of one of its groups (`mine`). The world is checking_handlers_port's driven port
(the domain-model fixture with the area `stock` of kind `port`, its operation `stock.reserve` and its port line
`stock-port#r1`, which governs it), with the adapter spec a1 nested in it at `adapters/stock-inventory/`, written at
the When: its spec/index.md of `kind: adapter` realising `stock-port#r1`, its provider
`bounded-context/example.org/fixture/inventory@1.2.0` and that provider's contract held as `spec obtain` keeps it,
declaring the one operation `inventory.hold`, with a requirement that governs it. Its `uses:` names, for the port
operation o1 (`stock.reserve`), the operation o2 the Givens say it uses: `inventory.debit`, which no contract it holds
declares (r135); none when a Given says o1 uses no operation (r136). The positive case, `uses:` naming
`inventory.hold`, is tests/scripts/test_adapter_uses.py's.

The When runs `spec check` on the adapter spec (`--root adapters/stock-inventory`); the Thens read its exit and what
its output names each operation by."""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = sys.modules["shop_work_queue_world"]
GROUPS = {"g135", "g136"}
NAME = "stock-inventory"
PARENT = "bounded-context/example.org/fixture/domain-model"
PROVIDER = "bounded-context/example.org/fixture/inventory"
VERSION = "1.2.0"
KINDS = ("port line", "operation", "requirement id", "adapter spec")

INDEX = """---
id: %s/adapter/%s
title: stock over inventory
kind: adapter
realises: [stock-port#r1]
providers: [%s@%s]
uses:
%slanguage: codified-2
imports: [request]
---

# stock over inventory

## Purpose

The adapter that realises the notes service's needs of the stock with inventory's operations.
"""

CONTRACT = """context = "%s"
version = "%s"
status = "published"

[operations."inventory.hold"]
parameters = ["item (text)", "quantity (number)"]
outcomes = ["done → the hold"]
requirements = [
  "holding#r1: When a client holds an item with a quantity, the inventory service shall complete the request.",
]
""" % (PROVIDER, VERSION)


def _module(name):
    return sys.modules["shop_handlers_%s" % hashlib.sha256(str(HERE / name).encode()).hexdigest()[:12]]


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("uses", {"kinds": {}, "order": [], "unused": False})


def given_instance(step):
    if not mine(step) or step.kind not in KINDS:
        return False
    w = world(step)
    w["kinds"][step.names[0]] = step.kind
    if step.kind == "operation":
        w["order"].append(step.names[0])


def given_state(step):
    """`the port line p1 governs the operation o1`, `... has the requirement id r1`, `the adapter spec a1 realises
    the requirement id r1`, `the operation o1 uses the operation o2` and `no contract in the adapter spec a1 holds the
    operation o2`: the world as written; `the operation o1 uses no operation`: its `uses:` empty."""
    if not mine(step) or step.term not in ("govern", "has", "realise", "use", "holds", "hold"):
        return False
    if step.term == "use" and "no operation" in step.text:
        world(step)["unused"] = True


def build(step):
    """The driven port with the adapter spec nested beside it, and what the output names each operation by."""
    w = world(step)
    _module("checking_handlers_port.py").build(step)
    adapter = step.repo / "adapters" / NAME
    (adapter / "spec").mkdir(parents=True)
    port, used = (w["order"] + [None, None])[:2]
    entries = "" if w["unused"] else "  - stock.reserve → inventory.debit\n"
    (adapter / "spec" / "index.md").write_text(INDEX % (PARENT, NAME, PROVIDER, VERSION, entries))
    kept = adapter / "provider" / "example.org" / "fixture" / "inventory" / VERSION
    kept.mkdir(parents=True)
    (kept / "contract.toml").write_text(CONTRACT)
    says = step.context.setdefault("says", {})
    says[port] = "stock.reserve"
    if used:
        says[used] = "inventory.debit"


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "--root", "adapters/" + NAME, "check")


def then_fails(step):
    """`the specification service fails this check`."""
    if not mine(step) or "uses" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr


def then_names(step):
    """`the specification service names the operation o2`: a line of `spec check`'s output names it."""
    if not mine(step) or "uses" not in step.context or step.term != "name":
        return False
    done, said = step.context["result"], step.context["says"][step.names[0]]
    assert any(said in line for line in done.stdout.splitlines()), done.stdout + done.stderr


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_state)
W.local("GivenDoesNot")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenExitsErr")(then_fails)
W.local("ThenDoes")(then_names)
