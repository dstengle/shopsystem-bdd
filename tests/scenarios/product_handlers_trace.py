"""Handlers of features/product.feature's trace (product r26-r30, b644), beside product_handlers.py, whose world and
Givens of instances they share; each a `work_queue_world.local` that takes only a step of a scenario of its groups
(`mine`), tried before product_handlers'. The Givens are kept as facts (`said`); at the When of `spec trace` the world
they pick is written: the domain-model fixture (tests/scripts/fixtures/domain-model/), its notebook's lines, and

- a group that serves the job, notebook's g1 (r1, which requests nothing the job's trace needs: r26);
- a group whose requirement uses an operation and a different requirement that governs it: notebook's g2 serving the
  job (r2, whose response asks the notes service to archive the note) and `shelf`, another capability whose r1 is on
  a request to archive a note (r27);
- a port line that governs it and an adapter spec that realises the port line's id: checking_handlers_port's driven
  port `stock` beside the fixture, notebook's g10 serving the job (r10, which requests `stock.reserve`), and the
  adapter spec `adapters/stock-ledger/` realising `stock-port#r1` (r28);
- of those, the ledger's contract held in the adapter spec at `bounded-context/example.org/fixture/ledger@1.0.0`,
  its `[operations."ledger.post"]` listing `ledger#r1`, and `uses:` naming ledger.post for stock.reserve (r35);
- a group that serves a need of the job: the product file holding the job and its need `n1`, notebook's g1 serving
  the need and shelf's g1 serving the job (so that the job is served, but not by the line returned: r29);
- no group serving the job: nothing serves it (r30).

The When runs `spec trace` on the job; the Thens read the requirement's id or the adapter spec's id in its output,
and of a refusal its exit and the job it names."""
import hashlib
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def _module(name):
    return sys.modules["shop_handlers_%s" % hashlib.sha256(str(HERE / name).encode()).hexdigest()[:12]]


P = _module("product_handlers.py")
W = sys.modules["shop_work_queue_world"]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g26", "g27", "g28", "g29", "g30", "g35"}
PARENT = "bounded-context/example.org/fixture/domain-model"
ADAPTER = "%s/adapter/stock-ledger" % PARENT
TERMS = ("serve", "has", "use", "govern", "realise", "need", "hold")

SHELF = """---
id: capability/example.org/fixture/domain-model/shelf
title: Shelf
narrator: a person keeping notes
group: service
area: notes
specifies: service notes
language: codified-2
retired: []
unbuilt: []
---

# Shelf

## Purpose
The notes put away.

## Behaviour

### [g1] A note put away is retired
%s- [r1] %s
"""
ARCHIVES = "When the person archives a note, the notes service shall set the status of the note to `retired`."
LISTS = "When the person lists the notes, the notes service shall complete the request."

INDEX = """---
id: %s
title: stock over a ledger
kind: adapter
realises: [stock-port#r1]
providers: []
language: codified-2
imports: [request]
---

# stock over a ledger

## Purpose

The adapter that realises the notes service's needs of the stock.
"""


LEDGER = "bounded-context/example.org/fixture/ledger"
LEDGER_REQ = "ledger#r1"
LEDGER_CONTRACT = """context = "%s"
version = "1.0.0"
status = "published"

[operations."ledger.post"]
requirements = [
  "%s: When a client posts an entry, the ledger service shall complete the request.",
]
""" % (LEDGER, LEDGER_REQ)


def ledger(adapter):
    """The ledger's contract held in the adapter spec at its pin, and `uses:` naming its ledger.post for stock.reserve."""
    index = adapter / "spec" / "index.md"
    index.write_text(index.read_text().replace("providers: []\n", "providers: [%s@1.0.0]\nuses:\n"
                                               "  - stock.reserve → ledger.post\n" % LEDGER))
    kept = adapter / "provider" / "example.org" / "fixture" / "ledger" / "1.0.0"
    kept.mkdir(parents=True)
    (kept / "contract.toml").write_text(LEDGER_CONTRACT)


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return P.mine(step) and found is not None and bool(GROUPS & set(found.tags))


def said(step):
    return P.world(step).setdefault("trace", [])


def given_does(step):
    """`the requirement group r1 serves the job j1`, `... has the requirement r2`, `the requirement r2 uses the
    operation o1`, `the requirement r3 governs ...`, `the adapter spec a1 realises ...`, `the job j1 needs the need n1`:
    each kept with what it names; `no requirement group serves the job j1`: nothing serves it."""
    if not mine(step) or step.term not in TERMS + ("serves", "uses", "governs", "realises", "needs", "holds"):
        return False
    if (step.subject or "").startswith("no "):      # `no requirement group serves the job j1`: nothing serves it
        P.world(step)["unserved"] = True
        return None
    said(step).append((step.term if step.term == "has" else step.term.rstrip("s"), tuple(step.names)))


def serve(path, group, job):
    head = next(line for line in path.read_text().splitlines() if line.startswith("### [%s] " % group))
    path.write_text(path.read_text().replace(head + "\n", "%s\nserves: %s\n" % (head, job), 1))


def build(step, job):
    """The world the facts pick, written into the repository; {instance: what the output names it by}."""
    facts, repo = said(step), step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    spec = repo / "spec"
    notebook, index = spec / "capabilities" / "notebook.md", spec / "index.md"
    names = P.world(step)["kinds"]
    kinds = {names.get(n) for _, ns in facts for n in ns}
    by_kind = {k: n for n, k in names.items()}
    by_term = {term: ns for term, ns in facts}
    shelf = None
    if "adapter spec" in kinds:
        port = _module("checking_handlers_port.py")
        (spec / "model" / "stock.md").write_text(port.MODEL % "port")
        (spec / "vocabulary" / "stock.md").write_text(port.VOCABULARY)
        (spec / "capabilities" / "stock-port.md").write_text(port.PORT % "Relied on by: notebook#r10.\n")
        notes = spec / "model" / "notes.md"
        notes.write_text(notes.read_text().replace("imports: []\n", "imports: [stock]\n"))
        notebook.write_text(notebook.read_text() + port.CORE)
        index.write_text(index.read_text().replace("| notes | core | notebook |\n",
                                                   "| notes | core | notebook |\n| stock | port | stock-port |\n"))
        (repo / "adapters" / "stock-ledger" / "spec").mkdir(parents=True)
        (repo / "adapters" / "stock-ledger" / "spec" / "index.md").write_text(INDEX % ADAPTER)
        serve(notebook, "g10", job)
        says = {by_kind["requirement"]: "notebook#r10", by_kind["adapter spec"]: ADAPTER}
        if "contract" in kinds:     # r35: the ledger's contract held, its ledger.post used for stock.reserve
            ledger(repo / "adapters" / "stock-ledger")
            says = {next(ns[-1] for t, ns in facts if t == "hold" and names.get(ns[0]) == "contract"): LEDGER_REQ}
    elif "operation" in kinds:
        shelf = SHELF % ("", ARCHIVES)
        serve(notebook, "g2", job)
        says = {by_term["has"][-1]: "notebook#r2", by_term["govern"][0]: "shelf#r1"}
    elif "need" in kinds:
        need = by_kind["need"]
        shelf = SHELF % ("serves: %s\n" % job, LISTS)
        serve(notebook, "g1", need)
        product = {"actors": [], "jobs": {n: {"actors": [], "statement": P.FORMED % n, "needs": [need] if n == job
                                               else []} for n in (job, need)}}
        (repo / P.REL).parent.mkdir(parents=True, exist_ok=True)
        (repo / P.REL).write_text(P.scripts("product_store").render(product))
        says = {by_kind["requirement"]: "notebook#r1"}
    elif P.world(step).get("unserved"):
        says = {}
    else:
        serve(notebook, "g1", job)
        says = {by_kind["requirement"]: "notebook#r1"}
    if shelf:
        (spec / "capabilities" / "shelf.md").write_text(shelf)
        index.write_text(index.read_text().replace("| notes | core | notebook |", "| notes | core | notebook, shelf |"))
    done = step.run("features", "generate")
    assert done.returncode == 0, done.stdout + done.stderr
    return says


def runs(step):
    if not mine(step) or step.term != "`spec trace`":
        return False
    job = next(n for n in step.names if P.world(step)["kinds"].get(n) == "job")
    step.context["says"] = build(step, job)
    step.context["head"] = W.init(step.repo)
    step.context["result"] = step.run("spec", "trace", job)


def then_returns(step):
    """`the product service returns the requirement r2` (or the adapter spec a1): a line of the trace names it."""
    if not mine(step) or "says" not in step.context:
        return False
    done = step.context["result"]
    want = step.context["says"][step.names[-1]]
    assert done.returncode == 0, done.stdout + done.stderr
    named = [w[2] if w[:2] == ["adapter", "spec"] else w[0] for w in map(str.split, done.stdout.splitlines()[1:]) if w]
    assert want in named, done.stdout


def then_does(step):
    """`the product service refuses this request` (an error exit, no usage error, nothing kept) and `... names the job j1`."""
    if not mine(step) or "says" not in step.context or step.term not in ("refuse", "name"):
        return False
    done = step.context["result"]
    told = done.stdout + done.stderr
    assert done.returncode == 1 and "Traceback" not in told and "usage:" not in told, told
    if step.term == "name":
        assert step.names[-1] in done.stderr, told
    assert P.git(step.repo, "rev-parse", "HEAD").strip() == step.context["head"]


W.local("GivenDoes")(given_does)
W.local("WhenRuns")(runs)
W.local("ThenPrints")(then_returns)
W.local("ThenDoes")(then_does)
