"""A capability new on an item laid in the driven port the item makes (batches r151, b701): beside readiness_world's
codified spec, the domain-model fixture's model, vocabulary, CLI contract and notebook (the index importing the request pack); the
capability c1 the new `stock-port`, the driven port d1 the new area `stock`, the item's block of the capability saying
`area: stock` and `kind: port` with a port line excluding the refusal of a reservation (so a core line relies on it,
v_pb4), its `### stock model` block declaring the reservation (for a note, an object of the area `notes`) and the
stock service's `reserve`, and notebook's lines of checking_handlers_port, one whose response requests it and one on
its completion. The Thens read off the batch's branch after `work batch start`: the capability file saying
`area: stock`, the Composition row of `stock` of kind `port` naming it, and spec/model/stock.md in the lay's commit,
of kind `port`, importing `notes`; notes' model importing `stock`; no CLI table of `stock.reserve`."""
import re
import shutil
import sys
from pathlib import Path

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
CAPABILITY, PORT = "stock-port", "stock"
BLOCK = """### stock-port

narrator: the notes service
group: service
purpose: What the notes service needs of the stock it reaches.
area: stock
kind: port

#### [g1] A note reserved is reserved
- [r1] When the notes service reserves a note, the stock service shall not refuse the request.

### notebook

#### [g10] A person who starts has a note reserved
- [r10] When the person starts, the notes service shall reserve a note with the quantity `2`.

#### [g11] A reservation completed is kept
- [r11] When the stock service completes a reservation, the notes service shall keep the reservation.

### stock model

```model
object reservation kind of request
  relations: for → note (one)

service stock
  operation reserve(note, quantity)  outcomes: done → the reservation | refused: no stock
```

- **reservation** (noun) → object reservation. Stock set aside for a note.
- **reserve** (verb, action) → operation stock.reserve. Forms: reserves, reserved. Frame: <actor> reserves <note>.
- **the stock service** (proper noun) → service stock."""


def mine(step):
    """True when the step is of batches' scenario of r151."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and "r151" in found.tags


@four("GivenK", "driven port", *BOTH)
def given_port(step):
    """a driven port d1: `stock`, new to the world; the fixture's model, vocabulary, CLI contract and notebook beside
    the world's codified spec."""
    if not mine(step):
        return False
    sys.modules["shop_readiness_world"].codify(step)
    spec = step.repo / "spec"
    for folder in ("model", "vocabulary", "adapters"):
        shutil.copytree(FIXTURE / folder, spec / folder, dirs_exist_ok=True)
    shutil.copy(FIXTURE / "capabilities" / "notebook.md", spec / "capabilities" / "notebook.md")
    index = spec / "index.md"
    index.write_text(index.read_text().replace("imports: [cli]", "imports: [request]"))


@four("GivenDoes", "holds", *BOTH)
def holds(step):
    """the driven port d1 holds the capability c1: what the item's block will say; the item i1 holds the driven port
    d1: its blocks (BLOCK) in place of the new capability batches_handlers4 gave it."""
    (k1, n1), (k2, n2) = parts(step)
    if not mine(step) or (k1, k2) not in (("driven port", "capability"), ("item", "driven port")):
        return False
    if k1 == "driven port":
        step.context["new_capability"][n2] = CAPABILITY
    else:
        B.write_item(step, n1, sections={"Requirements": BLOCK})


def _branch(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    return branches[0]


def _laid(step, rel):
    """The file `rel` on the batch's branch, in the lay's commit there."""
    branch = _branch(step)
    assert rel in T.git(step, "log", "--format=", "--name-only", "-1", branch, "--", rel), rel
    return T.git(step, "show", "%s:%s" % (branch, rel))


def _imports(text):
    found = re.search(r"(?m)^imports: \[(.*)\]$", text)
    return [n.strip() for n in found.group(1).split(",") if n.strip()] if found else []


@four("ThenDoes", "holds", *BOTH)
def holds_then(step):
    """the driven port d1 holds the capability c1: the capability file says `area: stock`, the Composition row of
    `stock` is of kind `port` and names the capability, and spec/model/stock.md is of kind `port`."""
    (k1, _), (k2, n2) = parts(step)
    if not mine(step) or (k1, k2) != ("driven port", "capability"):
        return False
    text = _laid(step, "spec/capabilities/%s.md" % step.context["new_capability"][n2])
    assert re.search(r"(?m)^area: %s$" % PORT, text), text
    index = T.git(step, "show", "%s:spec/index.md" % _branch(step))
    rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in index.splitlines() if r.startswith("|")]
    assert [r for r in rows if r[0] == PORT] == [[PORT, "port", CAPABILITY]], index
    model = _laid(step, "spec/model/%s.md" % PORT)
    assert re.search(r"(?m)^kind: port$", model), model


def keeps(step):
    """the batches service keeps the driven port d1: spec/model/stock.md in the lay's commit, of kind `port` and
    importing `notes`, whose words its lines read; notes' model importing `stock`, whose words notebook's line reads;
    and the contract giving the port's `stock.reserve` no CLI table."""
    if not mine(step) or parts(step)[1][0] != "driven port":
        return False
    model = _laid(step, "spec/model/%s.md" % PORT)
    assert re.search(r"(?m)^kind: port$", model) and _imports(model) == ["notes"], model
    notes = T.git(step, "show", "%s:spec/model/notes.md" % _branch(step))
    assert PORT in _imports(notes), notes
    contract = T.git(step, "show", "%s:spec/adapters/cli.toml" % _branch(step))
    assert '[operations."stock.reserve"]' not in contract, contract


for _verb in ("write", "commit", "post", "keep", "make", "rewrite", "publish"):     # requested.py's, as pack's
    four("ThenDoes", _verb, *BOTH)(keeps)
