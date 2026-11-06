"""Handlers of features/batches.feature (workflow simplification plan 4): `work batch` run on the batches, tasks,
commits and pull requests batches_world.py builds, over the items backlog_world.py writes and the spec
readiness_world.py writes, and what the run wrote, committed, printed, pushed and gave gh read back.

A step whose key another capability claims (`ThenDoes` with `write`, `ThenPrints` with `` `work` ``, `ThenR` with
`of`) is taken through work_queue_world's `local` table by its kind, so test_batches.py binds with `bind_all`; a
local chained over the backlog's (`ThenPrints item`, `ThenR question`) returns False for a run that is not a batch
command's."""
import importlib.util
import sys
from pathlib import Path

from vocab import handler


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
R = shared("shop_readiness_world", "readiness_world.py")
T = shared("shop_batches_world", "batches_world.py")
local, bare = W.local, B.bare
TASK_STATUSES = ("pending", "running", "done", "failed")


@handler("WhenRuns", "`work batch start`")
def batch_start(step):
    T.before_start(step)
    T.prepare(step)
    step.context["strict_not"] = True
    T.run_batch(step, "start")


@handler("WhenRuns", "`work batch status`")
def batch_status(step):
    T.prepare(step)
    T.ensure_batch(step)
    T.run_batch(step, "status", T.batch_name(step, step.names[-1]))


@handler("GivenK", "batch")
def given_batch(step):
    T.given(step, "batch", step.names[0])


@handler("GivenK_A", "batch")
def given_batch_is(step):
    status = bare(step.values[0])
    if " is not " in step.text:
        status = next(s for s in ("building", "in-review", "abandoned") if s != status)
    T.given(step, "batch", step.names[0])["status"] = status


@handler("GivenK", "task")
def given_task(step):
    T.given(step, "task", step.names[0])


@handler("GivenK_A", "task")
def given_task_is(step):
    status = bare(step.values[0])
    if " is not " in step.text:
        status = next(s for s in TASK_STATUSES if s != status)
    T.given(step, "task", step.names[0])["status"] = status


@handler("GivenR", "in")
def given_in_batch(step):
    item, batch = step.names
    T.given(step, "batch", batch)
    T.given(step, "item", item)["batch"] = batch
    if not B.item_rel(step.context, item):
        B.write_item(step, item)
    if T.status_of(step, item) == "idea":
        B.write_item(step, item, status="in-batch")


def task_of_batch(step):
    task, batch = step.names
    T.given(step, "batch", batch)
    T.given(step, "task", task)["batch"] = batch


B.OF_GIVENS["task"] = task_of_batch


@handler("ThenK_A", "batch")
def batch_is(step):
    """The batch's plan has the status (or has another); a negated Then requires the command to have exited 0
    (D21)."""
    got, wanted = T.plan_field(step, step.names[0], "status"), bare(step.values[0])
    done = step.context.get("result")
    if " is not " in step.text:
        assert done is not None and done.returncode == 0, (step.text, done and done.stderr)
        assert got is not None and got != wanted, (step.text, got)
    else:
        assert got == wanted, (step.text, got)


def plan_written(step):
    """The plan file the last run made and committed; its batch's name."""
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    made = [rel for rel in B.changed(step) if rel.startswith(".shop/batches/") and rel.endswith("/plan.md")]
    assert made, (step.text, B.changed(step))
    B.in_commits(step, made[0])
    return "batch-%s" % made[0].split("/")[2]


@local("ThenDoes", "batch")
def writes_batch(step):
    if step.term != "write":
        return False
    step.context.setdefault("batches", {})[step.names[0]] = plan_written(step)


@local("ThenDoes", "batch plan")
def writes_plan(step):
    if step.term != "write":
        return False
    step.context.setdefault("plans", {})[step.names[0]] = plan_written(step)


def batch_run(step):
    """The last run, when it was a `work batch` command."""
    runs = W.runs(step)
    return step.context["result"] if runs and runs[-1]["args"][1:2] == ["batch"] else None


@local("ThenPrints", "item")
def prints_item(step):
    done = batch_run(step)
    if done is None:
        return False
    assert done.returncode == 0, done.stderr
    assert "  %s " % step.context["says"][step.names[0]] in done.stdout, (step.text, done.stdout)


@local("ThenPrints", "task")
def prints_task(step):
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    name = step.names[0]
    found = step.context["given"]["task"][name]
    line = next((x for x in done.stdout.splitlines()
                 if x.strip().startswith("%s %s" % (T.task_id(step, name), B.ident(found["item"])))), None)
    assert line is not None, (step.text, done.stdout)
    if step.nps[0].startswith("the status of "):
        status, _ = T.task_row(step, name)
        assert ": %s," % status in line, (step.text, status, line)


def refused_quietly(step):
    """The run was refused (exit 1, not a usage error), pushed nothing and called no gh; its stderr."""
    done = step.context["result"]
    assert done.returncode == 1, (done.returncode, done.stdout, done.stderr)
    assert not T.git(step, "ls-remote", "origin", "refs/heads/batch-*").strip(), "a branch was pushed"
    assert T.gh_calls(step) == [], T.gh_calls(step)
    return done.stderr


@local("ThenExitsErr", "task")
def refused_naming_task(step):
    if batch_run(step) is None:
        return False
    said = refused_quietly(step)
    found = step.context["given"]["task"][step.names[0]]
    assert "%s %s" % (T.task_id(step, step.names[0]), step.context["says"][found["item"]]) in said, (step.text, said)


@local("ThenExitsErr", "commit")
def refused_naming_commit(step):
    said = refused_quietly(step)
    sha = step.context["commits"][step.names[0]]
    assert sha[:7] in said, (step.text, sha, said)


@local("ThenPrints", "batch brief")
def prints_brief(step):
    """The path of the batch brief the run wrote (bound by the Then that it writes it), printed whole."""
    done = batch_run(step)
    if done is None:
        return False
    assert done.returncode == 0, done.stderr
    rel = W.node_rel(step.context, step.names[0])
    assert rel, (step.text, "no batch brief was written")
    assert str(step.repo.resolve() / rel) in done.stdout.split(), (step.text, rel, done.stdout)
