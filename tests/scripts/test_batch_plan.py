"""The batch file `.shop/batches/<n>/plan.md` (workflow simplification plan 4, Task 1, D4): read and written
byte-stable, a malformed file refused naming the file and the field, and the batches found by name, by status and by
item."""
import batch_plan
import pytest
from backlog_testing import git
from batch_plan import Batch, Task
from workqueue import Refused

ONE = """---
id: batch/ex.com/prod/ctx/batch-1
kind: batch
status: building
base: main
forked_from: 3be6b387e1c0ffee
branch: batch-1
pull_request:
---

# batch-1

## Tasks

| task | item | status | branch |
|---|---|---|---|
| t1 | b3 | pending | batch-1-b3 |

## Plan

One task for each item: each builds its item's requirement lines, whose generated scenarios are its acceptance tests.
"""


def batch(name="batch-1", status="building", tasks=None, plan="Line one.\nLine two.", pull_request=None):
    tasks = tasks if tasks is not None else [Task("t1", "b3", "pending", "%s-b3" % name),
                                             Task("t2", "b4", "running", "%s-b4" % name)]
    return Batch(name=name, ident="batch/ex.com/prod/ctx/%s" % name, status=status, base="main",
                 forked_from="3be6b387e1c0ffee", branch=name, pull_request=pull_request, tasks=tasks, plan=plan)


def test_render_round_trips():
    b = batch(pull_request="https://github.com/ex/ctx/pull/1")
    assert batch_plan.parse(batch_plan.render(b), "x") == b
    one = batch(tasks=[Task("t1", "b3", "pending", "batch-1-b3")], plan=batch_plan.PLAN)
    assert batch_plan.render(one) == ONE
    assert batch_plan.parse(ONE, "x") == one


@pytest.mark.parametrize("edit, field", [
    (("kind: batch", "kind: item"), "kind"),
    (("status: building", "status: sleeping"), "status"),
    (("| t1 | b3 | pending |", "| t1 | b3 | asleep |"), "tasks"),
    (("| t1 | b3 | pending | batch-1-b3 |", "| t1 | b3 | pending |"), "tasks"),
    (("| t1 | b3 | pending | batch-1-b3 |", "| t1 | b3 | pending | batch-1-b3 |\n| t1 | b4 | pending | batch-1-b4 |"),
     "tasks"),
    (("# batch-1\n", ""), "title"),
])
def test_malformed_plans_are_refused(edit, field):
    text = ONE.replace(*edit)
    assert text != ONE
    with pytest.raises(Refused) as refused:
        batch_plan.parse(text, ".shop/batches/1/plan.md")
    assert str(refused.value).startswith(".shop/batches/1/plan.md: %s" % field), str(refused.value)


def write(root, b):
    path = root / batch_plan.rel_of(b.name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(batch_plan.render(b))


def test_next_name_open_batch_and_of_item(tmp_path):
    assert batch_plan.next_name(tmp_path) == "batch-1" and batch_plan.open_batch(tmp_path) is None
    write(tmp_path, batch("batch-1", "merged", [Task("t1", "b3", "done", "batch-1-b3")]))
    write(tmp_path, batch("batch-2", "building", [Task("t1", "b3", "pending", "batch-2-b3")]))
    assert batch_plan.names(tmp_path) == ["batch-1", "batch-2"]
    assert batch_plan.next_name(tmp_path) == "batch-3"
    assert batch_plan.open_batch(tmp_path).name == "batch-2"
    assert batch_plan.of_item(tmp_path, "b3").name == "batch-2"
    assert batch_plan.of_item(tmp_path, "b7") is None
    assert batch_plan.task(batch_plan.find(tmp_path, "batch-2"), "t1").item == "b3"
    with pytest.raises(Refused, match="batch-2 has no task t9"):
        batch_plan.task(batch_plan.find(tmp_path, "batch-2"), "t9")
    with pytest.raises(Refused, match=r"there is no batch batch-9 in \.shop/batches/"):
        batch_plan.find(tmp_path, "batch-9")


def test_a_file_not_named_by_number_is_refused(tmp_path):
    path = tmp_path / ".shop/batches/x/plan.md"
    path.parent.mkdir(parents=True)
    path.write_text(ONE)
    with pytest.raises(Refused, match=r"\.shop/batches/x/plan\.md"):
        batch_plan.names(tmp_path)


def test_on_base_refuses_another_branch(backlog_repo):
    git(backlog_repo, "checkout", "-q", "-b", "elsewhere")
    with pytest.raises(Refused) as refused:
        batch_plan.on_base(backlog_repo, batch())
    assert "batch-1 is built from main; run it on main, not elsewhere" in str(refused.value)
    git(backlog_repo, "checkout", "-q", "main")
    batch_plan.on_base(backlog_repo, batch())
