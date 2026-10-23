"""work-queue r7: `work withdraw` of a work-item already withdrawn has nothing to transition and commits nothing."""
import pathlib
import subprocess
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import workqueue

ITEM = "---\nid: work-item/x/w1\nkind: work-item\nstatus: withdrawn\n---\n\n# w1\n"


def git(repo, *args):
    return subprocess.run(["git", "-c", "user.name=T", "-c", "user.email=t@example.com", *args], cwd=repo,
                          capture_output=True, text=True, check=True).stdout


def test_withdrawing_a_withdrawn_work_item_is_refused_and_commits_nothing(tmp_path):
    (tmp_path / ".shop/work/i1").mkdir(parents=True)
    (tmp_path / ".shop/work/i1/w1.md").write_text(ITEM)
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "T")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "w1")
    before = git(tmp_path, "rev-parse", "HEAD")
    with pytest.raises(workqueue.Refused, match="withdrawn"):
        workqueue.withdraw(tmp_path, "w1")
    assert git(tmp_path, "rev-parse", "HEAD") == before
    assert git(tmp_path, "status", "--porcelain") == ""
