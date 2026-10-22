"""`work run`'s implementation stage (capability supervision): the implementer in its branch's worktree, the tests
work run runs there, and the merge of a branch that passes them. Standard library only; a part of supervise.Run."""
import re
import shlex
import subprocess
import time

import workqueue
from supervise_faults import Fault, fault_of
from supervise_worker import GitFailed, git, with_scripts
from workqueue import WORK

# The tests work run runs unless .shop/delivery.toml names its own: in parallel (`-n auto`) where the project's python3
# has pytest-xdist, the work-item's and the suite alike (supervision's Implementation); in one process where it has not.
# `--work-item` is the plugin's own pytest plugin, scripts/work_items.py, loaded by `-p` from the scripts directory
# work run puts on PYTHONPATH, so a repository delivered by work run needs no conftest of its own for it.
# The whole suite is given --work-item too (r22), with --whole-suite, which keeps every test (r4) and counts as expected
# the failures of requirements another work-item, neither green nor withdrawn, accepts (r43); -rfEx names those in the summary.
TESTS = {"work_item": "python3 -m pytest -q{parallel} -p work_items --work-item {work_item}",
         "suite": "python3 -m pytest -q{parallel} -rfEx -p work_items --work-item {work_item} --whole-suite"}



class Merge:
    """The part of supervise.Run that implements a ready work-item and merges its branch."""

    def tests(self, name):
        """The commands for `name`'s scenarios and the whole suite, as argument lists."""
        has = subprocess.run(["python3", "-c", "import xdist"], cwd=self.root, capture_output=True).returncode == 0
        parallel = " -n auto" if has else ""
        tests = dict({k: v.replace("{parallel}", parallel) for k, v in TESTS.items()}, **self.delivery().get("tests", {}))
        return {k: shlex.split(v.replace("{work_item}", name)) for k, v in tests.items()}

    def suite_record(self, tree, suite):
        """work run's own whole-suite run in `tree`, as the line `Suite: <N> passed, <M> failed at <hash> in <s> s`, with
        the failing and the expected (r43) named; and the run itself."""
        began = time.monotonic()
        done = subprocess.run(suite, cwd=tree, capture_output=True, text=True, env=with_scripts())
        seconds = time.monotonic() - began
        out = done.stdout + done.stderr
        summary = out.strip().splitlines()[-1] if out.strip() else ""

        def count(word):
            found = re.search(r"(\d+) %s\b" % word, summary)
            return int(found.group(1)) if found else 0
        def named(word):
            return [l.split(" ", 1)[1].split(" - ")[0] for l in out.splitlines() if l.startswith(word + " ")]
        failing, expected = named("FAILED"), named("XFAIL")
        head = git(tree, "rev-parse", "--short", "HEAD").stdout.strip()
        line = "Suite: %d passed, %d failed at %s in %.0f s" % (count("passed"), count("failed"), head, seconds)
        line += "; failing: %s" % ", ".join(failing) if failing else ""
        return line + ("; expected: %s" % ", ".join(expected) if expected else ""), done

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
        deleted (r18). A fault once it is claimed, a git command's failure among them, moves it to failed (r41); any
        other failure puts it to awaiting-ruling with the failure as its question, and is still work run's own (r10)."""
        try:
            self.move(name, "ready", "claimed")
            self.claimed(name)
        except (Fault, GitFailed) as fault:
            self.fail(name, fault_of(fault))
        except Exception as error:
            self.failed_claimed(name, error)
            raise

    def failed_claimed(self, name, error):
        """`name` to awaiting-ruling, asking about `error`, while it is still claimed; a failure of that move leaves the
        first failure the one work run ends with."""
        said = str(error) if isinstance(error, workqueue.Refused) else "%s: %s" % (type(error).__name__, error)
        with self.lock:
            try:
                if workqueue.agrees(self.root, self.initiative, name) == "claimed":
                    self.move(name, "claimed", "awaiting-ruling",
                              "work run failed on %s once it was claimed: %s" % (name, said))
            except Exception:
                pass

    def claimed(self, name):
        tests = self.tests(name)
        tree = self.worktree(name, name, "work/" + name)
        record, _ = self.suite_record(tree, tests["suite"])
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
        else the question it gives the person instead of the merge. What the worker left uncommitted is cleaned away
        first (its run directory in .shop/scratch/ aside): the tests run on the branch, which is what the merge takes."""
        git(tree, "clean", "-q", "-f", "-d", "-x", "-e", ".shop/scratch")
        git(tree, "rebase", "-q", self.branch)
        changed = self.under_work(tree, name)
        if changed:
            raise Fault("its implementer's branch work/%s changed %s under .shop/work/, outside its stage directory; "
                        "work run put it back on the branch and did not merge it" % (name, ", ".join(changed)))
        record, suite = self.suite_record(tree, tests["suite"])     # its expected red counted (r43)
        self.log(**{"work-item": name, "stage": "merge", "event": "suite", "record": record})
        scenarios = subprocess.run(tests["work_item"], cwd=tree, capture_output=True, text=True, env=with_scripts())
        for done in (scenarios, suite):
            if done.returncode != 0:
                return "`%s` failed on %s's branch work/%s:\n%s" % (
                    " ".join(done.args), name, name, (done.stdout + done.stderr).strip())
        git(self.root, "merge", "--ff-only", "work/" + name)
        self.move(name, "claimed", "done")
        return None
