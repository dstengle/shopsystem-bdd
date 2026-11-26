"""Handlers of checking's scenarios of a frame that does not end its term and of a slot that refers to nothing (r158,
r159, b840), each a `work_queue_world.local` that takes only a step of their groups (`mine`). The world is the
domain-model fixture (tests/scripts/fixtures/domain-model/), written at the When, the notes layer's `add` entry's
frame changed:

- g158: the frame f1 `<actor> adds <note>.` with text after it that starts no field (`UNENDED`), so it does not end
  the term; `spec check` run, its output naming the frame as written in a v_t13 row.
- g159: the frame f1 `<actor> adds <gadget>.`, its slot s1 `<gadget>` naming no kind, no actor and no parameter
  (`UNSLOTTED`); `spec check` run, its output naming the slot in a v_t13 row.

The Givens are the world the When writes; the Thens read the run's exit and output."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
VOCABULARY = Path("spec") / "vocabulary" / "notes.md"
READS = "Frame: <actor> adds <note>."
FRAME = "<actor> adds <note>."
UNENDED = READS + " Then it is kept by the tester."
SLOT = "<gadget>"
UNSLOTTED = "Frame: <actor> adds %s." % SLOT
# of each group, the frame its entry is given and what a v_t13 row of the check names
WORLDS = {"g158": (UNENDED, FRAME), "g159": (UNSLOTTED, SLOT)}


def group(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    if found is None or Path(found.feature.filename).stem != "checking":
        return None
    return next((g for g in WORLDS if g in found.tags), None)


def mine(step):
    return group(step) is not None


def frame(group_):
    """The `add` entry's frame of the group, written into the notes layer in place of the one that reads."""
    return WORLDS[group_][0]


def given(step):
    """a frame f1, a term t1, a slot s1; the term t1 has the frame f1, the frame f1 does not end the term t1, the frame
    f1 has the slot s1, the slot s1 refers to no term and to no parameter: the world the When writes."""
    return None if mine(step) else False


def build(step):
    repo = step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    vocabulary = repo / VOCABULARY
    text = vocabulary.read_text()
    assert READS in text, text
    vocabulary.write_text(text.replace(READS, frame(group(step)), 1))


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["slot_check"] = step.run("spec", "check")


def then_fails(step):
    """the specification service fails this check: `spec check` exits 1."""
    if not mine(step) or "slot_check" not in step.context:
        return False
    done = step.context["slot_check"]
    assert done.returncode == 1, done.stdout + done.stderr


def then_names(step):
    """the specification service names the frame f1 (as written) or the slot s1 (in its angle brackets): a v_t13 row
    of `spec check`'s output under the term says it."""
    if not mine(step) or "slot_check" not in step.context or step.term != "name":
        return False
    done = step.context["slot_check"]
    named = WORLDS[group(step)][1]
    rows = [line for line in done.stdout.splitlines() if "Frame:" in line]
    assert "v_t13" in done.stdout and any(named in row for row in rows), done.stdout + done.stderr


for _template in ("GivenK", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRuns")(runs)
W.local("ThenExitsErr")(then_fails)
W.local("ThenDoes")(then_names)
