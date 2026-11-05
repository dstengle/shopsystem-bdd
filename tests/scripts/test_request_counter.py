"""A request whose counter-proposal is settled closes (workflow simplification plan 4, Task 8, D24): `work outcome ...
rewritten --line` writes `<n>. <m>` under `## Counter-proposals`, and the turn rule, written once in request_text,
reads line n as no longer proposed; a request without the section turns as before."""
import pathlib
import re
import shutil
import sys

import pytest
import request_moves
import request_text
from backlog_testing import REPO, git, work, write_request
from request_testing import hosted
from test_backlog_lines import ABANDON
from test_intake_outcome import ASKED, request
from test_request_asker import repo  # noqa: F401  (the fixture)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain


@pytest.fixture
def taken(ready_repo):
    toolchain.require()
    write_request(ready_repo, "q1", lines=(ASKED,))
    return ready_repo


def test_a_counter_proposed_request_closes(taken):
    done = work(taken, "outcome", "q1", "1", "rewritten", "--line", ABANDON)
    assert done.returncode == 0, done.stderr
    text = request(taken)
    assert request_text.entries(text, "Lines") == ["1. %s" % ASKED, "2. %s" % ABANDON]
    assert request_text.entries(text, "Counter-proposals") == ["1. 2"]
    assert (request_text.field(text, "status"), request_text.field(text, "turn")) == ("awaiting-asker", "asker")
    assert work(taken, "turn", "q1").returncode == 0
    assert request_text.field(request(taken), "turn") == "upstream"
    done = work(taken, "outcome", "q1", "2", "accepted", "--into", "work-queue")
    assert done.returncode == 0, done.stderr
    assert work(taken, "turn", "q1").returncode == 0      # settled, one accepted: the turn stays, for the person
    text = request(taken)
    assert (request_text.field(text, "status"), request_text.field(text, "turn")) == ("awaiting-upstream", "upstream")
    done = work(taken, "accept", "q1")
    assert done.returncode == 0, done.stderr
    text = request(taken)
    assert (request_text.field(text, "status"), request_text.field(text, "turn")) == ("accepted", "upstream")


def old_turn(text):
    """The turn's edit before plan 4 (request_moves.turn at 3be6b387), kept here as it was written."""
    field, _with_field, _entries, SETTLED = (request_text.field, request_text.with_field, request_text.entries,
                                             request_text.SETTLED)
    if field(text, "turn") == "asker":
        return _with_field(_with_field(text, "status", "awaiting-upstream"), "turn", "upstream")
    words = [e.split(". ", 1)[1] for e in _entries(text, "Outcomes") if ". " in e]
    if len(words) == len(_entries(text, "Lines")) and all(w in SETTLED for w in words):
        if field(text, "status") != "delivered":
            text = _with_field(text, "status", "accepted" if "accepted" in words else "refused")
            if "accepted" in words:
                return text
    else:
        text = _with_field(text, "status", "awaiting-asker")
    return _with_field(text, "turn", "asker")


@pytest.mark.parametrize("outcomes, turn", [(("rewritten",), "upstream"), (("refused",), "upstream"),
                                            ((), "asker")])
def test_without_the_section_turn_is_as_before(ready_repo, outcomes, turn):
    lines = (ABANDON, ASKED)[:max(1, len(outcomes))]
    path = write_request(ready_repo, "q1", lines=lines, outcomes=outcomes, turn=turn)
    copy = pathlib.Path(str(path) + ".copy")
    shutil.copyfile(path, copy)
    assert work(ready_repo, "turn", "q1").returncode == 0
    assert path.read_text() == old_turn(copy.read_text())
    if outcomes == ("rewritten",):
        assert request_text.field(path.read_text(), "status") == "awaiting-asker"


@pytest.mark.parametrize("outcomes", [("accepted",), ("refused", "accepted")])
def test_an_upstream_turn_with_a_line_accepted_keeps_the_turn_and_the_status(ready_repo, outcomes):
    """requests r36: `accepted` is the person's, by `work accept`; the turn only waits for it."""
    path = write_request(ready_repo, "q1", lines=(ABANDON, ASKED)[:len(outcomes)], outcomes=outcomes)
    before = path.read_text()
    assert work(ready_repo, "turn", "q1").returncode == 0
    assert path.read_text() == before


def test_the_rewritten_path_and_turn_share_one_rule():
    assert '"awaiting-asker"' not in (REPO / "scripts" / "intake_moves.py").read_text()
    assert re.search(r"\bturned\(", (REPO / "scripts" / "intake_moves.py").read_text())


def test_model_check_takes_the_section(taken):
    assert work(taken, "outcome", "q1", "1", "rewritten", "--line", ABANDON).returncode == 0
    import subprocess
    done = subprocess.run([sys.executable, str(REPO / "scripts" / "model"), "--root", str(taken), "check"],
                          capture_output=True, text=True)
    assert done.returncode != 2, done.stderr
    assert not [line for line in done.stdout.splitlines() if "q1.md" in line], done.stdout
    git(taken, "status", "--porcelain")


def test_a_new_request_is_numbered_above_the_frozen_ones(repo, monkeypatch):  # noqa: F811  (the fixture above)
    """Plan 9, D7: a live request is `.shop/requests/q<n>.md`, its number one above the highest of `.shop/requests/`
    and the frozen `.shop/work/requests/`."""
    for rel in (".shop/work/requests/q7.md", ".shop/requests/q2.md"):
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text("---\nkind: request\nstatus: delivered\n---\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "requests")
    hosted(repo, repo.parent / (repo.name + "-gh"), monkeypatch=monkeypatch)
    name, _ = request_moves.request(repo, "t", "internal", None, ["observation/o1"], None)
    assert name == "q8"
    assert (repo / ".shop/requests/q8.md").is_file()
    assert not (repo / ".shop/work/requests/q8.md").exists()
