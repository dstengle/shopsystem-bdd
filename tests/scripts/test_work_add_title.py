"""work-queue r1, r7: `work add` writes a title as the `# ` heading; an empty title or one with a line break is refused."""
import pathlib
import subprocess
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import workqueue  # noqa: E402

INDEX = "---\nid: bounded-context/o/p/c\nkind: bounded-context\n---\n"


def git(repo, *args):
    return subprocess.run(["git", "-c", "user.name=T", "-c", "user.email=t@example.com", *args], cwd=repo,
                          capture_output=True, text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec/index.md").write_text(INDEX)
    (tmp_path / ".shop/work/i1").mkdir(parents=True)
    (tmp_path / ".shop/work/i1/.keep").write_text("")
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "T")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "start")
    return tmp_path


def add(repo, title):
    return workqueue.add(repo, "i1", title, "p", "c", ["c#r1"])


def test_a_title_with_a_slash_is_written_as_the_heading(repo):
    name = add(repo, "Show a/b")
    assert name == "w1"
    assert "\n# Show a/b\n" in (repo / ".shop/work/i1/w1.md").read_text()


@pytest.mark.parametrize("title, reason", [("", "empty"), ("Show\nstatus: ready", "newline"), ("Show\rthing", "newline")])
def test_an_empty_title_or_one_with_a_line_break_is_refused_and_changes_nothing(repo, title, reason):
    before = git(repo, "rev-parse", "HEAD")
    with pytest.raises(workqueue.Refused, match=reason):
        add(repo, title)
    assert git(repo, "rev-parse", "HEAD") == before
    assert git(repo, "status", "--porcelain") == ""
