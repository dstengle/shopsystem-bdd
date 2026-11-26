"""batch_broken (b696, batches r149): the task a batch's refused submit is to be fixed by, the task whose item's
scenario a failed test of the kept whole-suite run is, else one whose reached tests hold it, else none (b703); and
whether a fix of it exists (b713)."""
import subprocess

import batch_broken
import batch_rerun
from batch_plan import Batch, Task

FEATURE = """Feature: work queue

  @g4 @r5
  Scenario: Shelving a note
    Given a note n1

  @g5 @r6
  Scenario: The item's own line, 2nd
    Given a note n1
"""


def batch():
    tasks = [Task("t%d" % k, "b%d" % k, "done", "batch-1-b%d" % k) for k in (1, 2)]
    return Batch("batch-1", "batch/x/batch-1", "building", "main", "abc", "batch-1", None, tasks)


def test_a_scenario_is_its_test_function():
    assert batch_broken.test_name("The item's own line, 2nd") == "test_the_items_own_line_2nd"
    assert batch_broken.scenarios(FEATURE, "r6") == ["The item's own line, 2nd"]
    assert batch_broken.scenarios(FEATURE, "r7") == []


def picked(monkeypatch, failed, scenarios=None, reached=()):
    b = batch()
    monkeypatch.setattr(batch_broken, "failed", lambda root, batch: failed)
    monkeypatch.setattr(batch_broken, "_ids", lambda root, task: ["work-queue#r%d" % (4 + int(task.task[1]))])
    monkeypatch.setattr(batch_broken, "_scenario_tests", lambda root, batch, ids: (scenarios or {}).get(ids[0], set()))
    monkeypatch.setattr(batch_broken, "_reached", lambda root, batch, task, ids, path: (task.task, path) in reached)
    found = batch_broken.task_of("root", b, b.tasks)
    return found.task if found else None


def test_the_task_of_the_item_whose_scenario_broke(monkeypatch):
    test = "tests/scenarios/test_work_queue.py::test_the_items_own_line_2nd"
    scenarios = {"work-queue#r6": {("tests/scenarios/test_work_queue.py", "test_the_items_own_line_2nd")}}
    assert picked(monkeypatch, [test + "[x]"], scenarios) == "t2"


def test_else_a_task_whose_change_reaches_the_test(monkeypatch):
    reached = {("t2", "tests/scripts/test_x.py")}
    assert picked(monkeypatch, ["tests/scripts/test_x.py::test_y"], reached=reached) == "t2"


def test_else_none_and_none_with_nothing_kept(monkeypatch):
    assert picked(monkeypatch, ["tests/scripts/test_x.py::test_y"]) is None
    assert picked(monkeypatch, []) is None


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def test_a_commit_on_a_task_branch_since_the_submit_is_a_fix(tmp_path):
    """A fix (b713): with the failed run kept, a task branch that moved past its head at the submit."""
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@x", "commit", "-q", "--allow-empty", "-m", "base")
    b = batch()
    for task in b.tasks:
        _git(tmp_path, "branch", task.branch)
    batch_broken.submitted(tmp_path, b, b.tasks)
    assert not batch_broken.fixed(tmp_path, b, b.tasks)        # no failed run kept
    batch_rerun.keep(tmp_path, b.name, ["tests/scripts/test_x.py::test_y"])
    assert not batch_broken.fixed(tmp_path, b, b.tasks)        # no commit since the submit
    _git(tmp_path, "checkout", "-q", "batch-1-b2")
    _git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@x", "commit", "-q", "--allow-empty", "-m", "fix")
    assert batch_broken.fixed(tmp_path, b, b.tasks)
