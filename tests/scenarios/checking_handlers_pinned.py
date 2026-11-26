"""Handlers of checking's contract obtained at the version its adapter spec pins (r138, b735; b599), each a
`work_queue_world.local` that takes only a step of a scenario of g138 (`mine`), over checking_handlers_obtain's world
(the domain-model fixture, the stand-in gh, the bounded context `UPSTREAM` obtained from). The provider's version a
Given names is the version the nested adapter spec pins it at (`providers: [<id>@<version>]`); the contract the
provider has is hosted at the version a Given names, published, beside one at the pinned version, superseded. The When
runs `spec obtain` with the provider's id and no version, the registry checking_handlers_registry's stand-in recording
each request and answering as the shop-folder adapter does; the Then reads back the register it recorded, of the
contract at the pinned version for the adapter spec with the provider, and none at the published one."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
O = next(m for m in list(sys.modules.values()) if (getattr(m, "__file__", None) or "").endswith(
    "/checking_handlers_obtain.py"))     # loaded before this module: the glob is sorted
GROUPS = {"g138"}


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("pinned", {"kinds": {}, "versions": {}, "has": {}})


def given_instance(step):
    if not mine(step) or step.kind not in ("contract", "provider", "adapter spec"):
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_state(step):
    """`the provider p1 has the `1.2.0` version` and `the contract c1 has `1.3.0``: the version of each; `the provider p1 has the
    contract c1` and `the adapter spec a1 has the provider p1`."""
    if not mine(step) or step.term != "has":
        return False
    w = world(step)
    code = next((n.split("`")[1] for n in step.nps if "`" in n), None)     # bare, or "the `1.2.0` version" (b733)
    if code is not None:
        w["versions"][step.names[0]] = code
    else:
        w["has"][step.names[0]] = step.names[-1]


def _of(step, kind):
    w = world(step)
    return next(n for n, k in w["kinds"].items() if k == kind and n in w["versions"])


def pinned(step):
    return world(step)["versions"][_of(step, "provider")]


def _registry():
    return next(m for m in list(sys.modules.values()) if (getattr(m, "__file__", None) or "").endswith(
        "/checking_handlers_registry.py"))


def build(step):
    """The fixture with the upstream under `## Upstreams`, its contracts the stand-in gh serves (the pinned version
    superseded, the contract's published), and the adapter spec pinning the provider, committed."""
    repo, pin = step.repo, pinned(step)
    for part in ("spec", "features"):
        shutil.copytree(O.FIXTURE / part, repo / part, dirs_exist_ok=True)
    published = world(step)["versions"][_of(step, "contract")]
    repo_name = "ex/" + O.UPSTREAM.split("/", 1)[1].replace("/", "-").replace(".", "-")
    for version, status in ((pin, "superseded"), (published, "published")):
        path = O.outside(step) / "gh-repos" / repo_name / ".shop" / "contracts" / version / "contract.toml"
        path.parent.mkdir(parents=True)
        path.write_text(O.CONTRACT % (O.UPSTREAM, version, status))
    (O.outside(step) / "gh-repos" / repo_name / "spec").mkdir(parents=True)
    index = repo / "spec" / "index.md"
    index.write_text(index.read_text().rstrip("\n") + "\n\n## Upstreams\n\n- %s: github: %s\n" % (O.UPSTREAM,
                                                                                               repo_name))
    (repo / O.ADAPTER / "spec").mkdir(parents=True)
    adapter = O.INDEX % (O.PARENT, "%s@%s" % (O.UPSTREAM, pin))
    (repo / O.ADAPTER / "spec" / "index.md").write_text(adapter)
    world(step)["index"] = adapter
    W.init(repo)


def runs(step):
    if not mine(step) or step.term != "`spec obtain`":
        return False
    build(step)
    world(step)["calls"] = str(O.outside(step) / "registry-calls.jsonl")
    step.context["result"] = step.run("spec", "obtain", O.UPSTREAM, env=_registry().stand_in(step, world(step)["calls"]))


def then_does(step):
    """`the specification service registers the contract c2 for the adapter spec a1 with the provider p1 and the
    `1.2.0` version`: the register recorded at the version the step names, the adapter spec's pin."""
    if not mine(step) or "pinned" not in step.context or step.term != "register":
        return False
    import json
    path = Path(world(step)["calls"])
    made = [json.loads(line) for line in path.read_text().splitlines()] if path.is_file() else []
    code = next(n.split("`")[1] for n in step.nps if "`" in n)
    assert code == pinned(step), (code, pinned(step))
    _registry().registered(step, made, world(step)["kinds"], code)


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then_does)
