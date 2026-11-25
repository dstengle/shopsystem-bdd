"""Handlers of checking's requirement group that serves a job (r110, b641), each a `work_queue_world.local` that takes
only a step of a scenario of its group (`mine`). The world is the domain-model fixture (tests/scripts/fixtures/
domain-model/) written at the When: the capability c1 its notebook, whose group g1 (the requirement group r1) says
`serves: keep-notes` (the job j1); the capability c2 `shelf`, of the same area, whose one group serves the job too;
and, so that the rule is seen live, `drawer`, a capability whose group serves no job, which `spec check` names under
`w_unserved_cap`. The When runs `spec check`; the Then reads its output: no line of `w_unserved_cap` names c2."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g110"}
JOB = "keep-notes"
NAMES = {"c1": "notebook", "c2": "shelf"}

CAPABILITY = """---
id: capability/example.org/fixture/domain-model/%(name)s
title: %(title)s
narrator: a person keeping notes
group: service
area: notes
specifies: service notes
language: codified-2
retired: []
unbuilt: []
---

# %(title)s

## Purpose
%(title)s of the notes.

## Behaviour

### [g1] %(title)s
%(serves)s- [r1] %(line)s
"""
LINES = {"shelf": "When the person lists the notes, the notes service shall complete the request.",
         "drawer": "When the person labels a note with a tag, the notes service shall keep the tag."}


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def given(step):
    """The job, the requirement group, the capabilities and what the Givens say of them: the world written at the
    When."""
    if not mine(step):
        return False
    step.context["serving"] = True


def build(step):
    repo = step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    spec = repo / "spec"
    notebook = spec / "capabilities" / "notebook.md"
    head = "### [g1] A note added is filed\n"
    assert head in notebook.read_text(), notebook.read_text()
    notebook.write_text(notebook.read_text().replace(head, head + "serves: %s\n" % JOB))
    for name, serves in (("shelf", "serves: %s\n" % JOB), ("drawer", "")):
        (spec / "capabilities" / ("%s.md" % name)).write_text(CAPABILITY % {
            "name": name, "title": name.capitalize(), "serves": serves, "line": LINES[name]})
    index = spec / "index.md"
    row = "| notes | core | notebook |\n"
    assert row in index.read_text(), index.read_text()
    index.write_text(index.read_text().replace(row, "| notes | core | notebook, shelf, drawer |\n"))
    for args in (("features", "generate"), ("spec", "annotate")):
        done = step.run(*args)
        assert done.returncode == 0, done.stdout + done.stderr


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "check")


def then_not_returned(step):
    """`the specification service does not return the capability c2`: no line of `w_unserved_cap` names it, while
    one names drawer, whose group serves no job."""
    if not mine(step) or "serving" not in step.context:
        return False
    out = step.context["result"].stdout
    unserved, inside = [], False
    for line in out.splitlines():    # the rule's heading, then each capability it names, indented
        inside = "w_unserved_cap" in line or (inside and line.startswith(" "))
        unserved += [line] if inside else []
    assert any("/drawer" in line for line in unserved), out
    assert not any("/%s" % NAMES[step.names[0]] in line for line in unserved), out


W.local("GivenK")(given)
W.local("GivenDoes")(given)
W.local("WhenRuns")(runs)
W.local("ThenPrintsNot")(then_not_returned)
