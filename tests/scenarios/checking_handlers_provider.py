"""Handlers of checking's provider words in an adapter spec (g106-g109: r106-r109, b550), each a
`work_queue_world.local` that takes only a step of a scenario of one of its groups (`mine`). The world is
checking_handlers_adapter's: the domain-model fixture as the parent, the adapter spec a1 nested in it at
`adapters/stock-inventory/`, written at the When. When a Given says the adapter spec holds the contract, its
`providers:` names inventory at `1.2.0` and the contract is kept under its `provider/` with the provider's terms
(`TERMS`: the noun `product` and the verb `reserve`). A requirement of the adapter spec that uses the provider's term
is r1 of its capability `stock` (`STOCK`), its feature beside it. A provider's term that clashes with another term is
`product` beside the adapter spec's own `product` in its glossary; the adapter spec renames it with
`renames: [product → stocked product]` when a Given says so, r1 then saying the new word. An assumed description is
the capability `ledger` with `assumed: true` (`LEDGER`), its feature's one scenario tagged with its group alone when a
Given says no scenario refers to its requirement id.

The When runs `spec check` on the adapter spec; checking_handlers_adapter's Thens read its exit, and the Then here
what its output names each instance by (the term's word, the requirement id `ledger#r1`)."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g106", "g107", "g108", "g109"}
PARENT = "bounded-context/example.org/fixture/domain-model"
NAME = "stock-inventory"
PROVIDER = "bounded-context/example.org/fixture/inventory"
VERSION = "1.2.0"
KINDS = ("contract", "adapter spec", "requirement", "term", "assumed description", "requirement id")

INDEX = """---
id: %s/adapter/%s
title: stock over inventory
kind: adapter
realises: [notebook#r1]
providers: [%s]
renames: [%s]
language: codified-2
imports: [request]
---

# stock over inventory

## Purpose

The adapter that realises the notes service's needs with inventory's operations.

## Glossary

- **the stock service** (proper noun): the adapter. Kind of: service.
%s
## Composition
"""

OWN = "- **product** (noun): what the notes service asks the adapter to keep. Plural: products.\n"

CONTRACT = """context = "%s"
version = "%s"
status = "published"
terms = [
  "product (noun): A thing inventory keeps in stock. Plural: products.",
  "reserve (verb, action): Forms: reserves, reserved. Frame: <actor> reserves <product>.",
]

[objects."product"]
area = "stock"
""" % (PROVIDER, VERSION)

STOCK = """---
id: capability/example.org/fixture/domain-model/adapter/stock-inventory/stock
title: Stock
narrator: the stock service
group: service
language: codified-2
retired: []
unbuilt: []
---

# Stock

## Purpose

What the adapter does with inventory's products.

## Behaviour

### [g1] A product is reserved
- [r1] When the stock service reserves a %s, the stock service shall keep the %s.
"""

STOCK_FEATURE = """# generated from spec/capabilities/stock.md by features generate; do not edit
Feature: Stock
  Narrator: the stock service

  @g1 @r1
  Scenario: A product is reserved
    Given a %s p1
    When the stock service reserves the %s p1
    Then the stock service keeps the %s p1
"""

LEDGER = """---
id: capability/example.org/fixture/domain-model/adapter/stock-inventory/ledger
title: The stock ledger (assumed)
narrator: the ledger service
group: service
language: codified-2
assumed: true
provider: bounded-context/example.org/fixture/ledger
retired: []
unbuilt: []
---

# The stock ledger (assumed)

## Purpose

What the adapter relies on of the stock ledger, in its words, assumed: no published contract.

## Terms

- **the ledger service** (proper noun): the stock ledger. Kind of: service.
- **line** (noun): a count of one stocked thing in the ledger. Plural: lines.
- **decrement** (verb, action): Forms: decrements, decremented. Frame: agent decrements line.

## Behaviour

### [g1] A line decremented is kept
- [r1] When the stock service decrements a line, the ledger service shall keep the line.
"""

LEDGER_FEATURE = """# generated from spec/capabilities/ledger.md by features generate; do not edit
Feature: The stock ledger (assumed)
  Narrator: the ledger service

  @g1%s
  Scenario: A line decremented is kept
    Given a line l1
    When the stock service decrements the line l1
    Then the ledger service keeps the line l1
"""


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("provider", {"kinds": {}, "held": False, "uses": False, "clash": False,
                                                "renamed": False, "assumed": False, "unscenarioed": False})


def given_instance(step):
    if not mine(step) or step.kind not in KINDS:
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_state(step):
    """`the adapter spec a1 holds the contract c1`, `... has the requirement r1`, `the contract c1 holds the term
    t1`, `the requirement r1 uses the term t1`, `the term t1 clashes with the term t2`, `the adapter spec a1 renames
    the term t2` (and `does not rename`), `the assumed description a2 holds the requirement id r1`, `the adapter spec
    a1 holds the assumed description a2` and `no scenario refers to the requirement id r1`."""
    if not mine(step) or step.term not in ("has", "holds", "use", "clash", "rename", "refer"):
        return False
    w, said = world(step), " ".join(step.nps)
    if step.term == "refer":
        w["unscenarioed"] = True
    elif step.term == "rename":
        w["renamed"] = step.template == "GivenDoes"
    elif step.term == "clash":
        w["clash"] = True
    elif step.term == "use":
        w["uses"] = True
    elif step.term == "holds" and "the contract" in said:
        w["held"] = True
    elif "the assumed description" in said:
        w["assumed"] = True


def build(step):
    """The parent context with the adapter spec nested in it, and what the output names each instance by."""
    w, repo = world(step), step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    adapter = repo / "adapters" / NAME
    (adapter / "spec" / "capabilities").mkdir(parents=True)
    (adapter / "features").mkdir()
    providers = "%s@%s" % (PROVIDER, VERSION) if w["held"] else ""
    renames = "product → stocked product" if w["renamed"] else ""
    (adapter / "spec" / "index.md").write_text(INDEX % (PARENT, NAME, providers, renames, OWN if w["clash"] else ""))
    if w["held"]:
        kept = adapter / "provider" / "example.org" / "fixture" / "inventory" / VERSION
        kept.mkdir(parents=True)
        (kept / "contract.toml").write_text(CONTRACT)
    if w["uses"] or w["renamed"]:
        word = "stocked product" if w["renamed"] else "product"
        (adapter / "spec" / "capabilities" / "stock.md").write_text(STOCK % (word, word))
        (adapter / "features" / "stock.feature").write_text(STOCK_FEATURE % (word, word, word))
    if w["assumed"]:
        (adapter / "spec" / "capabilities" / "ledger.md").write_text(LEDGER)
        (adapter / "features" / "ledger.feature").write_text(LEDGER_FEATURE % ("" if w["unscenarioed"] else " @r1"))
    says = {"term": "product", "requirement id": "ledger#r1"}
    for name, kind in w["kinds"].items():
        if kind in says:
            step.context.setdefault("says", {})[name] = says[kind]


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["adapter"] = {}     # checking_handlers_adapter's Thens of the exit read the result
    step.context["result"] = step.run("spec", "--root", "adapters/" + NAME, "check")


def then_names(step):
    """`the specification service names the term t2`: a line of `spec check`'s output names it."""
    if not mine(step) or "provider" not in step.context or step.term != "name":
        return False
    done, said = step.context["result"], step.context["says"][step.names[0]]
    assert any(said in line for line in done.stdout.splitlines()), done.stdout + done.stderr


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_state)
W.local("GivenDoesNot")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then_names)
