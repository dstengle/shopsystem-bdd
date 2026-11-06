"""The plumbing of .shop/ that every command shares: the one refusal, frontmatter read with scripts/model's own reader
(so the two never disagree on a file), the context's path, a file's text, git, a commit of named files only and its
push (U4, backlog r18), bounded in time (r19), and an append to a log whole or not at all. Standard library only."""
import importlib.machinery
import importlib.util
import os
import signal
import subprocess
import sys
from pathlib import Path

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
    """`git push -u <remote> <branch>`, never asking for credentials nor waiting past the push's timeout (backlog r19):
    None when it is pushed, else git's first line of complaint, or that it timed out."""
    seconds = push_timeout()
    done = bounded(["git", "push", "-q", "-u", remote_name, branch], root, push_env(), seconds)
    if done is None:
        return "timed out after %d s" % seconds
    if done.returncode == 0:
        return None
    return (done.stderr.strip() or done.stdout.strip() or "exit %d" % done.returncode).splitlines()[0]


def push_env(root=None):
    """The environment of a push: no prompt for credentials, and ssh in batch mode (no passphrase nor host key asked),
    the option added to the command git would use: `$GIT_SSH_COMMAND`, else `core.sshCommand` of `root` (else of the
    current directory); a `$GIT_SSH` with neither left alone; else `ssh`."""
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    ssh = os.environ.get("GIT_SSH_COMMAND", "").strip()
    if not ssh:
        done = subprocess.run(["git", "config", "core.sshCommand"], cwd=root, capture_output=True, text=True)
        ssh = done.stdout.strip() if done.returncode == 0 else ""
    if not ssh and os.environ.get("GIT_SSH", "").strip():
        return env
    env["GIT_SSH_COMMAND"] = (ssh or "ssh") + " -o BatchMode=yes"
    return env


def push_timeout():
    """The seconds a push may take: `$SHOPSYSTEM_PUSH_TIMEOUT`, a positive whole number, else 60."""
    value = os.environ.get("SHOPSYSTEM_PUSH_TIMEOUT", "").strip()
    return int(value) if value.isdigit() and int(value) > 0 else 60


def bounded(argv, root, env, seconds):
    """`argv` run in `root` in its own process group, its output captured: the completed process, or None when it ran
    past `seconds`, the whole group killed (git's children, a remote's hook, hold the pipes open past git itself)."""
    proc = subprocess.Popen(argv, cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        out, err = proc.communicate(timeout=seconds)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.communicate()
        return None
    return subprocess.CompletedProcess(argv, proc.returncode, out, err)


def pushed(root):
    """The branch checked out in `root` pushed to its remote (U4); nothing on a detached HEAD or when the repository has
    no such remote. A push git refuses keeps the commit: it is printed on stderr as `not pushed: <remote>: <git's
    reason>` (`timed out after <n> s` for a remote that does not answer) and the command goes on to succeed (backlog
    r18, r19)."""
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
