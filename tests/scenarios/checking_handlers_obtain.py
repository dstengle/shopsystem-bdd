"""Handlers of checking's obtained contract scenarios (r81, r82, r88-r90, r102, r103; b587, b591, b593, b596, b601), each a `work_queue_world.local`
that takes only a step of a scenario of one of its groups (`mine`). The world is the domain-model fixture
(tests/scripts/fixtures/domain-model/), copied into the repository at the When with each bounded context under
`## Upstreams` of its index, hosted on GitHub, and committed; the stand-in gh (tests/scripts/stub_gh.py, run as
`$SHOPSYSTEM_WORK_GH` as requests_world runs it) serves those repositories' files: a contract kept at `1.1.0`
superseded and one at `1.2.0` published, or, when the bounded context has no contract, none, and, when its
availability is `unreachable`, no repository at all; when its health is `failing`, the repository but every read
of its contents refused (`$STUB_GH_FAIL` of `api -H`, b596). The fixture nests the adapter spec `adapters/stock-inventory/`
(`ADAPTER`) whose `providers:` name each bounded context obtained from (decision 0136), unless the scenario brings in
an adapter spec that no Given says has the provider, or a Given says no adapter spec has it (g103).

The bounded context the When obtains from is `bounded-context/example.org/fixture/inventory` (`UPSTREAM`), or, when
its id does not conform to the context id form, `bounded-context/example/inventory` (`MALFORMED`: a domain with no
dot); each other bounded context that has a contract (`OTHERS`) has an id that ends in the same word, and its contract
is obtained by `spec obtain` before the When, where it keeps it. The When runs `spec obtain` with the bounded
context's id; the Thens read back the contract kept under the adapter spec's provider/ in the run's commit, the contracts kept before it,
the context requests kept (none: no `.shop/requests/` file and no issue opened), the refusal and what it names."""
import json
import os
import shlex
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
STUB = ROOT / "tests" / "scripts" / "stub_gh.py"
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g81", "g82", "g88", "g89", "g90", "g102", "g103"}
UPSTREAM = "bounded-context/example.org/fixture/inventory"
MALFORMED = "bounded-context/example/inventory"
OTHERS = ["bounded-context/example.org/other/inventory", "bounded-context/example.org/third/inventory"]
PARENT = "bounded-context/example.org/fixture/domain-model"
ADAPTER = "adapters/stock-inventory"
KEPT = ADAPTER + "/provider/example.org/fixture/inventory/1.2.0/contract.toml"
INDEX = "---\nid: %s/adapter/stock-inventory\nkind: adapter\nproviders: [%s]\n---\n\n# stock over inventory\n"
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")    # requested.py's spellings of keep
CONTRACT = 'context = "%s"\nversion = "%s"\nstatus = "%s"\n'


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("obtained", {"kinds": {}, "empty": False, "malformed": False,
                                                "unreachable": False, "failing": False, "has": {}, "kept": {},
                                                "provides": False, "unheld": False})


def given_instance(step):
    if not mine(step) or step.kind not in ("contract", "bounded context", "id", "provider", "adapter spec"):
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_state(step):
    """`the bounded context b1 has no contract`, `... has the contract c1`, `... has the id i1` and `the id i1 does
    not conform to the context id form` (`... conforms to ...`, r103: the id kept in the form); `the adapter spec a1
    has the provider p1` and `no adapter spec has the provider p1` (r103: the nested adapter spec names no bounded
    context)."""
    if not mine(step) or step.term not in ("has", "conform"):
        return False
    w = world(step)
    if step.text.startswith("no adapter spec"):
        w["unheld"] = True
    elif step.term == "conform":
        w["malformed"] = w["malformed"] or step.template.endswith("Not")
    elif any(n.startswith("no contract") for n in step.nps):
        w["empty"] = True
    elif w["kinds"].get(step.names[-1]) == "provider":
        w["provides"] = True
    elif w["kinds"].get(step.names[-1]) == "contract":
        w["has"][step.names[0]] = step.names[-1]


def given_availability(step):
    """`the availability of the bounded context b1 is `unreachable`` and `the health of ... is `failing`` (r102)."""
    if not mine(step) or step.attribute not in ("availability", "health"):
        return False
    value = step.values[0].strip("`")
    world(step)["unreachable" if step.attribute == "availability" else "failing"] = value in ("unreachable", "failing")


def outside(step):
    """A directory beside the repository: the stand-in gh's files."""
    if "outside" not in step.context:
        step.context["outside"] = step.request.getfixturevalue("tmp_path_factory").mktemp("outside")
    return step.context["outside"]


def env(step, failing=False):
    """The stand-in gh's environment; `failing`, every read of a repository's contents refused (r102)."""
    failing = {"STUB_GH_FAIL": "api -H"} if failing else {}
    return dict(os.environ, **failing,
                SHOPSYSTEM_WORK_GH="%s %s" % (shlex.quote(sys.executable), shlex.quote(str(STUB))),
                STUB_GH_CALLS=str(outside(step) / "gh-calls.jsonl"), GH_TOKEN="", GIT_TERMINAL_PROMPT="0")


def gh_calls(step):
    path = outside(step) / "gh-calls.jsonl"
    return [json.loads(line)["argv"] for line in path.read_text().splitlines()] if path.is_file() else []


def obtained_from(step):
    """The id of the bounded context the When obtains from."""
    return MALFORMED if world(step)["malformed"] else UPSTREAM


def host(step, context, contracts=True):
    """`context` hosted on GitHub as `ex/<its path's parts>`, with its contracts unless it has none."""
    repo = "ex/" + context.split("/", 1)[1].replace("/", "-").replace(".", "-")
    hosted = outside(step) / "gh-repos" / repo
    (hosted / "spec").mkdir(parents=True)
    for version, status in (("1.1.0", "superseded"), ("1.2.0", "published")) if contracts else ():
        path = hosted / ".shop" / "contracts" / version / "contract.toml"
        path.parent.mkdir(parents=True)
        path.write_text(CONTRACT % (context, version, status))
    return "- %s: github: %s\n" % (context, repo)


def build(step):
    """The fixture with its upstreams, committed, the upstreams' files the stand-in gh serves, and each other bounded
    context's contract obtained before the When (`kept`: the contract's name to its path and text)."""
    import shutil
    w, repo = world(step), step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    others = dict(zip(w["has"].values(), OTHERS))
    bullets = "" if w["unreachable"] else host(step, obtained_from(step), not w["empty"])
    if w["unreachable"]:
        bullets = "- %s: github: ex/unreachable\n" % obtained_from(step)
    if w.get("unlisted"):       # hosted, but no upstream entry identifies it (checking_handlers_upstream, r132)
        bullets = ""
    if w.get("unhosted"):       # identified, but its entry holds no shared store (checking_handlers_upstream, r141)
        bullets = "- %s: the inventory context\n" % obtained_from(step)
    bullets += "".join(host(step, context) for context in others.values())
    index = repo / "spec" / "index.md"
    index.write_text(index.read_text().rstrip("\n") + "\n\n## Upstreams\n\n" + bullets)
    provides = not w["unheld"] and (w["provides"] or "adapter spec" not in w["kinds"].values())
    named = [obtained_from(step), *others.values()] if provides else []
    (repo / ADAPTER / "spec").mkdir(parents=True)
    (repo / ADAPTER / "spec" / "index.md").write_text(INDEX % (PARENT, ", ".join(named)))
    W.init(repo)
    for contract, context in others.items():
        done = step.run("spec", "obtain", context, env=env(step))
        assert done.returncode == 0, done.stdout + done.stderr
        rel = done.stdout.split()[-1]
        w["kept"][contract] = (rel, (repo / rel).read_bytes())


def runs(step):
    if not mine(step) or step.term != "`spec obtain`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "obtain", obtained_from(step),
                                       env=env(step, world(step)["failing"]))


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


def then_unchanged(step):
    """`the specification service does not change the contract c3`: kept where and as it was before the When."""
    if not mine(step) or "obtained" not in step.context or step.term != "change":
        return False
    _done(step)
    rel, text = world(step)["kept"][step.names[0]]
    assert (step.repo / rel).read_bytes() == text, (rel, (step.repo / rel).read_bytes())
    assert rel not in W.committed(step.repo), W.committed(step.repo)


def then_refuses(step):
    if not mine(step) or "obtained" not in step.context or step.term != "refuse":
        return False
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr
    assert not list(step.repo.rglob("provider")), list(step.repo.rglob("provider"))


def then_names(step):
    """`the specification service names the bounded context b1` and `... names the id i1`: its id; `... names the
    provider p1` (r103): its id as the provider's; `... names `bounded context unreachable``: the reason."""
    if not mine(step) or "obtained" not in step.context or step.term != "name":
        return False
    done = step.context["result"]
    code = next((n.strip("`") for n in step.nps if n.startswith("`")), None)
    kind = world(step)["kinds"].get(step.names[0]) if code is None else None
    if code is None:
        assert kind in ("bounded context", "id", "provider"), step.names
    if kind == "provider":
        assert "the provider %s" % obtained_from(step) in done.stdout + done.stderr, done.stdout + done.stderr
    assert (code or obtained_from(step)) in done.stdout + done.stderr, done.stdout + done.stderr


def then_does(step):
    for each in (then_keeps, then_unchanged, then_refuses, then_names):
        if each(step) is not False:
            return None
    return False


W.local("GivenK")(given_instance)
W.local("GivenK_A")(given_availability)
W.local("GivenDoes")(given_state)
W.local("GivenDoesNot")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then_does)
W.local("ThenDoesNot")(then_does)
