"""Handlers of checking's adapter contract scenarios (r48-r51, b368): `spec annotate` and `spec check` on a copy of
the domain-model fixture (tests/scripts/fixtures/domain-model/: the notes service, its CLI contract and the notebook
capability's lines), each step a `work_queue_world.local` that takes only a step of a checking scenario of its own.

The Givens keep what they say (`world`); at the When the world is built: the operation o1 is `notes.file`, the
requirement r1 one that governs it (`notebook#r7`) unless a Given says it does not (then `notebook#r6`, which governs
`notes.list`), every adapter contract the fixture's `spec/adapters/cli.toml`, its requirements taken out. A Given of what an operation holds
annotates the contract first (`spec annotate`), then takes r1 out of o1 or puts it in. What the output names each by
is kept in `says`. The Thens read the contract back (adapter_cli): an operation no Given placed is the one of the kept
contract that holds the requirement."""
import re
import shutil
import sys
from pathlib import Path

from vocab import handler

W = sys.modules["shop_work_queue_world"] if "shop_work_queue_world" in sys.modules else None
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
CONTRACT = "spec/adapters/cli.toml"
KINDS = ("operation", "adapter contract", "requirement")
OPERATION, GOVERNING, OTHER = "notes.file", "notebook#r7", "notebook#r6"


def _world():
    global W
    if W is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("shop_work_queue_world",
                                                      Path(__file__).with_name("work_queue_world.py"))
        sys.modules["shop_work_queue_world"] = W = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(W)
    return W


def mine(step):
    """A step of one of checking's own scenarios (not a group moved in from another capability)."""
    return sys.modules["vocab"].origin(step.request.node) == "checking"


def world(step):
    return step.context.setdefault("annotate", {"facts": set(), "names": {}})


def negated(step):
    return step.template.endswith("Not")


def given_instance(step):
    if not mine(step) or step.kind not in KINDS:
        return False
    world(step)["names"].setdefault(step.names[0], step.kind)
    step.context["build"] = build


def given_state(step):
    """`the requirement r1 governs the operation o1`, `the operation o1 does not hold the requirement r1`, ..."""
    if not mine(step) or "annotate" not in step.context or step.term not in ("govern", "holds"):
        return False
    world(step)["facts"].add((step.names[0], step.term, step.names[1], not negated(step)))


def build(step):
    """The fixture copied into the repository, the instances named, and what the operations hold set."""
    w, repo = world(step), step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    path = repo / CONTRACT       # the fixture is annotated: its operations hold nothing until annotate writes them
    path.write_text(scripts("adapter_annotate").annotated(path.read_text(), {}))
    governs = not any(v == "govern" and not pos for _, v, _, pos in w["facts"])
    named = {"operation": OPERATION, "requirement": GOVERNING if governs else OTHER, "adapter contract": CONTRACT}
    held = [(o, r, pos) for o, v, r, pos in w["facts"] if v == "holds" and w["names"].get(o) == "operation"]
    placed = {n for fact in w["facts"] for n in (fact[0], fact[2])}     # an operation a Given placed
    for name, kind in w["names"].items():
        if kind != "operation" or name in placed:
            w.setdefault("bound", {})[name] = named[kind]
            step.context.setdefault("says", {})[name] = named[kind]
    if held:
        done = step.run("spec", "annotate")
        assert done.returncode == 0, done.stdout + done.stderr
        path = repo / CONTRACT
        text = path.read_text()
        for _, r, pos in held:
            ident = w["bound"][r]
            if pos:
                text = text.replace('[operations."%s"]\n' % OPERATION, '[operations."%s"]\nrequirements = ["%s: a line"]\n'
                                    % (OPERATION, ident), 1) if '\nrequirements = [' not in _table(text) else \
                    text.replace(_table(text), _table(text).replace("requirements = [\n", 'requirements = [\n  "%s: a '
                                                                    'line",\n' % ident, 1), 1)
            else:
                text = re.sub(r'\n  "%s: [^\n]*",' % re.escape(ident), "", text)
        path.write_text(text)
    w["before"] = (repo / CONTRACT).read_text()


def _table(text):
    """The text of the operation's own table, its header to the next table's."""
    start = text.index('[operations."%s"]\n' % OPERATION)
    end = text.find("\n[", start + 1)
    return text[start:end if end > 0 else len(text)]


def scripts(name):
    """A module of the plugin's scripts."""
    import importlib
    if str(ROOT / "scripts") not in sys.path:
        sys.path.insert(0, str(ROOT / "scripts"))
    return importlib.import_module(name)


def contract(step):
    return scripts("adapter_cli").read(step.repo)


def annotate(step, *args):
    step.context.pop("build", lambda _: None)(step)
    step.context["result"] = step.run("spec", "annotate", *args)


@handler("WhenRuns", "`spec annotate`")
def runs_annotate(step):
    annotate(step)


@handler("WhenRuns", "`spec annotate --check`")
def runs_annotate_audit(step):
    annotate(step, "--check")


def runs_check(step):
    """`spec check` on the built world (no other world's base written over it)."""
    if not mine(step) or step.term != "`spec check`" or "annotate" not in step.context:
        return False
    step.context.pop("build")(step)
    step.context["result"] = step.run("spec", "check")


def operation_of(step, name, requirement=None):
    """The operation an instance names: the one a Given placed, else the kept contract's that holds `requirement`."""
    w = world(step)
    if name not in w.get("bound", {}):
        found = [i for i, op in contract(step).operations.items() if requirement in op.requirements]
        assert found, "no operation of %s holds %s" % (CONTRACT, requirement)
        w["bound"][name] = found[0]
    return w["bound"][name]


def then_state(step):
    """`the operation o2 holds the requirement r1`, `the adapter contract a2 holds the operation o2`."""
    if not mine(step) or "annotate" not in step.context or step.term not in ("holds", "keep", "write"):
        return False
    w, read = world(step), contract(step)
    if step.term in ("keep", "write"):      # the contract kept: annotate wrote it
        done = step.context["result"]
        assert done.returncode == 0 and "annotated %s" % CONTRACT in done.stdout, done.stdout + done.stderr
        assert (step.repo / CONTRACT).read_text() != w["before"]
        w["bound"].setdefault(step.names[0], CONTRACT)
        return None
    subject, thing = step.names[0], step.names[1]
    if w["names"].get(subject) == "operation":
        requirement = w["bound"][thing]
        assert requirement in read.operations[operation_of(step, subject, requirement)].requirements, requirement
    else:
        assert w["bound"].setdefault(subject, CONTRACT) == CONTRACT
        assert operation_of(step, thing) in read.operations


for _template in ("GivenK",):
    _world().local(_template)(given_instance)
for _template in ("GivenDoes", "GivenDoesNot"):
    _world().local(_template)(given_state)
_world().local("WhenRuns")(runs_check)
_world().local("ThenDoes")(then_state)
