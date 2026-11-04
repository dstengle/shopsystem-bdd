"""What the backlog's script tests share: `work` run in a repository, git read there, and an item file written by
hand (the fixture `backlog_repo` is in conftest.py)."""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def work(repo, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / "work"), "--root", str(repo), *args], capture_output=True,
                          text=True, timeout=60)


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True).stdout


def state(repo):
    """HEAD and the tree's changes: what a refused command must leave as they were."""
    return git(repo, "rev-parse", "HEAD"), git(repo, "status", "--porcelain")


def item_text(name="b1", title="Fix the parser", status="idea", provenance="own", value="", urgency="", size="",
              depends_on="", body="", kind="item"):
    return ("---\nid: item/ex.com/prod/ctx/%s\nkind: %s\nstatus: %s\nprovenance: %s\nvalue: %s\nurgency: %s\n"
            "size: %s\ndepends_on: [%s]\n---\n\n# %s\n%s" % (name, kind, status, provenance, value, urgency, size,
                                                             depends_on, title, body)).replace(": \n", ":\n")


def write_item(repo, name="b1", commit=True, **fields):
    path = Path(repo) / ".shop" / "backlog" / ("%s.md" % name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(item_text(name, **fields))
    if commit:
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "write %s" % name)
    return path


def request_text(name="q1", asker="bounded-context/ex.com/prod/peer", status="open", turn="upstream",
                 lines=(), outcomes=(), title="Archive old items"):
    """A request's file in the form `workqueue_request.request` writes it, with the line outcomes given."""
    numbered = "".join("%d. %s\n" % e for e in enumerate(lines, 1))
    settled = "".join("%d. %s\n" % e for e in enumerate(outcomes, 1) if e[1])
    return ("---\nid: request/ex.com/prod/ctx/%s\nkind: request\nasker: %s\npart_of: job-thread/ex.com/prod/t1\n"
            "status: %s\nturn: %s\n---\n\n# %s\n\n## Lines\n%s\n## Questions\n\n## Answers\n\n## Outcomes\n%s\n"
            "## Resolution\n" % (name, asker, status, turn, title, numbered, settled))


def write_request(repo, name="q1", commit=True, **fields):
    """A peer's request written by hand: `work request`'s gate (requests r32) takes only this repository's asker."""
    path = Path(repo) / ".shop" / "work" / "requests" / ("%s.md" % name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(request_text(name, **fields))
    if commit:
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "write %s" % name)
    return path
