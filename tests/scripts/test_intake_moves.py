"""intake r1, r5, r6 (workflow simplification plan 3, Task 3, D10, D11): `work intake` takes a peer's request in as a
`shaped` item, refuses one taken in already or out of the upstream's turn, and the item's request lines are part of
the readiness bar."""
import pathlib
import sys

import backlog_items
import intake_moves
import pytest
import readiness_bar
from backlog_testing import git, item_text, state, work, write_item, write_request
from test_backlog_lines import ABANDON

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

PEER = "bounded-context/ex.com/prod/peer"


@pytest.fixture
def asked(ready_repo):
    path = write_request(ready_repo, "q1", lines=(ABANDON,))
    return ready_repo, path


def test_intake_writes_a_shaped_peer_item_and_commits_only_it(asked):
    repo, path = asked
    before = path.read_bytes()
    done = work(repo, "intake", "q1")
    assert done.returncode == 0, done.stderr
    assert done.stdout == 'b1 "Archive old items" shaped\n'
    item = backlog_items.find(repo, "b1")
    assert (item.status, item.provenance, item.request, item.asked_by) == ("shaped", "peer", "q1", PEER)
    assert item.sections["Notes"] == 'taken in from request q1 "Archive old items"'
    assert git(repo, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]
    assert git(repo, "log", "-1", "--format=%s").strip() == 'work intake: q1 "Archive old items" -> b1 "Archive old items" shaped'
    assert path.read_bytes() == before


@pytest.mark.parametrize("asker, provenance", [("internal", "own"), ("bounded-context/ex.com/prod/ctx", "own"),
                                               ("ctx", "own"), ("product/ex.com/prod", "product"), (PEER, "peer")])
def test_provenance_is_read_off_the_asker(ready_repo, asker, provenance):
    assert intake_moves.provenance_of(ready_repo, asker) == provenance


def test_intake_refuses_a_request_taken_in(asked):
    repo, _ = asked
    assert work(repo, "intake", "q1").returncode == 0
    before = state(repo)
    done = work(repo, "intake", "q1")
    assert done.returncode == 1 and 'b1 "Archive old items"' in done.stderr, done.stderr
    assert state(repo) == before


@pytest.mark.parametrize("status, taken", [("awaiting-asker", False), ("delivered", False),
                                           ("awaiting-upstream", True)])
def test_intake_refuses_a_request_out_of_turn(ready_repo, status, taken):
    write_request(ready_repo, "q1", lines=(ABANDON,), status=status,
                  turn="upstream" if status == "awaiting-upstream" else "asker")
    before = state(ready_repo)
    done = work(ready_repo, "intake", "q1")
    if taken:
        assert done.returncode == 0, done.stderr
    else:
        assert done.returncode == 1 and status in done.stderr, done.stderr
        assert state(ready_repo) == before


def test_intake_refuses_a_request_there_is_not(ready_repo):
    done = work(ready_repo, "intake", "q7")
    assert done.returncode == 1 and "no request q7" in done.stderr, done.stderr


@pytest.mark.parametrize("fields", [{}, {"status": "shaped", "value": "high-value", "urgency": "low-urgency",
                                         "size": "small"}, {"depends_on": "b2, b3"},
                                    {"body": "\n## Notes\n\nA note.\n\n## Question\n\nWhich?\n"}])
def test_an_item_without_request_fields_renders_as_before(fields):
    text = item_text(**fields)
    assert backlog_items.render(backlog_items.parse(text, "b1.md")) == text


def test_request_fields_round_trip_and_a_bad_request_is_refused():
    text = item_text().replace("depends_on: []\n", "depends_on: []\nrequest: q1\nasked_by: %s\n" % PEER)
    assert backlog_items.render(backlog_items.parse(text, "b1.md")) == text
    with pytest.raises(backlog_items.Refused, match="b1.md: request"):
        backlog_items.parse(text.replace("request: q1", "request: 7"), "b1.md")


def test_ready_names_an_unsettled_line_of_the_items_request(asked):
    repo, _ = asked
    toolchain.require()
    assert work(repo, "intake", "q1").returncode == 0
    before = state(repo)
    done = work(repo, "ready", "b1")
    assert done.returncode == 1
    assert "line 1 of request q1" in done.stderr and "work line" in done.stderr, done.stderr
    assert state(repo) == before


def test_unsettled_names_each_line(ready_repo):
    write_request(ready_repo, "q1", lines=("one", "two", "three"), outcomes=("accepted", "question", "rewritten"))
    write_item(ready_repo, "b1", status="shaped")
    item = backlog_items.find(ready_repo, "b1")
    item.request = "q1"
    reasons = readiness_bar.unsettled(ready_repo, item)
    assert reasons == ["line 2 of request q1 is question, not settled: two"]


def test_json_names_the_request_of_an_item_taken_in(asked):
    import json
    repo, _ = asked
    assert work(repo, "intake", "q1").returncode == 0
    shown = json.loads(work(repo, "show", "b1", "--json").stdout)["item"]
    assert (shown["request"], shown["asked_by"]) == ("q1", PEER)
