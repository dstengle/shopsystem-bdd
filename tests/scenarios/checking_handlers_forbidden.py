"""Handlers of checking's scenario of a lifecycle transition only a forbidden set reaches (r112, b605), each a
`work_queue_world.local` that takes only a step of a scenario of its group (`mine`). The world is the domain-model
fixture (tests/scripts/fixtures/domain-model/: the notes area, whose note has the lifecycle of its status, its CLI
contract and the notebook capability's lines), written at the When, with the transition `draft → abandoned` added to
the lifecycle (and the value's word `abandoned`), which no operation performs, and r10, a notebook line whose response
forbids setting the status of a draft note to `abandoned` (`set-attribute` under "shall not"). The CLI contract is
annotated (`spec annotate`) and the features written by `features generate`.

The Givens say only what the world is, the transition t1 named in `spec check`'s rows as `note, status, draft,
abandoned`. The When runs `spec check`; the Thens read its output and its exit: the warning w_m5 names the transition,
and a warning is no failure."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g112"}
SAYS = {"transition": "note, status, draft, abandoned"}
LIFECYCLE = "draft → retired"
VALUE = "- **retired** (adjective) → value note.status retired.\n"

FORBIDDING = """
### [g10] A draft note archived is never abandoned
- [r10] While a note is `draft`, when the person archives the note, the notes service shall not set the status of the
  note to `abandoned`.
"""


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("forbidden", {"kinds": {}})


def given(step):
    """Each Given of the group: the world below says it; an instance's kind kept for what the output names it by."""
    if not mine(step):
        return False
    if step.template == "GivenK" and step.names:
        world(step)["kinds"][step.names[0]] = step.kind


def _replaced(path, old, new):
    text = path.read_text()
    assert old in text, text
    path.write_text(text.replace(old, new, 1))


def build(step):
    """The fixture copied into the repository with the transition, its value and the forbidding line."""
    repo = step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    spec = repo / "spec"
    _replaced(spec / "model" / "notes.md", LIFECYCLE, LIFECYCLE + "; draft → abandoned")
    _replaced(spec / "vocabulary" / "notes.md", VALUE,
              VALUE + "- **abandoned** (adjective) → value note.status abandoned.\n")
    notebook = spec / "capabilities" / "notebook.md"
    notebook.write_text(notebook.read_text() + FORBIDDING)
    for name, kind in world(step)["kinds"].items():
        if kind in SAYS:
            step.context.setdefault("says", {})[name] = SAYS[kind]
    for command in (("spec", "annotate"), ("features", "generate")):
        done = step.run(*command)
        assert done.returncode == 0, done.stdout + done.stderr


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "check")


def then_names(step):
    """`the specification service names the transition t1`: a row of `spec check`'s output names it."""
    if not mine(step) or "forbidden" not in step.context or step.term != "name":
        return False
    done, said = step.context["result"], step.context["says"][step.names[0]]
    assert any(line.strip() == said for line in done.stdout.splitlines()), done.stdout + done.stderr


def then_completes(step):
    """`the specification service completes this request`: `spec check` exits 0, its warning no failure."""
    if not mine(step) or "forbidden" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr


for _template in ("GivenK", "GivenDoes", "GivenDoesNot", "GivenNo", "GivenK_A"):
    W.local(_template)(given)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then_names)
W.local("ThenExitsOk")(then_completes)
