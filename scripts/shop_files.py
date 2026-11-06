"""The plumbing of .shop/ that every command shares: the one refusal, frontmatter read with scripts/model's own reader
(so the two never disagree on a file), the context's path, a file's text, git, a commit of named files only and its
push (U4, backlog r18), and an append to a log whole or not at all. Standard library only."""
import importlib.machinery
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

# A task's branch, `batch-<n>-b<j>` (batch_start), on which no command of .shop/ commits (backlog r20).
TASK_BRANCH = re.compile(r"(batch-[1-9]\d*)-(b[1-9]\d*)")
# Unicode's mandatory line breaks: LF, VT, FF, CR, NEL, LS, PS.
LINE_BREAKS = "\n\x0b\x0c\r\x85  "


def _load_model():
    path = Path(__file__).resolve().with_name("model")
    loader = importlib.machinery.SourceFileLoader("shopsystem_model", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


frontmatter = _load_model().frontmatter


class Refused(Exception):
    """What was asked cannot be done; the message says why, and nothing was changed."""


def context_path(root):
    """The <owner>/<product>/<context name> of spec/index.md's bounded-context id."""
    index = Path(root) / "spec" / "index.md"
    if not index.is_file():
        raise Refused("spec/index.md, which names the context, is missing")
    data, _ = frontmatter(read(index, root))
    ident = data.get("id")
    if not isinstance(ident, str) or "/" not in ident:
        raise Refused("spec/index.md gives no bounded-context id (bounded-context/<owner>/<product>/<context>)")
    return ident.split("/", 1)[1]


def read(path, root):
    """The text of `path`; a file that is not UTF-8 text is refused, naming it."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise Refused("%s is not UTF-8 text" % path.relative_to(root)) from None


def append(log, data):
    """Append `data` to `log` whole or not at all: a write that fails part-way is cut back to the size before it."""
    fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        size = os.fstat(fd).st_size
        try:
            written = 0
            while written < len(data):
                written += os.write(fd, data[written:])
        except OSError:
            os.ftruncate(fd, size)
            raise
    finally:
        os.close(fd)


def git(root, *args):
    """Run git in `root`; a git that fails is refused, with git's first line of complaint."""
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if done.returncode != 0:
        said = (done.stderr.strip() or done.stdout.strip() or "exit %d" % done.returncode).splitlines()[0]
        raise Refused("git %s failed: %s" % (args[0], said))
    return done.stdout


def committed(root, rels, message, write):
    """Make the change `write` makes to the files `rels` (relative to `root`), then commit them, and only them, on the
    current branch. A repository git cannot commit in is refused before anything is written, and a commit that fails
    puts the files back as they were."""
    git(root, "rev-parse", "--is-inside-work-tree")
    refuse_task_branch(root)
    paths = [Path(root) / rel for rel in rels]
    before = [p.read_bytes() if p.exists() else None for p in paths]
    write()
    try:
        git(root, "add", "--", *rels)
        git(root, "commit", "-q", "-m", message, "--", *rels)
    except Refused:
        for path, data in zip(paths, before):
            path.unlink(missing_ok=True) if data is None else path.write_bytes(data)
        subprocess.run(["git", "reset", "-q", "--", *rels], cwd=root, capture_output=True)
        raise
    pushed(root)


def remote(root, branch):
    """The remote `branch` pushes to: its upstream's, else `origin` (D11)."""
    done = subprocess.run(["git", "config", "branch.%s.remote" % branch], cwd=root, capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 and done.stdout.strip() else "origin"


def push_failure(root, remote_name, branch):
    """`git push -u <remote> <branch>`, never asking for credentials: None when it is pushed, else git's first line of
    complaint."""
    done = subprocess.run(["git", "push", "-q", "-u", remote_name, branch], cwd=root, capture_output=True, text=True,
                          env=dict(os.environ, GIT_TERMINAL_PROMPT="0"))
    if done.returncode == 0:
        return None
    return (done.stderr.strip() or done.stdout.strip() or "exit %d" % done.returncode).splitlines()[0]


def pushed(root):
    """The branch checked out in `root` pushed to its remote (U4); nothing on a detached HEAD or when the repository has
    no such remote. A push git refuses keeps the commit: it is printed on stderr as `not pushed: <remote>: <git's
    reason>` and the command goes on to succeed (backlog r18)."""
    found = subprocess.run(["git", "symbolic-ref", "-q", "--short", "HEAD"], cwd=root, capture_output=True, text=True)
    branch = found.stdout.strip()
    if found.returncode != 0 or not branch:
        return
    name = remote(root, branch)
    if name not in git(root, "remote").split():
        return
    said = push_failure(root, name, branch)
    if said is not None:
        print("not pushed: %s: %s" % (name, said), file=sys.stderr)


def branch_of(root):
    """The branch checked out in `root`, or None on a detached HEAD."""
    found = subprocess.run(["git", "symbolic-ref", "-q", "--short", "HEAD"], cwd=root, capture_output=True, text=True)
    return found.stdout.strip() if found.returncode == 0 and found.stdout.strip() else None


def task_of(root, branch):
    """`task t<k> of batch-<n>` when `branch` is a task's branch, its `t<k>` read from the batch's plan in the main
    worktree, where the batch commands keep it (`a task of batch-<n>` when the plan does not say); else None."""
    match = TASK_BRANCH.fullmatch(branch or "")
    if match is None:
        return None
    listed = subprocess.run(["git", "worktree", "list", "--porcelain"], cwd=root, capture_output=True, text=True)
    main = listed.stdout.split("\n", 1)[0].removeprefix("worktree ") if listed.returncode == 0 else ""
    plan = Path(main or root) / ".shop" / "batches" / match.group(1).split("-")[1] / "plan.md"
    text = plan.read_text(encoding="utf-8", errors="replace") if plan.is_file() else ""
    row = re.search(r"^\| (t[1-9]\d*) \| %s \| \S+ \| %s \|$" % (match.group(2), re.escape(branch)), text, re.MULTILINE)
    return ("task %s of %s" % (row.group(1), match.group(1))) if row else "a task of %s" % match.group(1)


def refuse_task_branch(root):
    """Refused when the branch checked out in `root` is a task's: a task's commits are its item's work, and what work
    commits under .shop/ belongs on the base branch, so nothing is written there and the task branch is never pushed
    (backlog r20)."""
    branch = branch_of(root)
    task = task_of(root, branch)
    if task is not None:
        raise Refused("%s is the branch of %s; work commits nothing on a task's branch: run it in the base "
                      "branch's checkout" % (branch, task))
