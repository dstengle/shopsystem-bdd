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
    """True in a scenario of features/telemetry.feature."""
    node = step.request.node
    scenario = getattr(getattr(node, "obj", None), "__scenario__", None)
    return scenario is not None and Path(scenario.feature.filename).name == "telemetry.feature"


@handler("GivenK", "review finding")
def given_review_finding(step):
    T.given(step, "review finding", step.names[0])


@local("GivenK_A", "review finding")
def review_finding_grade(step):
    if not telemetry(step):
        return False
    T.given(step, "review finding", step.names[0])["grade"] = step.values[0].strip("`")
    return None


@local("GivenDoes")
def given_link(step):
    """`the review finding r1 is on the pull request p1`, `the batch b1 has the pull request p1`, `the batch b1 holds
    the item i1`; a batch's role, which the measurement's sessions give, records nothing."""
    if not telemetry(step) or step.term not in ("on", "has", "holds"):
        return False
    one, other = step.names
    if step.term == "on":
        T.given(step, "review finding", one)["pull request"] = other
    elif step.nps[0].startswith("the pull request"):
        T.given(step, "pull request", other)["batch"] = one
    elif step.term == "holds":
        T.given(step, "item", other)["batch"] = one
    return None


def write_reviews(step):
    """A review record on main for each batch's pull request with review findings on it, one finding of each, in
    their grades, on an in-batch item of the batch."""
    prs = step.context["given"].get("pull request", {})
    findings = {}
    for name, found in sorted(step.context["given"].get("review finding", {}).items()):
        findings.setdefault(found.get("pull request"), []).append((name, found.get("grade", "Important")))
    for pr, found in findings.items():
        batch = prs.get(pr, {}).get("batch")
        if batch is None:
            continue
        name = T.batch_name(step, batch)
        item = next(i for i, f in step.context["given"]["item"].items() if f["batch"] == batch)
        head = T.git(step, "rev-parse", name).strip()
        rng = "%s..%s" % (T.plan_field(step, batch, "forked_from"), head)
        review = batch_findings.Review(
            1, name, "review/ex.com/prod/ctx/%s/review-1" % name, step.context["prs"][pr], head, rng, "fix-now",
            "Findings.", [batch_findings.Finding("f%d" % k, grade, "fix now", "a fault", B.ident(item), "src/x.txt:1",
                                                 "The line says one thing; the code does another.")
                          for k, (_, grade) in enumerate(found, 1)])
        path = step.repo / batch_findings.rel_of(name, 1)
        path.write_text(batch_findings.render(review), encoding="utf-8")
    W.init(step.repo)


@handler("WhenRuns", "`measure batch`")
def measure_batch(step):
    for pr in step.context.get("given", {}).get("pull request", {}).values():
        batch = pr.get("batch")
        if batch and not any(f.get("batch") == batch for f in step.context["given"].get("item", {}).values()):
            T.given(step, "item", "i1")["batch"] = batch
            B.write_item(step, "i1")
    T.prepare(step)
    T.ensure_batch(step)
    write_reviews(step)
    run_measure(step, "batch", T.batch_name(step, step.names[-1]))


@handler("WhenRuns", "`measure defect`")
def measure_defect(step):
    item = step.names[-1]
    batch = step.context.get("given", {}).get("item", {}).get(item, {}).get("batch", "b1")
    T.given(step, "batch", batch)["status"] = "merged"
    T.prepare(step)
    T.ensure_batch(step)
    run_measure(step, "defect", B.ident(item), "--says", "abandon leaves it started; run work abandon i1")


@local("WhenRuns")
def measure_compare(step):
    """`measure compare` in telemetry (batch-measurement's compares measurement files): Each batch the Whens name given a measurement from the script tests' complete figures
    (measure_batch_testing.FIGURES), then the batches compared by name."""
    if not telemetry(step) or step.command != "`measure compare`":
        return False
    testing = shared("shop_measure_batch_testing", "../scripts/measure_batch_testing.py")
    names = step.context.setdefault("compared", [])
    names += [T.batch_name(step, n) for n in step.names]
    if not (step.repo / "spec" / "index.md").is_file():
        B.index(step)
    for k, name in enumerate(names, 1):
        testing.write_measurement(step.repo, "2026-11-0%d" % k, dict(testing.FIGURES, batch=name, cost=float(k)))
    W.init(step.repo)
    run_measure(step, "compare", *(names * 2 if len(names) == 1 else names))
    return None
