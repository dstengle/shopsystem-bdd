"""`work batch review` (workflow simplification plan 4, Task 5, D5, D10, D11): every task of an in-batch item done,
their branches merged into `batch-<n>` in plan order, the tests run there, the branch pushed and a draft pull request
created citing each item; a parked item's commits left out; a review that fails halfway leaves things as they were."""
import json

import batch_plan
import pytest
from backlog_testing import git, state, work
from batch_testing import commit_on, gh_calls
from test_batch_tasks import build, resumed, started  # noqa: F401  (the fixture)

URL = "https://github.com/ex/ctx/pull/1"


@pytest.fixture
def both_done(started):  # noqa: F811
    resumed(started)
    build(started, "t1", "b1", ["r5"])
    build(started, "t2", "b2", ["r6"])
    for task in ("t1", "t2"):
        done = work(started, "batch", "done", "batch-1", task)
        assert done.returncode == 0, done.stderr
    return started


def remote_head(repo):
    found = git(repo, "ls-remote", "origin", "refs/heads/batch-1").split()
    return found[0] if found else None


def creates(where):
    return [c for c in gh_calls(where) if c[:2] == ["pr", "create"]]


def body_of(call):
    return call[call.index("--body") + 1]


def test_review_publishes_the_pull_request(both_done, batch_outside):
    done = work(both_done, "batch", "review", "batch-1")
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip().splitlines()[-1] == URL
    batch = batch_plan.find(both_done, "batch-1")
    assert batch.status == "in-review" and batch.pull_request == URL
    assert git(both_done, "log", "-1", "--format=%s").strip() == "work batch review: batch-1 -> in-review %s" % URL
    assert remote_head(both_done) == git(both_done, "rev-parse", "batch-1").strip()
    for item in ("b1", "b2"):
        assert git(both_done, "merge-base", "--is-ancestor", "batch-1-%s" % item, "batch-1") == ""
    call, = creates(batch_outside)
    assert call[:7] == ["pr", "create", "--draft", "--base", "main", "--head", "batch-1"]
    assert call[call.index("--title") + 1] == "batch-1: Abandon; Exit"
    assert '- b1 "Abandon": work-queue#r5' in body_of(call) and '- b2 "Exit": work-queue#r6' in body_of(call)
    # both tasks took their own id out of the one `unbuilt:` line: the merge settles it (batch_merge)
    assert "unbuilt: []" in git(both_done, "show", "batch-1:spec/capabilities/work-queue.md")
    merges = git(both_done, "log", "--merges", "--format=%B%x00", "batch-1").split("\x00")
    assert any('batch-1: b1 "Abandon"' in m and "Item: b1" in m for m in merges), merges


def test_a_parked_items_commits_are_not_published(both_done, batch_outside):
    parked = commit_on(both_done, "batch-1-b2", "src/b2.txt", "more\n", "more b2\n\nItem: b2")
    assert work(both_done, "batch", "park", "batch-1", "b2", "--question", "Which?").returncode == 0
    done = work(both_done, "batch", "review", "batch-1")
    assert done.returncode == 0, done.stderr
    assert parked not in git(both_done, "rev-list", "origin/batch-1").split()
    assert 'parked: b2 "Exit" (needs-input)' in body_of(creates(batch_outside)[0])


def test_review_refuses_a_task_not_done(started, batch_outside):  # noqa: F811
    resumed(started)
    build(started, "t1", "b1", ["r5"])
    assert work(started, "batch", "done", "batch-1", "t1").returncode == 0
    before = state(started)
    done = work(started, "batch", "review", "batch-1")
    assert done.returncode == 1 and 'work batch review: batch-1: t2 b2 "Exit" is running, not done' in done.stderr
    assert remote_head(started) is None and gh_calls(batch_outside) == [] and state(started) == before


def test_review_refuses_an_uncited_commit(both_done, batch_outside):
    sha = commit_on(both_done, "batch-1-b1", "src/x.txt", "x\n", "no trailer")
    before = state(both_done)
    done = work(both_done, "batch", "review", "batch-1")
    assert done.returncode == 1 and '%s "no trailer"' % sha[:7] in done.stderr, done.stderr
    assert remote_head(both_done) is None and gh_calls(batch_outside) == [] and state(both_done) == before


def conflict(repo):
    commit_on(repo, "batch-1-b1", "src/shared.txt", "one\n", "b1 shares\n\nItem: b1")
    commit_on(repo, "batch-1-b2", "src/shared.txt", "two\n", "b2 shares\n\nItem: b2")


def failing(repo):
    (repo / ".shop" / "delivery.toml").write_text("[batch]\ntests = \"python3 -c 'import sys; sys.exit(4)'\"\n")
    git(repo, "commit", "-q", "-am", "failing tests")


def no_remote(repo):
    git(repo, "remote", "set-url", "origin", str(repo.parent / "no-such-remote.git"))


def gh_fails(repo, monkeypatch):
    monkeypatch.setenv("STUB_GH_FAIL", "pr create")


CAUSES = {"conflict": (conflict, 'b2 "Exit"'), "tests": (failing, "exit 4"),
          "push": (no_remote, "the push of batch-1 to origin failed"), "gh": (gh_fails, "work batch review: gh pr create failed")}


@pytest.mark.parametrize("cause", sorted(CAUSES))
def test_a_failed_review_leaves_the_batch_building(both_done, monkeypatch, cause):
    """Review Focus 3."""
    make, named = CAUSES[cause]
    make(both_done, monkeypatch) if cause == "gh" else make(both_done)
    head, branch = git(both_done, "rev-parse", "HEAD"), git(both_done, "rev-parse", "batch-1")
    done = work(both_done, "batch", "review", "batch-1")
    assert done.returncode == 1 and named in done.stderr, done.stderr
    assert batch_plan.find(both_done, "batch-1").status == "building"
    assert git(both_done, "rev-parse", "batch-1") == branch and git(both_done, "rev-parse", "HEAD") == head
    assert cause == "push" or remote_head(both_done) is None
    if cause == "gh":
        monkeypatch.delenv("STUB_GH_FAIL")
        again = work(both_done, "batch", "review", "batch-1")
        assert again.returncode == 0, again.stderr
        assert batch_plan.find(both_done, "batch-1").status == "in-review"


def test_a_second_review_pushes_only(both_done, batch_outside):
    assert work(both_done, "batch", "review", "batch-1").returncode == 0
    path = both_done / ".shop/batches/1/plan.md"
    path.write_text(path.read_text().replace("status: in-review", "status: building"))
    git(both_done, "commit", "-q", "-am", "the fix loop")
    fix = commit_on(both_done, "batch-1-b1", "src/fix.txt", "fixed\n", "fix b1\n\nItem: b1")
    done = work(both_done, "batch", "review", "batch-1")
    assert done.returncode == 0, done.stderr
    assert git(both_done, "merge-base", "--is-ancestor", fix, "origin/batch-1") == ""
    assert len(creates(batch_outside)) == 1
    assert batch_plan.find(both_done, "batch-1").status == "in-review"


def test_review_leaves_the_checkout_alone(both_done):
    """Review Focus 2."""
    (both_done / "notes.txt").write_text("mine\n")
    git(both_done, "add", "notes.txt")
    git(both_done, "commit", "-q", "-m", "notes")
    (both_done / "notes.txt").write_text("mine, edited\n")
    spec = git(both_done, "rev-parse", "HEAD:spec")
    assert work(both_done, "batch", "review", "batch-1").returncode == 0
    assert git(both_done, "status", "--porcelain") == " M notes.txt\n"
    assert git(both_done, "symbolic-ref", "--short", "HEAD").strip() == "main"
    assert git(both_done, "rev-parse", "HEAD:spec") == spec
    assert json.loads(work(both_done, "batch", "status", "--json").stdout)["batch"]["status"] == "in-review"


def test_a_failed_review_removes_the_worktree_it_made(both_done):
    tree = both_done / ".shop" / "worktrees" / "batch-1"
    git(both_done, "worktree", "remove", "--force", str(tree))
    conflict(both_done)
    done = work(both_done, "batch", "review", "batch-1")
    assert done.returncode == 1 and "does not merge" in done.stderr, done.stderr
    assert not tree.exists()
    again = work(both_done, "batch", "status", "batch-1")
    assert "batch-1 building" in again.stdout


def test_a_pull_request_created_by_a_failing_gh_is_kept(both_done, batch_outside, monkeypatch):
    """Plan 4 review, M5: gh created the pull request, then failed; the review finds it and does not put back."""
    monkeypatch.setenv("STUB_GH_LATE", "pr create")
    done = work(both_done, "batch", "review", "batch-1")
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip().splitlines()[-1] == URL
    assert batch_plan.find(both_done, "batch-1").pull_request == URL
    assert remote_head(both_done) == git(both_done, "rev-parse", "batch-1").strip()
    assert len(creates(batch_outside)) == 1
