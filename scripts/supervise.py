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
from supervise_faults import Fault, Faults, fault_of
from supervise_merge import Merge
from supervise_review import Reviews
from supervise_worker import ROLE, WORKER, GitFailed, Workers, git, now
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


class Run(Workers, Briefs, Merge, Faults, Reviews):
    """One `work run` of one initiative in the repository at `root`: the workers' part is supervise_worker's, the briefs'
    supervise_brief's, the implementation stage's and its merge supervise_merge's, the faults' supervise_faults', the
    branch review's supervise_review's."""

    def __init__(self, root, initiative):
        self.root = Path(root).resolve()
        self.initiative = initiative
        self.dir = self.root / WORK / initiative
        self.claude = os.environ.get("SHOPSYSTEM_WORK_CLAUDE") or "claude"
        self.trees = []          # the worktrees this run added; removed when it ends
        self.outside = None      # where the worktrees go when the repository is inside the plugin's own directory
        self.lock = threading.RLock()     # held for each change to the main checkout while two implementers run (r20)
        self.faults = []         # (work-item, fault) of each work-item this run moved to failed (r40)
        self.own = set()         # the run directories work run copied into the main checkout and has not committed
        self.unlogged = []       # the lines work run appended to log.jsonl since it last committed it

    def rel(self, path):
        return str(Path(path).relative_to(self.root))

    def items(self):
        return [(name, status) for ini, name, status in workqueue.items(self.root) if ini == self.initiative]

    def check(self):
        """What work run was given, before anything changes (r10): the initiative, and each work-item's file and log."""
        if os.environ.get(WORKER):
            raise Refused("it was started by a worker of another `work run` (of %s); a worker starts no delivery"
                          % os.environ[WORKER])
        workqueue.entry(self.initiative, "initiative")
        if not self.dir.is_dir():
            raise Refused("the initiative %s does not exist (no %s)" % (self.initiative, self.rel(self.dir)))
        for name, _ in self.items():
            workqueue.agrees(self.root, self.initiative, name)
        self.branch = git(self.root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        if self.branch == "HEAD":     # detached: no initiative branch to merge onto, rebase on or put back from (r4, r6)
            raise Refused("HEAD is detached; check out the initiative branch work run is to deliver onto")
        status = git(self.root, "--no-optional-locks", "status", "--porcelain", "--untracked-files=all", "--", str(WORK))
        loose = sorted(line[3:] for line in status.stdout.splitlines())
        if loose:     # what a worker's end would put back (r28): committed first, or it is lost (r46)
            raise Refused("%s under %s %s not committed; commit %s before work run starts"
                          % (", ".join(loose), WORK, "is" if len(loose) == 1 else "are", "it" if len(loose) == 1 else "them"))

    def log(self, **line):
        with self.lock:
            text = json.dumps(dict(time=now(), **line)) + "\n"
            workqueue.append(self.dir / "log.jsonl", text.encode())
            self.unlogged.append(text)

    def commit(self, name, before, after, push=True):
        """A move's commit on the initiative branch: the work-item's file, its run directories and log.jsonl (r7); then
        the push of the initiative branch (r38)."""
        paths = [p for p in (self.dir / (name + ".md"), self.dir / "runs" / name, self.dir / "log.jsonl") if p.exists()]
        rels = [self.rel(p) for p in paths]
        git(self.root, "add", "--", *rels)
        git(self.root, "commit", "-q", "-m", "work: %s %s -> %s" % (name, before, after), "--", *rels)
        self.unlogged = []
        self.own = {d for d in self.own if not d.startswith(self.rel(self.dir / "runs" / name) + "/")}
        if push:
            self.push()

    def move(self, name, before, after, question=None, fileset=None):
        with self.lock:
            workqueue.move(self.root, self.initiative, name, after, by=BY)
            if question:
                self.section(name, "Questions", question)
            if fileset:
                self.write_fileset(name, fileset)
            self.commit(name, before, after)

    def section(self, name, heading, text):
        """Write `text` as the last bullet of the work-item's `## <heading>` section, before any section after it (r36);
        its continuation lines are indented, so none of them starts a heading."""
        path = self.dir / (name + ".md")
        old = path.read_text()
        bullet = "- %s\n" % text.strip().replace("\n", "\n  ")
        mark = "\n## %s\n" % heading
        if mark not in old:
            path.write_text(old.rstrip("\n") + "\n" + mark + bullet)
            return
        head, rest = old.split(mark, 1)
        held, sep, after = rest.partition("\n## ")
        held = held.rstrip("\n") + "\n" if held.strip() else ""
        path.write_text(head + mark + held + bullet + ("\n## " + after if sep else ""))

    def write_fileset(self, name, files):
        """The planner's file set as the work-item's `fileset:` (r31), in place of the one it had."""
        path = self.dir / (name + ".md")
        text = path.read_text()
        end = text.find("\n---", 4)
        head = "\n".join(l for l in text[:end].split("\n") if not l.startswith("fileset:"))
        path.write_text(head + "\nfileset: [%s]" % ", ".join(files) + text[end:])


    def step(self, name, status):
        if status == "planned":
            self.move(name, "planned", "ready")
        elif status == "ready":
            self.implement(name)
        else:
            try:
                self.stage(name, status)
            except (Fault, GitFailed) as fault:
                self.fail(name, fault_of(fault))

    def stage(self, name, status):
        """A worker of the stage `status` starts, in a detached worktree; its outcome makes the transition (r3, r5)."""
        stage, agent, after = STAGES[status]
        label, _ = self.run_dir(name, stage)
        tree = self.worktree(name, "%s-%s" % (name, label))
        try:
            start = git(tree, "rev-parse", "HEAD").stdout.strip()
            data, failure = self.worker(name, stage, agent, tree)
            changed = self.tree_changes(tree, start)
        finally:
            self.remove(tree)     # what the worker changed under .shop/work/ goes with it (r6)
        if changed:
            raise Fault("its %s changed %s under .shop/work/, outside its stage directory; work run put %s back"
                        % (ROLE[agent], ", ".join(changed), "it" if len(changed) == 1 else "them"))
        question = self.outcome(agent, data, failure)
        fileset = data.get("fileset") if question is None and agent == "bdd-planner" else None
        self.move(name, status, after if question is None else "awaiting-ruling", question,
                  fileset=fileset if isinstance(fileset, list) and fileset else None)

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

    def held(self, name, heading):
        """The bullets of the work-item's `## <heading>` section, each with its continuation lines."""
        text = (self.dir / (name + ".md")).read_text()
        if "\n## %s\n" % heading not in text:
            return []
        bullets = []
        for line in text.split("\n## %s\n" % heading, 1)[1].split("\n## ", 1)[0].splitlines():
            if line.startswith("- "):
                bullets.append([line])
            elif line.strip() and bullets:
                bullets[-1].append(line)
        return bullets

    def questions(self, name):
        """The lines of the work-item's open questions: those of its `## Questions` past the ones `## Rulings` rules on,
        the n-th ruling answering the n-th question (r32)."""
        return [l for bullet in self.held(name, "Questions")[len(self.held(name, "Rulings")):] for l in bullet]

    def run(self):
        """Pull the work-items one worker at a time until none can move (r1); print where each stands (r9)."""
        self.check()
        self.push_unpushed()
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
                if self.faults:     # a work-item failed: the run ends with it (r40)
                    break
            if all(s in ("green", "withdrawn") for _, s in self.items()):
                self.branch_review()     # inside the try: its worktree goes with the run's (r33)
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
            if status == "failed":
                for fault in self.faulted(name):
                    print("  - %s" % fault)
        if all(s in ("green", "withdrawn") for _, s in statuses):
            return 0
        return 3 if any(s == "awaiting-ruling" for _, s in statuses) and not any(s == "failed" for _, s in statuses) else 1

    def faulted(self, name):
        """The faults of a failed work-item: those its `## Faults` records, the ones this run met as it told them (with a
        failed push of the failure named), r40 and r52."""
        mine = [fault for failed, fault in self.faults if failed == name]
        recorded = [" ".join(b[0][2:].split() + [l.strip() for l in b[1:]]) for b in self.held(name, "Faults")]
        return [r for r in recorded if not any(m.startswith(r) for m in mine)] + mine


def claimed(entry, tracked):
    """What one file set entry claims: itself, and each of the `tracked` files it matches as a glob or holds as a
    directory."""
    under = entry.rstrip("/") + "/"
    return {entry} | {f for f in tracked if fnmatch.fnmatchcase(f, entry) or f.startswith(under)}


def run(root, initiative):
    return Run(root, initiative).run()
