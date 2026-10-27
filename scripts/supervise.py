"""`work run <initiative>`: the supervisor that takes an initiative's work-items through their stages (capability
supervision). Standard library only.

For each stage it starts a fresh `claude -p` worker of that stage's agent in a worktree of its own, with that stage's
tools only, given one brief file; it reads the outcome only from the worker's result file, which the worker writes in
its worktree's git-ignored .shop/scratch/, and makes the move itself through workqueue.move. Each move is its own commit
of the work-item's file, its run directory (the worker's scratch run directory, copied) and log.jsonl. It takes no
judgment: what is not DONE goes to the person as a question.
"""
import json
import os
import shutil
import threading
from pathlib import Path

import workqueue
import workqueue_request
from supervise_analysis import Analyses
from supervise_answers import Answers
from supervise_brief import Briefs
from supervise_done import Dones
from supervise_draft import Drafts
from supervise_faults import Fault, Faults, fault_of
from supervise_merge import Merge
from supervise_pool import Pool
from supervise_review import Reviews
from supervise_rounds import Rounds
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


class Run(Workers, Briefs, Merge, Faults, Reviews, Pool, Drafts, Rounds, Analyses, Dones, Answers):
    """One `work run` of one initiative in the repository at `root`: the workers' part is supervise_worker's, the briefs'
    supervise_brief's, the implementation stage's and its merge supervise_merge's, the faults' supervise_faults', the
    branch review's supervise_review's, the pool of workers' supervise_pool's, the drafting's supervise_draft's, a proposal's rounds' supervise_rounds', the measure and analysis of a finished
    initiative supervise_analysis', the answers under a request's delegation supervise_answers'."""

    def __init__(self, root, initiative):
        self.root = Path(root).resolve()
        self.initiative = initiative
        self.dir = self.root / WORK / initiative
        self.claude = os.environ.get("SHOPSYSTEM_WORK_CLAUDE") or "claude"
        self.trees = []          # the worktrees this run added; removed when it ends
        self.outside = None      # where the worktrees go when the repository is inside the plugin's own directory
        self.lock = threading.RLock()     # held for each change to the main checkout while two implementers run (r20)
        self.faults = []         # (work-item, fault) of each work-item this run moved to failed (r40)
        self.noted = []          # (node, fault) of each fault this run recorded and left the node's status as it was (r128)
        self.own = set()         # the run directories work run copied into the main checkout and has not committed
        self.unlogged = []       # the lines work run appended to log.jsonl since it last committed it
        self.delivered = {}      # .shop/delivery.toml, read once by check
        self.limit = 4           # the number of workers at the same time (r60), read from it
        self.finished = []       # the implementers that ended with a worker's end, in that order, not yet merged (r61)
        self.turns = threading.Condition()
        self.round_lock = threading.Lock()     # held by an integrate, apply or formulate round, shared by those runs (r95)
        self.group = [self]    # the runs of one `work run` with no initiative, which share the checkout (supervise_all)
        self.slots = threading.Semaphore(self.limit)     # the sessions at the same time (r60), shared by those runs

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
        self.read_delivery()
        if not self.dir.is_dir():
            raise Refused("the initiative %s does not exist (no %s)" % (self.initiative, self.rel(self.dir)))
        for name, _ in self.items():  # noqa: PERF102 -- items() is a list of pairs, not a dict
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

    def commit(self, name, before, after, push=True, also=()):
        """A move's commit on the initiative branch: the work-item's file, its run directories and log.jsonl (r7); then
        the push of the initiative branch (r38)."""
        item = "initiative.md" if name == self.initiative else name + ".md"
        paths = [p for p in (self.dir / item, self.dir / "runs" / name, self.dir / "log.jsonl") if p.exists()]
        rels = [self.rel(p) for p in paths] + list(also)
        git(self.root, "add", "--", *rels)
        git(self.root, "commit", "-q", "-m", "work: %s %s -> %s" % (name, before, after), "--", *rels)
        self.unlogged = []
        self.own = {d for d in self.own if not d.startswith(self.rel(self.dir / "runs" / name) + "/")}
        if push:
            self.push()

    def move(self, name, before, after, question=None, fileset=None, also=()):
        with self.lock:
            workqueue.move(self.root, self.initiative, name, after, by=BY)
            for each in [question] if isinstance(question, str) else question or []:     # a gate gives several
                self.section(name, "Questions", each)
            if fileset:
                self.write_fileset(name, fileset)
            self.commit(name, before, after, also=also)

    def section(self, name, heading, text):
        """Write `text` as the last bullet of the work-item's `## <heading>` section, before any section after it (r36);
        its continuation lines are indented, so none of them starts a heading."""
        path = self.dir / ("initiative.md" if name == self.initiative else name + ".md")
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
            data, failure = self.worker(name, stage, agent, tree, extra=self.merged(name) if stage == "review" else ())
            changed = self.tree_changes(tree, start)
        finally:
            self.remove(tree)     # what the worker changed under .shop/work/ goes with it (r6)
        if changed:
            raise Fault("its %s changed %s under .shop/work/, outside its stage directory; work run put %s back"
                        % (ROLE[agent], ", ".join(changed), "it" if len(changed) == 1 else "them"))
        question = self.outcome(agent, data, failure)
        fileset = data.get("fileset") if question is None and agent == "bdd-planner" else None
        self.move(name, status, after if question is None else "awaiting-answer", question,
                  fileset=fileset if isinstance(fileset, list) and fileset else None)

    def merged(self, name):
        """For a reviewer's brief: the commits the work-item's last merge brought and work run's whole-suite record on
        them, so the reviewer neither derives the one nor runs the other (agent-time analysis 2026-10-27)."""
        found = [l for l in workqueue.logged(self.dir / "log.jsonl", self.root)
                 if l.get("work-item") == name and l.get("event") == "merged"]
        if not found:
            return ()
        return (("Commits", " ".join(found[-1].get("commits") or []) or "none"), ("Suite record", found[-1].get("record")))

    def held(self, name, heading):
        """The bullets of the work-item's `## <heading>` section, each with its continuation lines."""
        text = (self.dir / ("initiative.md" if name == self.initiative else name + ".md")).read_text()
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
        """The lines of the work-item's open questions: those of its `## Questions` past the ones `## Answers` answers,
        the n-th answer answering the n-th question (r32)."""
        return [l for bullet in self.held(name, "Questions")[len(self.held(name, "Answers")):] for l in bullet]

    def run(self):
        """Pull the work-items through their stages, side by side, until none can move (r1); print where each stands
        (r9)."""
        self.check()
        self.push_unpushed()
        self.pull_through()
        return asked(self.root, self.show())

    def pull_through(self):
        """The initiative's part of a run once checked: answers, rounds, drafting, the pool, the branch review."""
        try:
            self.answers()
            refused = None
            try:
                self.rounds()
            except Refused as fault:     # r115: a round that stopped holds back its own node; the others go on, then the error
                refused = fault
            self.draft()
            self.pull(MOVABLE)
            if refused is None and self.items() and all(s in ("green", "withdrawn") for _, s in self.items()) \
                    and self.draft_retires():     # r123, r124: drafted before the review and the measurement, then pulled
                self.push()
                self.pull(MOVABLE)
            if refused is not None:
                if self.noted:     # r128: the node whose session faulted is printed with its fault, then the error
                    self.show()
                raise refused
            if self.items() and all(s in ("green", "withdrawn") for _, s in self.items()):     # r94, r97: none is not done
                kept = self.branch_review()     # inside the try: its worktree goes with the run's (r33)
                while kept is not None and self.fix_work_item(kept):     # r74: the fix is pulled
                    self.push()
                    self.pull(MOVABLE)
                    if not all(s in ("green", "withdrawn") for _, s in self.items()):
                        break     # a fix that did not turn green gets no review in this run
                    kept = self.branch_review()     # r110: the fix, reviewed in the same run
                if kept is not None and self.lists_nothing(kept) and any(s == "green" for _, s in self.items()):     # r75, r76
                    self.analyse()
                    self.set_done()     # r105, r109
        finally:
            for tree in list(self.trees):      # on every way out, a failure's too: the run leaves no worktree
                self.remove(tree)
            if self.outside is not None:
                shutil.rmtree(self.outside, ignore_errors=True)

    def show(self, nodes=None, indent=""):
        """Print each node's status, its open questions and its faults; the exit code of a run of this initiative alone."""
        statuses = self.items() + [(n, s) for n, s in self.proposals() if n != self.initiative] if nodes is None else nodes
        for name, status in statuses:
            print("%s%s %s" % (indent, name, status))
            if status == "awaiting-answer":
                for line in self.questions(name):
                    print("%s  %s" % (indent, line))
            if status == "failed" or any(noted == name for noted, _ in self.noted):
                for fault in self.faulted(name):
                    print("%s  - %s" % (indent, fault))
        if nodes is None:     # r128: a proposal or the initiative itself, which a round faulted
            for name in dict.fromkeys(n for n, _ in self.noted if n not in dict(statuses)):
                data, _ = workqueue.frontmatter((self.dir / ("initiative.md" if name == self.initiative else name + ".md")).read_text())
                print("%s %s" % (name, data.get("status")))
                for fault in self.faulted(name):
                    print("  - %s" % fault)
        if all(s in ("green", "withdrawn", "formulated", "merged") for _, s in statuses):     # a proposal ends formulated
            return 0
        return 3 if any(s == "awaiting-answer" for _, s in statuses) and not any(s == "failed" for _, s in statuses) else 1

    def draft(self):
        """The work-items of the initiative's formulated capability-proposals, drafted (r72) and pushed (r38)."""
        if self.draft_proposals():
            self.push()

    def faulted(self, name):
        """The faults of a failed work-item: those its `## Faults` records, the ones this run met as it told them (with a
        failed push of the failure named), r40 and r52."""
        mine = [fault for failed, fault in self.faults + self.noted if failed == name]
        recorded = [" ".join(b[0][2:].split() + [l.strip() for l in b[1:]]) for b in self.held(name, "Faults")]
        return [r for r in recorded if not any(m.startswith(r) for m in mine)] + mine


def asked(root, code):
    """Print each request whose asker is this context and which waits in the asker's turn, with its open questions; such
    a request makes a successful exit an error (r101)."""
    waiting = workqueue_request.asked_here(root)
    for name, open_questions in waiting:
        print("%s awaiting-asker" % name)
        for question in open_questions:
            print("  %s" % question)
    return 3 if waiting and code == 0 else code


def run(root, initiative):
    return Run(root, initiative).run()
