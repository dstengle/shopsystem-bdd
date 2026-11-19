"""The store adapter's checks (the decision "Git is the store and the isolation"; the domain contract design, §6.2):
what a service keeps is one commit of its named files on the branch checked out (`kept`), and shared once that
commit is on the branch's upstream remote (`shared`; `unshared`, U13's check, the remote a request's commit is not on).
The remote of a branch is its upstream's (`branch.<b>.remote`), else `origin`; the commit is looked for on the
branch's upstream branch there (`branch.<b>.merge`), else on the branch of its own name. Used by the scenario
driver's Thens (tests/scenarios/driver_cli.py) and by the decision's test."""
import subprocess
from pathlib import Path


def _git(root, *args):
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else None


def head(root):
    """(branch, its commit) checked out at `root`, or None outside git or on a detached HEAD; a branch with no commit
    yet has the commit None."""
    branch = (Path(root) / ".git").exists() and _git(root, "symbolic-ref", "-q", "--short", "HEAD")
    return (branch, _git(root, "rev-parse", "-q", "--verify", "HEAD")) if branch else None


def _new(root, before):
    """The commits on the branch checked out since `before` (a `head`), newest first."""
    after = head(root)
    if after is None or after == before or after[1] is None:
        return []
    since = before[1] if before and before[0] == after[0] and before[1] else None
    listed = _git(root, "rev-list", "%s..HEAD" % since if since else "HEAD")
    return listed.split() if listed else []


def kept(root, before, paths):
    """The commit since `before` that holds every one of `paths` (one commit of the thing's named files), or None."""
    want = set(paths)
    for commit in _new(root, before):
        files = _git(root, "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", commit) or ""
        if want <= set(files.split("\n")):
            return commit
    return None


def _upstream(root, branch):
    remote = _git(root, "config", "branch.%s.remote" % branch) or "origin"
    if remote not in (_git(root, "remote") or "").split():
        return None
    merge = (_git(root, "config", "branch.%s.merge" % branch) or branch).removeprefix("refs/heads/")
    return remote, "refs/remotes/%s/%s" % (remote, merge)


def shared(root, commit):
    """Whether `commit` is on the upstream remote of the branch checked out: None when the branch has no remote."""
    now = head(root)
    found = now and _upstream(root, now[0])
    if not found:
        return None
    ref = _git(root, "rev-parse", "-q", "--verify", found[1])
    if ref is None:
        return False
    done = subprocess.run(["git", "merge-base", "--is-ancestor", commit, ref], cwd=root, capture_output=True)
    return done.returncode == 0


def unshared(root, before):
    """The remote a commit made since `before` on the branch checked out is not on (U13), or None: none when nothing
    was committed there or the branch has no remote."""
    after = head(root)
    if not _new(root, before):
        return None
    found = _upstream(root, after[0])
    if found is None:
        return None
    return None if shared(root, after[1]) else found[0]
