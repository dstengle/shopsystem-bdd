"""`work run`'s briefs (capability supervision): the one file a worker is given, naming the work-item, the files to
read, where it works and where it writes its result. Standard library only; a part of supervise.Run."""
import json
import re

import supervise_drafts
import workqueue
import workqueue_request
from supervise_worker import ROUNDS, SCRIPTS, git

CHANGE_LIST = ("Give your change list in your result's `changes`: a list with one entry for each capability, each "
               '`{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as '
               "`<capability>#r<n>` or `term/<term>`.")


class Briefs:
    """The part of supervise.Run that writes a worker's brief."""

    def base(self):
        """The initiative's base: the commit that added its initiative.md, else none."""
        done = git(self.root, "log", "--diff-filter=A", "--format=%H", "--", self.rel(self.dir / "initiative.md"))
        lines = done.stdout.split()
        return lines[-1] if lines else None

    def brief(self, name, stage, agent, here, tree, branch, extra):
        """The one brief file a worker is given (r2): the work-item, the files to read, where it works and writes."""
        if stage == "answer":     # the question, the delegation and the files it names, and nothing else (r77)
            return self.answer_brief(here, tree, extra)
        item = self.dir / ("initiative.md" if name == self.initiative else name + ".md")
        data, _ = workqueue.frontmatter(item.read_text())
        read = [self.rel(item)]
        under = data.get("under")
        if isinstance(under, str) and under:
            read.append("spec/capabilities/%s.md" % under)
        runs = self.dir / "runs" / name
        read += [self.rel(p) for p in sorted(runs.iterdir()) if p.is_dir()] if runs.is_dir() else []
        rnd = stage in ROUNDS
        label = "Initiative" if stage == "integrate" else "Capability-proposal" if rnd else "Work-item"
        lines = ["%s: %s" % (label, self.rel(item)), "Agent: %s" % agent, "Scripts: %s" % SCRIPTS]
        if rnd:     # a round (supervise_rounds.py): the kind its agent runs
            lines.append("Kind: %s" % stage)
            if stage == "integrate":
                lines += self.integrate_lines(data, here)
            if stage == "gate":
                lines.append("Give the gate as questions in your result's `questions`, one string each: every question a "
                             "decision, with its readings and the recommended reading marked.")
                lines += ["%s: %s" % (kind.capitalize(), ", ".join(data.get(kind) or []) or "none")     # r104
                          for kind in ("adds", "changes", "removes")]
                lines.append("Ask questions only on the lines and terms listed above as adds, changes or removes, and on "
                             "no other line or term.")
            if stage == "apply":     # r114: the list the round applied, which `work run` writes into the proposal
                lines.append(CHANGE_LIST.replace("Give your change list", "Give the change list of what you applied"))
            if stage in ("gate", "apply"):     # r108: the kept drafts of the integrate round that wrote the proposal
                kept = re.search(r"The drafts of this proposal are in (\S+?)\.(?:\s|$)", item.read_text())
                if kept:
                    lines.append("Drafts path: %s" % kept.group(1))
                    read.append(kept.group(1))
        base = self.base()
        if base:
            lines.append("Base: %s" % base)
        lines += ["Worktree: %s" % tree, "Branch: %s" % (branch or "none (a detached checkout)")]
        if not rnd:
            lines.append("Work-item branch: work/%s" % name)
        lines += ["%s: %s" % kv for kv in extra]
        if stage == "research":
            lines += self.research_lines(data)
        if stage == "plan":
            lines += self.research_questions(name)
        if stage == "implement":
            lines += self.findings_lines(name)
        lines += self.answer_lines(name)
        path = here / "brief.md"
        path.write_text("# %s of %s\n\n%s\n\nRead (paths in your worktree):\n%s\nRun directory: %s\nResult file: %s\n\n"
                        "You start in your worktree, %s: run every command from there, as it is, and never change "
                        "directory (no `cd`, no `git -C`); a command that does is refused.\n\n"
                        "Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: "
                        "JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so "
                        "that a session that stops part-way still leaves a result, and one that does not claim the "
                        "work done. Write your notes, plan, report or findings in the run directory.\n"
                        % (stage, name, "\n".join(lines), "".join("- %s\n" % r for r in read), here, here / "result.json",
                           tree))
        return path

    def integrate_lines(self, data, here):
        """The request the initiative fulfils and the lines of it with the line outcome accepted, and no other; then the
        drafts path, which `work run` keeps with the round's stage directory however the round ends (r91), and the form
        of the change list the result gives (r92)."""
        ident = str(data.get("fulfils") or "").rsplit("/", 1)[-1]
        others = supervise_drafts.added_by_others(self.root, self.initiative)     # r102
        return ["Request: %s" % ident, "Accepted lines of the request:"] + [
            "- %d. %s" % line for line in workqueue_request.accepted_lines(self.root, ident)] + [
            "Ids drafted elsewhere (number added lines above each on the same capability): %s"
            % (", ".join(others) or "none"),
            "Drafts path: %s" % (here / "drafts"),
            CHANGE_LIST]

    def findings_lines(self, name):
        """For a work-item an answer to its reviewer's question returned to ready (r98), a line naming the findings file
        of its last review stage directory."""
        moves = []
        log = self.dir / "log.jsonl"
        for line in log.read_text().splitlines() if log.is_file() else []:
            data = json.loads(line)
            if isinstance(data, dict) and data.get("work-item") == name and "after" in data:
                moves.append((data.get("before"), data["after"]))
        into = [i for i, m in enumerate(moves) if m[1] == "ready"]     # the claim after it is no part of the route
        if not into or into[-1] == 0 or moves[into[-1]][0] != "awaiting-answer" or moves[into[-1] - 1] != ("done", "awaiting-answer"):
            return []
        runs = self.dir / "runs" / name
        reviews = sorted((p for p in runs.glob("*-review") if p.name.split("-")[0].isdigit()),
                         key=lambda p: int(p.name.split("-")[0])) if runs.is_dir() else []
        return ["Reviewer's findings: %s" % self.rel(reviews[-1] / "findings.md")] if reviews else []

    def answer_lines(self, name):
        """The work-item's answers as brief lines (r57), each beside the question it answers: the n-th bullet of
        `## Answers` answers the n-th bullet of `## Questions`."""
        pairs = list(zip(self.held(name, "Questions"), self.held(name, "Answers")))
        if not pairs:
            return []
        lines = ["Answers the person gave, each with the question it answers:"]
        for question, answer in pairs:
            lines += ["- Question: %s" % " ".join(l.strip() for l in question)[2:],
                      "  Answer: %s" % " ".join(l.strip() for l in answer)[2:]]
        return lines

    def research_questions(self, name):
        """The questions the work-item's last research run gave with its DONE, as brief lines for the planner (r16)."""
        runs = self.dir / "runs" / name
        done = sorted((p for p in runs.glob("*-research") if p.is_dir() and p.name.split("-")[0].isdigit()),
                      key=lambda p: int(p.name.split("-")[0])) if runs.is_dir() else []
        data = json.loads((done[-1] / "result.json").read_text()) if done else {}
        if data.get("status") != "DONE" or not data.get("questions"):
            return []
        asked = data["questions"] if isinstance(data["questions"], list) else [data["questions"]]
        return ["Questions the researcher gave with its DONE, for you to settle or ask:"] + [
            "- %s" % (q if isinstance(q, str) else json.dumps(q)) for q in asked]

    def research_lines(self, data):
        """The researcher's start (r19): the work-item's file set, and the scenarios it accepts, by feature file and
        title, so the researcher reads them rather than searching for them."""
        lines = []
        if data.get("fileset"):
            lines.append("File set: %s" % ", ".join(data["fileset"]))
        accepted = accepted_scenarios(self.root, data.get("accepts") or [])
        if accepted:
            lines += ["Accepted scenarios:"] + ["- %s: %s" % pair for pair in accepted]
        return lines


def accepted_scenarios(root, accepts):
    """(feature file, title) of each scenario tagged with a requirement in `accepts` (`<capability>#r<n>`, or a range
    `#r<n>-r<m>`), from features/<capability>.feature where there is one."""
    wanted = {}
    for one in accepts:
        cap, _, reqs = str(one).rpartition("/")[2].partition("#")
        lo, _, hi = reqs.lstrip("r").partition("-r")
        wanted.setdefault(cap, set()).update("@r%d" % n for n in range(int(lo), int(hi or lo) + 1))
    found = []
    for cap, tags in wanted.items():
        rel = "features/%s.feature" % cap
        path = root / rel
        held = set()
        for line in path.read_text().splitlines() if path.is_file() else []:
            line = line.strip()
            if line.startswith("@"):
                held |= set(line.split())
            elif re.match(r"Scenario( Outline)?:", line):
                if held & tags:
                    found.append((rel, line.split(":", 1)[1].strip()))
                held = set()
    return found
