"""`work run`'s faults (capability supervision, design-decision/a-failed-work-item): a work-item moved to `failed` with
its fault recorded, the initiative branch verified before a worker starts and pushed after each commit, and the
repository's own checkout kept to its last commit under .shop/work/ while workers run. Standard library only; a part
of supervise.Run."""
import json
import subprocess

import supervise_worker     # its git, at call time: supervise_worker imports this module's Fault
import workqueue
from workqueue import WORK, Refused


class Fault(Exception):
    """A fault of the work-item's stage that is no question for the person: the work-item goes to `failed` (r40)."""


class Faults:
    """The part of supervise.Run that verifies and pushes the initiative branch and moves a work-item to `failed`."""

    def remote(self):
        """The initiative branch's remote: its upstream's, else `origin`."""
        done = subprocess.run(["git", "config", "branch.%s.remote" % self.branch], cwd=self.root, capture_output=True,
                              text=True)
        return done.stdout.strip() or "origin"

    def git_push(self, *options):
        """`git push <options> <remote> <branch>`; None, else git's reason it failed."""
        done = subprocess.run(["git", "push", "-q", *options, self.remote(), self.branch], cwd=self.root,
                              capture_output=True, text=True)
        if done.returncode == 0:
            return None
        said = [l.strip() for l in (done.stderr + done.stdout).splitlines() if l.strip() and not l.startswith("hint:")]
        return "; ".join(said) or "exit %d" % done.returncode

    def verify_push(self, name, stage):
        """Verify, before a worker starts, that the initiative branch can be pushed (r35); a Fault if not (r39)."""
        reason = self.git_push("--dry-run")
        if reason:
            raise Fault("work run could not verify that it can push the initiative branch %s to %s before the %s "
                        "stage: %s" % (self.branch, self.remote(), stage, reason))
        self.log(**{"work-item": name, "stage": stage, "event": "push verified"})

    def push(self):
        """Push the initiative branch after a commit on it (r38); a Fault if git cannot (r41)."""
        reason = self.git_push()
        if reason:
            raise Fault("the push of the initiative branch %s to %s failed: %s" % (self.branch, self.remote(), reason))

    def fail(self, name, fault):
        """`name` to `failed` from whatever status it has, its fault recorded under `## Faults` and committed; the push
        is tried; a push that fails is named with the fault. The run ends with an error (r40)."""
        with self.lock:
            before = workqueue.agrees(self.root, self.initiative, name)
            workqueue.move(self.root, self.initiative, name, "failed", by="work run")
            self.section(name, "Faults", fault)
            self.commit(name, before, "failed", push=False)
            reason = self.git_push()
            if reason:      # the transition stays committed locally; the run ends naming the fault and the failed push
                fault = "%s; and the push of the failure failed: %s" % (fault, reason)
            self.faults.append((name, fault))

    def checkout_changes(self):
        """The paths under .shop/work/ in the repository's own checkout that differ from its last commit, other than
        what work run itself has written and not yet committed; each put back to its last commit (r28)."""
        out = supervise_worker.git(self.root, "status", "--porcelain", "--untracked-files=all", "--", WORK.as_posix()).stdout
        log = self.rel(self.dir / "log.jsonl")
        changed = []
        for line in out.splitlines():
            path = line[3:].strip('"')
            if any(path.startswith(own + "/") for own in self.own):
                continue
            if path == log and (self.dir / "log.jsonl").read_text() == self.committed(log) + "".join(self.unlogged):
                continue
            changed.append(path)
        for path in changed:
            if path == log:
                (self.dir / "log.jsonl").write_text(self.committed(log) + "".join(self.unlogged))
            elif supervise_worker.git(self.root, "ls-tree", "--name-only", "HEAD", "--", path).stdout.strip():
                supervise_worker.git(self.root, "checkout", "HEAD", "--", path)
            else:
                supervise_worker.git(self.root, "rm", "-q", "-f", "--cached", "--ignore-unmatch", "--", path)
                (self.root / path).unlink(missing_ok=True)
        return changed

    def committed(self, rel):
        done = subprocess.run(["git", "show", "HEAD:" + rel], cwd=self.root, capture_output=True, text=True)
        return done.stdout if done.returncode == 0 else ""

    def tree_changes(self, tree, start):
        """The paths under .shop/work/ a worker changed in its detached worktree since `start`, committed or not."""
        work = WORK.as_posix()
        changed = supervise_worker.git(tree, "diff", "--name-only", start, "--", work).stdout.split()
        changed += supervise_worker.git(tree, "ls-files", "--others", "--exclude-standard", "--", work).stdout.split()
        return sorted(set(changed))


def session_end(stdout, code):
    """How a `claude -p --output-format json` session ended, in words, from what it printed and its exit code (r42)."""
    try:
        data = json.loads(stdout)
    except ValueError:
        data = None
    if not isinstance(data, dict):
        return "its session exited with code %d, printing no result of its own" % code
    subtype, turns = data.get("subtype"), data.get("num_turns")
    how = {"success": "its session ended as a success", "error_max_turns": "its session ended at its turn limit",
           "error_during_execution": "its session ended on an error during execution"}.get(
        subtype, "its session ended with %s" % subtype)
    return "%s (%s, %s turns, exit code %d)" % (how, subtype, turns, code)


def fault_of(error):
    """The words of a fault raised as a Fault or by a git command that failed (supervise_worker.git's Refused)."""
    return str(error) if isinstance(error, (Fault, Refused)) else "%s: %s" % (type(error).__name__, error)
