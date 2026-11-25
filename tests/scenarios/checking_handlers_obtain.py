"""Handlers of checking's obtained contract scenarios (r81, r82, b587), each a `work_queue_world.local` that takes only
a step of a scenario of one of its groups (`mine`). The world is the domain-model fixture (tests/scripts/fixtures/
domain-model/), copied into the repository at the When with the upstream `bounded-context/example.org/fixture/
inventory` under `## Upstreams` of its index, hosted on GitHub as `ex/inventory`, and committed; the stand-in gh
(tests/scripts/stub_gh.py, run as `$SHOPSYSTEM_WORK_GH` as requests_world runs it) serves that repository's files: a contract kept at `1.1.0`
superseded and the contract c1 at `1.2.0` published, or, when the bounded context has no contract, none.

The When runs `spec obtain` with the bounded context's id; the Thens read back the contract kept under
`provider/inventory/1.2.0/` in the run's commit, the context requests kept (none: no `.shop/requests/` file and no
issue opened), the refusal and what it names."""
import json
import os
import shlex
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
STUB = ROOT / "tests" / "scripts" / "stub_gh.py"
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g81", "g82"}
UPSTREAM = "bounded-context/example.org/fixture/inventory"
KEPT = "provider/inventory/1.2.0/contract.toml"
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")    # requested.py's spellings of keep
CONTRACT = 'context = "%s"\nversion = "%s"\nstatus = "%s"\n'


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("obtained", {"kinds": {}, "empty": False})


def given_instance(step):
    if not mine(step) or step.kind not in ("contract", "bounded context"):
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_none(step):
    """`the bounded context b1 has no contract`."""
    if not mine(step) or step.term != "has" or not any(n.startswith("no contract") for n in step.nps):
        return False
    world(step)["empty"] = True


def outside(step):
    """A directory beside the repository: the stand-in gh's files."""
    if "outside" not in step.context:
        step.context["outside"] = step.request.getfixturevalue("tmp_path_factory").mktemp("outside")
    return step.context["outside"]


def env(step):
    return dict(os.environ, SHOPSYSTEM_WORK_GH="%s %s" % (shlex.quote(sys.executable), shlex.quote(str(STUB))),
                STUB_GH_CALLS=str(outside(step) / "gh-calls.jsonl"), GH_TOKEN="", GIT_TERMINAL_PROMPT="0")


def gh_calls(step):
    path = outside(step) / "gh-calls.jsonl"
    return [json.loads(line)["argv"] for line in path.read_text().splitlines()] if path.is_file() else []


def build(step):
    """The fixture with its upstream, committed, and the upstream's files the stand-in gh serves."""
    import shutil
    w, repo = world(step), step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    index = repo / "spec" / "index.md"
    index.write_text(index.read_text().rstrip("\n") + "\n\n## Upstreams\n\n- %s: github: ex/inventory\n" % UPSTREAM)
    hosted = outside(step) / "gh-repos" / "ex" / "inventory"
    (hosted / "spec").mkdir(parents=True)
    if not w["empty"]:
        for version, status in (("1.1.0", "superseded"), ("1.2.0", "published")):
            path = hosted / ".shop" / "contracts" / version / "contract.toml"
            path.parent.mkdir(parents=True)
            path.write_text(CONTRACT % (UPSTREAM, version, status))
    W.init(repo)


def runs(step):
    if not mine(step) or step.term != "`spec obtain`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "obtain", UPSTREAM, env=env(step))


def _done(step):
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr
    return done


def then_keeps(step):
    """`the specification service keeps the contract c1`: the upstream's published contract, byte for byte, under
    provider/ in the run's commit; `... does not keep a context request`: no request written, no issue opened."""
    if not mine(step) or "obtained" not in step.context or step.term not in KEEPS:
        return False
    _done(step)
    if step.template.endswith("Not"):
        assert any("context request" in n for n in step.nps), step.nps
        assert not list((step.repo / ".shop").glob("requests/*")), list((step.repo / ".shop").rglob("*"))
        assert not [c for c in gh_calls(step) if c[:1] == ["issue"]], gh_calls(step)
        return None
    assert world(step)["kinds"].get(step.names[0]) == "contract", step.names
    assert (step.repo / KEPT).read_text() == CONTRACT % (UPSTREAM, "1.2.0", "published")
    assert KEPT in W.committed(step.repo), W.committed(step.repo)


def then_refuses(step):
    if not mine(step) or "obtained" not in step.context or step.term != "refuse":
        return False
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr
    assert not (step.repo / "provider").exists()


def then_names(step):
    """`the specification service names the bounded context b1`: its id."""
    if not mine(step) or "obtained" not in step.context or step.term != "name":
        return False
    done = step.context["result"]
    assert world(step)["kinds"].get(step.names[0]) == "bounded context", step.names
    assert UPSTREAM in done.stdout + done.stderr, done.stdout + done.stderr


def then_does(step):
    for each in (then_keeps, then_refuses, then_names):
        if each(step) is not False:
            return None
    return False


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_none)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then_does)
W.local("ThenDoesNot")(then_does)
