"""The git plumbing of a batch (capability batches; workflow simplification plan 4, D11, D17, D19): git run in a
repository, `.shop/delivery.toml`, the lock every committing batch command holds, the worktrees a batch's tasks are
built in, and the push of a batch's branch. `git` and `GitFailed` are `work run`'s, moved here; supervise_worker
imports them back. Standard library only."""
import contextlib
import fcntl
import os
import subprocess
import tomllib
from pathlib import Path

from workqueue import Refused

SCRIPTS = Path(__file__).resolve().parent
TREES = Path(".shop") / "worktrees"


class GitFailed(Refused):
    """A git command that failed: work run's refusal before any stage (r10), the work-item's fault during one (r41)."""


def git(root, *args):
    """Run git in `root`; a git that fails raises GitFailed, with git's first line of complaint."""
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if done.returncode != 0:
        said = (done.stderr.strip() or done.stdout.strip() or "exit %d" % done.returncode).splitlines()[0]
        raise GitFailed("git %s failed: %s" % (" ".join(args), said))
    return done


def delivery(root):
    """`.shop/delivery.toml` of `root`, read; {} when there is none."""
    path = Path(root) / ".shop" / "delivery.toml"
    if not path.is_file():
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as err:
        raise Refused(".shop/delivery.toml: %s" % err) from None


def scripts_env():
    """The environment with the plugin's scripts directory last on PYTHONPATH, so `-p work_items` and the scripts'
    modules are found in a worktree."""
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([p for p in env.get("PYTHONPATH", "").split(os.pathsep) if p] + [str(SCRIPTS)])
    return env


def common_dir(root):
    found = Path(git(root, "rev-parse", "--git-common-dir").stdout.strip())
    return found if found.is_absolute() else Path(root) / found


@contextlib.contextmanager
def locked(root):
    """An exclusive lock on `<git common dir>/shop-batch.lock`, held from a batch command's first read to its commit
    (D17), so commands run at once (several subagents' `done`) land one after another."""
    with open(common_dir(root) / "shop-batch.lock", "a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def current_branch(root):
    """The branch checked out in `root`, or None on a detached HEAD."""
    done = subprocess.run(["git", "symbolic-ref", "-q", "--short", "HEAD"], cwd=root, capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 and done.stdout.strip() else None


def has_branch(root, branch):
    return subprocess.run(["git", "rev-parse", "--verify", "-q", "refs/heads/%s" % branch], cwd=root,
                          capture_output=True).returncode == 0


def trees_path(root):
    """Where a batch's worktrees go: `[batch] worktrees` of `.shop/delivery.toml` (relative to the root, or
    absolute), else `.shop/worktrees/` (D19)."""
    given = delivery(root).get("batch", {}).get("worktrees")
    return Path(root) / (given if given else TREES)


def trees_dir(root):
    """`trees_path`, made with a `.gitignore` of `*`, so the base checkout stays clean (D19)."""
    path = trees_path(root)
    path.mkdir(parents=True, exist_ok=True)
    ignore = path / ".gitignore"
    if not ignore.is_file():
        ignore.write_text("*\n")
    return path


def add_tree(root, path, branch, start=None):
    """A worktree at `path` on `branch`: an existing branch is checked out there, else the branch is made at
    `start`. The path."""
    git(root, "worktree", "prune")
    if has_branch(root, branch):
        git(root, "worktree", "add", "-q", str(path), branch)
    else:
        git(root, "worktree", "add", "-q", "-b", branch, str(path), start or "HEAD")
    return Path(path)


def _top(path):
    done = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(done.stdout.strip()).resolve() if done.returncode == 0 and done.stdout.strip() else None


def is_tree(path, branch=None):
    """Whether `path` is itself a worktree (not a directory inside another checkout), on `branch` when one is given
    (plan 4 review, S1)."""
    path = Path(path)
    if not path.is_dir() or _top(path) != path.resolve():
        return False
    return branch is None or current_branch(path) == branch


def tree_for(root, path, branch, command, start=None):
    """The worktree of `branch` at `path`, made when it is not there: an empty directory there is replaced, anything
    else that is not that worktree is refused, naming the path. Whether it was made."""
    path = Path(path)
    if is_tree(path, branch):
        return False
    if path.exists():
        if not path.is_dir() or any(path.iterdir()):
            raise Refused("%s: %s is not the worktree of %s; move it away, then run %s again" % (
                command, path, branch, command))
        path.rmdir()
    add_tree(root, path, branch, start)
    return True


def uncommitted(tree):
    """The paths a worktree has changed and not committed, untracked files included (`.shop/scratch/` left out)."""
    out = git(tree, "status", "--porcelain", "--untracked-files=all").stdout.splitlines()
    return [line[3:] for line in out if not line[3:].startswith(".shop/scratch")]


def remove_tree(root, path):
    """The worktree at `path` removed, its changes with it, and git's record of it pruned; a missing path is no
    error, an empty directory is removed, and a directory that is not a worktree is left alone (S1)."""
    path = Path(path)
    if is_tree(path):
        git(root, "worktree", "remove", "--force", str(path))
    elif path.is_dir() and not any(path.iterdir()):
        path.rmdir()
    git(root, "worktree", "prune")


def remote(root, branch):
    """The remote `branch` pushes to: its upstream's, else `origin` (D11)."""
    done = subprocess.run(["git", "config", "branch.%s.remote" % branch], cwd=root, capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 and done.stdout.strip() else "origin"


def push(root, remote_name, branch, command="work batch"):
    """`git push -u <remote> <branch>`; refused under `command`, naming the branch, the remote and git's reason."""
    done = subprocess.run(["git", "push", "-q", "-u", remote_name, branch], cwd=root, capture_output=True, text=True)
    if done.returncode != 0:
        said = (done.stderr.strip() or done.stdout.strip() or "exit %d" % done.returncode).splitlines()[0]
        raise Refused("%s: the push of %s to %s failed: %s" % (command, branch, remote_name, said))
