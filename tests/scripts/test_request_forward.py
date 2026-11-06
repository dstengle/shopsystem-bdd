"""`work watch --forward` (requests r57, r58) through the stand-in gh: a repository the account administers forwarded
(`gh webhook forward`, the extension installed when missing), one it does not polled through GitHub's notifications
and named on stderr, and a watch that finds nothing ended after its waits."""
import json
import subprocess
import sys

from backlog_testing import SCRIPTS, git
from request_testing import calls
from test_request_watch import OTHER, TURN, issue, request, world


def watch(repo, env, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / "work"), "--root", str(repo), "watch", "--forward", *args],
                          capture_output=True, text=True, env=env, timeout=60)


def pending(where, found):
    (where / "gh-pending.json").write_text(json.dumps(found))


def test_a_repository_not_administered_is_polled_through_notifications(backlog_repo, tmp_path_factory,
                                                                        monkeypatch):
    where = tmp_path_factory.mktemp("gh")
    request(backlog_repo, "q1", OTHER)
    env = world(backlog_repo, where, {OTHER: issue()}, monkeypatch)
    env["STUB_GH_NOT_ADMIN"] = "ex/up"
    pending(where, {OTHER: issue(comments=[(OTHER + "#issuecomment-9", TURN)])})
    done = watch(backlog_repo, env, "--every", "0.2", "--polls", "50")
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines() == [
        "q1 %s comment 9: %s#issuecomment-9 (`work sync` records it)" % (OTHER, OTHER)]
    assert "polling GitHub's notifications for ex/up" in done.stderr
    forwards = calls(where, "webhook", "forward")
    assert [argv[argv.index("--repo") + 1] for argv in forwards] == ["ex/ctx"]
    assert "issues,issue_comment" in forwards[0]
    noted = calls(where, "api")
    assert noted and "If-Modified-Since" not in " ".join(noted[0]) and "If-Modified-Since" in " ".join(noted[-1])
    assert git(backlog_repo, "status", "--porcelain") == ""


def test_the_extension_is_installed_when_gh_does_not_list_it(backlog_repo, tmp_path_factory, monkeypatch):
    where = tmp_path_factory.mktemp("gh")
    request(backlog_repo, "q1", OTHER)
    env = world(backlog_repo, where, {OTHER: issue()}, monkeypatch)
    env["STUB_GH_NO_WEBHOOK"] = "1"
    done = watch(backlog_repo, env, "--every", "0.2", "--polls", "1")
    assert done.returncode == 1 and done.stdout == "", done.stdout
    assert "nothing new after 1 wait" in done.stderr
    assert calls(where, "extension", "install") == [["extension", "install", "cli/gh-webhook"]]
    assert calls(where, "webhook", "forward")


def test_a_watch_that_finds_nothing_ends_after_its_waits(backlog_repo, tmp_path_factory, monkeypatch):
    where = tmp_path_factory.mktemp("gh")
    request(backlog_repo, "q1", OTHER)
    env = world(backlog_repo, where, {OTHER: issue()}, monkeypatch)
    done = watch(backlog_repo, env, "--every", "0.2", "--polls", "2")
    assert done.returncode == 1, done.stderr
    assert "nothing new after 2 waits" in done.stderr
    assert len(calls(where, "webhook", "forward")) == 2 and not calls(where, "api")     # both forwarded, none polled
