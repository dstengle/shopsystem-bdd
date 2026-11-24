"""Handlers of checking's contract scenarios (r64-r67, b547), each a `work_queue_world.local` that takes only a step of
a scenario of one of its groups (`mine`). The world is the domain-model fixture (tests/scripts/fixtures/domain-model/:
the notes service, its CLI contract and the notebook capability's lines), copied into the repository at the When.

The Givens keep what they say (`world`): the requirement r1 is `notebook#r7`, which governs the operation o1
`notes.file`; a property p1 the operation has is `idempotent by note`, written on `file`'s model line; a property
that refers to an operation that does not exist is `compensated by unfile`, written there in its place. The When runs
`spec prepare` with `--contract` the contract's version (`VERSION`), or `spec check`. The Thens read the contract
`spec prepare` printed back by contract_form."""
import shutil
import sys
import tomllib
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g64", "g65", "g66", "g67"}
VERSION = "1.0.0"
OPERATION, GOVERNING, LINE = "notes.file", "notebook#r7", "  operation file(note)"
HAD, UNREFERRED = "idempotent by note", "compensated by unfile"


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("contract", {"kinds": {}, "facts": set()})


def given_instance(step):
    if not mine(step) or step.kind not in ("contract", "requirement", "operation", "property"):
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_state(step):
    """`the requirement r1 governs the operation o1`, `the operation o1 has the property p1`, `the property p1
    refers to the operation o1`, `the operation o1 does not exist`."""
    if not mine(step) or step.term not in ("govern", "has", "refer", "exist"):
        return False
    world(step)["facts"].add((step.term, not step.template.endswith("Not")))


def build(step):
    """The fixture copied into the repository, `file`'s model line given the property the Givens say, and what the
    output names each instance by."""
    w, repo = world(step), step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    facts = {term for term, _ in w["facts"]}
    prop = UNREFERRED if ("exist", False) in w["facts"] else HAD if "has" in facts else None
    if prop:
        path = repo / "spec" / "model" / "notes.md"
        text = path.read_text()
        assert LINE + "\n" in text, text
        path.write_text(text.replace(LINE + "\n", "%s  %s\n" % (LINE, prop), 1))
    says = {"contract": VERSION, "requirement": GOVERNING, "operation": OPERATION, "property": prop}
    for name, kind in w["kinds"].items():
        step.context.setdefault("says", {})[name] = says[kind]
    w["before"] = _files(repo)


def _files(repo):
    return {p.relative_to(repo): p.read_bytes() for p in sorted(repo.rglob("*")) if p.is_file() and ".git" not in p.parts}


def runs(step):
    if not mine(step) or step.term not in ("`spec prepare`", "`spec check`"):
        return False
    build(step)
    words = ["prepare", "--contract", VERSION] if step.term == "`spec prepare`" else ["check"]
    step.context["result"] = step.run("spec", *words)


def printed(step):
    """The contract `spec prepare` printed, read as TOML."""
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr
    return tomllib.loads(done.stdout)


def then_prints(step):
    """`spec` prints the contract c2."""
    if not mine(step) or "contract" not in step.context or step.term != "`spec`":
        return False
    found = printed(step)
    assert found.get("version") == VERSION, found
    world(step)["printed"] = step.names[0]


def then_does(step):
    """`the contract c2 conforms to the contract form`, `the contract c2 holds the requirement r1`, `... the property
    p1`."""
    if step.term == "name":
        return then_names(step)
    if not mine(step) or "contract" not in step.context or step.term not in ("conform", "holds"):
        return False
    w, says = world(step), step.context["says"]
    assert step.names[0] == w.get("printed"), (step.names, w)
    text = step.context["result"].stdout
    if step.term == "conform":
        problems = _scripts("contract_form").problems(text)
        assert not problems, problems
        return None
    operation = printed(step)["operations"][OPERATION]
    thing = step.names[1]
    if w["kinds"].get(thing) == "requirement":
        assert any(r.startswith(says[thing] + ": ") for r in operation.get("requirements", [])), operation
    else:
        assert says[thing] in operation.get("properties", []), operation


def then_unchanged(step):
    """`the specification service changes nothing`: no file of the repository written or removed."""
    if not mine(step) or "contract" not in step.context:
        return False
    assert _files(step.repo) == world(step)["before"]


def then_fails(step):
    """`spec check` fails this check: the domain model breaks its own rules (v_m8)."""
    if not mine(step) or "contract" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 1 and "v_m8" in done.stdout, done.stdout + done.stderr


def then_names(step):
    """`the specification service names the property p1`: a v_m8 finding of the property."""
    if not mine(step) or "contract" not in step.context or step.term != "name":
        return False
    done, said = step.context["result"], step.context["says"][step.names[0]]
    found = done.stdout.partition("v_m8 ")[2].split("\nv_")[0]     # the findings of v_m8, one a line
    assert any(" %s, " % said in line for line in found.splitlines()), done.stdout + done.stderr


def _scripts(name):
    import importlib
    if str(ROOT / "scripts") not in sys.path:
        sys.path.insert(0, str(ROOT / "scripts"))
    return importlib.import_module(name)


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_state)
W.local("GivenDoesNot")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenPrints")(then_prints)
W.local("ThenDoes")(then_does)
W.local("ThenChangesNothing")(then_unchanged)
W.local("ThenExitsErr")(then_fails)
