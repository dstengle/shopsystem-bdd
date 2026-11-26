"""Handlers of checking's scenarios of the contract registry's replies (g128-g130: r128-r130, b636), each a
`work_queue_world.local` that takes only a step of a scenario of one of its groups (`mine`). The registry is
checking_handlers_registry's stand-in, answering as the When says (`$STAND_IN_REGISTRY_REPLY`): it completes the
deposit of `spec publish --version 1.2.0` (checking_handlers_publish's world, no contract kept before), returns its own
contract to `spec fetch --version 1.2.0` (the folder keeping another at that version), or refuses the retrieval of
`spec obtain` at `1.2.0` (checking_handlers_obtain's world, the upstream holding that version). The Given of the
core's request only says which request the reply is on. The Thens: the contract kept (committed at its version as
the published one, once the stand-in recorded its completion, and the command done), the contract returned (the
stand-in's printed, not the folder's), the version named in the refusal, the contract asked at that version, and
nothing changed (no file, no commit)."""
import os
import sys
import tomllib
from pathlib import Path

from vocab import handler

W = sys.modules["shop_work_queue_world"]
GROUPS = {"g128", "g129", "g130"}
VERSION = "1.2.0"
REPLIES = {"complete": "`spec publish`", "return": "`spec fetch`", "refuse": "`spec obtain`"}
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")


def _module(name):
    return next(m for m in list(sys.modules.values()) if (getattr(m, "__file__", None) or "").endswith("/" + name))


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("replies", {})


def given_instance(step):
    if not mine(step) or step.kind != "contract":
        return False
    world(step)


def given_request(step):
    """`the specification service deposits the contract c1`, `... retrieves the contract c1`: the request replied to."""
    if not mine(step) or step.term not in ("deposit", "retrieve"):
        return False
    world(step)["request"] = step.term


def _files(repo):
    return {p.relative_to(repo).as_posix(): p.read_bytes() for p in sorted(repo.rglob("*"))
            if p.is_file() and ".git" not in p.parts}


def replies(step):
    """`the contract registry service completes the request to deposit the contract c1`, `... returns ...`, `...
    refuses the request to retrieve ...`: the command whose request it is run with the stand-in so answering."""
    if not mine(step) or step.term not in REPLIES:
        return False
    w, registry = world(step), _module("checking_handlers_registry.py")
    obtain = _module("checking_handlers_obtain.py")
    w["calls"] = str(obtain.outside(step) / "registry-calls.jsonl")
    env = dict(obtain.env(step), SHOPSYSTEM_CONTRACT_REGISTRY=str(registry.STAND_IN),
               STAND_IN_REGISTRY_CALLS=w["calls"], STAND_IN_REGISTRY_REPLY=step.term,
               PYTHONPATH=os.pathsep.join([str(registry.STAND_IN.parent), os.environ.get("PYTHONPATH", "")]))
    if step.term == "refuse":
        obtain.build(step)
        words = ["obtain", obtain.UPSTREAM]
    else:
        _module("checking_handlers_publish.py").build(step, step.term == "return", VERSION)
        words = [REPLIES[step.term].strip("`").split()[1]]
    w["head"], w["before"] = W.head(step.repo), _files(step.repo)
    step.context["result"] = step.run("spec", *words, "--version", VERSION, env=env)


def calls(step):
    import json
    path = Path(world(step)["calls"])
    return [json.loads(line) for line in path.read_text().splitlines()] if path.is_file() else []


def _done(step):
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr
    return done


def then_keeps(step):
    """`the specification service keeps the contract c1`: done once the stand-in completed the deposit, the contract
    committed at the version as the published one, and the command saying it kept it."""
    if not mine(step) or "replies" not in step.context or step.term not in KEEPS:
        return False
    done, rel = _done(step), ".shop/contracts/%s/contract.toml" % VERSION
    assert [c["operation"] for c in calls(step)][-2:] == ["deposit", "completed"], calls(step)
    assert rel in W.committed(step.repo) and W.head(step.repo) != world(step)["head"], W.committed(step.repo)
    assert tomllib.loads((step.repo / rel).read_text())["status"] == "published"
    assert "published %s" % rel in done.stdout, done.stdout


def then_returns(step):
    """`the specification service returns the contract c1`: the contract the stand-in returned printed."""
    if not mine(step) or "replies" not in step.context:
        return False
    stand_in = 'context = "the stand-in registry"'
    assert _done(step).stdout.startswith(stand_in), step.context["result"].stdout


def then_does(step):
    """`the specification service names the version v1` (the refusal names `1.2.0`), `the contract c1 has the version
    v1` (the retrieval asked at it)."""
    if not mine(step) or "replies" not in step.context or step.term not in ("name", "has"):
        return False
    done = step.context["result"]
    if step.term == "name":
        assert done.returncode == 1 and VERSION in done.stdout + done.stderr, done.stdout + done.stderr
    else:
        assert [c["version"] for c in calls(step) if c["operation"] == "retrieve"] == [VERSION], calls(step)


def then_unchanged(step):
    if not mine(step) or "replies" not in step.context:
        return False
    assert W.head(step.repo) == world(step)["head"] and _files(step.repo) == world(step)["before"]


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_request)
W.local("WhenHappens")(replies)
W.local("ThenDoes")(lambda step: then_keeps(step) if then_keeps(step) is not False else then_does(step))
W.local("ThenPrints")(then_returns)
W.local("ThenChangesNothing")(then_unchanged)


def untaken(step):
    """The registry's key of a reply's When, which `features vocab --check` reads: what is left when the local above
    takes no step."""
    raise AssertionError("no handler of this scenario's feature took the step: %s" % step.text)


for term in REPLIES:
    handler("WhenHappens", term)(untaken)
