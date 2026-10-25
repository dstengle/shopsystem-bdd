"""`work run`'s rounds for a capability-proposal (capability supervision r70, r71, r80, r83): an `awaiting-answer`
proposal whose every question has an answer is given to an apply round and, once that has ended, approved; an approved one
is given to a formulate round and, once that has ended, formulated. Standard library only; a part of supervise.Run."""
import json
import subprocess

import workqueue
from supervise_faults import Fault, fault_of
from supervise_worker import GitFailed, git
from workqueue import Refused

AFTER = {"drafted": ("gate", "awaiting-answer"), "awaiting-answer": ("apply", "approved"), "approved": ("formulate", "formulated")}


class Rounds:
    """The part of supervise.Run that runs a capability-proposal's rounds, one session at a time."""

    def proposals(self):
        """(name, status) of each capability-proposal of the initiative, by name."""
        found = []
        for path in sorted(self.dir.glob("*.md")):
            data, _ = workqueue.frontmatter(path.read_text())
            if data.get("kind") == "capability-proposal":
                found.append((path.stem, data.get("status")))
        return found

    def due(self):
        """(name, round, status after) of the first proposal with a round to run, else None. Its questions all have an
        answer when its `## Answers` holds as many bullets as its `## Questions`, none at all included (r70)."""
        for name, status in self.proposals():
            if status in AFTER and (status != "awaiting-answer"
                                    or len(self.held(name, "Answers")) >= len(self.held(name, "Questions"))):
                return (name, *AFTER[status])
        return None

    def rounds(self):
        """Run the rounds due until none is; a Refused naming the round when one faults (it keeps the proposal as it was)."""
        due = self.due()
        while due:
            self.round(*due)
            due = self.due()

    def round(self, name, kind, after):
        before = workqueue.agrees(self.root, self.initiative, name)
        label, _ = self.run_dir(name, kind)
        branch = "round/%s-%s" % (name, label)
        tree = None
        try:
            tree = self.worktree(name, "%s-%s" % (name, label), branch)
            data, failure = self.worker(name, kind, "initiative-round", tree, branch)
            if failure:
                raise Fault(failure)
            self.remove(tree)
            with self.lock:     # the round's commits reach the initiative branch before the transition
                git(self.root, "merge", "-q", "--no-edit", branch)
                git(self.root, "branch", "-q", "-d", branch)
        except (Fault, GitFailed) as fault:
            if tree is not None:
                self.remove(tree)
            subprocess.run(["git", "merge", "--abort"], cwd=self.root, capture_output=True)
            self.keep_round(name, kind, label)
            raise Refused("the %s round of %s (%s) faulted, and %s keeps its status %s: %s" % (
                kind, name, self.rel(self.dir / "runs" / name / label), name, before, fault_of(fault))) from None
        asked = [q if isinstance(q, str) else json.dumps(q) for q in data.get("questions") or []] if kind == "gate" else None
        self.move(name, before, after, asked)

    def keep_round(self, name, kind, label):
        """The round's stage directory and log lines, committed with no transition, so the next `work run` finds nothing
        uncommitted under .shop/work/ and starts the round again."""
        rels = [self.rel(p) for p in (self.dir / "runs" / name, self.dir / "log.jsonl") if p.exists()]
        if rels and git(self.root, "status", "--porcelain", "--", *rels).stdout.strip():
            git(self.root, "add", "--", *rels)
            git(self.root, "commit", "-q", "-m", "work: %s %s round %s faulted" % (name, kind, label), "--", *rels)
            self.unlogged = []
            self.own = {d for d in self.own if not d.startswith(self.rel(self.dir / "runs" / name) + "/")}
            self.git_push()
