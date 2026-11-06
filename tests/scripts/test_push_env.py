"""The environment of `work`'s push (backlog r19): ssh in batch mode added to the command git would use, never
overriding the repository's `core.sshCommand` nor a `$GIT_SSH` (review 1 of batch-8, f1)."""
import subprocess

import pytest
from shop_files import push_env


@pytest.fixture
def repo(tmp_path, monkeypatch):
    for name in ("GIT_SSH_COMMAND", "GIT_SSH"):
        monkeypatch.delenv(name, raising=False)
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    return tmp_path


def configure(repo, command):
    subprocess.run(["git", "config", "core.sshCommand", command], cwd=repo, check=True)


def test_no_ssh_setting_runs_ssh_in_batch_mode(repo):
    env = push_env(repo)
    assert env["GIT_SSH_COMMAND"] == "ssh -o BatchMode=yes"
    assert env["GIT_TERMINAL_PROMPT"] == "0"


def test_core_ssh_command_is_kept_with_batch_mode(repo):
    configure(repo, "ssh -i ~/.ssh/deploy_key")
    assert push_env(repo)["GIT_SSH_COMMAND"] == "ssh -i ~/.ssh/deploy_key -o BatchMode=yes"


def test_git_ssh_command_wins_over_core_ssh_command(repo, monkeypatch):
    configure(repo, "ssh -i ~/.ssh/deploy_key")
    monkeypatch.setenv("GIT_SSH_COMMAND", "ssh -p 2222")
    assert push_env(repo)["GIT_SSH_COMMAND"] == "ssh -p 2222 -o BatchMode=yes"


def test_git_ssh_leaves_the_ssh_environment_alone(repo, monkeypatch):
    monkeypatch.setenv("GIT_SSH", "plink")
    env = push_env(repo)
    assert "GIT_SSH_COMMAND" not in env
    assert env["GIT_SSH"] == "plink"
    assert env["GIT_TERMINAL_PROMPT"] == "0"


def test_core_ssh_command_wins_over_git_ssh(repo, monkeypatch):
    configure(repo, "ssh -i ~/.ssh/deploy_key")
    monkeypatch.setenv("GIT_SSH", "plink")
    assert push_env(repo)["GIT_SSH_COMMAND"] == "ssh -i ~/.ssh/deploy_key -o BatchMode=yes"


def test_with_no_root_the_current_directory_is_read(repo, monkeypatch):
    configure(repo, "ssh -i ~/.ssh/deploy_key")
    monkeypatch.chdir(repo)
    assert push_env()["GIT_SSH_COMMAND"] == "ssh -i ~/.ssh/deploy_key -o BatchMode=yes"
