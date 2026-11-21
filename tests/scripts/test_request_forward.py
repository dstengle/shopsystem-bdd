"""`work watch --forward` (requests r57, r58) through the stand-in gh: a repository the account administers forwarded
(`gh webhook forward`, the extension installed when missing), one it does not polled through GitHub's notifications
and named on stderr, and a watch that finds nothing ended after its waits."""
import json
import subprocess
import sys

from backlog_testing import SCRIPTS, git
from batch_testing import STUB
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
        "q1 %s comment 9: %s#issuecomment-9 (`work sync` applies it)" % (OTHER, OTHER)]
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


def test_a_comment_listed_by_the_notifications_baseline_wakes_the_watch(backlog_repo, tmp_path_factory, monkeypatch):
    where = tmp_path_factory.mktemp("gh")
    request(backlog_repo, "q1", OTHER)
    env = world(backlog_repo, where, {OTHER: issue()}, monkeypatch)
    env["STUB_GH_NOT_ADMIN"], env["STUB_GH_BASELINE"] = "ex/ctx,ex/up", "1"     # no forward's event
    pending(where, {OTHER: issue(comments=[(OTHER + "#issuecomment-9", TURN)])})
    done = watch(backlog_repo, env, "--every", "0.2", "--polls", "5")
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines() == [
        "q1 %s comment 9: %s#issuecomment-9 (`work sync` applies it)" % (OTHER, OTHER)]
    assert "If-Modified-Since" not in " ".join(calls(where, "api")[0])


STAGED = '''import json, os, sys
calls, stub, how = os.environ["STUB_GH_CALLS"], sys.argv[1], os.environ["STAGED"]
argv = sys.argv[2:]
noted = [json.loads(line)["argv"] for line in open(calls)] if os.path.exists(calls) else []
first = argv[:1] == ["api"] and not any(c[:1] == ["api"] for c in noted)
if how == "end" and argv[:2] == ["webhook", "forward"] or how == "503" and first:
    open(calls, "a").write(json.dumps({"argv": argv}) + "\\n")
    if first:
        print("HTTP/2.0 503 Service Unavailable\\nX-Poll-Interval: 0\\n")
    sys.exit(1 if first else 0)
os.environ["STUB_GH_FAIL" if how == "fail" and first else "STUB_GH_BASELINE"] = "api --include" if first else "1"
os.execv(sys.executable, [sys.executable, stub, *argv])
'''


def staged(where, env, how):
    """The stand-in gh behind a script whose first notifications call fails (`fail`) or is a 503 (`503`), or whose
    forwards end at once (`end`); each later notifications call with no If-Modified-Since lists what is pending."""
    (where / "staged.py").write_text(STAGED)
    (where / "gh").write_text('#!/bin/sh\nexec %s %s %s "$@"\n' % (sys.executable, where / "staged.py",
                                                                    STUB))
    env["STAGED"] = how
    return env


def a_comment_after_the_start_is_reported(backlog_repo, tmp_path_factory, monkeypatch, how, unadministered):
    where = tmp_path_factory.mktemp("gh")
    request(backlog_repo, "q1", OTHER)
    env = staged(where, world(backlog_repo, where, {OTHER: issue()}, monkeypatch), how)
    env["STUB_GH_NOT_ADMIN"] = unadministered
    pending(where, {OTHER: issue(comments=[(OTHER + "#issuecomment-9", TURN)])})
    done = watch(backlog_repo, env, "--every", "0.2", "--polls", "5")
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines() == [
        "q1 %s comment 9: %s#issuecomment-9 (`work sync` applies it)" % (OTHER, OTHER)]
    return where


def test_a_failed_baseline_then_a_comment_is_reported(backlog_repo, tmp_path_factory, monkeypatch):
    where = a_comment_after_the_start_is_reported(backlog_repo, tmp_path_factory, monkeypatch, "fail", "ex/ctx,ex/up")
    assert [" ".join(argv).count("If-Modified-Since") for argv in calls(where, "api")][:2] == [0, 0]


def test_a_comment_before_a_delayed_ready_is_reported(backlog_repo, tmp_path_factory, monkeypatch):
    a_comment_after_the_start_is_reported(backlog_repo, tmp_path_factory, monkeypatch, "503", "ex/ctx,ex/up")


def test_a_comment_before_a_repository_first_polled_after_its_forward_is_reported(backlog_repo, tmp_path_factory,
                                                                                    monkeypatch):
    where = a_comment_after_the_start_is_reported(backlog_repo, tmp_path_factory, monkeypatch, "end", "")
    assert calls(where, "webhook", "forward") and calls(where, "api")
