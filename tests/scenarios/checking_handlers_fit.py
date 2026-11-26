"""Handlers of checking's scenario of a term whose part of speech does not fit the element it means (r157, b825), each
a `work_queue_world.local` that takes only a step of its group (`mine`). The world is the domain-model fixture
(tests/scripts/fixtures/domain-model/), written at the When: the term t1 `personal`, an adjective in the notes layer;
the element e1 the actor `the person`, which no adjective fits and no other entry of the notes layer means (so no
v_t20 names the term). `spec check` is run; the Thens read its exit and its output."""
import re
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
WORD = "personal"
MISFIT = "- **personal** (adjective) → actor the person. Of the person.\n"


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and "g157" in found.tags


def given(step):
    """a term t1, an element e1; the term t1 does not fit the element e1 and means it: the world built at the When."""
    return None if mine(step) else False


def build(step):
    repo = step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    vocabulary = repo / "spec" / "vocabulary" / "notes.md"
    vocabulary.write_text(vocabulary.read_text().rstrip("\n") + "\n" + MISFIT)


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["fit_check"] = step.run("spec", "check")


def then_fails(step):
    """the specification service fails this check: `spec check` exits 1."""
    if not mine(step) or "fit_check" not in step.context:
        return False
    done = step.context["fit_check"]
    assert done.returncode == 1, done.stdout + done.stderr


def then_names(step):
    """the specification service names the term t1: a row of `spec check`'s output names its word."""
    if not mine(step) or "fit_check" not in step.context or step.term != "name":
        return False
    done = step.context["fit_check"]
    rows = [line.strip() for line in done.stdout.splitlines()]
    assert any(re.match(r"%s\b" % WORD, row) for row in rows), done.stdout + done.stderr


for _template in ("GivenK", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRuns")(runs)
W.local("ThenExitsErr")(then_fails)
W.local("ThenDoes")(then_names)
