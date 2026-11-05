"""The fix loop (workflow simplification plan 5, Task 4, D5, D11, D14, D15, D22): a fix-now finding fixed by commits on
its item's branch citing `Finding: f<m>`, checked and pushed by `work batch review`, and the re-review's brief reading
only the commits after the last review, with each finding's own."""
import subprocess

import batch_findings
import batch_merge
import batch_plan
import pytest
from backlog_testing import git, state, work
from batch_testing import commit_on, gh_calls, tree_of
from review_testing import (
    CLEAN,
    FIX_NOW_B1,
    FIXED_F1,
    URL,
    findings,
    head,
    ok,
    published,
    scratch,
)

TITLE = "abandon leaves the initiative started"


@pytest.fixture
def fixing(batch_repo):
    """The batch `building` after review 1, with f1 open on b1."""
    published(batch_repo)
    ok(work(batch_repo, "batch", "brief", "batch-1"))
    findings(batch_repo).write_text(FIX_NOW_B1)
    ok(work(batch_repo, "batch", "reviewed", "batch-1"))
    return batch_repo


def fix(repo, message="fix b1\n\nItem: b1\nFinding: f1"):
    return commit_on(repo, "batch-1-b1", "src/fix.txt", "fixed\n", message)


def remote(repo):
    return git(repo, "ls-remote", "origin")


def brief_text(repo, k=2):
    done = ok(work(repo, "batch", "brief", "batch-1"))
    assert done.stdout.strip().splitlines()[-1] == str(scratch(repo, k) / "brief.md")
    return (scratch(repo, k) / "brief.md").read_text()


def section(text, heading):
    return text.split("## %s\n" % heading, 1)[1].split("\n## ", 1)[0]


def test_the_re_review_brief_gives_the_commits_for_each_finding(fixing, batch_outside):
    """Review Focus 3."""
    last = batch_findings.reviews(fixing, "batch-1")[-1].head
    sha = fix(fixing)
    ok(work(fixing, "batch", "review", "batch-1"))
    assert batch_plan.find(fixing, "batch-1").status == "in-review"
    assert len([c for c in gh_calls(batch_outside) if c[:2] == ["pr", "create"]]) == 1
    text = brief_text(fixing)
    assert "Review: 2 (re-review of the fix)" in text and "Range: %s..%s" % (last, head(fixing)) in text
    assert "## Items" not in text
    earlier = section(text, "Earlier findings")
    assert "f1 Important fix now: %s" % TITLE in earlier and '%s "fix b1"' % sha[:7] in earlier
    want = git(fixing, "rev-list", "--reverse", "%s..batch-1" % last).split()
    listed = [line.split()[1] for line in section(text, "Commits").splitlines() if line.startswith("- ")]
    assert len(want) == 2 and len(listed) == 2 and all(w.startswith(s) for s, w in zip(listed, want))
    change = (scratch(fixing, 2) / "change.diff").read_text()
    assert "src/fix.txt" in change and "src/b1.txt" not in change


def refused_with_nothing_done(repo, where, named):
    before, pushed, calls = state(repo), remote(repo), gh_calls(where)
    done = work(repo, "batch", "review", "batch-1")
    assert done.returncode == 1, done.stdout
    for name in named:
        assert name in done.stderr, done.stderr
    assert state(repo) == before and remote(repo) == pushed and gh_calls(where) == calls
    assert batch_plan.find(repo, "batch-1").status == "building"


def test_review_refuses_a_fix_commit_that_cites_no_finding(fixing, batch_outside):
    """Review Focus 4."""
    fix(fixing)
    bare = commit_on(fixing, "batch-1-b1", "src/more.txt", "more\n", "more b1\n\nItem: b1")
    refused_with_nothing_done(fixing, batch_outside, ['%s "more b1"' % bare[:7], "Finding: f<m>"])


def test_review_refuses_an_open_finding_with_no_commit(fixing, batch_outside):
    """Review Focus 4."""
    refused_with_nothing_done(fixing, batch_outside, ['f1 b1 "Abandon"', "or park b1"])


def test_a_parked_items_finding_needs_no_fix(fixing):
    """Review Focus 3, D22."""
    ok(work(fixing, "batch", "park", "batch-1", "b1", "--question", TITLE))
    ok(work(fixing, "batch", "review", "batch-1"))
    text = brief_text(fixing)
    assert "the requirement lines of b1" in section(text, "Commits")
    assert "f1" not in section(text, "Earlier findings")
    findings(fixing, 2).write_text(CLEAN)
    ok(work(fixing, "batch", "reviewed", "batch-1"))
    assert batch_plan.find(fixing, "batch-1").status == "awaiting-merge"


@pytest.mark.parametrize("earlier, named", [("", "f1"), ("\n## Earlier findings\n- f1: fixed\n- f9: fixed\n", "f9")],
                         ids=["left-out", "not-open"])
def test_reviewed_refuses_a_re_review_that_leaves_out_an_open_finding(fixing, earlier, named):
    """Review Focus 1."""
    fix(fixing)
    ok(work(fixing, "batch", "review", "batch-1"))
    brief_text(fixing)
    findings(fixing, 2).write_text(CLEAN + earlier)
    before = state(fixing)
    done = work(fixing, "batch", "reviewed", "batch-1")
    assert done.returncode == 1 and named in done.stderr and "findings.md" in done.stderr, done.stderr
    assert state(fixing) == before


def test_a_fixed_finding_closes_and_the_review_is_clean(fixing):
    fix(fixing)
    ok(work(fixing, "batch", "review", "batch-1"))
    brief_text(fixing)
    findings(fixing, 2).write_text(FIXED_F1)
    ok(work(fixing, "batch", "reviewed", "batch-1"))
    assert batch_plan.find(fixing, "batch-1").status == "awaiting-merge"
    assert batch_findings.open_findings(fixing, "batch-1") == []


def test_a_finding_not_fixed_stays_open(fixing):
    fix(fixing)
    ok(work(fixing, "batch", "review", "batch-1"))
    brief_text(fixing)
    findings(fixing, 2).write_text(CLEAN + "\n## Earlier findings\n- f1: not fixed: still started\n")
    ok(work(fixing, "batch", "reviewed", "batch-1"))
    assert batch_plan.find(fixing, "batch-1").status == "building"
    assert [f.fid for f in batch_findings.open_findings(fixing, "batch-1")] == ["f1"]


def test_resume_gives_the_worktree_for_each_open_finding(fixing):
    tree = fixing / ".shop" / "worktrees" / "batch-1-t1"
    tip = head(fixing, "batch-1-b1")
    git(fixing, "worktree", "remove", "--force", str(tree))
    before = state(fixing)
    done = ok(work(fixing, "batch", "resume", "batch-1"))
    assert git(tree, "rev-parse", "HEAD").strip() == tip
    assert git(tree, "symbolic-ref", "--short", "HEAD").strip() == "batch-1-b1"
    assert ('f1 Important b1 "Abandon" src/b1.txt:1: %s: fix in %s on batch-1-b1 with Item: b1 and Finding: f1; '
            'then work batch review batch-1' % (TITLE, tree)) in done.stdout.splitlines()
    assert batch_plan.task(batch_plan.find(fixing, "batch-1"), "t1").status == "done"
    assert state(fixing) == before


def test_review_prints_the_next_step(fixing):
    fix(fixing)
    out = ok(work(fixing, "batch", "review", "batch-1")).stdout.strip().splitlines()
    assert out[-1] == URL
    assert out[-2] == "next: work batch brief batch-1, the pr-reviewer on it, then work batch reviewed batch-1"


TWO_FIX_NOW = FIX_NOW_B1 + """
### Important fix now: exit leaves the queue open
- item: b2
- where: src/b2.txt:1
The line says `closed`; the code writes `open`.
"""


def test_a_fix_may_merge_another_items_fix_to_resolve_a_conflict(batch_repo):
    """Review S1, Q1: f1 on b1 and f3 on b2 fixed in one file; b2's branch merges b1's to resolve the conflict, and
    its merged-in commit cites f1, an open finding of another in-batch item."""
    published(batch_repo)
    ok(work(batch_repo, "batch", "brief", "batch-1"))
    findings(batch_repo).write_text(TWO_FIX_NOW)
    ok(work(batch_repo, "batch", "reviewed", "batch-1"))
    commit_on(batch_repo, "batch-1-b1", "src/shared.txt", "f1\n", "fix f1\n\nItem: b1\nFinding: f1")
    commit_on(batch_repo, "batch-1-b2", "src/shared.txt", "f2\n", "fix f3\n\nItem: b2\nFinding: f3")
    tree = tree_of(batch_repo, "batch-1-b2")
    assert work(batch_repo, "batch", "review", "batch-1").returncode == 1
    subprocess.run(["git", "merge", "-q", "batch-1-b1"], cwd=tree, capture_output=True)
    spec = "spec/capabilities/work-queue.md"
    (tree / spec).write_text(batch_merge.settled(tree, spec))
    (tree / "src" / "shared.txt").write_text("f1\nf2\n")
    git(tree, "add", spec, "src/shared.txt")
    git(tree, "commit", "-q", "-m", "merge b1's fix\n\nItem: b2\nFinding: f3")
    ok(work(batch_repo, "batch", "review", "batch-1"))
    assert batch_plan.find(batch_repo, "batch-1").status == "in-review"


def test_the_brief_gives_each_commit_its_own_patch(fixing):
    """Review S4: each non-merge commit of the range has its patch, named in `## Commits` and under its finding."""
    sha = fix(fixing)
    ok(work(fixing, "batch", "review", "batch-1"))
    text = brief_text(fixing)
    patch = scratch(fixing, 2) / "commits" / ("%s.patch" % sha[:7])
    assert "patch: %s" % patch in section(text, "Earlier findings")
    line = next(c for c in section(text, "Commits").splitlines() if c.startswith("- %s " % sha[:7]))
    assert line.endswith("patch: %s" % patch)
    own = patch.read_text()
    assert "src/fix.txt" in own and "src/b1.txt" not in own and sha in own
    merges = [c.split()[1] for c in section(text, "Commits").splitlines() if c.startswith("- ") and "patch: " not in c]
    assert len(merges) == 1 and head(fixing).startswith(merges[0]), merges


def test_an_item_line_git_does_not_read_is_explained(fixing, batch_outside):
    """Review M3: `-m "Item: b1" -m "Finding: f1"` leaves `Item:` out of the last paragraph."""
    fix(fixing, "fix b1\n\nItem: b1\n\nFinding: f1")
    refused_with_nothing_done(fixing, batch_outside, ["cites no item", "git reads trailers from the last paragraph"])
