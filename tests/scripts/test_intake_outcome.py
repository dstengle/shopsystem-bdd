"""intake r2-r4 (workflow simplification plan 3, Task 4, D12, D13): `work outcome` on a request an item was taken in
from accepts a line into the item, refuses it with a reason, or counter-proposes a line and passes the turn to the
asker; on a request no item was taken in from, given none of the new options, it is the old `work outcome`."""
import pathlib
import shutil
import subprocess
import sys

import backlog_items
import backlog_lines
import pytest
import readiness_bar
import workqueue_request
from backlog_testing import REPO, git, state, work, write_request
from test_backlog_lines import ABANDON, FROBNICATE

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

# A peer's line no transition allows (a `proposed` initiative abandoned), and the counter-proposal that fixes it.
ASKED = ("When the person runs `work abandon` on an initiative that is `proposed`, `work` shall set its status to "
         "`abandoned`.")
COUNTER = ABANDON


@pytest.fixture
def taken(ready_repo):
    toolchain.require()
    write_request(ready_repo, "q1", lines=(ABANDON,))
    assert work(ready_repo, "intake", "q1").returncode == 0
    return ready_repo


def request(repo, name="q1"):
    return (repo / ".shop" / "work" / "requests" / ("%s.md" % name)).read_text()


def entries(text, section):
    return workqueue_request._entries(text, section)


def committed(repo):
    return sorted(git(repo, "show", "--name-only", "--format=", "HEAD").split())


BOTH = [".shop/backlog/b1.md", ".shop/work/requests/q1.md"]


def test_accepted_writes_the_line_into_the_item(taken):
    done = work(taken, "outcome", "q1", "1", "accepted", "--into", "work-queue")
    assert done.returncode == 0, done.stderr
    assert entries(request(taken), "Outcomes") == ["1. accepted"]
    item = backlog_items.find(taken, "b1")
    blocks = backlog_lines.read(item, "b1")
    assert [(g.id, g.requirements) for b in blocks for g in b.groups] == [("g4", [("r5", ABANDON)])]
    assert item.sections["Notes"].splitlines()[-1] == "line 1 of request q1 accepted into work-queue#r5"
    assert committed(taken) == BOTH
    assert git(taken, "log", "-1", "--format=%s").strip() == 'work outcome: q1 line 1 accepted -> b1 "Archive old items"'
    done = work(taken, "ready", "b1")
    assert done.returncode == 0, done.stderr


def test_accepted_without_into_is_refused(taken):
    before = state(taken)
    done = work(taken, "outcome", "q1", "1", "accepted")
    assert done.returncode == 1 and "--into" in done.stderr, done.stderr
    assert state(taken) == before


def test_refused_writes_the_reason(taken):
    before = state(taken)
    done = work(taken, "outcome", "q1", "1", "refused")
    assert done.returncode == 1 and "--reason" in done.stderr, done.stderr
    assert state(taken) == before
    done = work(taken, "outcome", "q1", "1", "refused", "--reason", "out of scope")
    assert done.returncode == 0, done.stderr
    text = request(taken)
    assert entries(text, "Outcomes") == ["1. refused"] and entries(text, "Reasons") == ["1. out of scope"]
    assert backlog_items.find(taken, "b1").sections["Notes"].splitlines()[-1] == (
        "line 1 of request q1 refused: out of scope")
    assert committed(taken) == BOTH


def test_rewritten_with_a_line_passes_the_turn(ready_repo):
    toolchain.require()
    write_request(ready_repo, "q2", lines=(ASKED,))
    done = work(ready_repo, "outcome", "q2", "1", "rewritten", "--line", COUNTER)
    assert done.returncode == 0, done.stderr
    text = request(ready_repo, "q2")
    assert entries(text, "Lines") == ["1. %s" % ASKED, "2. %s" % COUNTER]
    assert entries(text, "Outcomes") == ["1. rewritten"]
    assert entries(text, "Reasons") == ["1. rewritten as line 2"]
    assert (workqueue_request.field(text, "status"), workqueue_request.field(text, "turn")) == ("awaiting-asker",
                                                                                               "asker")
    assert committed(ready_repo) == [".shop/work/requests/q2.md"]


def test_a_counter_proposal_that_does_not_parse_is_refused(taken):
    before = state(taken)
    done = work(taken, "outcome", "q1", "1", "rewritten", "--line", FROBNICATE)
    assert done.returncode == 1 and "parsed up to:" in done.stderr, done.stderr
    assert state(taken) == before


def test_line_only_with_rewritten_and_into_only_with_accepted(taken):
    before = state(taken)
    for args in (("accepted", "--into", "work-queue", "--line", COUNTER), ("refused", "--into", "work-queue",
                                                                          "--reason", "no"), ("9", "accepted",
                                                                                              "--into", "work-queue")):
        words = ("1",) + args if args[0] != "9" else args
        done = work(taken, "outcome", "q1", *words)
        assert done.returncode == 1, (args, done.stdout)
    assert state(taken) == before


def test_the_rewritten_line_is_not_the_items(taken):
    assert work(taken, "outcome", "q1", "1", "rewritten", "--line", COUNTER).returncode == 0
    assert work(taken, "turn", "q1").returncode == 0      # the asker passes the turn back
    done = work(taken, "outcome", "q1", "2", "accepted", "--into", "work-queue")
    assert done.returncode == 0, done.stderr
    item = backlog_items.find(taken, "b1")
    assert [n for n, _, _ in readiness_bar.request_lines(taken, item)] == [2]
    done = work(taken, "ready", "b1")
    assert done.returncode == 0, done.stderr


def test_the_asker_turn_still_refuses(ready_repo):
    write_request(ready_repo, "q1", lines=(ABANDON,), status="awaiting-asker", turn="asker")
    before = state(ready_repo)
    done = work(ready_repo, "outcome", "q1", "1", "refused", "--reason", "out of scope")
    assert done.returncode == 1 and "in the asker's turn" in done.stderr, done.stderr
    assert state(ready_repo) == before


def test_old_outcome_is_unchanged(ready_repo, tmp_path):
    write_request(ready_repo, "q2", lines=(ABANDON,))
    copy = tmp_path / "copy"
    shutil.copytree(ready_repo, copy)
    workqueue_request.outcome(copy, "q2", 1, "accepted")
    done = work(ready_repo, "outcome", "q2", "1", "accepted")
    assert done.returncode == 0 and done.stdout == "", done.stderr
    assert committed(ready_repo) == committed(copy)
    assert git(ready_repo, "log", "-1", "--format=%s") == git(copy, "log", "-1", "--format=%s")
    assert request(ready_repo, "q2") == request(copy, "q2")


def test_model_check_accepts_reasons(taken):
    assert work(taken, "outcome", "q1", "1", "refused", "--reason", "out of scope").returncode == 0
    done = subprocess.run([sys.executable, str(REPO / "scripts" / "model"), "check", "--root", str(taken)],
                          capture_output=True, text=True)
    assert "a section other than" not in done.stdout + done.stderr, done.stdout
