"""Handlers of checking's contract registry scenarios (r125-r127, b636), each a `work_queue_world.local` that takes
only a step of a scenario of one of its groups (`mine`). The registry is swapped for the stand-in adapter
tests/scenarios/stand_in_registry.py (`$SHOPSYSTEM_CONTRACT_REGISTRY`), which records each request and makes it of
the shop-folder adapter. The version v1 is `1.2.0` (`VERSION`). A publish and a fetch run in checking_handlers_publish's
world (the domain-model fixture; of a fetch, the contract c1 kept at the version beside a later one published), an
obtain in checking_handlers_obtain's (its upstream `UPSTREAM` hosted with the stand-in gh, its adapter spec naming it
as its provider). The Thens read back the requests the stand-in recorded: a deposit of the contract at the version, a
retrieve at the version, of the bounded context obtained from when the step names one."""
import json
import os
import sys
import tomllib
from pathlib import Path

from vocab import handler

W = sys.modules["shop_work_queue_world"]
STAND_IN = Path(__file__).resolve().parent / "stand_in_registry.py"
GROUPS = {"g125", "g126", "g127"}
VERSION = "1.2.0"
KINDS = ("contract", "version", "downstream context", "bounded context")


def _module(name):
    return next(m for m in list(sys.modules.values()) if (getattr(m, "__file__", None) or "").endswith("/" + name))


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("registry", {"kinds": {}})


def given_instance(step):
    if not mine(step) or step.kind not in KINDS:
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def calls(step):
    path = Path(world(step)["calls"])
    return [json.loads(line) for line in path.read_text().splitlines()] if path.is_file() else []


def runs(step):
    if not mine(step) or step.term not in ("`spec publish`", "`spec fetch`", "`spec obtain`"):
        return False
    obtain = _module("checking_handlers_obtain.py")
    world(step)["calls"] = str(obtain.outside(step) / "registry-calls.jsonl")
    env = dict(obtain.env(step), SHOPSYSTEM_CONTRACT_REGISTRY=str(STAND_IN), STAND_IN_REGISTRY_CALLS=world(step)["calls"],
               PYTHONPATH=os.pathsep.join([str(STAND_IN.parent), os.environ.get("PYTHONPATH", "")]))
    if step.term == "`spec obtain`":
        obtain.build(step)
        words = ["obtain", obtain.UPSTREAM]
    else:
        _module("checking_handlers_publish.py").build(step, step.term == "`spec fetch`", VERSION)
        words = [step.term.strip("`").split()[1]]
    world(step)["upstream"] = obtain.UPSTREAM
    step.context["result"] = step.run("spec", *words, "--version", VERSION, env=env)


def then_requests(step):
    """`the specification service deposits the contract c1 with the version v1`, `... retrieves the contract c1 with
    the version v1` and `... with the bounded context b1 and the version v1`: a request of the stand-in so made."""
    if not mine(step) or "registry" not in step.context or step.term not in ("deposit", "retrieve"):
        return False
    w, done = world(step), step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr
    context = w["upstream"] if "bounded context" in [w["kinds"].get(n) for n in step.names] else None
    made = [c for c in calls(step) if c["operation"] == step.term and c["version"] == VERSION
            and c["context"] == context]
    assert made, (step.term, context, calls(step))
    if step.term == "deposit":
        assert tomllib.loads(made[-1]["contract"])["version"] == VERSION, made[-1]


W.local("GivenK")(given_instance)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then_requests)


def untaken(step):
    """The registry's key of a deposit and a retrieve Then, which `features vocab --check` reads: what is left when the local above takes no
    step."""
    raise AssertionError("no handler of this scenario's feature took the step: %s" % step.text)


for key in (("ThenDoes", "deposit"), ("ThenDoes", "retrieve")):
    handler(*key)(untaken)
