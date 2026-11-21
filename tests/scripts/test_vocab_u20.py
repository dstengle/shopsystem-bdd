"""U20's check after a generated scenario (tests/scenarios/vocab.py, b60): a run made while the repository's branch
checked out is a task's (`batch-<n>-b<j>`) keeps no change there: a commit on that branch since the run began fails
U20, naming the task; a run on any other branch, or one that kept nothing, passes."""
import subprocess

from test_vocab_u17 import vocab

DONE = {"args": ["work", "idea", "x"], "returncode": 0, "stdout": "", "stderr": "", "changed": [], "unshared": None}


def git(repo, *args):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args], cwd=repo,
                          capture_output=True, text=True, check=True).stdout


def test_a_change_kept_on_a_task_branch_fails_u20_naming_the_task():
    problems = vocab().u_problems([dict(DONE, task="task t1 of batch-1", kept=True)])
    assert len(problems) == 1 and problems[0].startswith("U20:") and "task t1 of batch-1" in problems[0]


def test_nothing_kept_on_a_task_branch_or_a_change_kept_elsewhere_passes():
    assert vocab().u_problems([dict(DONE, returncode=1, stderr="work: refused\n", task="task t1 of batch-1",
                                    kept=False)]) == []
    assert vocab().u_problems([dict(DONE, task=None, kept=True)]) == []


def test_tasked_reads_the_task_of_the_branch_and_whether_a_commit_was_kept_on_it(tmp_path):
    u = vocab()
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "commit", "-q", "--allow-empty", "-m", "init")
    at = u.store_git.head(tmp_path)
    assert u.tasked(tmp_path, at) == {"task": None, "kept": False}
    git(tmp_path, "checkout", "-q", "-b", "batch-1-b1")
    at = u.store_git.head(tmp_path)
    assert u.tasked(tmp_path, at) == {"task": "a task of batch-1", "kept": False}
    git(tmp_path, "commit", "-q", "--allow-empty", "-m", "kept")
    assert u.tasked(tmp_path, at) == {"task": "a task of batch-1", "kept": True}
