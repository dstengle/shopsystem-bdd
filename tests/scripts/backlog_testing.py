"""What the backlog's script tests share: `work` run in a repository, git read there, and an item file written by
hand (the fixture `backlog_repo` is in conftest.py)."""
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def work(repo, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / "work"), "--root", str(repo), *args], capture_output=True,
                          text=True)


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True).stdout


def state(repo):
    """HEAD and the tree's changes: what a refused command must leave as they were."""
    return git(repo, "rev-parse", "HEAD"), git(repo, "status", "--porcelain")


def item_text(name="b1", title="Fix the parser", status="idea", provenance="own", value="", urgency="", size="",
              depends_on="", body=""):
    return ("---\nid: item/ex.com/prod/ctx/%s\nkind: item\nstatus: %s\nprovenance: %s\nvalue: %s\nurgency: %s\n"
            "size: %s\ndepends_on: [%s]\n---\n\n# %s\n%s" % (name, status, provenance, value, urgency, size,
                                                             depends_on, title, body)).replace(": \n", ":\n")


def write_item(repo, name="b1", commit=True, **fields):
    path = Path(repo) / ".shop" / "backlog" / ("%s.md" % name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(item_text(name, **fields))
    if commit:
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "write %s" % name)
    return path
