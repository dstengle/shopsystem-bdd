"""batch_next's pick (b683): one step, the first that applies in the order stop, review change, fix finding, park
item, finish task, build task, submit batch; and the step's lines."""
import batch_next
from batch_findings import Finding
from batch_plan import Batch, Task


def batch(status, *statuses):
    tasks = [Task("t%d" % k, "b%d" % k, s, "batch-1-b%d" % k) for k, s in enumerate(statuses, 1)]
    return Batch("batch-1", "batch/x/batch-1", status, "main", "abc", "batch-1", None, tasks)


FINDING = Finding("f1", "Important", "fix now", "a finding", "b1", "src/b1.txt", "body")


def picked(b, unfixed=()):
    instruction, task, finding = batch_next.pick(b, b.tasks, list(unfixed))
    return instruction, task.task if task else None, finding.fid if finding else None


def test_the_order():
    assert picked(batch("awaiting-merge", "pending")) == ("stop", None, None)
    assert picked(batch("merged")) == ("stop", None, None)
    assert picked(batch("in-review", "failed"), [FINDING]) == ("review change", None, None)
    assert picked(batch("building", "failed"), [FINDING]) == ("fix finding", None, "f1")
    assert picked(batch("building", "pending", "running", "failed")) == ("park item", "t3", None)
    assert picked(batch("building", "pending", "running")) == ("finish task", "t2", None)
    assert picked(batch("building", "done", "pending")) == ("prepare task", "t2", None)
    assert picked(batch("building", "done", "done")) == ("submit batch", None, None)


def test_a_batch_with_no_task_in_it_stops():
    assert picked(batch("building")) == ("stop", None, None)


def test_the_lines():
    b = batch("building", "running")
    instruction, task, finding = batch_next.pick(b, b.tasks, [])
    step = {"batch": "batch-1", "status": "building", "instruction": instruction,
            "task": batch_next._task(task), "batch brief": None, "review folder": None, "review finding": None,
            "report": batch_next.report(b, instruction, task, finding)}
    assert batch_next.text(step) == ("batch-1 building: finish task\ntask: t1 b1 (running), branch batch-1-b1\n"
                                     "report: shop work batch done batch-1 t1\n")
