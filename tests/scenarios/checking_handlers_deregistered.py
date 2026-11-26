"""Handlers of checking's completed deregistration (g143: r143, b754), each a `work_queue_world.local` that takes only
a step of a scenario of g143 (`mine`), over checking_handlers_compensate's world (two adapter specs of one provider,
the register for the first refused after the one for the second, `adapters/stock-archive/`, was written, so `spec
obtain` deregisters the contract for the second: the adapter spec a1 of g143). The registry is
checking_handlers_registry's stand-in, refusing the register for the first adapter spec and completing the deregister as
the shop-folder adapter does, recording its completion with the commit the repository is then at. The Then: after that
completion, the command refused and the specification service changed nothing (the same commit, no file changed)."""
import json
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
GROUPS = {"g143"}


def _module(name):
    return next(m for m in list(sys.modules.values()) if (getattr(m, "__file__", None) or "").endswith("/" + name))


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("deregistered", {"kinds": {}})


def given_instance(step):
    if not mine(step) or step.kind not in ("adapter spec", "contract"):
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_request(step):
    """`the specification service deregisters the contract c1 for the adapter spec a1`: the request replied to."""
    if not mine(step) or step.term != "deregister":
        return False
    assert [world(step)["kinds"].get(n) for n in step.names] == ["contract", "adapter spec"], step.names


def completes(step):
    """`the contract registry service completes the request to deregister the contract c1 for the adapter spec a1`:
    `spec obtain` run with the stand-in refusing the register for the first adapter spec, so deregistering the
    contract it wrote for the second, and recording that deregister's completion."""
    if not mine(step) or step.term != "complete":
        return False
    obtain, registry = _module("checking_handlers_obtain.py"), _module("checking_handlers_registry.py")
    w = world(step)
    w["calls"] = str(obtain.outside(step) / "registry-calls.jsonl")
    _module("checking_handlers_compensate.py").build(step)
    env = registry.stand_in(step, w["calls"], STAND_IN_REGISTRY_REFUSE_FOR=obtain.ADAPTER,
                            STAND_IN_REGISTRY_REPLY="complete", STAND_IN_REGISTRY_ON="deregister")
    step.context["result"] = step.run("spec", "obtain", obtain.UPSTREAM, env=env)


def then_unchanged(step):
    """`the specification service changes nothing`: the deregister for a1's folder completed, then nothing: the
    command refused, the repository at the commit it was at when the deregister completed and no file changed."""
    if not mine(step) or "deregistered" not in step.context:
        return False
    other = _module("checking_handlers_compensate.py").OTHER
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr
    path = Path(world(step)["calls"])
    made = [json.loads(line) for line in path.read_text().splitlines() if '"retrieve"' not in line]
    assert [(c["operation"], c.get("adapter spec")) for c in made][-2:] == [("deregister", other), ("completed", None)]
    assert W.head(step.repo) == made[-1]["head"], W.committed(step.repo)
    assert W.git(step.repo, "status", "--porcelain") == "", W.git(step.repo, "status", "--porcelain")


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_request)
W.local("WhenHappens")(completes)
W.local("ThenChangesNothing")(then_unchanged)
