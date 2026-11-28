"""An item applied again to a task's workspace (batch_relay; batches r198, r204, b889): an item with two blockers in
the batch, its task's workspace holding every blocker's lines beside its own after an amend of a blocker and after an
amend of its own."""
import re

import backlog_items
import batch_plan
import batch_relay
import pytest
from backlog_testing import git, work
from batch_testing import ready_item
from test_backlog_lines import ABANDON
from test_batch_pick import SECOND, THIRD

import toolchain

CAP = "spec/capabilities/work-queue.md"
OTHER = "While an initiative is `abandoned`, when the person runs `work abandon` on the initiative, `work` shall print the initiative."

TIDY = "While an initiative is `started`, when the person runs `work tidy` on the initiative, `work` shall exit successfully."


@pytest.fixture
def opened(batch_repo):
    """b1 and b2 ready, b3 ready depending on both, all picked into batch-1."""
    toolchain.require()
    ready_item(batch_repo, "b1", "Abandon", ABANDON, value="high-value", urgency="high-urgency", size="small")
    ready_item(batch_repo, "b2", "Exit", SECOND, value="high-value", urgency="high-urgency", size="small")
    ready_item(batch_repo, "b3", "Again", THIRD, depends_on="b1, b2")
    done = work(batch_repo, "batch", "start")
    assert done.returncode == 0, done.stderr
    assert [t.item for t in batch_plan.find(batch_repo, "batch-1").tasks] == ["b1", "b2", "b3"], done.stdout
    return batch_repo


def _lines(repo, name):
    item = backlog_items.find(repo, name)
    return re.findall(r"(?m)^- \[r\d+\] (.*)$", item.sections["Requirements"])


def test_blockers_and_dependents_are_the_batch_items_depended_on_directly_or_not(opened):
    batch = batch_plan.find(opened, "batch-1")
    b3 = backlog_items.find(opened, "b3")
    assert [i.name for i in batch_relay.blockers(opened, batch, b3)] == ["b1", "b2"]
    assert [i.name for i in batch_relay.dependents(opened, batch, backlog_items.find(opened, "b2"))] == ["b3"]
    assert batch_relay.dependents(opened, batch, b3) == []


def test_a_dependent_keeps_every_blockers_lines_through_amends(opened):
    assert work(opened, "line", "b1", "--reword", "work-queue#r5", OTHER).returncode == 0
    done = work(opened, "batch", "amend", "b1")
    assert done.returncode == 0, done.stderr
    assert "batch-1-b3" in done.stdout.splitlines()[0], done.stdout
    task = git(opened, "show", "batch-1-b3:%s" % CAP)
    for text in _lines(opened, "b1") + _lines(opened, "b2") + _lines(opened, "b3"):
        assert text in task, (text, task)
    assert ABANDON not in task, task
    body = git(opened, "log", "-1", "--format=%B", "batch-1-b3")
    assert "Item: b3" in body and "Item: b1" in body, body
    rid = re.search(r"(?m)^- \[(r\d+)\] ", backlog_items.find(opened, "b3").sections["Requirements"]).group(1)
    reworded = work(opened, "line", "b3", "--reword", "work-queue#%s" % rid, TIDY)
    assert reworded.returncode == 0, reworded.stderr
    done = work(opened, "batch", "amend", "b3")
    assert done.returncode == 0, done.stderr
    task = git(opened, "show", "batch-1-b3:%s" % CAP)
    for text in _lines(opened, "b1") + _lines(opened, "b2") + _lines(opened, "b3"):
        assert text in task, (text, task)
