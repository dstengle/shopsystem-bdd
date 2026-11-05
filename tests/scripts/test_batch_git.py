"""The batches' git and gh plumbing (workflow simplification plan 4, Task 1, D11, D17, D19, D20): `git` moved from
supervise_worker, the worktrees directory ignoring itself, worktrees on new and existing branches, the push to the
bare remote, the lock, and gh through the stand-in."""
import json
import subprocess
import sys

import batch_gh
import batch_git
import pytest
import supervise_worker
from backlog_testing import git
from batch_testing import gh_calls
from workqueue import Refused


def test_git_still_imports_from_supervise_worker():
    assert supervise_worker.git is batch_git.git and supervise_worker.GitFailed is batch_git.GitFailed


def test_delivery_reads_the_toml(batch_repo, batch_outside):
    assert batch_git.delivery(batch_repo)["batch"]["tests"] == "python3 -c pass"
    assert batch_git.delivery(batch_outside) == {}


def test_trees_dir_is_ignored(batch_repo):
    trees = batch_git.trees_dir(batch_repo)
    assert trees == batch_repo / ".shop" / "worktrees"
    batch_git.add_tree(batch_repo, trees / "batch-1-t1", "batch-1-b1", "main")
    assert (trees / "batch-1-t1" / "spec" / "index.md").is_file()
    assert git(batch_repo, "status", "--porcelain") == ""
    assert batch_git.current_branch(batch_repo) == "main"


def test_add_tree_on_an_existing_branch_keeps_its_commits(batch_repo):
    trees = batch_git.trees_dir(batch_repo)
    tree = batch_git.add_tree(batch_repo, trees / "one", "batch-1-b1", "main")
    (tree / "src.txt").write_text("built\n")
    git(tree, "add", "-A")
    git(tree, "commit", "-q", "-m", "build")
    head = git(tree, "rev-parse", "HEAD")
    batch_git.remove_tree(batch_repo, tree)
    assert not tree.exists()
    again = batch_git.add_tree(batch_repo, trees / "two", "batch-1-b1")
    assert git(again, "rev-parse", "HEAD") == head and (again / "src.txt").is_file()


def test_remove_tree_of_a_missing_path_is_quiet(batch_repo):
    batch_git.remove_tree(batch_repo, batch_repo / ".shop" / "worktrees" / "nothing")


def test_current_branch_of_a_detached_head_is_none(batch_repo):
    git(batch_repo, "checkout", "-q", "--detach")
    assert batch_git.current_branch(batch_repo) is None


def test_push_goes_to_the_bare_remote(batch_repo):
    git(batch_repo, "branch", "batch-1")
    assert batch_git.remote(batch_repo, "main") == "origin"
    batch_git.push(batch_repo, "origin", "batch-1")
    assert git(batch_repo, "ls-remote", "origin", "batch-1").split()[0] == git(batch_repo, "rev-parse", "batch-1").strip()


def test_a_refused_push_names_git(batch_repo, tmp_path):
    git(batch_repo, "branch", "batch-1")
    git(batch_repo, "remote", "set-url", "origin", str(tmp_path / "no-such-remote.git"))
    with pytest.raises(Refused) as refused:
        batch_git.push(batch_repo, "origin", "batch-1")
    assert str(refused.value).startswith("work batch: the push of batch-1 to origin failed: "), str(refused.value)


HOLD = """
import sys, time
sys.path.insert(0, %r)
import batch_git
with batch_git.locked(sys.argv[1]):
    start = time.monotonic()
    time.sleep(0.3)
    end = time.monotonic()
with open(sys.argv[2], "a") as out:
    out.write("%%f %%f\\n" %% (start, end))
"""


def test_locked_serialises(batch_repo, tmp_path):
    times = tmp_path / "times"
    code = HOLD % str(batch_git.SCRIPTS)
    procs = [subprocess.Popen([sys.executable, "-c", code, str(batch_repo), str(times)]) for _ in range(2)]
    assert [p.wait(timeout=30) for p in procs] == [0, 0]
    (a0, a1), (b0, b1) = sorted(tuple(map(float, line.split())) for line in times.read_text().splitlines())
    assert a1 <= b0, ((a0, a1), (b0, b1))


def test_gh_create_state_close_through_the_stand_in(batch_repo, batch_outside, monkeypatch):
    where = batch_outside
    url = batch_gh.create(batch_repo, "main", "batch-1", "batch-1: a title", "the body")
    assert url == "https://github.com/ex/ctx/pull/1"
    assert gh_calls(where)[0][:9] == ["pr", "create", "--draft", "--base", "main", "--head", "batch-1", "--title",
                                      "batch-1: a title"]
    assert batch_gh.state(batch_repo, url) == ("OPEN", None)
    (where / "gh-state.json").write_text(json.dumps({url: {"state": "MERGED", "mergeCommit": {"oid": "abc"}}}))
    assert batch_gh.state(batch_repo, url) == ("MERGED", "abc")
    batch_gh.close(batch_repo, url)
    assert gh_calls(where)[-1] == ["pr", "close", url]
    monkeypatch.setenv("STUB_GH_FAIL", "pr create")
    with pytest.raises(Refused, match="work batch: gh pr create failed: stand-in gh: refused"):
        batch_gh.create(batch_repo, "main", "batch-1", "t", "b")
    monkeypatch.delenv("STUB_GH_FAIL")
    assert batch_gh.create(batch_repo, "main", "batch-1", "t", "b") == "https://github.com/ex/ctx/pull/2"

