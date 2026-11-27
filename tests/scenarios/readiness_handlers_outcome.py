"""items#r72's Givens (b721), `local` handlers loaded after readiness_handlers_givens.py and so tried before it, in a
context with a domain model: tests/scripts/fixtures/domain-model/'s spec, the item making the driven port: the new
capability `stock-port` of the new area `stock` of kind `port`, whose port line governs the stock service's `reserve`
and excludes its refusal ("shall not refuse the request"), its `### stock model` block declaring the operation with
the outcomes `done` and `refused: no stock`, and notebook's core line whose response requests it (applying_handlers_pieces'
lines, less the core line on its completion). So no core line handles the outcome `stock.reserve done` and no port
line excludes it: the lay brings v_pb2 of it. What `work ready` names the outcome by is its name in the bound check."""
import importlib.util
import shutil
import sys
from pathlib import Path


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
OUTCOME = "stock.reserve done"
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
    """True when the step is of items' scenario of r72."""
    requested = sys.modules["vocab"].vocab4.requested
    found = requested.scenario(step.request.node)
    return requested.capability(step.request.node) == "items" and found is not None and "r72" in found.tags


def spec(step):
    """The fixture's spec over the repository's `spec/`, once."""
    if not step.context.get("model_spec"):
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        step.context["model_spec"] = True


@W.local("GivenK")
def given_named(step):
    """`a port line p1`, `an operation o1`, `an operation outcome o2`: the spec they are read in; the outcome named
    by its name in the bound check."""
    if not mine(step) or step.kind not in ("port line", "operation", "operation outcome"):
        return False
    spec(step)
    if step.kind == "operation outcome":
        step.context.setdefault("says", {})[step.names[0]] = OUTCOME
    return None


@W.local("GivenDoes")
def given_held(step):
    """`the item i1 holds the port line p1`: the item's BLOCK; the port line governing the operation, the operation's
    outcome, and no core line handling it and no port line excluding it: so BLOCK says."""
    if not mine(step) or step.term not in ("holds", "hold", "governs", "govern", "has", "have", "handles", "handle",
                                           "excludes", "exclude"):
        return False
    if step.term in ("holds", "hold") and step.subject.startswith("the item "):
        B.write_item(step, step.names[0], sections={"Requirements": BLOCK})
    return None
