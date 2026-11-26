"""Handlers of features/product.feature's coordination of a job (product r31-r33, b680; decision 0134), beside
product_handlers.py, whose world and Givens of instances they share; each a `work_queue_world.local` that takes only a
step of a scenario of its groups (`mine`), tried before product_handlers'. The Givens are kept as facts (`said`); at the
When of `spec trace` the world they pick is written: the domain-model fixture (tests/scripts/fixtures/domain-model/)
with checking_handlers_port's driven port `stock` beside it and notebook's g10 serving the job, its r10 requesting
`stock.reserve`, and

- an operation with no property and an operation outcome no requirement handles: `stock.reserve` as the fixture
  declares it, no line on the reservation's outcomes (r31);
- a requirement that handles it and uses an operation that performs a transition: notebook's g11, on the stock
  service's completion of a reservation, archiving a note, which r9 retires (the note's lifecycle: r32);
- two operations of the driven port with a property that refers to an operation: `stock.allocate` beside
  `stock.reserve`, both requested by r10, each `compensated by release` (r33).

The When runs `spec trace` on the job, as text and with `--json`; the Thens read the coordination of the job (the
text's `coordination: <kind>` line and the content's `coordination`) and that the trace returned is the job's."""
import hashlib
import json
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
GROUPS = {"g31", "g32", "g33"}

SERVED = """
### [g10] A person who starts has a note reserved
- [r10] When the person starts, the notes service shall reserve a note with the quantity `2`.
"""
SAGA = """
### [g10] A person who starts has a note reserved and allocated
- [r10] When the person starts, the notes service shall reserve a note with the quantity `2` and allocate a note.
"""
HANDLED = """
### [g11] A reservation completed archives a note
- [r11] When the stock service completes a reservation, the notes service shall archive a note.
"""
COMPENSATED = """  operation reserve(note, quantity)  compensated by release; outcomes: done → the reservation
  operation allocate(note)  compensated by release; outcomes: done
  operation release(note)  outcomes: done
"""
WORDS = """- **allocate** (verb, action) → operation stock.allocate. Forms: allocates, allocated. Frame: <actor> allocates <note>.
- **release** (verb, action) → operation stock.release. Forms: releases, released. Frame: <actor> releases <note>.
"""


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return P.mine(step) and found is not None and bool(GROUPS & set(found.tags))


def said(step):
    return P.world(step).setdefault("coordination", [])


def given_does(step):
    """`the requirement group r1 serves the job j1`, `... has the requirement r2`, `the requirement r2 uses the
    operation o1`, `the port line p1 governs ...`, `the driven port d1 holds ...`, `the property p1 refers to ...`,
    `the operation o3 performs the transition t1`, `the requirement r3 handles ...`, `the operation o1 has no
    operation outcome`: each kept with what it names."""
    if not mine(step):
        return False
    said(step).append((step.term, tuple(step.names)))


def build(step, job):
    """The world the facts pick, written into the repository."""
    repo, T, PORT = step.repo, _module("product_handlers_trace.py"), _module("checking_handlers_port.py")
    kinds = set(P.world(step)["kinds"].values())
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    spec = repo / "spec"
    model = PORT.MODEL % "port"
    words = PORT.VOCABULARY
    core = SERVED
    if "property" in kinds:
        model = model.replace("  operation reserve(note, quantity)  outcomes: done → the reservation\n", COMPENSATED)
        words += WORDS
        core = SAGA
    elif "transition" in kinds:
        core += HANDLED
    (spec / "model" / "stock.md").write_text(model)
    (spec / "vocabulary" / "stock.md").write_text(words)
    (spec / "capabilities" / "stock-port.md").write_text(PORT.PORT % "Relied on by: notebook#r10.\n")
    notes = spec / "model" / "notes.md"
    notes.write_text(notes.read_text().replace("imports: []\n", "imports: [stock]\n"))
    notebook = spec / "capabilities" / "notebook.md"
    notebook.write_text(notebook.read_text() + core)
    index = spec / "index.md"
    index.write_text(index.read_text().replace("| notes | core | notebook |\n",
                                               "| notes | core | notebook |\n| stock | port | stock-port |\n"))
    T.serve(notebook, "g10", job)
    done = step.run("features", "generate")
    assert done.returncode == 0, done.stdout + done.stderr


def runs(step):
    if not mine(step) or step.term != "`spec trace`":
        return False
    job = next(n for n in step.names if P.world(step)["kinds"].get(n) == "job")
    build(step, job)
    step.context["coordinated"] = job
    step.context["result"] = step.run("spec", "trace", job)
    step.context["json"] = step.run("spec", "trace", job, "--json")


def then_value(step):
    """`the coordination of the job j1 is `port request``: the text's `coordination:` line and the content's."""
    if not mine(step) or "coordinated" not in step.context or step.attribute != "coordination":
        return False
    want = step.values[0].strip("`")
    done, raw = step.context["result"], step.context["json"]
    assert done.returncode == 0, done.stdout + done.stderr
    assert "  coordination: %s" % want in done.stdout.splitlines(), done.stdout
    assert raw.returncode == 0, raw.stdout + raw.stderr
    assert json.loads(raw.stdout)["content"]["coordination"] == want, raw.stdout


def then_returns(step):
    """`the product service returns the job j1`: the trace printed is the job's, and the content's job is it."""
    if not mine(step) or "coordinated" not in step.context:
        return False
    done, raw, job = step.context["result"], step.context["json"], step.context["coordinated"]
    assert done.returncode == 0 and done.stdout.splitlines()[0] == "the trace of the job %s:" % job, done.stdout
    assert json.loads(raw.stdout)["content"]["job"] == job, raw.stdout


W.local("GivenDoes")(given_does)
W.local("GivenDoesNot")(given_does)
W.local("WhenRuns")(runs)
sys.modules["vocab"].handler("ThenK_A", "job")(then_value)     # a claim `features vocab --check` sees
W.local("ThenPrints")(then_returns)
