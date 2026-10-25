"""`work run`'s briefs (capability supervision): the one file a worker is given, naming the work-item, the files to
read, where it works and where it writes its result. Standard library only; a part of supervise.Run."""
import json
import re

import workqueue
from supervise_worker import ROUNDS, SCRIPTS, git


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
        item = self.dir / (name + ".md")
        data, _ = workqueue.frontmatter(item.read_text())
        read = [self.rel(item)]
        under = data.get("under")
        if isinstance(under, str) and under:
            read.append("spec/capabilities/%s.md" % under)
        runs = self.dir / "runs" / name
        read += [self.rel(p) for p in sorted(runs.iterdir()) if p.is_dir()] if runs.is_dir() else []
        rnd = stage in ROUNDS
        lines = ["%s: %s" % ("Capability-proposal" if rnd else "Work-item", self.rel(item)), "Agent: %s" % agent,
                 "Scripts: %s" % SCRIPTS]
        if rnd:     # a capability-proposal's round (supervise_rounds.py): the kind its agent runs
            lines.append("Kind: %s" % stage)
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
