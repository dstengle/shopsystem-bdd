"""`work run`'s rounds for a capability-proposal (capability supervision r70, r71, r80, r83): an `awaiting-answer`
proposal whose every question has an answer is given to an apply round and, once that has ended, approved; an approved one
is given to a formulate round and, once that has ended, formulated. Standard library only; a part of supervise.Run."""
import json
import subprocess

import workqueue
import workqueue_done
import workqueue_request
from supervise_change import BadChanges, Changes, entries
from supervise_faults import Fault, fault_of
from supervise_worker import GitFailed, git
from workqueue import Refused

SERIAL = ("integrate", "apply", "formulate")     # the rounds one at a time across initiatives (r95)
AFTER ={"drafted": ("gate", "awaiting-answer"), "awaiting-answer": ("apply", "approved"), "approved": ("formulate", "formulated")}


class Rounds(Changes):
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
        data, _ = workqueue.frontmatter((self.dir / "initiative.md").read_text())
        if data.get("fulfils") and (data.get("status") == "proposed" or (     # r79: no request, no lines to integrate
                data.get("status") == "started" and not self.proposals() and not self.items())):     # r93
            try:     # a request the queue lacks gives no round, before anything moves
                workqueue_request.accepted_lines(self.root, str(data["fulfils"]).rsplit("/", 1)[-1])
                return (self.initiative, "integrate", "started")
            except Refused:
                pass
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
        """One round. An integrate, apply or formulate round holds the round lock of every initiative a `work run`
        takes, from before its session to its last commit, so no two run side by side (r95); the gate round does not."""
        if kind not in SERIAL:
            return self.run_round(name, kind, after)
        with self.round_lock:
            return self.run_round(name, kind, after)

    def run_round(self, name, kind, after):
        if kind == "integrate":     # r84: the initiative is started as its integrate round is, before the round's session
            status, _ = workqueue.frontmatter((self.dir / "initiative.md").read_text())
            if status.get("status") == "proposed":     # r93: one already started has no transition to make
                self.start_initiative(name, after)
            before = after
        else:
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
        if data.get("status") != "DONE":     # r87: no transition, and nothing written on the node; r88: the run stops
            self.keep_round(name, kind, label)
            raise Refused("the %s round of %s (%s) gave the outcome %s, and %s keeps its status %s: %s" % (
                kind, name, self.rel(self.dir / "runs" / name / label), data.get("status"), name, before,
                data.get("summary", "")))
        found = []
        if kind == "integrate":     # r96, r92: a DONE without a change list is an error; the list gives the proposals
            try:
                found = entries(data)
            except BadChanges as bad:
                self.refuse_integrate(name, label, before, "its result cannot be read: %s" % bad)
            if not found:
                self.refuse_integrate(name, label, before, "it gave DONE without a change list")
        absent = self.unknown(found, self.dir / "runs" / name / label) if kind == "integrate" else []
        if absent and len(absent) == len(found):     # r107: no proposal for it; the round is kept as r96 keeps it
            self.refuse_integrate(name, label, before, "its change list names %s, which neither spec/capabilities/ nor "
                                  "its drafts have" % ", ".join(absent))
        found = [one for one in found if one["capability"] not in absent]
        asked = [q if isinstance(q, str) else json.dumps(q) for q in data.get("questions") or []] if kind == "gate" else None
        if kind == "gate" and not asked:     # r117: a gate with nothing to decide still asks for the approval of the lines
            asked = ["Are the lines of %s approved as drafted? Readings: approve %s as drafted (recommended), "
                     "or change its lines." % (name, name)]
        if kind != "integrate":
            self.move(name, before, after, asked)
        else:     # r84: the round's stage directory is committed once it has ended, on top of the commit of started
            with self.lock:
                proposals = self.write_proposals(found, self.kept_path(self.dir / "runs" / name / label))
                self.commit(name, after, after, also=[self.rel(p) for p in proposals])
            if absent:     # r107: the known capabilities' proposals are written; the unknown ones are an error
                raise Refused("the integrate round of %s (%s) named %s, which neither spec/capabilities/ nor its drafts have; "
                              "no capability-proposal was written for %s" % (
                                  name, self.rel(self.dir / "runs" / name / label), ", ".join(absent),
                                  "it" if len(absent) == 1 else "them"))

    def refuse_integrate(self, name, label, before, why):
        """The integrate round ended DONE with no change list `work run` can use: its stage directory and drafts kept,
        the status kept, and the run's error naming the round (r96)."""
        self.keep_round(name, "integrate", label)
        raise Refused("the integrate round of %s (%s) gave DONE, and %s keeps its status %s: %s" % (
            name, self.rel(self.dir / "runs" / name / label), name, before, why))

    def start_initiative(self, name, after):
        """The initiative's own transition from proposed: its status written, logged and committed (not a work-item's move)."""
        with self.lock:
            workqueue_done.mark(self.dir, self.root, after)
            self.log(**{"work-item": name, "before": "proposed", "after": after, "by": "work run"})
            self.commit(name, "proposed", after)

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
