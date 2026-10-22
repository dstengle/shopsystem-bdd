"""supervision's scenarios: the repository work run runs in, the stand-in claude's record and the helpers the
step modules (supervision_given.py, supervision_then_workers.py, test_supervision.py) share."""
import json
import os
import re
import subprocess

import pytest

from .conftest import ROOT, SCRIPTS, full

STUB = ROOT / "tests" / "scripts" / "stub_claude.py"
AGENTS = ["code-scout", "bdd-planner", "bdd-implementer", "bdd-task-reviewer"]
ROLES = dict(zip(["researcher", "planner", "implementer", "reviewer"], AGENTS))
TESTS_PY = """import json, os, sys
if os.environ.get("STUB_CLAUDE_CALLS"):
    with open(os.environ["STUB_CLAUDE_CALLS"], "a") as out:
        out.write(json.dumps({"event": "tests", "argv": sys.argv[1:], "cwd": os.getcwd()}) + "\\n")
which = "scenarios" if "--work-item" in sys.argv else "suite"
if os.path.exists(which + "-fail"):
    print("FAILED: %s-fail is here, so the %s fails" % (which, which))
    sys.exit(1)
print("1 passed in 0.01s")
"""
NEEDS_FEATURE = """import os, sys
if "--work-item" in sys.argv and not os.path.exists("feature.txt"):
    print("FAILED: no feature.txt")
    sys.exit(1)
print("passed")
"""
# The repository's conftest.py records each pytest run in it (not an xdist worker's) to the stand-in's record: its
# arguments, the --work-item it was given (with the plugin loaded) and where it ran.
CONFTEST_PY = """import json, os
def pytest_configure(config):
    if os.environ.get("STUB_CLAUDE_CALLS") and not hasattr(config, "workerinput"):
        with open(os.environ["STUB_CLAUDE_CALLS"], "a") as out:
            out.write(json.dumps({"event": "pytest", "args": list(config.invocation_params.args), "cwd": os.getcwd(),
                                  "work_item": getattr(config.option, "work_item", None)}) + "\\n")
"""
# The environment a worker of another `work run` starts a program in.
BY_WORKER = {"SHOPSYSTEM_WORK_RUN_WORKER": "w0"}
DELIVERY = '[tests]\nwork_item = "python3 tests.py --work-item {work_item}"\nsuite = "python3 tests.py"\n'


@pytest.fixture
def repo(tmp_path):
    """The repository work run runs in; the stand-in's script and record live beside it, outside it."""
    path = tmp_path / "repo"
    path.mkdir()
    return path


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True).stdout


def write(repo, rel, text):
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return p


def commit_all(repo, message):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "--allow-empty", "-m", message)


PRE_RECEIVE = '#!/bin/sh\nif [ -e "$GIT_DIR/refuse" ]; then echo "the remote refuses pushes to this branch" >&2; exit 1; fi\n'
POST_RECEIVE = '#!/bin/sh\ncat >> "$GIT_DIR/pushed"\n'


def remote(repo):
    """A bare repository beside `repo`, its `origin`, with main pushed to it: its pre-receive hook refuses every push
    while the file `refuse` is in it, and its post-receive hook appends each pushed `<old> <new> <ref>` to `pushed`."""
    bare = remote_dir(repo)
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True, capture_output=True)
    for name, text in (("pre-receive", PRE_RECEIVE), ("post-receive", POST_RECEIVE)):
        (bare / "hooks" / name).write_text(text)
        (bare / "hooks" / name).chmod(0o755)
    git(repo, "remote", "add", "origin", str(bare))
    git(repo, "push", "-q", "-u", "origin", "main")
    return bare


def remote_dir(repo):
    return repo.parent / "remote.git"


def item_text(name, status, under="thing", fileset=None):
    """A work-item's file; with `fileset` (a list of paths), its `fileset:` too."""
    files = "fileset: [%s]\n" % ", ".join(fileset) if fileset else ""
    return "---\nid: %s\nkind: work-item\npart_of: capability-proposal/p1\nstatus: %s\nunder: %s\naccepts: [%s#r1]\n%s---\n\n# %s\n" % (
        full("work-item", name), status, under, under, files, name)


def fields(path):
    head = path.read_text().split("---\n")[1]
    return dict(line.split(": ", 1) for line in head.splitlines() if ": " in line)


def calls(repo, events=("start", "end")):
    """The stand-in's record: its starts and ends, or with `events` the Bash commands it ran or refused."""
    path = repo.parent / "stub" / "calls.jsonl"
    lines = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    return [c for c in lines if c["event"] in events]


def starts(repo):
    return [c for c in calls(repo) if c["event"] == "start"]


def work_item_of(call):
    """The work-item a worker's brief names; None for a brief that names none (the branch reviewer's)."""
    found = re.search(r"^Work-item: \.shop/work/i1/(\S+)\.md$", call["brief"], re.M)
    return found.group(1) if found else None


def option(argv, name):
    return argv[argv.index(name) + 1] if name in argv else None


def log_lines(repo):
    path = repo / ".shop/work/i1/log.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def moves(repo, name="w1"):
    return [(l["before"], l["after"]) for l in log_lines(repo) if l.get("work-item") == name and "after" in l]


def work_commits(repo):
    """(sha, subject) of each commit work run made on the initiative branch for a transition, oldest first."""
    lines = [l.split(" ", 1) for l in git(repo, "log", "--reverse", "main", "--format=%H %s").splitlines()]
    return [(sha, subject) for sha, subject in lines if subject.startswith("work: ")]


def state(repo):
    """The repository as files (outside .git/), its commits and branches, and what git says is not committed."""
    files = {str(p.relative_to(repo)): p.read_bytes() for p in repo.rglob("*")
             if p.is_file() and ".git" not in p.relative_to(repo).parts}
    if not (repo / ".git").exists():
        return files, None
    return files, git(repo, "rev-parse", "HEAD"), git(repo, "branch", "-a"), git(repo, "status", "--porcelain")


def committed(what):
    """What the implementer commits, for one part of "committing feature.txt and ...": {path: text, or None to delete}."""
    m = re.match(r"setting (\S+?)'s status to (\S+)$", what) or re.match(r"(\S+?)'s status set to (\S+)$", what)
    if m:
        name = os.path.basename(m.group(1))[:-3]
        return {m.group(1): item_text(name, m.group(2))}
    for word in ("deleting ", "the deletion of "):
        if what.startswith(word):
            return {what[len(word):]: None}
    for word in ("adding ", "a new "):
        if what.startswith(word):
            return {what[len(word):]: "added by a worker\n"}
    return {what: "\n" if what.endswith("-fail") else "the feature\n"}


def scripts_in(text):
    """`text` with `{scripts}` read as the directory of work run's own scripts."""
    return text.replace("{scripts}", str(SCRIPTS))


def tree_has(repo, rel):
    return subprocess.run(["git", "cat-file", "-e", "main:" + rel], cwd=repo).returncode == 0


def section(text, heading):
    return text.split("\n## %s\n" % heading, 1)[1].split("\n## ", 1)[0] if "\n## %s\n" % heading in text else ""
