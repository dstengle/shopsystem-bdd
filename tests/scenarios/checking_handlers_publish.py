"""Handlers of checking's published contract scenarios (r73-r80, b348), each a `work_queue_world.local` that takes only
a step of a scenario of one of its groups (`mine`). The world is the domain-model fixture (tests/scripts/fixtures/
domain-model/: the notes service and the notebook capability's lines), copied into the repository at the When and
committed, with the contracts the Givens keep under `.shop/contracts/<version>/contract.toml` (contract_publish).

The Givens keep what they say (`world`): a contract with a status or a version is kept at it (`1.0.0`, `1.1.0`, ...
by default, `published` by default); of a fetch, the contract c1 is kept at the version the request names (a later
`9.9.9` published beside it) or, with none or one no contract has, at `1.2.0` published (an earlier `1.1.0`
superseded beside it); the requirements r1, r2 are `notebook#r1`, `notebook#r2`, the terms t1, t2 `note` and `tag`,
and t3 `parameter`, a word of the request pack, no term of the context's own; a requirement that does not conform to
the language reference is a line grammar 4 does not read, written as `notebook#r10`; a version v1 that does not
conform to the version form is `../1.2.0` (`MALFORMED`). The When runs `spec publish` or
`spec fetch` with `--version` the code it names; the Thens read the contract kept or printed back."""
import shutil
import sys
import tomllib
from pathlib import Path

from vocab import handler

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g%d" % n for n in range(73, 81)} | {"g83"}
KEPT = Path(".shop") / "contracts"
SAYS = {"requirement": ["notebook#r1", "notebook#r2"], "term": ["note", "tag", "parameter"]}
NONCONFORMING = "- [r10] When the person adds a note, the notes service shall banana the note.\n"
MALFORMED = "../1.2.0"    # a version not in the version form: it would name a folder outside .shop/contracts/
requested = sys.modules["vocab"].vocab4.requested     # KEEPS: the spellings of keep


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("published", {"kinds": {}, "status": {}, "version": {}, "nonconforming": False,
                                                 "absent": set()})


def given_instance(step):
    if not mine(step) or step.kind not in ("contract", "requirement", "term", "downstream context", "version"):
        return False
    w = world(step)
    w["kinds"][step.names[0]] = step.kind
    if step.kind in SAYS:
        said = [n for n, k in w["kinds"].items() if k == step.kind]
        step.context.setdefault("says", {})[step.names[0]] = SAYS[step.kind][len(said) - 1]


def given_status(step):
    """`the status of the contract c2 is `published``."""
    if not mine(step) or step.attribute != "status":
        return False
    world(step)["status"][step.names[0]] = step.values[0].strip("`")


def given_state(step):
    """`the contract c1 has `1.2.0``, `no contract has `2.0.0``, `the requirement r1 does not conform to the language
    reference`, `the contract c2 holds the term t1` (the contract published holds every term: nothing to write)."""
    if not mine(step) or step.term not in ("has", "conform", "holds"):
        return False
    w, code = world(step), next((n for n in step.nps if n.startswith("`")), None)
    if step.term == "conform" and w["kinds"].get(step.names[0]) == "version":
        step.context.setdefault("says", {})[step.names[0]] = MALFORMED
    elif step.term == "conform":
        w["nonconforming"] = True
    elif step.term == "has" and step.names:
        w["version"][step.names[0]] = code.strip("`")
    elif step.term == "has":
        w["absent"].add(code.strip("`"))


def _keep(repo, version, status):
    path = repo / KEPT / version / "contract.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('context = "bounded-context/example.org/fixture/domain-model"\nversion = "%s"\nstatus = "%s"\n'
                    % (version, status))
    return path.relative_to(repo).as_posix()


def build(step, fetching, version):
    """The fixture and the contracts the Givens keep written and committed."""
    w, repo = world(step), step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    if w["nonconforming"]:
        path = repo / "spec" / "capabilities" / "notebook.md"
        text = path.read_text()
        assert "## Behaviour\n" in text, text
        path.write_text(text.rstrip("\n") + "\n\n### [g10] A line out of the language\n" + NONCONFORMING)
        for name, kind in w["kinds"].items():
            if kind == "requirement":
                step.context.setdefault("says", {})[name] = "notebook#r10"
    w["paths"] = {}
    if fetching:
        if version and version not in w["absent"]:
            w["paths"]["c1"] = _keep(repo, version, "superseded")
            _keep(repo, "9.9.9", "published")
        else:
            _keep(repo, "1.1.0", "superseded")
            w["paths"]["c1"] = _keep(repo, "1.2.0", "published")
    else:
        kept = [n for n in w["kinds"] if n in w["status"] or n in w["version"]]
        for k, name in enumerate(kept):
            w["paths"][name] = _keep(repo, w["version"].get(name, "1.%d.0" % k), w["status"].get(name, "published"))
    W.init(repo)
    w["before"] = _files(repo)


def _files(repo):
    return {p.relative_to(repo).as_posix(): p.read_bytes() for p in sorted(repo.rglob("*"))
            if p.is_file() and ".git" not in p.parts}


def runs(step):
    if not mine(step) or step.term not in ("`spec publish`", "`spec fetch`"):
        return False
    says = step.context.get("says", {})
    version = next((says.get(v.split()[-1], v).strip("`") for o, v in step.options if o == "`--version`" and v), None)
    build(step, step.term == "`spec fetch`", version)
    words = [step.term.strip("`").split()[1]] + (["--version", version] if version else [])
    step.context["result"] = step.run("spec", *words)
    world(step)["fetched"] = step.term == "`spec fetch`"


def _done(step):
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr
    return done


def _new(step):
    """The contract the run kept anew: the one file under .shop/contracts/ it wrote that was not there before."""
    w = world(step)
    found = [p for p in _files(step.repo) if p.startswith(KEPT.as_posix()) and p not in w["before"]]
    assert len(found) == 1, found
    return found[0]


def _contract(step, name):
    """The contract an instance names, read: the one printed by a fetch, else the one kept at its path."""
    w = world(step)
    if w["fetched"]:
        return tomllib.loads(_done(step).stdout)
    if name not in w["paths"]:
        w["paths"][name] = _new(step)
    return tomllib.loads((step.repo / w["paths"][name]).read_text())


def then_keeps(step):
    """`the specification service keeps the contract c2` (committed), `... the requirement r1`, `... the term t1`
    (the contract kept holds it), and their negation."""
    if not mine(step) or "published" not in step.context or step.term not in requested.KEEPS:
        return False
    w, name, positive = world(step), step.names[0], not step.template.endswith("Not")
    _done(step)
    kind = w["kinds"].get(name, "contract")
    if kind == "contract":
        rel = _new(step)
        w["paths"][name] = rel
        assert rel in W.committed(step.repo), (rel, W.committed(step.repo))
        return None
    kept, said = _contract(step, "the kept"), step.context["says"][name]
    if kind == "requirement":
        found = any(r.startswith(said + ": ") for r in kept.get("requirements", []))
    else:
        found = any(t.startswith(said + " (") for t in kept.get("terms", []))
    assert found == positive, (said, kept.get("requirements"), kept.get("terms"))


def then_has(step):
    """`the contract c2 has `1.2.0``."""
    if not mine(step) or "published" not in step.context or step.term != "has":
        return False
    code = next(n for n in step.nps if n.startswith("`")).strip("`")
    assert _contract(step, step.names[0])["version"] == code


def then_status(step):
    """`the status of the contract c2 is `published``."""
    if not mine(step) or "published" not in step.context or step.attribute != "status":
        return False
    assert _contract(step, step.names[0]).get("status") == step.values[0].strip("`")


def then_set(step):
    """`the specification service sets the status of the contract c2 to `superseded``, and its negation: the file
    of the contract kept before is changed to it in the run's commit, or left as it was."""
    if not mine(step) or "published" not in step.context or step.term != "set":
        return False
    w, name = world(step), step.names[0]
    _done(step)
    rel, value = w["paths"][name], step.values[0].strip("`")
    now = tomllib.loads((step.repo / rel).read_text())
    if step.template.endswith("Not"):
        assert (step.repo / rel).read_bytes() == w["before"][rel], rel
    else:
        assert now["status"] == value and rel in W.committed(step.repo), (rel, now)


def then_refuses(step):
    if not mine(step) or "published" not in step.context or step.term != "refuse":
        return False
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr


def then_names(step):
    """`the specification service names `1.2.0``, `... names the requirement r1`."""
    if not mine(step) or "published" not in step.context or step.term != "name":
        return False
    done = step.context["result"]
    said = step.context.get("says", {}).get(step.names[0]) if step.names else step.nps[-1].strip("`")
    assert said and said in done.stdout + done.stderr, (said, done.stdout + done.stderr)


def then_does(step):
    for each in (then_keeps, then_has, then_set, then_refuses, then_names):
        if each(step) is not False:
            return None
    return False


def then_returns(step):
    """`the specification service returns the contract c1`: the printed contract is the one kept as c1."""
    if not mine(step) or "published" not in step.context:
        return False
    w = world(step)
    printed = tomllib.loads(_done(step).stdout)
    assert printed == tomllib.loads((step.repo / w["paths"][step.names[0]]).read_text()), printed


def then_unchanged(step):
    if not mine(step) or "published" not in step.context:
        return False
    assert _files(step.repo) == world(step)["before"]


W.local("GivenK")(given_instance)
W.local("GivenK_A")(given_status)
W.local("GivenDoes")(given_state)
W.local("GivenDoesNot")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then_does)
W.local("ThenDoesNot")(then_does)
W.local("ThenK_A", "contract")(then_status)


@handler("ThenK_A", "contract")
def untaken(step):
    """The registry's key of a contract's status Then, which `features vocab --check` reads: what is left when the
    local above takes no step."""
    raise AssertionError("no handler of this scenario's feature took the step: %s" % step.text)
W.local("ThenPrints")(then_returns)
W.local("ThenChangesNothing")(then_unchanged)
