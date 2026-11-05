"""Handlers of features/telemetry.feature (workflow simplification plan 7, D13): `measure batch`, `measure defect`
and `measure compare` run in a repository batches_world.py builds (the batch, its items, its pull request), with
Claude Code's store a directory of the scenario's own, never the person's.

The When leaves in `step.context["world"]` a `Ran`, which has what batch-measurement's `include` and `prints` Thens
read (`code`, `out`, `err`, `record()`, `figures()`, `written()`), and sets `step.context["telemetry"]`. A step
whose key another capability claims is taken through work_queue_world's `local` table by its kind, so
test_telemetry.py binds with `bind_all`; each local returns False outside a telemetry run."""
import importlib.util
import json
import os
import sys
from pathlib import Path

from vocab import handler

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.append(str(SCRIPTS))

import batch_findings


def shared(name, file):
    """A world module loaded once by path (relative to this directory), the one the other handler modules load under
    the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).parent / file)
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
T = shared("shop_batches_world", "batches_world.py")
local = W.local
MEASUREMENTS = ".shop/records/measurements/"


class Ran:
    """A `measure` run, as batch-measurement's Thens read one."""

    existing = None

    def __init__(self, repo, done):
        self.repo, self.code, self.out, self.err = repo, done.returncode, done.stdout, done.stderr

    def record(self):
        return self.repo / self.out.strip().splitlines()[-1]

    def figures(self):
        return json.loads(self.record().read_text().split("```json\n", 1)[1].split("\n```", 1)[0])

    def written(self):
        folder = self.repo / MEASUREMENTS
        return sorted(p.name for p in folder.glob("*.md")) if folder.is_dir() else []


def run_measure(step, *args):
    env = dict(os.environ, CLAUDE_CONFIG_DIR=str(T.outside(step) / "store"))
    ran = Ran(step.repo, step.run("measure", *args, env=env))
    step.context["world"], step.context["telemetry"] = ran, True
    return ran


def telemetry(step):
    return bool(step.context.get("telemetry"))


@handler("GivenK", "review finding")
def given_review_finding(step):
    T.given(step, "review finding", step.names[0])


@local("GivenR", "review finding")
def review_finding_on(step):
    if step.term != "on":
        return False
    finding, pr = step.names
    T.given(step, "review finding", finding)["pull request"] = pr


def write_reviews(step):
    """A review record on main for each review finding on a batch's pull request: review 1, one Important fix-now
    finding on an in-batch item of the batch."""
    prs = step.context["given"].get("pull request", {})
    for found in step.context["given"].get("review finding", {}).values():
        batch = prs.get(found.get("pull request"), {}).get("batch")
        if batch is None:
            continue
        name = T.batch_name(step, batch)
        item = next(i for i, f in step.context["given"]["item"].items() if f["batch"] == batch)
        head = T.git(step, "rev-parse", name).strip()
        rng = "%s..%s" % (T.plan_field(step, batch, "forked_from"), head)
        review = batch_findings.Review(
            1, name, "review/ex.com/prod/ctx/%s/review-1" % name, step.context["prs"][found["pull request"]], head,
            rng, "fix-now", "One finding.",
            [batch_findings.Finding("f1", "Important", "fix now", "a fault", B.ident(item), "src/x.txt:1",
                                    "The line says one thing; the code does another.")])
        path = step.repo / batch_findings.rel_of(name, 1)
        path.write_text(batch_findings.render(review), encoding="utf-8")
    W.init(step.repo)


@handler("WhenRuns", "`measure batch`")
def measure_batch(step):
    T.prepare(step)
    T.ensure_batch(step)
    write_reviews(step)
    run_measure(step, "batch", T.batch_name(step, step.names[-1]))


@local("ThenDoes", "measurement")
def writes_measurement(step):
    if not telemetry(step) or step.term != "write":
        return False
    ran = step.context["world"]
    assert ran.code == 0, ran.err
    assert ran.record().is_file() and ran.out.strip().startswith(MEASUREMENTS), (step.text, ran.out)


@local("ThenR", "measurement")
def measurement_of(step):
    if not telemetry(step) or step.term != "of":
        return False
    assert step.context["world"].figures()["batch"] == T.batch_name(step, step.names[1]), step.text


@local("ThenDoes", "review finding")
def includes_grade(step):
    if not telemetry(step) or step.term != "include":
        return False
    ran = step.context["world"]
    assert ran.code == 0, ran.err
    assert ran.figures()["findings_by_grade"]["Important"] >= 1, ran.figures()["findings_by_grade"]
    assert "Important" in ran.record().read_text(), step.text


@handler("WhenRuns", "`measure defect`")
def measure_defect(step):
    item = step.names[-1]
    batch = step.context.get("given", {}).get("item", {}).get(item, {}).get("batch", "b1")
    T.given(step, "batch", batch)["status"] = "merged"
    T.prepare(step)
    T.ensure_batch(step)
    run_measure(step, "defect", B.ident(item), "--says", "abandon leaves it started; run work abandon i1")


def defect_field(step, key):
    ran = step.context["world"]
    assert ran.code == 0, ran.err
    return W.field(ran.repo / ran.out.strip(), key)


@local("ThenDoes", "defect")
def writes_defect(step):
    if not telemetry(step) or step.term != "write":
        return False
    ran = step.context["world"]
    assert ran.code == 0, ran.err
    rel = ran.out.strip()
    assert (ran.repo / rel).is_file() and rel.startswith(".shop/batches/"), (step.text, rel)
    subject = T.git(step, "log", "-1", "--format=%s").strip()
    name = rel.rsplit("defect-", 1)[1].split(".")[0]
    assert subject.startswith("measure defect: ") and " d%s of " % name in subject, (step.text, subject)


@local("ThenR", "defect")
def defect_of_for(step):
    if not telemetry(step) or step.term not in ("of", "for"):
        return False
    if step.term == "of":
        assert defect_field(step, "item") == B.ident(step.names[1]), step.text
    else:
        assert defect_field(step, "batch") == T.batch_name(step, step.names[1]), step.text


@handler("WhenRuns", "`measure compare batch-2 batch-3`")
def measure_compare(step):
    """Two batches' measurements written from the script tests' complete figures (measure_batch_testing.FIGURES),
    then compared by name."""
    testing = shared("shop_measure_batch_testing", "../scripts/measure_batch_testing.py")
    B.index(step)
    for date, name, cost in (("2026-11-01", "batch-2", 1.0), ("2026-11-02", "batch-3", 2.0)):
        testing.write_measurement(step.repo, date, dict(testing.FIGURES, batch=name, cost=cost))
    W.init(step.repo)
    run_measure(step, "compare", "batch-2", "batch-3")
