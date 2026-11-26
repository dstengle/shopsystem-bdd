"""A ready item whose port outcome no line handles reopened at the batch's opening (batches r160, b721): beside
readiness_world's codified spec, the domain-model fixture's model, vocabulary, CLI contract and notebook (the index
importing the request pack), as batches_handlers_port's world; the item holds readiness_handlers_outcome's BLOCK, the
driven port `stock-port` whose port line governs `stock.reserve` and excludes its refusal, its model line, and
notebook's core line requesting it, no core line on its completion, so the outcome `stock.reserve done` no line
handles. The Then of the outcome named reads `work batch start`'s output for its name in the bound check."""
import shutil
import sys
from pathlib import Path

B, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
OUTCOME = "stock.reserve done"
TERMS = ("holds", "hold", "governs", "govern", "has", "have", "handles", "handle", "excludes", "exclude")


def mine(step):
    """True when the step is of batches' scenario of r160."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and "r160" in found.tags


def _block():
    """readiness_handlers_outcome's BLOCK, by the module vocab's glob loaded it as."""
    return next(m for m in list(sys.modules.values()) if getattr(m, "__file__", None)
                and m.__file__.endswith("/readiness_handlers_outcome.py")).BLOCK


def _spec(step):
    """The fixture's model, vocabulary, CLI contract and notebook beside the world's codified spec, once."""
    if step.context.get("outcome_spec"):
        return
    sys.modules["shop_readiness_world"].codify(step)
    spec = step.repo / "spec"
    for folder in ("model", "vocabulary", "adapters"):
        shutil.copytree(FIXTURE / folder, spec / folder, dirs_exist_ok=True)
    shutil.copy(FIXTURE / "capabilities" / "notebook.md", spec / "capabilities" / "notebook.md")
    index = spec / "index.md"
    index.write_text(index.read_text().replace("imports: [cli]", "imports: [request]"))
    step.context["outcome_spec"] = True


def _given(kind):
    def given(step):
        """`a port line p1`, `an operation o1`, `an operation outcome o2`: the spec they are read in."""
        if not mine(step):
            return False
        _spec(step)
        if kind == "operation outcome":
            step.context.setdefault("outcomes", {})[step.names[0]] = OUTCOME
    return given


for _kind in ("port line", "operation", "operation outcome"):
    four("GivenK", _kind, *BOTH)(_given(_kind))


def held(step):
    """`the item i1 holds the port line p1`: the item's BLOCK; the port line governing the operation, the operation's
    outcome, and no core line handling it and no port line excluding it: so BLOCK says."""
    if not mine(step):
        return False
    (k1, n1), (k2, _) = parts(step)[:2]
    if (k1, k2) == ("item", "port line"):
        B.write_item(step, n1, sections={"Requirements": _block()})


for _term in TERMS:
    four("GivenDoes", _term, *BOTH)(held)


@four("ThenDoes", "name", *BOTH)
def names_outcome(step):
    """The batches service names the operation outcome: `work batch start` printed its name beside the item it gave
    back."""
    k, name = parts(step)[1]
    if k != "operation outcome" or name not in step.context.get("outcomes", {}):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    assert step.context["outcomes"][name] in done.stdout, (step.text, done.stdout)
