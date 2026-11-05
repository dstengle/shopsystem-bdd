"""The suite's git repositories run no background maintenance (plan 5 review, S6): a `git commit` would otherwise start
a detached `git maintenance run --auto`, whose `.git/objects/maintenance.lock` races a test's copy of the repository.
The root conftest.py sets `maintenance.auto` and `gc.auto` for every git the suite runs, `work`'s included."""
import subprocess


def config(where, key):
    return subprocess.run(["git", "config", "--get", key], cwd=where, capture_output=True, text=True).stdout.strip()


def test_a_test_repository_runs_no_background_maintenance(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    assert config(tmp_path, "maintenance.auto") == "false"
    assert config(tmp_path, "gc.auto") == "0"


def test_a_git_the_scripts_run_inherits_it(backlog_repo):
    import batch_git
    assert batch_git.git(backlog_repo, "config", "--get", "maintenance.auto").stdout.strip() == "false"
