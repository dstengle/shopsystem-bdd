"""store_git: the store adapter's checks (the decision "Git is the store and the isolation"; the domain contract
design, §6.2): a thing kept is one commit of its named files on the branch checked out, shared when that commit is on
the branch's upstream remote."""
import subprocess

import pytest
import store_git


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    remote, root = tmp_path / "remote.git", tmp_path / "repo"
    git(tmp_path, "init", "-q", "--bare", "-b", "main", str(remote))
    git(tmp_path, "init", "-q", "-b", "main", str(root))
    git(root, "config", "user.email", "t@example.com")
    git(root, "config", "user.name", "t")
    (root / "a.md").write_text("a\n")
    git(root, "add", "a.md")
    git(root, "commit", "-q", "-m", "first")
    git(root, "remote", "add", "origin", str(remote))
    git(root, "push", "-q", "-u", "origin", "main")
    return root


def commit(root, *names):
    for name in names:
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(name + "\n")
    git(root, "add", *names)
    git(root, "commit", "-q", "-m", "keep " + " ".join(names))


def test_kept_and_shared(repo):
    before = store_git.head(repo)
    commit(repo, "spec/decisions/0001-x.md", "spec/decisions/index.md")
    git(repo, "push", "-q")
    kept = store_git.kept(repo, before, ["spec/decisions/0001-x.md", "spec/decisions/index.md"])
    assert kept == git(repo, "rev-parse", "HEAD")
    assert store_git.shared(repo, kept) is True
    assert store_git.unshared(repo, before) is None


def test_kept_not_shared(repo):
    before = store_git.head(repo)
    commit(repo, "b.md")
    kept = store_git.kept(repo, before, ["b.md"])
    assert kept is not None and store_git.shared(repo, kept) is False
    assert store_git.unshared(repo, before) == "origin"


def test_a_thing_is_kept_in_one_commit_of_its_files(repo):
    before = store_git.head(repo)
    commit(repo, "b.md")
    commit(repo, "c.md")
    assert store_git.kept(repo, before, ["b.md"]) is not None
    assert store_git.kept(repo, before, ["b.md", "c.md"]) is None


def test_nothing_kept_on_a_refusal(repo):
    before = store_git.head(repo)
    assert store_git.kept(repo, before, ["b.md"]) is None
    assert store_git.unshared(repo, before) is None


def test_no_remote_no_sharing(tmp_path):
    root = tmp_path / "solo"
    git(tmp_path, "init", "-q", "-b", "main", str(root))
    git(root, "config", "user.email", "t@example.com")
    git(root, "config", "user.name", "t")
    before = store_git.head(root)
    commit(root, "a.md")
    kept = store_git.kept(root, before, ["a.md"])
    assert kept is not None and store_git.shared(root, kept) is None
