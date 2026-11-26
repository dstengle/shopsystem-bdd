"""Handlers of features/contract-registry.feature (r1-r3, b636), each a `work_queue_world.local` that takes only a step
of its scenarios (`mine`): the requests of the contract registry, a driven port, made in process of contract_registry
with the adapter wired in, the shop-folder adapter, in the scenario's repository (a git repository holding the
context's spec/index.md). A contract a Given brings in is deposited at `1.2.0` before the When (`DEPOSITED`), unless
it is the one the When deposits; the version v1 is `9.9.9` (`VERSION`), which no contract has. The When deposits the
contract c1 at `1.2.0`, or retrieves this bounded context's contract, published or at the version it names, and keeps
the registry's reply, a domain_envelope Response; or registers the contract c1 at `1.2.0` for the adapter spec a1,
`adapters/stock-inventory/` (`ADAPTER`, providing `PROVIDER`), r4 (b735). The Thens read it back: completed (the
contract kept at its version and committed, or held by the adapter spec at its version and committed), returned (the bytes of the contract deposited), refused (`version not deposited`) and named
(the version among the refusal's names). A port's request has no CLI command, so requested.py leaves it as it is and
re-keys its Thens to ThenExitsOk, ThenPrints and ThenDoes (refuse, name), which these handlers take."""
import sys
from pathlib import Path

from vocab import handler

W = sys.modules["shop_work_queue_world"]
DEPOSITED = "1.2.0"
VERSION = "9.9.9"
INDEX = "---\nid: bounded-context/example.org/fixture/registry\nlanguage: codified-2\n---\n\n# registry\n"
ADAPTER = "adapters/stock-inventory"
PROVIDER = "bounded-context/example.org/fixture/inventory"
SPEC = "---\nid: bounded-context/example.org/fixture/registry/adapter/stock-inventory\nkind: adapter\nproviders: [%s]\n---\n"
CONTRACT = 'context = "bounded-context/example.org/fixture/registry"\nversion = "%s"\nstatus = "published"\n'


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "contract-registry"


def world(step):
    return step.context.setdefault("registry", {"kinds": {}, "absent": False})


def given_instance(step):
    if not mine(step) or step.kind not in ("contract", "version", "adapter spec"):
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_absent(step):
    """`no contract has the version v1`: the version no contract is deposited at."""
    if not mine(step) or step.term != "has" or not step.text.startswith("no contract"):
        return False
    world(step)["absent"] = True


def requests(step):
    """`the specification service deposits the contract c1`, `... retrieves the contract c1 [with the version v1]`."""
    import contract_registry
    if not mine(step) or step.template != "WhenRequests":
        return False
    w, repo = world(step), step.repo
    (repo / "spec").mkdir(parents=True, exist_ok=True)
    (repo / "spec" / "index.md").write_text(INDEX)
    if step.term.endswith(".register"):
        (repo / ADAPTER / "spec").mkdir(parents=True)
        (repo / ADAPTER / "spec" / "index.md").write_text(SPEC % PROVIDER)
    W.init(repo)
    w["head"] = W.head(repo)
    if step.term.endswith(".register"):
        w["registered"] = True
        w["response"] = contract_registry.register(repo, (CONTRACT % DEPOSITED).encode(), ADAPTER, PROVIDER, DEPOSITED)
        return None
    depositing = step.term.endswith(".deposit")
    if not depositing:
        contract_registry.deposit(repo, CONTRACT % DEPOSITED, DEPOSITED)
    w["head"] = W.head(repo)
    version = VERSION if "version" in [w["kinds"].get(n) for n in step.names] else None
    w["response"] = (contract_registry.deposit(repo, CONTRACT % DEPOSITED, DEPOSITED) if depositing
                     else contract_registry.retrieve(repo, None, version))


def _response(step, outcome):
    found = world(step).get("response")
    assert found is not None and found.outcome == outcome, found
    return found


def then_completes(step):
    """`the contract registry service completes this request`: the contract kept at its version, committed."""
    if not mine(step) or "registry" not in step.context:
        return False
    done = _response(step, "done")
    if world(step).get("registered"):
        import contract_registry
        held = contract_registry.held(step.repo / ADAPTER, PROVIDER, DEPOSITED)
        assert [p.read_bytes() for p in held] == [(CONTRACT % DEPOSITED).encode()], held
        assert done.content["kept"] in W.committed(step.repo) and W.head(step.repo) != world(step)["head"], done
        return None
    import contract_registry_folder
    kept = contract_registry_folder.kept(step.repo)
    assert kept.get(DEPOSITED, (None, None))[1] == "published", kept
    assert W.head(step.repo) != world(step)["head"]
    assert kept[DEPOSITED][0] in W.committed(step.repo), W.committed(step.repo)


def then_returns(step):
    """`the contract registry service returns the contract c1`: the bytes of the contract deposited."""
    if not mine(step) or "registry" not in step.context:
        return False
    assert _response(step, "returned").content == (DEPOSITED, (CONTRACT % DEPOSITED).encode()), world(step)


def then_does(step):
    """`... refuses this request` (`version not deposited`), `... names the version v1` (among its names)."""
    import contract_registry
    if not mine(step) or "registry" not in step.context or step.term not in ("refuse", "name"):
        return False
    error = _response(step, "refused").errors[0]
    if step.term == "refuse":
        assert error["reason"] == contract_registry.REASON, error
    else:
        assert "version:%s" % VERSION in error["names"], error


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_absent)
W.local("WhenRequests")(requests)
W.local("ThenExitsOk")(then_completes)
W.local("ThenPrints")(then_returns)
W.local("ThenDoes")(then_does)


def untaken(step):
    """The registry's key of the registry's requests, which `features vocab --check` reads: what is left when the local above takes no
    step."""
    raise AssertionError("no handler of this scenario's feature took the step: %s" % step.text)


for key in (("WhenRequests", "contract registry.deposit"), ("WhenRequests", "contract registry.retrieve"),
            ("WhenRequests", "contract registry.register")):
    handler(*key)(untaken)
