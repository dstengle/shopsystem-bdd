"""`work run <initiative>`: the supervisor that takes an initiative's work-items through their stages (capability
supervision). Standard library only.

For each stage it starts a fresh `claude -p` worker of that stage's agent in a worktree of its own, with that stage's
tools only, given one brief file; it reads the outcome only from the worker's result file, which the worker writes in
its worktree's git-ignored .shop/scratch/, and makes the move itself through workqueue.move. Each move is its own commit
of the work-item's file, its run directory (the worker's scratch run directory, copied) and log.jsonl. It takes no
judgment: what is not DONE goes to the person as a question.
"""
import fnmatch
import json
import os
import shutil
import threading
from pathlib import Path

import workqueue
from supervise_brief import Briefs
from supervise_merge import Merge
from supervise_worker import Workers, git, now
from workqueue import WORK, Refused

BY = "work run"
# The status a worker starts from: its stage, its agent and the status its DONE moves the work-item to.
STAGES = {
    "drafted": ("research", "code-scout", "researched"),
    "researched": ("plan", "bdd-planner", "planned"),
    "ready": ("implement", "bdd-implementer", "done"),
    "done": ("review", "bdd-task-reviewer", "green"),
}
MOVABLE = ("drafted", "researched", "planned", "ready", "done")


class Run(Workers, Briefs, Merge):
    """One `work run` of one initiative in the repository at `root`: the workers' part is supervise_worker's, the briefs'
    supervise_brief's, the implementation stage's and its merge supervise_merge's."""

    def __init__(self, root, initiative):
        self.root = Path(root).resolve()
        self.initiative = initiative
        self.dir = self.root / WORK / initiative
        self.claude = os.environ.get("SHOPSYSTEM_WORK_CLAUDE") or "claude"
        self.trees = []          # the worktrees this run added; removed when it ends
        self.outside = None      # where the worktrees go when the repository is inside the plugin's own directory
        self.lock = threading.RLock()     # held for each change to the main checkout while two implementers run (r20)

    def rel(self, path):
        return str(Path(path).relative_to(self.root))

    def items(self):
        return [(name, status) for ini, name, status in workqueue.items(self.root) if ini == self.initiative]

    def check(self):
        """What work run was given, before anything changes (r10): the initiative, and each work-item's file and log."""
        workqueue.entry(self.initiative, "initiative")
        if not self.dir.is_dir():
            raise Refused("the initiative %s does not exist (no %s)" % (self.initiative, self.rel(self.dir)))
        for name, _ in self.items():
            workqueue.agrees(self.root, self.initiative, name)
        self.branch = git(self.root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        if self.branch == "HEAD":     # detached: no initiative branch to merge onto, rebase on or put back from (r4, r6)
            raise Refused("HEAD is detached; check out the initiative branch work run is to deliver onto")

    def log(self, **line):
        with self.lock:
            workqueue.append(self.dir / "log.jsonl", (json.dumps(dict(time=now(), **line)) + "\n").encode())

    def commit(self, name, before, after):
        """A move's commit on the initiative branch: the work-item's file, its run directories and log.jsonl (r7)."""
        paths = [p for p in (self.dir / (name + ".md"), self.dir / "runs" / name, self.dir / "log.jsonl") if p.exists()]
        rels = [self.rel(p) for p in paths]
        git(self.root, "add", "--", *rels)
        git(self.root, "commit", "-q", "-m", "work: %s %s -> %s" % (name, before, after), "--", *rels)

    def move(self, name, before, after, question=None):
        with self.lock:
            workqueue.move(self.root, self.initiative, name, after, by=BY)
            if question:
                self.ask(name, question)
            self.commit(name, before, after)

    def ask(self, name, question):
        """Write `question` as the last bullet of the work-item's `## Questions` section, before any section after it;
        its continuation lines are indented, so none of them starts a heading."""
        path = self.dir / (name + ".md")
        text = path.read_text()
        bullet = "- %s\n" % question.strip().replace("\n", "\n  ")
        if "\n## Questions\n" not in text:
            path.write_text(text.rstrip("\n") + "\n\n## Questions\n" + bullet)
            return
        head, rest = text.split("\n## Questions\n", 1)
        section, sep, after = rest.partition("\n## ")
        section = section.rstrip("\n") + "\n" if section.strip() else ""
        path.write_text(head + "\n## Questions\n" + section + bullet + ("\n## " + after if sep else ""))


    def step(self, name, status):
        if status == "planned":
            self.move(name, "planned", "ready")
        elif status == "ready":
            self.implement(name)
        else:
            stage, agent, after = STAGES[status]
            label, _ = self.run_dir(name, stage)
            tree = self.worktree(name, "%s-%s" % (name, label))
            try:
                data, failure = self.worker(name, stage, agent, tree)
            finally:
                self.remove(tree)
            question = self.outcome(agent, data, failure)
            self.move(name, status, after if question is None else "awaiting-ruling", question)

    def pair(self, ready):
        """Two of the `ready` work-items whose file sets do not overlap, the first such in their order (r20); else
        none. A work-item without a file set is in no pair. A glob or a directory in a file set claims each tracked file
        it holds, so two implementers never edit one file."""
        tracked = git(self.root, "ls-files").stdout.splitlines()
        files = {}
        for name in ready:
            data, _ = workqueue.frontmatter((self.dir / (name + ".md")).read_text())
            if data.get("fileset"):
                files[name] = {f for entry in data["fileset"] for f in claimed(entry, tracked)}
        for i, first in enumerate(files):
            for second in list(files)[i + 1:]:
                if not files[first] & files[second]:
                    return first, second
        return None

    def together(self, names):
        """Implement the work-items at the same time, each in a thread of its own; their merges take the lock in turn.
        A refusal in either is raised once both have ended."""
        failed = []

        def implement(name):
            try:
                self.implement(name)
            except Exception as error:    # carried to the run's own thread, which ends with it (r10)
                failed.append(error)
        threads = [threading.Thread(target=implement, args=(name,)) for name in names]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if failed:
            raise failed[0]

    def questions(self, name):
        """The lines of the work-item's `## Questions` section: its open questions."""
        text = (self.dir / (name + ".md")).read_text()
        if "\n## Questions\n" not in text:
            return []
        return [l for l in text.split("\n## Questions\n", 1)[1].split("\n## ", 1)[0].splitlines() if l.strip()]

    def run(self):
        """Pull the work-items one worker at a time until none can move (r1); print where each stands (r9)."""
        self.check()
        try:
            while True:
                movable = [(n, s) for n, s in self.items() if s in MOVABLE]
                if not movable:
                    break
                pair = self.pair([n for n, s in movable if s == "ready"])
                if pair:
                    self.together(pair)
                else:
                    self.step(*movable[0])
        finally:
            for tree in list(self.trees):      # on every way out, a failure's too: the run leaves no worktree
                self.remove(tree)
            if self.outside is not None:
                shutil.rmtree(self.outside, ignore_errors=True)
        statuses = self.items()
        for name, status in statuses:
            print("%s %s" % (name, status))
            if status == "awaiting-ruling":
                for line in self.questions(name):
                    print("  %s" % line)
        if all(s in ("green", "withdrawn") for _, s in statuses):
            return 0
        return 3 if any(s == "awaiting-ruling" for _, s in statuses) else 1


def claimed(entry, tracked):
    """What one file set entry claims: itself, and each of the `tracked` files it matches as a glob or holds as a
    directory."""
    under = entry.rstrip("/") + "/"
    return {entry} | {f for f in tracked if fnmatch.fnmatchcase(f, entry) or f.startswith(under)}


def run(root, initiative):
    return Run(root, initiative).run()
