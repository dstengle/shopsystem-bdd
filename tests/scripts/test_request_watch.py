"""`work watch` (requests r42, r43): one poll of the requests' issues through the stand-in gh, what it prints, what it
keeps in the git dir and never commits, a gh failure tried again, and nothing printed twice."""
import json
import subprocess
import sys

import request_sync
import request_watch
from backlog_testing import SCRIPTS, git
from request_testing import hosted
from shop_files import Refused

OWN = "https://github.com/ex/ctx/issues/1"
OTHER = "https://github.com/ex/up/issues/4"
TURN = "~~~shop-request\nstep: turn\nstatus: open\nturn: upstream\n~~~\n"
ASK = "~~~shop-request\nstep: ask\nasker: bounded-context/ex.com/prod/down\ntitle: Old items\nask: I need it\n~~~\n"


def request(repo, name, issue, status="open", held=()):
    comments = "".join("%d. %s turn\n" % (k, url) for k, url in enumerate(held, 1))
    path = repo / ".shop" / "requests" / ("%s.md" % name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nid: request/ex.com/prod/ctx/%s\nkind: request\nasker: bounded-context/ex.com/prod/ctx\n"
                    "upstream: bounded-context/ex.com/prod/up\nissue: %s\nstatus: %s\nturn: upstream\n---\n\n# %s\n\n"
                    "## Comments\n%s" % (name, issue, status, name, comments))


def world(repo, where, issues, monkeypatch):
    env = hosted(repo, where, monkeypatch=monkeypatch)
    (where / "gh-issues.json").write_text(json.dumps(issues))
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "requests")
    return env


def issue(body="", comments=(), state="OPEN"):
    return {"title": "Old items", "body": body, "state": state,
            "comments": [{"url": url, "body": text} for url, text in comments]}


def watch(repo, *args, env):
    return subprocess.run([sys.executable, str(SCRIPTS / "work"), "--root", str(repo), "watch", "--every", "0",
                           "--polls", "1", *args], capture_output=True, text=True, env=env, timeout=60)


def test_a_comment_not_held_is_printed_once_and_nothing_is_written(backlog_repo, tmp_path_factory, monkeypatch):
    where = tmp_path_factory.mktemp("gh")
    request(backlog_repo, "q1", OTHER, held=[OTHER + "#issuecomment-1"])
    request(backlog_repo, "q2", OTHER.replace("/4", "/5"), status="delivered")
    env = world(backlog_repo, where, {
        OTHER: issue(comments=[(OTHER + "#issuecomment-1", TURN), (OTHER + "#issuecomment-2", "no block")]),
        OTHER.replace("/4", "/5"): issue(comments=[(OTHER.replace("/4", "/5") + "#issuecomment-3", TURN)])}, monkeypatch)
    before = git(backlog_repo, "rev-parse", "HEAD")
    done = watch(backlog_repo, env=env)
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines() == [
        "q1 %s comment 2: %s#issuecomment-2 (`work sync` records it)" % (OTHER, OTHER)]
    assert git(backlog_repo, "rev-parse", "HEAD") == before
    assert git(backlog_repo, "status", "--porcelain") == ""
    again = watch(backlog_repo, env=env)
    assert again.returncode == 1 and again.stdout == "", again.stdout
    assert "nothing new after 1 poll" in again.stderr


def test_an_untaken_ask_is_printed_and_a_held_one_or_no_ask_is_not(backlog_repo, tmp_path_factory, monkeypatch):
    where = tmp_path_factory.mktemp("gh")
    request(backlog_repo, "q1", OWN)
    env = world(backlog_repo, where, {
        OWN: issue(ASK), OWN.replace("/1", "/2"): issue(ASK), OWN.replace("/1", "/3"): issue(TURN),
        OWN.replace("/1", "/4"): issue("just words")}, monkeypatch)
    done = watch(backlog_repo, env=env)
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines() == ["ask %s Old items (`work sync` takes it in)" % OWN.replace("/1", "/2")]


def test_a_gh_failure_is_said_and_the_poll_tried_again(backlog_repo, tmp_path_factory, monkeypatch, capsys):
    where = tmp_path_factory.mktemp("gh")
    request(backlog_repo, "q1", OTHER)
    world(backlog_repo, where, {OTHER: issue(comments=[(OTHER + "#issuecomment-7", TURN)])}, monkeypatch)
    real, failures, slept = request_sync.unheld_comments, [1], []

    def flaky(*args):
        if failures:
            failures.pop()
            raise Refused("work watch: gh issue view failed: offline")
        return real(*args)
    monkeypatch.setattr(request_sync, "unheld_comments", flaky)
    assert request_watch.watch(backlog_repo, every=5, sleep=slept.append) == 0
    out = capsys.readouterr()
    assert "gh issue view failed: offline; polling again in 5s" in out.err
    assert slept == [5] and "#issuecomment-7" in out.out
    assert request_watch.kept(backlog_repo) == {OTHER + "#issuecomment-7"}
