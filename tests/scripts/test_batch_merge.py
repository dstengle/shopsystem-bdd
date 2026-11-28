"""The merge of a task's branch by batch_merge (plan 4; b491, b874): the paths the apply writes kept as the batch's
branch holds them with the task's own changes after its lines, any other conflict refused naming the file and the
items, a recorded resolution used again."""
import subprocess

import batch_merge
import pytest
from backlog_testing import git
from plumbing.shop_files import Refused

HEAD = "---\nid: x\nunbuilt: [%s]\n---\n\n# X\n\n%s\n"


def _rebuilt(tmp_path, body="body"):
    """`theirs` a task's branch: its lines commit (the apply's outputs: `spec/cap.md`'s `unbuilt:`, a feature) and,
    after it, the task's own work under `spec/` (its body corrected, a decision added, its `r2` built) and in code;
    `main` the batch's branch, the specification rebuilt there with `body`. The lines commit."""
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "config", "user.email", "t@ex.com")
    git(tmp_path, "config", "user.name", "t")
    cap = tmp_path / "spec" / "cap.md"
    cap.parent.mkdir()
    cap.write_text(HEAD % ("r1", "body"))
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "base")
    git(tmp_path, "checkout", "-q", "-b", "theirs")
    cap.write_text(HEAD % ("r1, r2, r3", "body"))
    (tmp_path / "features").mkdir()
    (tmp_path / "features" / "cap.feature").write_text("by the task's apply\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "theirs: the requirement lines")
    since = git(tmp_path, "rev-parse", "HEAD").strip()
    cap.write_text(HEAD % ("r1, r3", "body corrected"))
    (tmp_path / "spec" / "theirs.md").write_text("theirs\n")
    (tmp_path / "code.py").write_text("x = 1\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "theirs: r2 built")
    git(tmp_path, "checkout", "-q", "main")
    cap.write_text(HEAD % ("r1, r2, r3, r9", body))
    git(tmp_path, "commit", "-q", "-am", "ours: the rebuild")
    return since


def test_a_path_the_apply_writes_is_kept_as_the_rebuild_holds_it_with_the_task_s_own_changes(tmp_path):
    """b874, review f1: `spec/` is the rebuild's, so the apply's outputs on the task's branch (a file its lines
    commit added) are not taken, while what the task changed there after its lines commit is (a corrected body, a
    decision it added), `unbuilt:` left as the rebuild holds it; its other changes are merged."""
    since = _rebuilt(tmp_path)
    batch_merge.merge(tmp_path, "theirs", "merge theirs", since=since)
    assert (tmp_path / "spec" / "cap.md").read_text() == HEAD % ("r1, r2, r3, r9", "body corrected")
    assert (tmp_path / "spec" / "theirs.md").read_text() == "theirs\n"
    assert not (tmp_path / "features" / "cap.feature").exists() and (tmp_path / "code.py").read_text() == "x = 1\n"
    assert git(tmp_path, "log", "-1", "--format=%s") == "merge theirs\n" and not git(tmp_path, "status", "--porcelain")


def test_a_task_s_own_change_the_rebuild_changed_otherwise_is_refused_naming_the_path(tmp_path):
    """b874, review f1: a task's change to a path the apply writes that does not merge with the rebuild is refused,
    naming the path and the item, and nothing is merged."""
    since = _rebuilt(tmp_path, body="body rebuilt")
    head = git(tmp_path, "rev-parse", "HEAD")
    with pytest.raises(Refused) as refused:
        batch_merge.merge(tmp_path, "theirs", "merge theirs", 'b2 "Two"', since=since)
    assert str(refused.value) == ('theirs does not merge: spec/cap.md, as b2 "Two" changed it after its lines, '
                                  "conflicts with the batch's rebuilt specification")
    assert git(tmp_path, "rev-parse", "HEAD") == head and not git(tmp_path, "status", "--porcelain")


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
