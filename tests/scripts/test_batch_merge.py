"""The settle of the `unbuilt:` line by batch_merge (plan 4, Deviation 1; plan 4 review, M6): the base's ids kept by
both sides, and every id either side added."""
import batch_merge
from backlog_testing import git

HEAD = "---\nid: x\nunbuilt: [%s]\n---\n\n# X\n\nbody\n"


def test_an_id_one_side_added_is_kept(tmp_path):
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "config", "user.email", "t@ex.com")
    git(tmp_path, "config", "user.name", "t")
    cap = tmp_path / "cap.md"
    cap.write_text(HEAD % "r1, r2, r3")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "base")
    git(tmp_path, "checkout", "-q", "-b", "theirs")
    cap.write_text(HEAD % "r1, r3")
    git(tmp_path, "commit", "-q", "-am", "theirs: r2 built")
    git(tmp_path, "checkout", "-q", "main")
    cap.write_text(HEAD % "r2, r3, r9")
    git(tmp_path, "commit", "-q", "-am", "ours: r1 built, r9 added")
    batch_merge.merge(tmp_path, "theirs", "merge theirs")
    assert cap.read_text() == HEAD % "r3, r9"
    assert git(tmp_path, "log", "-1", "--format=%s") == "merge theirs\n"
