"""intake r6 (workflow simplification plan 3, Task 3, D10, D11): an item taken in from a request (`work accept`) names
it and its asker, its provenance is read off the asker, and the item's request lines are part of the readiness bar."""
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


@pytest.mark.parametrize("asker, provenance", [("internal", "own"), ("bounded-context/ex.com/prod/ctx", "own"),
                                               ("ctx", "own"), ("product/ex.com/prod", "product"), (PEER, "peer")])
def test_provenance_is_read_off_the_asker(ready_repo, asker, provenance):
    assert intake_moves.provenance_of(ready_repo, asker) == provenance


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


def test_ready_names_an_unsettled_line_of_the_items_request(ready_repo):
    toolchain.require()
    write_request(ready_repo, "q1", lines=(ABANDON,))
    write_item(ready_repo, "b1", status="shaped", body="")
    path = ready_repo / ".shop" / "backlog" / "b1.md"
    path.write_text(path.read_text().replace("depends_on: []\n", "depends_on: []\nrequest: q1\nasked_by: %s\n" % PEER))
    git(ready_repo, "commit", "-qam", "b1 taken in from q1")
    before = state(ready_repo)
    done = work(ready_repo, "ready", "b1")
    assert done.returncode == 1
    assert "line 1 of request q1" in done.stderr and "work line" in done.stderr, done.stderr
    assert state(ready_repo) == before


def test_unsettled_names_each_line(ready_repo):
    write_request(ready_repo, "q1", lines=("one", "two", "three"), outcomes=("accepted", "question", "rewritten"))
    write_item(ready_repo, "b1", status="shaped")
    item = backlog_items.find(ready_repo, "b1")
    item.request = "q1"
    reasons = readiness_bar.unsettled(ready_repo, item)
    assert reasons == ["line 2 of request q1 is question, not settled: two"]


def test_json_names_the_request_of_an_item_taken_in(ready_repo):
    import json
    write_item(ready_repo, "b1", status="shaped")
    path = ready_repo / ".shop" / "backlog" / "b1.md"
    path.write_text(path.read_text().replace("depends_on: []\n", "depends_on: []\nrequest: q1\nasked_by: %s\n" % PEER))
    shown = json.loads(work(ready_repo, "show", "b1", "--json").stdout)["item"]
    assert (shown["request"], shown["asked_by"]) == ("q1", PEER)
