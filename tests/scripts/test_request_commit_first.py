"""A request's record is committed before its step is posted (b36, requests r45-r47): in a repository whose git
refuses the commit, `work offer`, `accept`, `resolve`, `outcome rewritten` and a
`turn` that leaves the record unchanged post nothing; a post GitHub refuses
puts the record back, in a commit, so that no record is left with a step it did not post."""
import json
import pathlib
import sys

import pytest
import request_text
from backlog_testing import git, work, write_request
from request_testing import calls, hosted
from test_backlog_lines import ABANDON
from test_intake_outcome import ASKED

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

ISSUE = "https://github.com/ex/ctx/issues/1"


@pytest.fixture
def on_issue(ready_repo, tmp_path, monkeypatch):
    """A request q1 on an issue the stand-in gh holds; (repo, the stand-in's directory, write)."""
    hosted(ready_repo, tmp_path, monkeypatch=monkeypatch)
    (tmp_path / "gh-issues.json").write_text(json.dumps({ISSUE: {"title": "t", "body": "", "state": "OPEN",
                                                                 "comments": []}}))

    def write(extra="", **fields):
        path = write_request(ready_repo, "q1", commit=False, **fields)
        path.write_text(path.read_text().replace("kind: request\n", "kind: request\nissue: %s\n" % ISSUE) + extra)
        git(ready_repo, "add", "-A")
        git(ready_repo, "commit", "-qm", "q1")
        return path
    return ready_repo, tmp_path, write


def uncommittable(repo):
    hook = repo / ".git" / "hooks" / "pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)


@pytest.mark.parametrize("command, fields, extra", [
    (("offer", "q1", "--capability", "work-queue"), {}, ""),
    (("accept", "q1"), {"lines": (ABANDON,), "outcomes": ("accepted",)}, "\n## Into\n1. work-queue\n"),
    (("resolve", "q1", "--line", "1", "work-queue#r1", "1.0.0"), {"lines": (ABANDON,), "outcomes": ("accepted",),
                                                                  "status": "accepted"}, ""),
    (("outcome", "q1", "1", "rewritten", "--line", ABANDON), {"lines": (ASKED,)}, ""),
    (("turn", "q1"), {"lines": (ABANDON,), "outcomes": ("accepted",)}, ""),  # r36: a turn that changes nothing
])
def test_an_uncommittable_repository_posts_nothing(on_issue, command, fields, extra):
    repo, where, write = on_issue
    if command[0] == "outcome":
        toolchain.require()
    before = write(extra, **fields).read_text()
    head = git(repo, "rev-parse", "HEAD")
    uncommittable(repo)
    done = work(repo, *command)
    assert done.returncode != 0, done.stdout
    assert calls(where, "issue") == [], calls(where, "issue")
    assert (repo / ".shop" / "requests" / "q1.md").read_text() == before
    assert git(repo, "rev-parse", "HEAD") == head and not (repo / ".shop" / "backlog" / "b1.md").exists()


def test_a_comment_github_refuses_puts_the_record_back(on_issue, monkeypatch):
    repo, where, write = on_issue
    before = write(lines=(ABANDON,), outcomes=("accepted",), status="accepted").read_text()
    monkeypatch.setenv("STUB_GH_FAIL", "issue comment")
    done = work(repo, "resolve", "q1", "--line", "1", "work-queue#r1", "1.0.0")
    assert done.returncode != 0 and "refused" in done.stderr, done.stdout
    assert (repo / ".shop" / "requests" / "q1.md").read_text() == before
    assert git(repo, "status", "--porcelain", "--", ".shop") == ""
    assert calls(where, "issue", "close") == []


def test_an_issue_github_refuses_leaves_no_request(on_issue, monkeypatch):
    repo, _, _ = on_issue
    monkeypatch.setenv("STUB_GH_FAIL", "issue create")
    done = work(repo, "request", "a request", "--from", "internal", "--source", "observation/ex.com/prod/ctx/o1")
    assert done.returncode != 0 and "refused" in done.stderr, done.stdout
    assert not list((repo / ".shop" / "requests").glob("q*.md")) and git(repo, "status", "--porcelain", "--", ".shop") == ""


def test_the_request_is_committed_then_its_issue_recorded(on_issue):
    repo, where, _ = on_issue
    done = work(repo, "request", "a request", "--from", "internal", "--source", "observation/ex.com/prod/ctx/o1")
    assert done.returncode == 0, done.stderr
    first, second = git(repo, "log", "-2", "--format=%H").split()[::-1]
    assert "issue:" not in git(repo, "show", "%s:.shop/requests/q1.md" % first)
    url = calls(where, "issue", "create") and request_text.field(
        git(repo, "show", "%s:.shop/requests/q1.md" % second), "issue")
    assert url and request_text.entries(git(repo, "show", "%s:.shop/requests/q1.md" % second), "Comments") == [
        "1. %s ask" % url]
