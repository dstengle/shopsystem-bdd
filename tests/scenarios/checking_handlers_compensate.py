"""Handlers of checking's registration refused after another was completed (g142: r142, b743), each a
`work_queue_world.local` that takes only a step of a scenario of g142 (`mine`), over checking_handlers_obtain's world
(the domain-model fixture, the stand-in gh, the bounded context `UPSTREAM` obtained from, its adapter spec `ADAPTER`)
with a second adapter spec of the same provider, `adapters/stock-archive/` (`OTHER`, the adapter spec a2: the
different one), whose folder sorts before the first's, so `spec obtain` registers its contract first. The registry is
checking_handlers_registry's stand-in, answering as the shop-folder adapter does but refusing the register for the
adapter spec a1 (`$STAND_IN_REGISTRY_REFUSE_FOR`). The Thens read back the deregister the stand-in recorded of the
contract for a2's folder, a2 holding no contract of the provider and the command refused, and a2's `providers:`."""
import json
import sys
from pathlib import Path

from vocab import handler

W = sys.modules["shop_work_queue_world"]
GROUPS = {"g142"}
OTHER = "adapters/stock-archive"


def _module(name):
    return next(m for m in list(sys.modules.values()) if (getattr(m, "__file__", None) or "").endswith("/" + name))


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("compensate", {"kinds": {}})


def given_instance(step):
    if not mine(step) or step.kind not in ("provider", "adapter spec", "contract"):
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_state(step):
    """`the adapter spec a1 has the provider p1` (each adapter spec of the world names the upstream as its provider)
    and `the specification service registers the contract c1 for the adapter spec a1` (the request replied to)."""
    if not mine(step) or step.term not in ("has", "register"):
        return False
    assert world(step)["kinds"].get(step.names[-1]) in ("provider", "adapter spec"), step.names


def build(step):
    """checking_handlers_obtain's world with the second adapter spec beside the first, committed."""
    obtain = _module("checking_handlers_obtain.py")
    obtain.build(step)
    index = (step.repo / obtain.ADAPTER / "spec" / "index.md").read_text().replace("stock-inventory", "stock-archive")
    (step.repo / OTHER / "spec").mkdir(parents=True)
    (step.repo / OTHER / "spec" / "index.md").write_text(index)
    W.git(step.repo, "add", "--", OTHER)
    W.git(step.repo, "commit", "-q", "-m", "a second adapter spec of the provider")


def refuses(step):
    """`the contract registry service refuses the request to register the contract c1 for the adapter spec a1`:
    `spec obtain` run with the stand-in refusing the register for a1's folder alone."""
    if not mine(step) or step.term != "refuse":
        return False
    obtain, registry = _module("checking_handlers_obtain.py"), _module("checking_handlers_registry.py")
    w = world(step)
    w["calls"] = str(obtain.outside(step) / "registry-calls.jsonl")
    build(step)
    env = registry.stand_in(step, w["calls"], STAND_IN_REGISTRY_REFUSE_FOR=obtain.ADAPTER)
    step.context["result"] = step.run("spec", "obtain", obtain.UPSTREAM, env=env)


def calls(step):
    path = Path(world(step)["calls"])
    return [json.loads(line) for line in path.read_text().splitlines()] if path.is_file() else []


def then_deregisters(step):
    """`the specification service deregisters the contract c1 for the adapter spec a2`: the command refused, the
    stand-in's register for a2 completed before the one refused, then a deregister for a2's folder, and a2 holding no
    contract of the provider."""
    if not mine(step) or "compensate" not in step.context or step.term != "deregister":
        return False
    import contract_registry_folder
    obtain, done = _module("checking_handlers_obtain.py"), step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr
    made = [(c["operation"], c.get("adapter spec")) for c in calls(step) if c["operation"] != "retrieve"]
    assert made == [("register", OTHER), ("register", obtain.ADAPTER), ("deregister", OTHER)], calls(step)
    assert contract_registry_folder.held(step.repo / OTHER, obtain.UPSTREAM) == [], list(step.repo.rglob("provider"))


def then_has(step):
    """`the adapter spec a2 has the provider p1`: a2's `providers:` name the bounded context obtained from."""
    if not mine(step) or "compensate" not in step.context or step.term != "has":
        return False
    obtain = _module("checking_handlers_obtain.py")
    index = (step.repo / OTHER / "spec" / "index.md").read_text()
    assert "providers: [%s]" % obtain.UPSTREAM in index, index


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_state)
W.local("WhenHappens")(refuses)
W.local("ThenDoes")(lambda step: then_deregisters(step) if then_deregisters(step) is not False else then_has(step))


def untaken(step):
    """The registry's key of a deregister's Then, which `features vocab --check` reads: what is left when the local
    above takes no step."""
    raise AssertionError("no handler of this scenario's feature took the step: %s" % step.text)


handler("ThenDoes", "deregister")(untaken)
