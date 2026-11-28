"""The merge of a task's branch by batch_merge (plan 4; b491, b874): the paths the apply writes kept as the batch's
branch holds them, any other conflict refused naming the file and the items, a recorded resolution used again."""
import subprocess

import batch_merge
import pytest
from backlog_testing import git
from plumbing.shop_files import Refused

HEAD = "---\nid: x\nunbuilt: [%s]\n---\n\n# X\n\nbody\n"


def test_a_path_the_apply_writes_is_kept_as_the_batch_branch_holds_it(tmp_path):
    """b874: `spec/` is the rebuild's, so a conflict there keeps the batch branch's side, and a file only the merged
    branch added there is taken out; its other changes are merged."""
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "config", "user.email", "t@ex.com")
    git(tmp_path, "config", "user.name", "t")
    cap = tmp_path / "spec" / "cap.md"
    cap.parent.mkdir()
    cap.write_text(HEAD % "r1, r2, r3")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "base")
    git(tmp_path, "checkout", "-q", "-b", "theirs")
    cap.write_text(HEAD % "r1, r3")
    (tmp_path / "spec" / "theirs.md").write_text("theirs\n")
    (tmp_path / "code.py").write_text("x = 1\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "theirs: r2 built")
    git(tmp_path, "checkout", "-q", "main")
    cap.write_text(HEAD % "r2, r3, r9")
    git(tmp_path, "commit", "-q", "-am", "ours: the rebuild")
    batch_merge.merge(tmp_path, "theirs", "merge theirs")
    assert cap.read_text() == HEAD % "r2, r3, r9"
    assert not (tmp_path / "spec" / "theirs.md").exists() and (tmp_path / "code.py").read_text() == "x = 1\n"
    assert git(tmp_path, "log", "-1", "--format=%s") == "merge theirs\n"


def _two_sides(tmp_path):
    """A file whose first line `ours` (main) and `theirs` change otherwise."""
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "config", "user.email", "t@ex.com")
    git(tmp_path, "config", "user.name", "t")
    shared = tmp_path / "shared.txt"
    shared.write_text("a\nb\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "base")
    git(tmp_path, "checkout", "-q", "-b", "theirs")
    shared.write_text("theirs\nb\n")
    git(tmp_path, "commit", "-q", "-am", "theirs")
    git(tmp_path, "checkout", "-q", "main")
    shared.write_text("ours\nb\n")
    git(tmp_path, "commit", "-q", "-am", "ours")
    return shared


def test_a_conflict_left_is_refused_naming_the_file_and_both_items(tmp_path):
    _two_sides(tmp_path)
    head = git(tmp_path, "rev-parse", "HEAD")
    with pytest.raises(Refused) as refused:
        batch_merge.merge(tmp_path, "theirs", "merge theirs", 'b2 "Two"', [('b1 "One"', "main")])
    assert str(refused.value) == 'theirs does not merge: shared.txt conflicts between b2 "Two" and b1 "One"'
    assert git(tmp_path, "rev-parse", "HEAD") == head and not git(tmp_path, "status", "--porcelain")


def test_a_recorded_resolution_is_used_again(tmp_path):
    """A conflict settled by hand once with rerere on merges by itself the next time (b491)."""
    shared = _two_sides(tmp_path)
    head = git(tmp_path, "rev-parse", "HEAD").strip()
    subprocess.run(["git", "-c", "rerere.enabled=true", "merge", "-q", "theirs"], cwd=tmp_path, capture_output=True)
    shared.write_text("ours and theirs\nb\n")
    git(tmp_path, "add", "shared.txt")
    git(tmp_path, "-c", "rerere.enabled=true", "commit", "-q", "--no-edit")
    git(tmp_path, "reset", "-q", "--hard", head)
    batch_merge.merge(tmp_path, "theirs", "merge theirs")
    assert shared.read_text() == "ours and theirs\nb\n"
    assert git(tmp_path, "log", "-1", "--format=%s") == "merge theirs\n"
