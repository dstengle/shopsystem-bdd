"""`work outcome` (intake r7, requests r14, r38): the upstream's line outcome of a request. An accepted line parses in
this context's grammar and names the capability (and group) it goes into, under `## Into`, and no item is written
until `work accept`; a refused line may carry its reason; a rewritten line's counter-proposal parses, is appended to
the request's lines and passes the turn to the asker, posted on the request's issue."""
import pathlib
import subprocess
import sys

import backlog_items
import pytest
import readiness_bar
import request_moves
import request_text
from backlog_testing import REPO, git, state, work, write_request
from request_testing import calls, hosted
from test_backlog_lines import ABANDON, FROBNICATE

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

# A peer's line no transition allows (a `proposed` initiative abandoned), and the counter-proposal that fixes it.
ASKED = ("While an initiative is `proposed`, when the person runs `work abandon` on the initiative, `work` shall set the status of the initiative to "
         "`abandoned`.")
COUNTER = ABANDON


@pytest.fixture
def taken(ready_repo):
    toolchain.require()
    write_request(ready_repo, "q1", lines=(ABANDON,))
    return ready_repo


def request(repo, name="q1"):
    return (repo / ".shop" / "requests" / ("%s.md" % name)).read_text()


def entries(text, section):
    return request_text.entries(text, section)


def committed(repo):
    return sorted(git(repo, "show", "--name-only", "--format=", "HEAD").split())


def test_accepted_names_where_the_line_goes_and_writes_no_item(taken):
    done = work(taken, "outcome", "q1", "1", "accepted", "--into", "work-queue", "--group", "g4")
    assert done.returncode == 0, done.stderr
    text = request(taken)
    assert entries(text, "Outcomes") == ["1. accepted"] and entries(text, "Into") == ["1. work-queue g4"]
    assert committed(taken) == [".shop/requests/q1.md"]
    assert git(taken, "log", "-1", "--format=%s").strip() == "work outcome: q1 line 1 accepted"
    assert not (taken / ".shop" / "backlog").is_dir() or not list((taken / ".shop" / "backlog").glob("b*.md"))


def test_accepted_without_into_or_into_no_capability_is_refused(taken):
    before = state(taken)
    for extra in ((), ("--into", "nowhere")):
        done = work(taken, "outcome", "q1", "1", "accepted", *extra)
        assert done.returncode == 1 and ("--into" in done.stderr or "nowhere" in done.stderr), done.stderr
    assert state(taken) == before


def test_an_accepted_line_that_does_not_parse_is_refused_naming_it(ready_repo):
    """r38."""
    toolchain.require()
    write_request(ready_repo, "q1", lines=(FROBNICATE,))
    before = state(ready_repo)
    done = work(ready_repo, "outcome", "q1", "1", "accepted", "--into", "work-queue")
    assert done.returncode == 1, done.stdout
    assert "line 1 of q1" in done.stderr and FROBNICATE in done.stderr and "parsed up to:" in done.stderr, done.stderr
    assert state(ready_repo) == before


def test_refused_writes_its_reason_when_given(taken):
    done = work(taken, "outcome", "q1", "1", "refused", "--reason", "out of scope")
    assert done.returncode == 0, done.stderr
    text = request(taken)
    assert entries(text, "Outcomes") == ["1. refused"] and entries(text, "Reasons") == ["1. out of scope"]


def test_rewritten_with_a_line_passes_the_turn_and_posts_it(ready_repo, tmp_path):
    toolchain.require()
    env = hosted(ready_repo, tmp_path)
    path = write_request(ready_repo, "q2", lines=(ASKED,))
    path.write_text(path.read_text().replace("kind: request\n", "kind: request\nissue: https://github.com/ex/ctx/"
                                             "issues/1\n"))
    git(ready_repo, "commit", "-qam", "on its issue")
    (tmp_path / "gh-issues.json").write_text('{"https://github.com/ex/ctx/issues/1": {"title": "t", "body": "", '
                                             '"state": "OPEN", "comments": []}}')
    done = subprocess.run([sys.executable, str(REPO / "scripts" / "work"), "--root", str(ready_repo), "outcome", "q2",
                           "1", "rewritten", "--line", COUNTER], capture_output=True, text=True, env=env)
    assert done.returncode == 0, done.stderr
    text = request(ready_repo, "q2")
    assert entries(text, "Lines") == ["1. %s" % ASKED, "2. %s" % COUNTER]
    assert entries(text, "Outcomes") == ["1. rewritten"] and entries(text, "Reasons") == ["1. rewritten as line 2"]
    assert (request_moves.field(text, "status"), request_moves.field(text, "turn")) == ("awaiting-asker", "asker")
    posted = calls(tmp_path, "issue", "comment")
    assert len(posted) == 1 and "counter 1: 2" in posted[0][-1] and "line 2: %s" % COUNTER in posted[0][-1]
    assert entries(text, "Comments") == ["1. https://github.com/ex/ctx/issues/1#issuecomment-1 turn"]
    assert committed(ready_repo) == [".shop/requests/q2.md"]


def test_a_counter_proposal_that_does_not_parse_is_refused_and_named_so(taken):
    before = state(taken)
    done = work(taken, "outcome", "q1", "1", "rewritten", "--line", FROBNICATE)
    assert done.returncode == 1 and "the counter-proposal does not parse" in done.stderr, done.stderr
    assert "parsed up to:" in done.stderr, done.stderr
    assert "line 1 does not parse" not in done.stderr, done.stderr
    assert state(taken) == before


def test_the_rewritten_line_is_not_the_items(ready_repo):
    """intake's Implementation: an item's request lines are its request's lines not `rewritten`."""
    toolchain.require()
    write_request(ready_repo, "q1", lines=(ASKED,))
    assert work(ready_repo, "outcome", "q1", "1", "rewritten", "--line", COUNTER).returncode == 0
    assert work(ready_repo, "turn", "q1").returncode == 0      # the asker passes the turn back
    done = work(ready_repo, "outcome", "q1", "2", "accepted", "--into", "work-queue")
    assert done.returncode == 0, done.stderr
    assert work(ready_repo, "turn", "q1").returncode == 0
    done = work(ready_repo, "accept", "q1")
    assert done.returncode == 0, done.stderr
    written = (ready_repo / ".shop" / "backlog" / "b1.md").read_text()
    assert COUNTER in written and ASKED not in written, written
    item = backlog_items.find(ready_repo, "b1")
    assert [n for n, _, _ in readiness_bar.request_lines(ready_repo, item)] == [2]


def test_line_only_with_rewritten_and_into_only_with_accepted(taken):
    before = state(taken)
    for words in (("1", "accepted", "--into", "work-queue", "--line", COUNTER),
                  ("1", "refused", "--into", "work-queue", "--reason", "no"), ("1", "rewritten"),
                  ("9", "accepted", "--into", "work-queue")):
        done = work(taken, "outcome", "q1", *words)
        assert done.returncode == 1, (words, done.stdout)
    assert state(taken) == before


def test_the_asker_turn_still_refuses(ready_repo):
    write_request(ready_repo, "q1", lines=(ABANDON,), status="awaiting-asker", turn="asker")
    before = state(ready_repo)
    done = work(ready_repo, "outcome", "q1", "1", "refused", "--reason", "out of scope")
    assert done.returncode == 1 and "in the asker's turn" in done.stderr, done.stderr
    assert state(ready_repo) == before


def test_model_check_accepts_reasons_and_into(taken):
    assert work(taken, "outcome", "q1", "1", "accepted", "--into", "work-queue", "--reason", "fits").returncode == 0
    done = subprocess.run([sys.executable, str(REPO / "scripts" / "model"), "--root", str(taken), "check"],
                          capture_output=True, text=True)
    assert done.returncode != 2, done.stderr
    assert [n for n in (done.stdout + done.stderr).splitlines() if "q1.md" in n] == [], done.stdout


def test_a_word_that_is_not_a_line_outcome_is_refused(taken):
    """plan-3 review M1: the glossary's `line outcome` values only."""
    before = state(taken)
    done = work(taken, "outcome", "q1", "1", "bogus")
    assert done.returncode == 1 and "bogus" in done.stderr and "withdrawn" in done.stderr, done.stderr
    assert state(taken) == before


def test_outcome_takes_no_abbreviated_option(taken):
    """plan-3 review M2: `--in` (work line's) is not read as `--into`."""
    before = state(taken)
    done = work(taken, "outcome", "q1", "1", "accepted", "--in", "g1")
    assert done.returncode == 2 and "--in" in done.stderr, done.stderr
    assert state(taken) == before
