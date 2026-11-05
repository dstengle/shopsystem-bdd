"""A batch's worktree paths (plan 4 review, S1): a directory at a worktree's path that is not that worktree is never
used as one. An empty one is made the worktree; anything else is refused, naming the path, and the base checkout is
left as it was."""
import batch_git
from backlog_testing import git, state, work
from test_batch_review import both_done, failing  # noqa: F401  (the fixture)
from test_batch_tasks import build, resumed, started, tree  # noqa: F401  (the fixture)

INDEX = "spec/index.md"


def dirty(repo):
    path = repo / INDEX
    path.write_text(path.read_text() + "\nthe person's edit\n")
    return git(repo, "status", "--porcelain")


def test_is_tree_is_the_worktree_on_its_branch(started):  # noqa: F811
    resumed(started)
    assert batch_git.is_tree(tree(started, "t1"), "batch-1-b1")
    assert not batch_git.is_tree(tree(started, "t1"), "batch-1-b2")
    assert not batch_git.is_tree(started / "spec", "main")
    assert not batch_git.is_tree(started / "nowhere", "main")


def test_review_makes_its_worktree_in_an_empty_directory(both_done):  # noqa: F811
    batch_tree = both_done / ".shop" / "worktrees" / "batch-1"
    git(both_done, "worktree", "remove", "--force", str(batch_tree))
    batch_tree.mkdir()
    failing(both_done)
    was, head = dirty(both_done), git(both_done, "rev-parse", "HEAD")
    done = work(both_done, "batch", "review", "batch-1")
    assert done.returncode == 1 and "exit 4" in done.stderr, done.stderr
    assert git(both_done, "status", "--porcelain") == was and git(both_done, "rev-parse", "HEAD") == head
    assert "the person's edit" in (both_done / INDEX).read_text()


def test_review_refuses_a_directory_that_is_not_its_worktree(both_done):  # noqa: F811
    batch_tree = both_done / ".shop" / "worktrees" / "batch-1"
    git(both_done, "worktree", "remove", "--force", str(batch_tree))
    batch_tree.mkdir()
    (batch_tree / "mine.txt").write_text("x\n")
    dirty(both_done)
    before = state(both_done)
    done = work(both_done, "batch", "review", "batch-1")
    assert done.returncode == 1 and str(batch_tree) in done.stderr and "not the worktree" in done.stderr, done.stderr
    assert state(both_done) == before and (batch_tree / "mine.txt").is_file()


def test_resume_makes_a_task_worktree_in_an_empty_directory(started):  # noqa: F811
    resumed(started)
    git(started, "worktree", "remove", "--force", str(tree(started, "t1")))
    tree(started, "t1").mkdir()
    was = dirty(started)
    resumed(started)
    assert batch_git.is_tree(tree(started, "t1"), "batch-1-b1")
    assert git(started, "status", "--porcelain") == was


def test_done_refuses_a_directory_that_is_not_its_worktree(started):  # noqa: F811
    resumed(started)
    build(started, "t1", "b1", ["r5"])
    git(started, "worktree", "remove", "--force", str(tree(started, "t1")))
    tree(started, "t1").mkdir()
    before = state(started)
    done = work(started, "batch", "done", "batch-1", "t1")
    assert done.returncode == 1 and "has no worktree" in done.stderr, done.stderr
    assert state(started) == before
