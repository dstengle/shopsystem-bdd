"""The pick of `work batch start` (workflow simplification plan 4, Task 2, D7, D8): ready items in rank order up to
`batch_size`, a blocked item passed over unless what blocks it is picked first, the bar checked again alone and laid
with the items picked before, ids renumbered, and nothing written."""
import pathlib
import sys

import backlog_items
import batch_pick
import pytest
from backlog_testing import git, state, write_item
from batch_testing import ready_item
from test_backlog_lines import ABANDON, FROBNICATE

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

SECOND = "While an initiative is `started`, when the person runs `work abandon` on the initiative, `work` shall exit successfully."
CLASH = ("While an initiative is `started`, when the person runs `work abandon` on the initiative, `work` shall set the status of the initiative to "
         "`done`.")


@pytest.fixture
def repo(ready_repo):
    toolchain.require()
    return ready_repo


def size(repo, n):
    (repo / ".shop").mkdir(exist_ok=True)
    (repo / ".shop" / "delivery.toml").write_text("batch_size = %d\n" % n)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "size")


def names(found):
    return [i.name for i in found]


def test_pick_takes_ready_items_in_rank_order_up_to_the_size(repo):
    ratings = {"b1": ("high-value", "medium-urgency"), "b2": ("low-value", "medium-urgency"),
               "b3": ("high-value", "high-urgency"), "b4": ("low-value", "low-urgency"),
               "b5": ("medium-value", "medium-urgency")}
    for name, (value, urgency) in ratings.items():
        ready_item(repo, name, "Item %s" % name, ABANDON if name in ("b3", "b5") else SECOND, value=value,
                   urgency=urgency, size="small")
    size(repo, 3)
    found = batch_pick.pick(repo)
    assert names(found.picked) == ["b3", "b1", "b5"], (found.returned, found.left_out)
    ids = [i.sections["Requirements"].split("- [")[1].split("]")[0] for i in found.picked]
    assert len(set(ids)) == 3, ids
    note = found.picked[1].sections["Notes"]
    assert note.startswith("renumbered by work batch start: ") and "work-queue#r5 -> work-queue#r6" in note


def test_pick_returns_an_item_that_no_longer_passes(repo):
    ready_item(repo, "b1", "Frobnicate", FROBNICATE, value="high-value", urgency="high-urgency", size="small")
    ready_item(repo, "b2", "Abandon", ABANDON)
    found = batch_pick.pick(repo)
    assert names(found.picked) == ["b2"]
    (item, reasons), = found.returned
    assert item.name == "b1" and item.status == "shaped" and "frobnicate" in " ".join(reasons)
    assert "work batch start" in item.sections["Notes"] and "frobnicate" in item.sections["Notes"]


def test_a_blocked_item_is_not_picked(repo):
    write_item(repo, "b9", title="Later")
    ready_item(repo, "b2", "Abandon", ABANDON, depends_on="b9")
    found = batch_pick.pick(repo)
    assert found == batch_pick.Pick([], [], [])
    assert backlog_items.find(repo, "b2").status == "ready"


def test_a_dependency_in_the_same_pick_does_not_block(repo):
    ready_item(repo, "b1", "First", ABANDON, value="high-value", urgency="high-urgency", size="small", depends_on="b2")
    ready_item(repo, "b2", "Second", SECOND)
    assert names(batch_pick.pick(repo).picked) == ["b2", "b1"]


def test_a_dependency_fills_the_size_first(repo):
    ready_item(repo, "b1", "First", ABANDON, value="high-value", urgency="high-urgency", size="small", depends_on="b2")
    ready_item(repo, "b2", "Second", SECOND)
    size(repo, 1)
    found = batch_pick.pick(repo)
    assert names(found.picked) == ["b2"] and found.returned == [] and found.left_out == []


def test_an_item_that_clashes_with_one_picked_is_left_out(repo):
    ready_item(repo, "b1", "Abandon", ABANDON, value="high-value", urgency="high-urgency", size="small")
    ready_item(repo, "b2", "Clash", CLASH)
    found = batch_pick.pick(repo)
    assert names(found.picked) == ["b1"]
    (item, reasons), = found.left_out
    assert item.name == "b2" and item.status == "ready"
    assert any(r.startswith("L1 ") and "work-queue#r5" in r and "r6" in r for r in reasons), reasons


def test_pick_writes_nothing(repo):
    ready_item(repo, "b1", "Frobnicate", FROBNICATE)
    ready_item(repo, "b2", "Abandon", ABANDON)
    ready_item(repo, "b3", "Second", SECOND)
    before = state(repo)
    batch_pick.pick(repo)
    assert state(repo) == before
