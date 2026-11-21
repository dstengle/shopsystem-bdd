"""`work chore` (b316): an item's `## Chore` written and replaced, a path under spec/, features/ or .shop/ or outside
the repository refused, the paths a chore covers, and its check run."""
import backlog_chore
import backlog_items
from backlog_testing import git, state, work, write_item


def test_chore_written_then_replaced_and_committed(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "chore", "b1", "--file", "scripts/a.py", "--file", "docs/", "--check", "true")
    assert done.returncode == 0, done.stderr
    item = backlog_items.find(ready_repo, "b1")
    assert backlog_chore.read(item) == backlog_chore.Chore(("scripts/a.py", "docs/"), "true")
    assert git(ready_repo, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]
    assert work(ready_repo, "chore", "b1", "--file", "README.md", "--check", "false").returncode == 0
    assert backlog_chore.read(backlog_items.find(ready_repo, "b1")) == backlog_chore.Chore(("README.md",), "false")


def test_owned_or_outside_paths_refused(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    before = state(ready_repo)
    for path in ("spec/index.md", "features/x.feature", ".shop/backlog/b2.md", "../elsewhere", "/etc/passwd"):
        done = work(ready_repo, "chore", "b1", "--file", path, "--check", "true")
        assert done.returncode == 1 and path in done.stderr, (path, done.stderr)
    assert state(ready_repo) == before


def test_in_batch_item_refused(ready_repo):
    write_item(ready_repo, "b1", status="in-batch")
    before = state(ready_repo)
    done = work(ready_repo, "chore", "b1", "--file", "scripts/a.py", "--check", "true")
    assert done.returncode == 1 and "in-batch" in done.stderr, done.stderr
    assert state(ready_repo) == before


def test_covers_files_and_directories():
    chore = backlog_chore.Chore(("scripts/a.py", "docs/"), "true")
    assert backlog_chore.outside(chore, ["scripts/a.py", "docs/x/y.md", "scripts/b.py", "docsx.md"]) == [
        "scripts/b.py", "docsx.md"]


def test_check_run_in_the_tree(tmp_path):
    (tmp_path / "f").write_text("x")
    assert backlog_chore.run(backlog_chore.Chore(("f",), "test -f f"), tmp_path)[0] == 0
    assert backlog_chore.run(backlog_chore.Chore(("f",), "test -f g"), tmp_path)[0] == 1
