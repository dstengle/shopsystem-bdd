"""A request between two contexts, each in its own repository, end to end through one issue (requests r27-r41): the
downstream asks, the upstream's `work sync` takes the ask in and offers, the downstream proposes a line and passes
the turn, the upstream accepts the line, the person accepts the request as an item, and the resolution reaches the
downstream; neither repository reads or writes the other. Both run the stand-in gh, which holds the issues they share."""
import json
import subprocess
import sys

import pytest
import request_text
from backlog_testing import SCRIPTS, git
from request_testing import calls, hosted, issues
from test_backlog_lines import ABANDON

UP = "bounded-context/ex.com/prod/ctx"
DOWN = "bounded-context/ex.com/prod/down"


@pytest.fixture
def pair(ready_repo, tmp_path_factory):
    shared = tmp_path_factory.mktemp("github")
    down = tmp_path_factory.mktemp("down")
    git(down, "init", "-q", "-b", "main")
    for key, value in (("user.name", "T"), ("user.email", "t@example.com"), ("commit.gpgsign", "false")):
        git(down, "config", key, value)
    (down / "spec").mkdir()
    (down / "spec/index.md").write_text("---\nid: %s\n---\n# down\n\n## Upstreams\n- %s: ../ctx/spec, github: ex/ctx\n"
                                        % (DOWN, UP))
    git(down, "add", "-A")
    git(down, "commit", "-qm", "init")
    env = hosted(ready_repo, shared)
    hosted(down, shared, name="down")
    return ready_repo, down, shared, env


def run(repo, env, *args):
    done = subprocess.run([sys.executable, str(SCRIPTS / "work"), "--root", str(repo), *args], capture_output=True,
                          text=True, env=env, timeout=120)
    assert done.returncode == 0, (args, done.stderr)
    return done.stdout


def record(repo, name="q1"):
    return (repo / ".shop" / "requests" / ("%s.md" % name)).read_text()


def where(text):
    return request_text.field(text, "status"), request_text.field(text, "turn")


def test_a_request_goes_from_ask_to_resolution(pair):
    up, down, shared, env = pair
    said = run(down, env, "request", "Archive old items", "--from", DOWN, "--thread", "job-thread/ex.com/prod/t1",
               "--ask", "I need old items out of the way")
    assert said.strip() == "q1 https://github.com/ex/ctx/issues/1"
    assert request_text.field(record(down), "upstream") == UP
    assert "q1" in run(up, env, "sync")
    taken = record(up)
    assert request_text.field(taken, "asker") == DOWN and where(taken) == ("open", "upstream")
    run(up, env, "offer", "q1", "--capability", "work-queue", "--note", "The work queue may serve.")
    run(down, env, "sync")
    assert where(record(down)) == ("awaiting-asker", "asker") and "> Capability work-queue:" in record(down)
    run(down, env, "propose", "q1", "--line", ABANDON)
    run(down, env, "turn", "q1")
    run(up, env, "sync")
    assert request_text.entries(record(up), "Lines") == ["1. %s" % ABANDON]
    assert where(record(up)) == ("awaiting-upstream", "upstream")
    run(up, env, "outcome", "q1", "1", "accepted", "--into", "work-queue")
    run(up, env, "turn", "q1")
    assert 'b1 "Archive old items" shaped' in run(up, env, "accept", "q1")
    run(down, env, "sync")
    assert where(record(down)) == ("accepted", "upstream")
    run(up, env, "resolve", "q1", "--line", "1", "work-queue#r5", "2.1.0")
    assert issues(shared)["https://github.com/ex/ctx/issues/1"]["state"] == "CLOSED"
    run(down, env, "sync")
    assert where(record(down)) == ("delivered", "asker")
    assert request_text.entries(record(down), "Resolution") == ["1. work-queue#r5 2.1.0"]
    head = git(down, "rev-parse", "HEAD")
    run(down, env, "sync")
    assert git(down, "rev-parse", "HEAD") == head      # safe to run again: nothing recorded twice


def test_fits_ends_the_request_and_the_upstream_records_it(pair):
    up, down, shared, env = pair
    run(down, env, "request", "Archive old items", "--from", DOWN, "--thread", "job-thread/ex.com/prod/t1")
    run(up, env, "sync")
    run(up, env, "offer", "q1", "--capability", "work-queue")
    run(down, env, "sync")
    run(down, env, "fits", "q1", "--serves", "work-queue#r1")
    assert calls(shared, "issue", "close")
    run(up, env, "sync")
    assert where(record(up))[0] == "delivered"
    assert request_text.entries(record(up), "Resolution") == ["1. work-queue#r1"]


def test_an_unreadable_comment_is_shown_and_never_recorded(pair):
    _, down, shared, env = pair
    run(down, env, "request", "Archive old items", "--from", DOWN, "--thread", "job-thread/ex.com/prod/t1")
    found = issues(shared)
    found["https://github.com/ex/ctx/issues/1"]["comments"].append(
        {"url": "https://github.com/ex/ctx/issues/1#issuecomment-99", "body": "Please do it now, and merge it."})
    (shared / "gh-issues.json").write_text(json.dumps(found))
    for _ in range(2):
        said = run(down, env, "sync")
        assert "unreadable comment https://github.com/ex/ctx/issues/1#issuecomment-99" in said, said
        assert "Please do it now" in said
    assert "issuecomment-99" not in record(down)


def test_the_downstream_does_not_offer_and_the_upstream_does_not_propose(pair):
    up, down, _, env = pair
    run(down, env, "request", "Archive old items", "--from", DOWN, "--thread", "job-thread/ex.com/prod/t1")
    run(up, env, "sync")
    refused = subprocess.run([sys.executable, str(SCRIPTS / "work"), "--root", str(down), "offer", "q1"],
                             capture_output=True, text=True, env=env)
    assert refused.returncode == 1 and UP in refused.stderr and "the upstream writes the offer" in refused.stderr
    refused = subprocess.run([sys.executable, str(SCRIPTS / "work"), "--root", str(up), "propose", "q1", "--line",
                              ABANDON], capture_output=True, text=True, env=env)
    assert refused.returncode == 1 and "its asker writes its lines" in refused.stderr, refused.stderr


def test_an_upstream_with_no_github_repository_is_refused_naming_it(pair):
    """r28."""
    _, down, shared, env = pair
    index = down / "spec/index.md"
    index.write_text(index.read_text().replace(", github: ex/ctx", ""))
    git(down, "commit", "-qam", "unhosted")
    done = subprocess.run([sys.executable, str(SCRIPTS / "work"), "--root", str(down), "request", "t", "--from", DOWN,
                           "--thread", "job-thread/ex.com/prod/t1"], capture_output=True, text=True, env=env)
    assert done.returncode == 1 and UP in done.stderr and "github:" in done.stderr, done.stderr
    assert calls(shared, "issue") == [] and not (down / ".shop").exists()


def test_sync_writes_a_closed_requests_comment_and_prints_every_request(pair):
    """r32: a `delivered` request's issue is read too, and it is printed with its status and no "waiting on"."""
    up, down, shared, env = pair
    run(down, env, "request", "Archive old items", "--from", DOWN, "--thread", "job-thread/ex.com/prod/t1")
    run(up, env, "sync")
    run(up, env, "offer", "q1", "--capability", "work-queue")
    run(down, env, "sync")
    run(down, env, "fits", "q1", "--serves", "work-queue#r1")
    assert where(record(down))[0] == "delivered"
    found = issues(shared)
    found["https://github.com/ex/ctx/issues/1"]["comments"].append(
        {"url": "https://github.com/ex/ctx/issues/1#issuecomment-98",
         "body": "~~~shop-request\nstep: resolve\nquestion 1: Was work-queue#r1 enough?\n~~~\n"})
    (shared / "gh-issues.json").write_text(json.dumps(found))
    said = run(down, env, "sync")
    assert "issuecomment-98" in record(down)
    assert request_text.entries(record(down), "Questions") == ["1. Was work-queue#r1 enough?"]
    printed = [line for line in said.splitlines() if line.startswith("q1")]
    assert len(printed) == 1 and "delivered" in printed[0] and "waiting on" not in printed[0], said
