"""supervision r27, r50 with the agent-time analysis of 2026-10-27: on a branch the initiatives share, a branch review of
i1 is due for unread commits that touch i1's own files, not for another initiative's commits."""
import pathlib
import subprocess
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from supervise_brief import Briefs
from supervise_review import Reviews


def git(repo, *args):
    return subprocess.run(["git", "-c", "user.name=T", "-c", "user.email=t@example.com", *args], cwd=repo,
                          capture_output=True, text=True, check=True).stdout


def commit(repo, rel, text, message):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD").strip()


class Stand(Reviews, Briefs):
    def __init__(self, root):
        self.root, self.dir = root, root / ".shop/work/i1"

    def rel(self, path):
        return str(pathlib.Path(path).relative_to(self.root))


def reviewed(repo, head):
    commit(repo, ".shop/work/i1/runs/branch-review/1/brief.md", "Head: %s\n" % head, "branch review 1 of i1")


def test_another_initiatives_commit_calls_for_no_review(tmp_path):
    git(tmp_path, "init", "-q")
    commit(tmp_path, ".shop/work/i1/initiative.md", "i1\n", "start i1")
    head = commit(tmp_path, ".shop/work/i1/w1.md", "green\n", "w1 green")
    reviewed(tmp_path, head)
    commit(tmp_path, ".shop/work/i2/w2.md", "green\n", "w2 green")
    commit(tmp_path, "scripts/thing.py", "x = 1\n", "w2's code")
    stand = Stand(tmp_path)
    assert stand.unread() and not stand.unread_mine()


def test_this_initiatives_new_work_calls_for_a_review(tmp_path):
    git(tmp_path, "init", "-q")
    commit(tmp_path, ".shop/work/i1/initiative.md", "i1\n", "start i1")
    head = commit(tmp_path, ".shop/work/i1/w1.md", "green\n", "w1 green")
    reviewed(tmp_path, head)
    commit(tmp_path, "scripts/thing.py", "x = 1\n", "w3's code")
    mine = commit(tmp_path, ".shop/work/i1/w3.md", "green\n", "w3 green")
    assert Stand(tmp_path).unread_mine() == [mine]
