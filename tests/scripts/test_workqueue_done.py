"""work-queue r23 with observation 2026-10-27-done-with-proposal-open: an initiative whose work-items are all green or
withdrawn is not done while one of its capability-proposals is neither formulated, withdrawn nor merged."""
import pathlib
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import workqueue_done

INDEX = "---\nid: bounded-context/ex.com/prod/ctx\nkind: bounded-context\n---\n"
INITIATIVE = "---\nid: initiative/ex.com/prod/ctx/i1\nkind: capability-change\nstatus: started\n---\n"
ITEM = "---\nid: work-item/ex.com/prod/ctx/w1\nkind: work-item\nstatus: green\n---\n"
PROPOSAL = "---\nid: capability-proposal/ex.com/prod/ctx/i1-thing\nkind: capability-proposal\nstatus: %s\n---\n"


@pytest.mark.parametrize("status, done", [("awaiting-answer", False), ("drafted", False), ("approved", False),
                                          ("formulated", True), ("withdrawn", True), ("merged", True)])
def test_an_open_proposal_keeps_the_initiative_from_done(tmp_path, status, done):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec/index.md").write_text(INDEX)
    directory = tmp_path / ".shop/work/i1"
    directory.mkdir(parents=True)
    (directory / "initiative.md").write_text(INITIATIVE)
    (directory / "w1.md").write_text(ITEM)
    (directory / "thing.md").write_text(PROPOSAL % status)
    assert workqueue_done.holds(tmp_path, directory, "initiative/ex.com/prod/ctx/i1") is done
