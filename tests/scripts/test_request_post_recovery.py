"""A post GitHub took whose URL git then refused to commit (b36, finding f6): the refusal names what was posted and
`work sync`, which records it; a run of the command again records it too and posts nothing twice."""
import request_text
from backlog_testing import git, work
from request_testing import calls, issues
from test_backlog_lines import ABANDON
from test_request_commit_first import ISSUE, on_issue  # noqa: F401  (a fixture)

ASK = ("request", "a request", "--from", "internal", "--source", "observation/ex.com/prod/ctx/o1")
OPENED = "https://github.com/ex/ctx/issues/2"


def refuses_urls(repo):
    """A pre-commit hook that refuses a commit adding a GitHub URL: the one recording a post, not the step's own."""
    hook = repo / ".git" / "hooks" / "pre-commit"
    hook.write_text("#!/bin/sh\ngit diff --cached -U0 | grep -q '^+.*https://github.com' && exit 1\nexit 0\n")
    hook.chmod(0o755)
    return hook


def record(repo, name="q1"):
    return (repo / ".shop" / "requests" / (name + ".md")).read_text()


def test_a_comment_posted_but_not_recorded_is_named_and_synced(on_issue):  # noqa: F811
    repo, where, write = on_issue
    write(lines=(ABANDON,), outcomes=("accepted",))
    hook = refuses_urls(repo)
    done = work(repo, "turn", "q1")
    posted = calls(where, "issue", "comment")
    assert done.returncode != 0 and len(posted) == 1, done.stdout
    url = issues(where)[ISSUE]["comments"][0]["url"]
    assert url in done.stderr and "work sync" in done.stderr, done.stderr
    hook.unlink()
    assert work(repo, "sync").returncode == 0
    assert url in request_text.entries(record(repo), "Comments")[-1]
    assert git(repo, "status", "--porcelain", "--", ".shop") == ""


def test_a_comment_posted_but_not_recorded_is_not_posted_again(on_issue):  # noqa: F811
    repo, where, write = on_issue
    write(lines=(ABANDON,), outcomes=("accepted",))
    hook = refuses_urls(repo)
    assert work(repo, "turn", "q1").returncode != 0
    hook.unlink()
    done = work(repo, "turn", "q1")
    assert done.returncode == 0, done.stderr
    assert len(calls(where, "issue", "comment")) == 1 and len(issues(where)[ISSUE]["comments"]) == 1
    url = issues(where)[ISSUE]["comments"][0]["url"]
    assert request_text.entries(record(repo), "Comments") == ["1. %s turn" % url]


def test_an_issue_opened_but_not_recorded_is_named_and_synced(on_issue):  # noqa: F811
    repo, where, _ = on_issue
    hook = refuses_urls(repo)
    done = work(repo, *ASK)
    assert done.returncode != 0 and OPENED in done.stderr and "work sync" in done.stderr, done.stderr
    assert "issue:" not in record(repo)
    hook.unlink()
    assert work(repo, "sync").returncode == 0
    assert request_text.field(record(repo), "issue") == OPENED
    assert request_text.entries(record(repo), "Comments") == ["1. %s ask" % OPENED]
    assert not (repo / ".shop" / "requests" / "q2.md").exists() and len(calls(where, "issue", "create")) == 1


def test_an_issue_opened_but_not_recorded_is_not_opened_again(on_issue):  # noqa: F811
    repo, where, _ = on_issue
    hook = refuses_urls(repo)
    assert work(repo, *ASK).returncode != 0
    hook.unlink()
    done = work(repo, *ASK)
    assert done.returncode == 0, done.stderr
    assert len(calls(where, "issue", "create")) == 1 and OPENED in done.stdout
    assert request_text.field(record(repo), "issue") == OPENED
    assert not (repo / ".shop" / "requests" / "q2.md").exists()
