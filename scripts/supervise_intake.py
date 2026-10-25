"""`work run`'s intake rounds (capability supervision r67): a request this context is the upstream of, `open` or
`awaiting-upstream`, is given to a session of `initiative-round` of the kind intake, which writes a line outcome for each
of the request's lines and passes the turn, with `work outcome` and `work turn`. A `Run` whose directory is
`.shop/work/requests/`: its worker, worktree, lock and limit of sessions are `Run`'s. Standard library only."""
import os
import subprocess

import workqueue
import workqueue_request
from supervise import Run
from supervise_faults import Fault, fault_of
from supervise_worker import SCRIPTS, WORKER, GitFailed, git
from workqueue import WORK, Refused

WAITING = ("open", "awaiting-upstream")


def due(root):
    """The names of the requests with a round to run, in the order `workqueue.requests` gives them (r67)."""
    return [name for name, status, _, _ in workqueue.requests(root) if status in WAITING]


def intakes(root):
    """One `Intake` for each request due."""
    return [Intake(root, name) for name in due(root)]


class Intake(Run):
    """The intake round of one request."""

    def __init__(self, root, request):
        super().__init__(root, "requests")
        self.request = request

    def check(self):
        """What the round needs before anything changes (r10): not started by a worker, delivery.toml readable, a branch
        checked out, and nothing uncommitted under .shop/work/ (r46)."""
        if os.environ.get(WORKER):
            raise Refused("it was started by a worker of another `work run` (of %s); a worker starts no delivery"
                          % os.environ[WORKER])
        self.read_delivery()
        self.branch = git(self.root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        if self.branch == "HEAD":
            raise Refused("HEAD is detached; check out the branch work run is to deliver onto")
        status = git(self.root, "--no-optional-locks", "status", "--porcelain", "--untracked-files=all", "--", str(WORK))
        loose = sorted(line[3:] for line in status.stdout.splitlines())
        if loose:
            raise Refused("%s under %s %s not committed; commit %s before work run starts"
                          % (", ".join(loose), WORK, "is" if len(loose) == 1 else "are", "it" if len(loose) == 1 else "them"))

    def brief(self, name, stage, agent, here, tree, branch, extra):
        """The intake round's brief: the request, its lines, and the commands it writes with."""
        path = self.rel(self.dir / (name + ".md"))
        text = (self.dir / (name + ".md")).read_text()
        held = text.split("\n## Lines\n", 1)[1].split("\n## ", 1)[0].strip().splitlines() if "\n## Lines\n" in text else []
        work = "python3 %s/work" % SCRIPTS
        brief = here / "brief.md"
        brief.write_text(
            "# intake of %s\n\nRequest: %s\nAgent: %s\nScripts: %s\nKind: intake\nWorktree: %s\nBranch: %s\n"
            "Lines of the request:\n%s\n\nRead (paths in your worktree):\n- %s\n- spec/index.md\n\n"
            "Write the line outcome of each line with `%s outcome %s <line> <accepted|refused|withdrawn>`; for a line you "
            "cannot judge write no line outcome, and give a question on it in your result's `questions` as "
            "`<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with "
            "`%s turn %s`.\n\n"
            "Run directory: %s\nResult file: %s\n\n"
            "You start in your worktree, %s: run every command from there, as it is, and never change directory (no `cd`, "
            "no `git -C`); a command that does is refused.\n\n"
            "Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, "
            "`summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way "
            "still leaves a result, and one that does not claim the work done.\n"
            % (name, path, agent, SCRIPTS, tree, branch, "\n".join("- " + l for l in held), path, work, name, work, name,
               here, here / "result.json", tree))
        return brief

    def take(self):
        """Run the round; a Refused naming it when it faults or does not end DONE, and the request keeps its state."""
        name = self.request
        label, _ = self.run_dir(name, "intake")
        branch = "round/%s-%s" % (name, label)
        where = self.rel(self.dir / "runs" / name / label)
        tree = None
        try:
            tree = self.worktree(name, "%s-%s" % (name, label), branch)
            data, failure = self.worker(name, "intake", "initiative-round", tree, branch)
            if failure:
                raise Fault(failure)
            self.remove(tree)
            if data.get("status") == "DONE":
                with self.lock:
                    head = git(self.root, "rev-parse", "HEAD").stdout.strip()
                    try:     # r100: the questions are written while the request is in the upstream's turn, then merged
                        for question in data.get("questions") or []:
                            number, text = str(question).split(". ", 1)
                            workqueue_request.ask(self.root, name, int(number), text)
                        git(self.root, "merge", "-q", "--no-edit", branch)
                    except (Refused, ValueError, GitFailed) as error:
                        subprocess.run(["git", "merge", "--abort"], cwd=self.root, capture_output=True)
                        git(self.root, "reset", "-q", "--hard", head)
                        raise Fault(str(error)) from None
                    git(self.root, "branch", "-q", "-d", branch)
        except (Fault, GitFailed) as fault:
            if tree is not None:
                self.remove(tree)
            subprocess.run(["git", "merge", "--abort"], cwd=self.root, capture_output=True)
            self.keep(name, label, "faulted")
            raise Refused("the intake round of %s (%s) faulted, and %s stays as it was: %s"
                          % (name, where, name, fault_of(fault))) from None
        if data.get("status") != "DONE":
            self.keep(name, label, "gave " + str(data.get("status")))
            raise Refused("the intake round of %s (%s) gave the outcome %s, and %s stays as it was: %s"
                          % (name, where, data.get("status"), name, data.get("summary", "")))
        self.keep(name, label, "ended")

    def keep(self, name, label, how):
        """The round's stage directory and log lines, committed (and pushed), so the next `work run` finds nothing
        uncommitted under .shop/work/ (r46)."""
        rels = [self.rel(p) for p in (self.dir / "runs" / name, self.dir / "log.jsonl") if p.exists()]
        if rels and git(self.root, "status", "--porcelain", "--", *rels).stdout.strip():
            git(self.root, "add", "--", *rels)
            git(self.root, "commit", "-q", "-m", "work: %s intake round %s %s" % (name, label, how), "--", *rels)
            self.unlogged = []
            self.own = {d for d in self.own if not d.startswith(self.rel(self.dir / "runs" / name) + "/")}
            self.git_push()
