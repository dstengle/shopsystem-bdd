"""`work accept` (requests r39, r40): the upstream's person accepts a request whose lines proposed are all settled with
one accepted; the item is written `shaped` with each accepted line under the capability its outcome named, the request
is `accepted` in the upstream's turn, the request and the item are one commit, and the acceptance is posted after it."""
import json

import backlog_items
import backlog_lines
import pytest
import request_text
from backlog_testing import git, state, work, write_request
from request_testing import calls, hosted
from test_backlog_lines import ABANDON
from test_intake_outcome import ASKED

PEER = "bounded-context/ex.com/prod/peer"
ISSUE = "https://github.com/ex/ctx/issues/1"


@pytest.fixture
def asked(ready_repo, tmp_path, monkeypatch):
    hosted(ready_repo, tmp_path, monkeypatch=monkeypatch)
    (tmp_path / "gh-issues.json").write_text(json.dumps({ISSUE: {"title": "t", "body": "", "state": "OPEN",
                                                                 "comments": []}}))

    def write(outcomes, into=("work-queue", "work-queue")):
        path = write_request(ready_repo, "q1", lines=(ABANDON, ASKED), outcomes=outcomes, commit=False)
        text = path.read_text().replace("kind: request\n", "kind: request\nissue: %s\n" % ISSUE)
        text += "\n## Into\n%s" % "".join("%d. %s\n" % e for e in enumerate(into, 1) if e[1])
        path.write_text(text)
        git(ready_repo, "add", "-A")
        git(ready_repo, "commit", "-qm", "q1")
        return path
    return ready_repo, tmp_path, write


def test_accept_writes_the_shaped_item_with_its_lines_and_posts(asked):
    repo, where, write = asked
    path = write(("accepted", "refused"))
    done = work(repo, "accept", "q1")
    assert done.returncode == 0, done.stderr
    assert done.stdout == 'b1 "Archive old items" shaped\n'
    item = backlog_items.find(repo, "b1")
    assert (item.status, item.provenance, item.request, item.asked_by) == ("shaped", "peer", "q1", PEER)
    assert item.sections["Notes"] == 'taken in from request q1 "Archive old items"'
    blocks = backlog_lines.read(item, "b1")
    assert [(b.capability, g.title, g.requirements) for b in blocks for g in b.groups] == [
        ("work-queue", "Archive old items", [("r5", ABANDON)])]
    text = path.read_text()
    assert (request_text.field(text, "status"), request_text.field(text, "turn")) == ("accepted", "upstream")
    assert len(calls(where, "issue", "comment")) == 1 and "step: accept" in calls(where, "issue", "comment")[0][-1]
    assert sorted(git(repo, "show", "--name-only", "--format=", "HEAD~1").split()) == [".shop/backlog/b1.md",
                                                                                        ".shop/requests/q1.md"]
    assert git(repo, "show", "--name-only", "--format=", "HEAD").split() == [".shop/requests/q1.md"]  # the URL (b36)
    done = work(repo, "ready", "b1")
    assert done.returncode == 0, done.stderr


def test_two_lines_of_one_capability_share_a_group(asked):
    repo, _, write = asked
    write(("accepted", "accepted"))
    assert work(repo, "accept", "q1").returncode == 0
    blocks = backlog_lines.read(backlog_items.find(repo, "b1"), "b1")
    assert [(g.id, [r for r, _ in g.requirements]) for b in blocks for g in b.groups] == [("g4", ["r5", "r6"])]


@pytest.mark.parametrize("outcomes, into, said", [(("accepted", "question"), ("work-queue",), "line 2 of request q1"),
                                                  (("accepted", None), ("work-queue",), "line 2 of request q1"),
                                                  (("refused", "refused"), (), "no accepted line"),
                                                  (("accepted", "refused"), (), "names no capability")])
def test_accept_refuses_and_changes_nothing(asked, outcomes, into, said):
    repo, where, write = asked
    write(outcomes, into)
    before = state(repo)
    done = work(repo, "accept", "q1")
    assert done.returncode == 1 and said in done.stderr, done.stderr
    assert state(repo) == before and calls(where, "issue") == []


def test_accept_refuses_a_request_in_the_askers_turn(asked):
    repo, _, write = asked
    path = write(("accepted", "refused"))
    path.write_text(path.read_text().replace("turn: upstream", "turn: asker").replace("status: open",
                                                                                    "status: awaiting-asker"))
    git(repo, "commit", "-qam", "the asker's turn")
    done = work(repo, "accept", "q1")
    assert done.returncode == 1 and "the asker's turn" in done.stderr, done.stderr
