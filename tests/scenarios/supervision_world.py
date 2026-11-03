"""What supervision's handlers share (not a handler module itself, so the glob does not load it; the handler modules
load it by path, as `vocab.load_handlers` loads them): the repository `work run` runs in, built from what the Givens
recorded, the stand-in claude, the run, and the readings of the stand-in's record, log.jsonl and git.

The Givens write the nodes (world_nodes.py) and record the rest under `context["sv"]`; the When builds the repository
around them (`build`): a git repository on main with a remote, the tests `.shop/delivery.toml` names, the capability
`thing`, each node rewritten in the form `work run` reads, and the stand-in first on PATH and as
$SHOPSYSTEM_WORK_CLAUDE, told what to do by supervision_plans.py; then it runs `work run` once (`deliver`)."""
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
STUB = ROOT / "tests" / "scripts" / "stub_claude.py"
GENERATE = ROOT / "tests" / "scripts" / "fixtures" / "generate" / "repo" / "spec"
PATH = "ex.com/prod/ctx"
WORK = ".shop/work"
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
DELIVERY = '[tests]\nwork_item = "python3 tests.py --work-item {work_item}"\nsuite = "python3 tests.py"\n'
BY_WORKER = {"SHOPSYSTEM_WORK_RUN_WORKER": "w0"}
PRE_RECEIVE = '#!/bin/sh\nif [ -e "$GIT_DIR/refuse" ]; then echo "the remote refuses pushes to this branch" >&2; exit 1; fi\n'
POST_RECEIVE = '#!/bin/sh\ncat >> "$GIT_DIR/pushed"\n'
CAP = """---
id: capability/%s/thing
title: thing
narrator: a client
group: service
rests_on: []
retired: []
---

# thing

## Purpose
Something.

## Behaviour
- [r1] **When** asked, `thing` shall answer.

## Not yet
- None.
""" % PATH


def full(kind, name):
    return "%s/%s/%s" % (kind, PATH, name)


def sv(context):
    """What the Givens of a supervision scenario recorded."""
    return context.setdefault("sv", {"stages": {}, "results": {}, "sessions": {}, "conds": {}, "for": {}, "with": {},
                                     "on": {}, "blocked": {}, "questions": {}, "inst": {},
                                     "dirty": [], "things": {}})


def git(repo, *args, check=True):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=check).stdout


def write(repo, rel, text):
    path = Path(repo) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def commit_all(repo, message):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "--allow-empty", "-m", message)


def field(text, name):
    found = re.search(r"^%s: (.*)$" % re.escape(name), text, re.MULTILINE)
    return found.group(1).strip() if found else None


def set_field(text, name, value):
    if field(text, name) is not None:
        return re.sub(r"^%s: .*$" % re.escape(name), "%s: %s" % (name, value), text, count=1, flags=re.MULTILINE)
    return text.replace("\n---\n", "\n%s: %s\n---\n" % (name, value), 1)


def nodes(context, kind=None):
    """{name: rel} of the nodes the Givens wrote, of one kind or all."""
    return {n: rel for n, (k, rel) in context.get("nodes", {}).items() if kind in (None, k)}


def item_text(name, status, initiative, fileset=None, blocked_by=None):
    extra = "fileset: [%s]\n" % ", ".join(fileset) if fileset else ""
    extra += "blocked_by: [%s]\n" % ", ".join(blocked_by) if blocked_by else ""
    return ("---\nid: %s\nkind: work-item\npart_of: %s\nstatus: %s\nunder: thing\naccepts: [thing#r1]\n%s---\n\n# %s\n"
            % (full("work-item", name), full("capability-proposal", "p1"), status, extra, name))


def remote_dir(repo):
    return Path(repo).parent / "remote.git"


def remote(repo):
    bare = remote_dir(repo)
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True, capture_output=True)
    for name, text in (("pre-receive", PRE_RECEIVE), ("post-receive", POST_RECEIVE)):
        (bare / "hooks" / name).write_text(text)
        (bare / "hooks" / name).chmod(0o755)
    git(repo, "remote", "add", "origin", str(bare))
    git(repo, "push", "-q", "-u", "origin", "main")


def stub(repo):
    """The stand-in claude in a directory beside the repository; its record and its plan beside it."""
    there = Path(repo).parent / "stub"
    (there / "bin").mkdir(parents=True, exist_ok=True)
    claude = there / "bin" / "claude"
    claude.write_text("#!/bin/sh\nexec %s %s \"$@\"\n" % (shlex.quote(sys.executable), shlex.quote(str(STUB))))
    claude.chmod(0o755)
    return there


def calls(repo, events=("start", "end")):
    path = Path(repo).parent / "stub" / "calls.jsonl"
    lines = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    return [c for c in lines if c["event"] in events]


def starts(repo):
    return calls(repo, ("start",))


def log_lines(repo, initiative="i1"):
    path = Path(repo) / WORK / initiative / "log.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def state(repo):
    """The repository as files (outside .git/), its HEAD and branches, and what git says is not committed."""
    repo = Path(repo)
    files = {str(p.relative_to(repo)): p.read_bytes() for p in repo.rglob("*")
             if p.is_file() and ".git" not in p.relative_to(repo).parts}
    if not (repo / ".git").exists():
        return files, None
    return files, git(repo, "rev-parse", "HEAD"), git(repo, "branch", "-a"), git(repo, "status", "--porcelain")


def run_work(repo, context, plan, args):
    """`work run <args>` as a program, with the stand-in; its completed process kept as context["result"]."""
    there = stub(repo)
    (there / "plan.json").write_text(json.dumps(plan))
    env = dict({k: v for k, v in os.environ.items() if k != "SHOPSYSTEM_WORK_RUN_WORKER"},
               PATH="%s%s%s" % (there / "bin", os.pathsep, os.environ.get("PATH", "")),
               SHOPSYSTEM_WORK_CLAUDE=str(there / "bin" / "claude"), STUB_CLAUDE_PLAN=str(there / "plan.json"),
               STUB_CLAUDE_CALLS=str(there / "calls.jsonl"), PYTEST_XDIST_AUTO_NUM_WORKERS="2",
               CLAUDE_CONFIG_DIR=str(there / "claude"), **context.get("env", {}))
    env["PYTHONPATH"] = os.pathsep.join(p for p in env.get("PYTHONPATH", "").split(os.pathsep)
                                        if p and not (Path(p) / "work_items.py").exists())
    context["before"] = state(repo)
    context["result"] = subprocess.run([sys.executable, str(SCRIPTS / "work"), "run", *args], cwd=repo, env=env,
                                       capture_output=True, text=True, timeout=300)
    done = context["result"]     # beside the repository, for whoever reads a failed scenario's directory
    (Path(repo).parent / "run.txt").write_text("exit %d\n%s\n%s" % (done.returncode, done.stdout, done.stderr))
    return done


def init(repo):
    git(repo, "init", "-q", "-b", "main")
    init_identity(repo)


def init_identity(repo):
    for key, value in (("user.name", "Someone"), ("user.email", "someone@example.com"), ("commit.gpgsign", "false")):
        git(repo, "config", key, value)


def base(repo, codified):
    """The files every scenario's repository has; `codified`: the generation fixture's codified spec beside them."""
    if codified:
        for rel in ("index.md", "capabilities/work-queue.md"):
            write(repo, "spec/" + rel, (GENERATE / rel).read_text())
    elif not (Path(repo) / "spec" / "index.md").is_file():
        write(repo, "spec/index.md", "---\nid: bounded-context/%s\n---\n# ctx\n\n## Glossary\n\n" % PATH)
    write(repo, "spec/capabilities/thing.md", CAP)
    write(repo, ".shop/delivery.toml", DELIVERY)
    write(repo, "tests.py", TESTS_PY)
    write(repo, "README.md", "# repo\n")
