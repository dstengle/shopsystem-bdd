"""Handlers of checking's scenarios of a verb's frame (r150, r151, b796), each a `work_queue_world.local` that takes
only a step of a scenario of their groups (`mine`). The world is docs/recipes.md's sketch context
tests/scripts/fixtures/docs-checklists, written at the When:

- g150: as it is, its `list` and `show` entries' frames a fixed phrase before a noun phrase (`<actor> lists the
  characters of <note>.`), each a verb naming an operation; `spec check` run, which completes only when the frames read.
- g151: the frame f1 that violates `v_t13` written as `list`'s first frame, `<actor> lists <note> <checklist>.` (a kind
  after a kind with no word between); `spec check` run, its output naming the frame as written, angle brackets kept.

The Givens keep what they say (`world`); the Thens read the run's exit and output."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "docs-checklists"
GROUPS = {"g150", "g151"}
VOCABULARY = Path("spec") / "vocabulary" / "checklists.md"
READS = "Frame: <actor> lists <checklist>."
UNREAD = "<actor> lists <note> <checklist>."


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("frame", {"violates": False})


def given(step):
    """a frame f1, a term t1, a fixed phrase f2, a noun phrase n1; the term t1 has the frame f1, the frame f1 has the
    fixed phrase f2, the frame f1 takes the noun phrase n1: the fixture's frames; the frame f1 violates `v_t13`."""
    if not mine(step):
        return False
    if step.template == "GivenDoes" and step.term == "violate":
        world(step)["violates"] = True


def build(step):
    repo, w = step.repo, world(step)
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    if w["violates"]:
        vocabulary = repo / VOCABULARY
        text = vocabulary.read_text()
        assert READS in text, text
        vocabulary.write_text(text.replace(READS, "Frame: " + UNREAD, 1))


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "check")


def then_completes(step):
    """the specification service completes this request: `spec check` exits 0."""
    if not mine(step) or "result" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr


def then_fails(step):
    """the specification service fails this check: `spec check` exits 1."""
    if not mine(step) or "result" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr


def then_names(step):
    """the specification service names the frame f1: a v_t13 line of `spec check`'s output says it as written."""
    if not mine(step) or "result" not in step.context or step.term != "name":
        return False
    done = step.context["result"]
    assert any(UNREAD in line and "Frame:" in line for line in done.stdout.splitlines()), done.stdout + done.stderr


for _template in ("GivenK", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRuns")(runs)
W.local("ThenExitsOk")(then_completes)
W.local("ThenExitsErr")(then_fails)
W.local("ThenDoes")(then_names)
