"""Handlers of checking's check for an item (r152, b797; r153-r155, b808), each a `work_queue_world.local` that takes only a step of a
scenario of its group (`mine`). The Givens are taken as said; the world is written at the When over the
domain-model fixture (tests/scripts/fixtures/domain-model/): the product file holding the job `keep-notes` (j1, and
j2, the job that violates `w_unserved_job` with no item laid), held by this bounded context, and the item b1 (i1)
holding a group of notebook of its own (the requirement group r1) that serves the job, which no live group serves.
The When runs `spec check --item b1`; the Then reads the rows under `w_unserved_job`: none names the job, while
`spec check` without the item names it (so the Then could fail). Of r153 and r154 the same item, whose group g10 has no
scenario and whose r10 governs `notes.list`, which the context's contract does not hold, so the lay alone would bring
v_s3 and v_a5: the Thens read that no v_s3 row names the group and no v_a5 row the requirement. Of r155 the item's r10
sets a retired note's status to `active`, a transition the lifecycle does not allow (v_m6, of severity error): the
Thens read the check's exit 1 and the v_m6 row naming the requirement."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
GROUPS = {"g152", "g153", "g154", "g155"}
CONTEXT, JOB, RULE = "example.org/fixture/domain-model", "keep-notes", "w_unserved_job"
PRODUCT = """id = "example.org/fixture"
purpose = "Notes kept."
actors = []

[jobs."%(job)s"]
actors = []
statement = "When notes pile up, a person wants them kept, so they can find them."
needs = []

[contexts."%(context)s"]
addresses = []
jobs = ["%(job)s"]
"""
ITEM = """---
id: item/%(context)s/b1
kind: item
status: ready
provenance: own
value: high-value
urgency: medium-urgency
size: small
depends_on: []
---

# Notes kept

## Notes

Notes kept.

## Requirements

### notebook

serves: [g10 %(job)s]

#### [g10] A note listed is kept for the job
- [r10] When the person lists the notes, the notes service shall complete the request.
"""
VIOLATING = ("#### [g10] A retired note archived becomes active\n- [r10] While a note is `retired`, when the person "
             "archives the note, the notes service shall set the status of the note to `active`.\n")
GROUP, REQUIREMENT = "notebook#g10", "notebook#r10"


def tags(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return set(found.tags) if found is not None and Path(found.feature.filename).stem == "checking" else set()


def mine(step):
    return bool(GROUPS & tags(step))


def item(step):
    """The item's text: of r155 its group the violating one, else the group serving the job."""
    if "g155" not in tags(step):
        return ITEM
    head, _, _ = ITEM.partition("serves:")
    return head + VIOLATING


def given(step):
    """The job, the requirement group, the item and what the Givens say of them: the world written at the When."""
    if not mine(step):
        return False
    step.context["item check"] = True


def build(repo, text=ITEM):
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    for rel, body in ((".shop/product/product.toml", PRODUCT), (".shop/backlog/b1.md", text)):
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(body % {"context": CONTEXT, "job": JOB})


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step.repo, item(step))
    for args in (("features", "generate"), ("spec", "annotate")):
        done = step.run(*args)
        assert done.returncode == 0, done.stdout + done.stderr
    step.context["without item"] = step.run("spec", "check")
    step.context["result"] = step.run("spec", "check", "--item", "b1")


def rows(out, code):
    """The rows `spec check` printed under the rule `code`: its heading, then each row it names, indented."""
    found, inside = [], False
    for line in out.splitlines():
        if not line.startswith(" "):
            inside = line.removeprefix("warning ").split("  ")[0] == code
        elif inside:
            found.append(line.strip())
    return found


def then_not_returned(step):
    """`the specification service does not return the job j2`: no row of `w_unserved_job` names the job with the item
    laid, while one names it without."""
    if not mine(step) or "result" not in step.context:
        return False
    if "g152" not in tags(step):
        return then_lay_only(step)
    without, done = step.context["without item"], step.context["result"]
    assert any(JOB in row for row in rows(without.stdout, RULE)), without.stdout + without.stderr
    assert "Traceback" not in done.stderr and "usage:" not in done.stderr, done.stdout + done.stderr
    assert not any(JOB in row for row in rows(done.stdout, RULE)), done.stdout + done.stderr


def then_lay_only(step):
    """`... does not return the requirement group r2` (r153): no v_s3 row names the item's group; `... the operation
    o2` (r154): no v_a5 row names the item's requirement."""
    done = step.context["result"]
    code, said = ("v_s3", GROUP) if "g153" in tags(step) else ("v_a5", REQUIREMENT)
    assert "Traceback" not in done.stderr and "usage:" not in done.stderr, done.stdout + done.stderr
    assert not any(said in row for row in rows(done.stdout, code)), done.stdout + done.stderr


def then_fails(step):
    """`the specification service fails this check` (r155): `spec check --item` exits 1."""
    if "g155" not in tags(step) or "result" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 1 and "Traceback" not in done.stderr, done.stdout + done.stderr


def then_names(step):
    """`the specification service names the rule r2` (r155): a row of `v_m6` names the item's requirement."""
    if "g155" not in tags(step) or "result" not in step.context or step.term != "name":
        return False
    done = step.context["result"]
    assert any(REQUIREMENT in row for row in rows(done.stdout, "v_m6")), done.stdout + done.stderr


for template in ("GivenK", "GivenDoes", "GivenCode", "GivenK_A"):
    W.local(template)(given)
W.local("WhenRuns")(runs)
W.local("ThenPrintsNot")(then_not_returned)
W.local("ThenExitsErr")(then_fails)
W.local("ThenDoes")(then_names)
