"""`work run`'s answers under a delegation (capability supervision r77, r78): when the request an initiative fulfils gives
a delegation, each open question of its awaiting-answer work-items and capability-proposals goes to a session of its own,
given the question, the delegation and the files the question names, and nothing else. An answer the session gives is
written naming the delegation. Standard library only; a part of supervise.Run."""
import datetime
import json
import re

import workqueue
import workqueue_answer
import workqueue_request
from supervise_faults import Fault, fault_of
from supervise_worker import SCRIPTS, GitFailed, git
from workqueue import Refused

AGENT = "delegation-answerer"
VERDICT = (" The question is a reviewer's: also give `verdict`, `change` when the answer asks for the work-item to be "
           "changed, `accept` when it takes the work-item as it is.")
PATH = re.compile(r"[\w.\-]+(?:/[\w.\-]+)+\.\w+")


def files_named(question):
    """The relative paths a question names, in order of appearance, each once: a word of it, less the punctuation round
    it, that has a `/` and a file suffix."""
    found = []
    for word in question.split():
        word = word.strip("\"'`.,;:?!()[]")
        if PATH.fullmatch(word) and word not in found:
            found.append(word)
    return found


class Answers:
    """The part of supervise.Run that has a delegation's questions answered by sessions."""

    def delegation(self):
        """The delegation of the request the initiative fulfils, else None."""
        try:
            fulfils = workqueue_request.field(workqueue.read(self.dir / "initiative.md", self.root), "fulfils")
            if not fulfils:
                return None
            path = workqueue_request.path_of(self.root, fulfils.rsplit("/", 1)[-1])
            value = workqueue_request.field(workqueue.read(path, self.root), "delegation")
        except (Refused, OSError):
            return None
        if value and value.startswith('"') and value.endswith('"') and len(value) > 1:
            value = json.loads(value)
        return value or None

    def asking(self):
        """The names of the initiative's work-items and capability-proposals that are awaiting-answer."""
        found = []
        for path in sorted(self.dir.glob("*.md")):
            data, _ = workqueue.frontmatter(path.read_text())
            if data.get("status") == "awaiting-answer" and data.get("kind") in ("work-item", "capability-proposal"):
                found.append((path.stem, data["kind"]))
        return found

    def open_questions(self, name):
        return [" ".join(l.strip() for l in bullet)[2:] for bullet in self.held(name, "Questions")[len(self.held(name, "Answers")):]]

    def answers(self):
        """Give each open question of the initiative, under its request's delegation, to a session of its own; a
        question the session answers is written as answered (r77, r78)."""
        delegation = self.delegation()
        if delegation is None:
            return
        self.verdicts = {}
        for name, kind in self.asking():
            before = workqueue.agrees(self.root, self.initiative, name)
            left = False
            for question in self.open_questions(name):
                answer = self.ask(name, question, delegation)
                if answer is None or left:     # the n-th answer answers the n-th question: none is written after a gap
                    left = True
                    continue
                self.section(name, "Answers", "%s: %s\nby: work run, under the delegation \"%s\"" % (
                    datetime.date.today().isoformat(), answer, delegation))
                self.commit(name, before, before)     # kept now: the next session's end must not find it uncommitted (r28)
            if kind == "work-item" and not left and self.open_questions(name) == []:
                path = self.dir / (name + ".md")
                if workqueue_answer.asked_by_reviewer(self.root, path, name):
                    target = workqueue_answer.reviewer_status(self.verdicts[name] == "change")
                else:
                    target = workqueue_answer.asked_from(self.root, path, name)
                self.move(name, before, target)
            elif self.uncommitted(name):
                self.commit(name, before, before)
        self.push()

    def uncommitted(self, name):
        """Whether the item's file, its run directories or the log differ from the last commit."""
        item = self.dir / (name + ".md")
        rels = [self.rel(p) for p in (item, self.dir / "runs" / name, self.dir / "log.jsonl") if p.exists()]
        return bool(git(self.root, "status", "--porcelain", "--untracked-files=all", "--", *rels).stdout.strip())

    def ask(self, name, question, delegation):
        """One session given `question` under `delegation`: its answer, else None when it leaves the question for the
        person (a DONE with no answer, any other outcome, or an answer of more than one line)."""
        label, _ = self.run_dir(name, "answer")
        tree = self.worktree(name, "%s-%s" % (name, label))
        try:
            start = git(tree, "rev-parse", "HEAD").stdout.strip()
            reviewer = workqueue_answer.asked_by_reviewer(self.root, self.dir / (name + ".md"), name)
            extra = (("Question", question), ("Delegation", delegation)) + ((("Reviewer", "yes"),) if reviewer else ())
            data, failure = self.worker(name, "answer", AGENT, tree, extra=extra)
            changed = self.tree_changes(tree, start)
        except (Fault, GitFailed) as fault:
            failure, changed = fault_of(fault), []
        finally:
            self.remove(tree)
        if failure or changed:
            self.keep_round(name, "answer", label)     # the record is kept in the initiative's history, then the run stops
            raise Refused("the session answering %s's question faulted: %s" % (
                name, failure or "it changed %s under .shop/work/" % ", ".join(changed)))
        answer = data.get("answer")
        if data.get("status") != "DONE" or not isinstance(answer, str) or not answer.strip():
            return None
        if workqueue_answer.asked_by_reviewer(self.root, self.dir / (name + ".md"), name):
            if data.get("verdict") not in ("change", "accept"):     # no verdict: the question is left for the person
                return None
            self.verdicts[name] = data["verdict"]
        return None if any(c in answer for c in workqueue_answer.LINE_BREAKS) else answer.strip()

    def answer_brief(self, here, tree, extra):
        """The brief of an answering session (r77): the question, the delegation, the files the question names to read,
        and where it works and writes its result."""
        given = dict(extra)
        files = files_named(given["Question"])
        path = here / "brief.md"
        path.write_text("# answer\n\nAgent: %s\nScripts: %s\nBase: none\nWorktree: %s\nBranch: none (a detached checkout)\n"
                        "Question: %s\nDelegation: %s\n\nRead (paths in your worktree):\n%sRun directory: %s\n"
                        "Result file: %s\n\nYou start in your worktree, %s: run every command from there, as it is, and "
                        "never change directory (no `cd`, no `git -C`); a command that does is refused.\n\n"
                        "Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON "
                        "with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the "
                        "delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise "
                        "give `DONE` with no `answer`.%s\n"
                        % (AGENT, SCRIPTS, tree, given["Question"], given["Delegation"],
                           "".join("- %s\n" % f for f in files), here, here / "result.json", tree,
                           VERDICT if given.get("Reviewer") else ""))
        return path
