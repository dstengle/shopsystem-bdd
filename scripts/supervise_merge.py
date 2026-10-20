"""`work run`'s implementation stage (capability supervision): the implementer in its branch's worktree, the tests
work run runs there, and the merge of a branch that passes them. Standard library only; a part of supervise.Run."""
import re
import shlex
import subprocess
import time

from supervise_worker import git
from workqueue import WORK

# The tests work run runs unless .shop/delivery.toml names its own: in parallel (pytest-xdist), the work-item's and the
# suite alike (supervision's Implementation).
TESTS = {"work_item": "python3 -m pytest -q -n auto --work-item {work_item}", "suite": "python3 -m pytest -q -n auto"}


class Merge:
    """The part of supervise.Run that implements a ready work-item and merges its branch."""

    def tests(self):
        return dict(TESTS, **self.delivery().get("tests", {}))

    def suite_record(self, tree, suite):
        """work run's own whole-suite run in `tree`, as the line `Suite: <N> passed, <M> failed at <hash> in <s> s`."""
        began = time.monotonic()
        done = subprocess.run(shlex.split(suite), cwd=tree, capture_output=True, text=True)
        seconds = time.monotonic() - began
        out = done.stdout + done.stderr
        summary = out.strip().splitlines()[-1] if out.strip() else ""

        def count(word):
            found = re.search(r"(\d+) %s\b" % word, summary)
            return int(found.group(1)) if found else 0
        failing = [l.split(" ", 1)[1].split(" - ")[0] for l in out.splitlines() if l.startswith("FAILED ")]
        head = git(tree, "rev-parse", "--short", "HEAD").stdout.strip()
        line = "Suite: %d passed, %d failed at %s in %.0f s" % (count("passed"), count("failed"), head, seconds)
        return line + ("; failing: %s" % ", ".join(failing) if failing else "")

    def under_work(self, tree, name):
        """The branch's changes under .shop/work/ since the initiative branch, put back on the branch by a commit there
        (r6); the paths it had changed."""
        changed = git(tree, "diff", "--name-only", "%s...HEAD" % self.branch, "--", WORK.as_posix()).stdout.split()
        for path in changed:
            if git(tree, "ls-tree", "--name-only", self.branch, "--", path).stdout.strip():
                git(tree, "checkout", self.branch, "--", path)
            else:
                git(tree, "rm", "-q", "-f", "--", path)
        if changed:
            git(tree, "commit", "-q", "-m", "work: put back %s's changes under .shop/work/" % name)
        return changed

    def implement(self, name):
        """ready -> claimed, the implementer in its worktree, and its branch merged only on passing tests (r4), then
        deleted (r18)."""
        self.move(name, "ready", "claimed")
        tests = self.tests()
        tree = self.worktree(name, name, "work/" + name)
        record = self.suite_record(tree, tests["suite"])
        self.log(**{"work-item": name, "stage": "implement", "event": "suite", "record": record})
        try:
            data, failure = self.worker(name, "implement", "bdd-implementer", tree, "work/" + name,
                                        [("Suite record", record)])
            question = self.outcome("bdd-implementer", data, failure)
            with self.lock:     # one merge at a time, each branch rebased on the one merged before it (r20)
                if question is None:
                    question = self.merge(name, tree, tests)
                if question is not None:
                    self.move(name, "claimed", "awaiting-ruling", question)
                    return
        finally:
            self.remove(tree)
        with self.lock:
            git(self.root, "branch", "-q", "-d", "work/" + name)     # merged, so no longer needed; once its worktree is gone (r18)

    def merge(self, name, tree, tests):
        """The branch rebased on the initiative branch, put back under .shop/work/, tested and merged (r4, r6); None,
        else the question it gives the person instead of the merge."""
        done = subprocess.run(["git", "rebase", "-q", self.branch], cwd=tree, capture_output=True, text=True)
        if done.returncode != 0:
            return "`git rebase %s` failed on %s's branch work/%s:\n%s" % (
                self.branch, name, name, (done.stdout + done.stderr).strip())
        changed = self.under_work(tree, name)
        if changed:
            return ("bdd-implementer's branch work/%s changed %s under .shop/work/, which only work run "
                    "writes; work run put it back on the branch and did not merge it" % (name, ", ".join(changed)))
        for cmd in (shlex.split(tests["work_item"].format(work_item=name)), shlex.split(tests["suite"])):
            done = subprocess.run(cmd, cwd=tree, capture_output=True, text=True)
            if done.returncode != 0:
                return "`%s` failed on %s's branch work/%s:\n%s" % (
                    " ".join(cmd), name, name, (done.stdout + done.stderr).strip())
        git(self.root, "merge", "--ff-only", "work/" + name)
        self.move(name, "claimed", "done")
        return None
