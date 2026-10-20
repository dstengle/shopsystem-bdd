"""`work run <initiative>`: the supervisor that takes an initiative's work-items through their stages (capability
supervision). Standard library only.

For each stage it starts a fresh `claude -p` worker of that stage's agent in a worktree of its own, with that stage's
tools only, given one brief file; it reads the outcome only from the worker's result file, which the worker writes in
its worktree's git-ignored .shop/scratch/, and makes the move itself through workqueue.move. Each move is its own commit
of the work-item's file, its run directory (the worker's scratch run directory, copied) and log.jsonl. It takes no
judgment: what is not DONE goes to the person as a question.
"""
import datetime
import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import time
import tomllib
import uuid
from pathlib import Path

import workqueue
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
TESTS = {"work_item": "python3 -m pytest -q --work-item {work_item}", "suite": "python3 -m pytest -q"}
AGENT_PREFIX = "shopsystem-bdd:"
SCRIPTS = Path(__file__).resolve().parent
# The worker's agents are this plugin's: claude is given the plugin root, so an installed copy of another version
# (whose agents may be older or missing) is not the one --agent finds.
# Each stage's tools, the narrowest its agent needs; .shop/delivery.toml's [allowed_tools] replaces a stage's list. No
# list gives a bare Write or Edit, the delivery.toml's either: a worker's writes are left to acceptEdits, which keeps
# them in the worktree it is started in (r13; the bare Write let a researcher write into the main checkout). A
# `claude -p --agent` session does not preload an agent's `skills:`, so each is added as `Skill(<skill>)` to whatever
# list the stage has, and the worker loads it itself.
# A worker's Bash runs pytest, the plugin's scripts by their path and the git commands its stage needs, and no other
# Python (r14).
PYTHON = ["Bash(python3 -m pytest*)", "Bash(python3 %s/*)" % SCRIPTS]
READER = ["Read", "Glob", "Grep", *PYTHON, "Bash(git status*)", "Bash(git diff*)", "Bash(git log*)", "Bash(git show*)"]
TOOLS = {
    "research": READER,
    "plan": ["Read", "Glob", "Grep"],
    "implement": ["Read", "Glob", "Grep", *PYTHON, "Bash(git add *)", "Bash(git commit *)", "Bash(git status*)",
                  "Bash(git diff*)"],
    "review": READER,
}


def git(root, *args):
    """Run git in `root`; a git that fails is work run's refusal, with git's first line of complaint (r10)."""
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if done.returncode != 0:
        said = (done.stderr.strip() or done.stdout.strip() or "exit %d" % done.returncode).splitlines()[0]
        raise Refused("git %s failed: %s" % (" ".join(args), said))
    return done


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


class Run:
    """One `work run` of one initiative in the repository at `root`."""

    def __init__(self, root, initiative):
        self.root = Path(root).resolve()
        self.initiative = initiative
        self.dir = self.root / WORK / initiative
        self.claude = os.environ.get("SHOPSYSTEM_WORK_CLAUDE") or "claude"
        self.trees = []          # the worktrees this run added; removed when it ends
        self.outside = None      # where the worktrees go when the repository is inside the plugin's own directory

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

    def log(self, **line):
        workqueue.append(self.dir / "log.jsonl", (json.dumps(dict(time=now(), **line)) + "\n").encode())

    def commit(self, name, before, after):
        """A move's commit on the initiative branch: the work-item's file, its run directories and log.jsonl (r7)."""
        paths = [p for p in (self.dir / (name + ".md"), self.dir / "runs" / name, self.dir / "log.jsonl") if p.exists()]
        rels = [self.rel(p) for p in paths]
        git(self.root, "add", "--", *rels)
        git(self.root, "commit", "-q", "-m", "work: %s %s -> %s" % (name, before, after), "--", *rels)

    def move(self, name, before, after, question=None):
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

    def run_dir(self, name, stage):
        """The name of the stage's next run directory, `<k>-<stage>`, and its place in the main checkout."""
        runs = self.dir / "runs" / name
        k = len([p for p in runs.iterdir() if p.is_dir()]) + 1 if runs.is_dir() else 1
        return "%d-%s" % (k, stage), runs / ("%d-%s" % (k, stage))

    def base(self):
        """The initiative's base: the commit that added its initiative.md, else none."""
        done = git(self.root, "log", "--diff-filter=A", "--format=%H", "--", self.rel(self.dir / "initiative.md"))
        lines = done.stdout.split()
        return lines[-1] if lines else None

    def brief(self, name, stage, agent, here, tree, branch, extra):
        """The one brief file a worker is given (r2): the work-item, the files to read, where it works and writes."""
        item = self.dir / (name + ".md")
        data, _ = workqueue.frontmatter(item.read_text())
        read = [self.rel(item)]
        under = data.get("under")
        if isinstance(under, str) and under:
            read.append("spec/capabilities/%s.md" % under)
        runs = self.dir / "runs" / name
        read += [self.rel(p) for p in sorted(runs.iterdir()) if p.is_dir()] if runs.is_dir() else []
        lines = ["Work-item: %s" % self.rel(item), "Agent: %s" % agent, "Scripts: %s" % SCRIPTS]
        base = self.base()
        if base:
            lines.append("Base: %s" % base)
        lines += ["Worktree: %s" % tree, "Branch: %s" % (branch or "none (a detached checkout)")]
        lines += ["%s: %s" % kv for kv in extra]
        if stage == "plan":
            lines += self.research_questions(name)
        path = here / "brief.md"
        path.write_text("# %s of %s\n\n%s\n\nRead (paths in your worktree):\n%s\nRun directory: %s\nResult file: %s\n\n"
                        "You start in your worktree, %s: run every command from there, as it is, and never change "
                        "directory (no `cd`, no `git -C`); a command that does is refused.\n\n"
                        "Write your notes, plan, report or findings in the run directory and, last, the result file: "
                        "JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings).\n"
                        % (stage, name, "\n".join(lines), "".join("- %s\n" % r for r in read), here, here / "result.json",
                           tree))
        return path

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

    def snapshot(self):
        """.shop/work/ of the main checkout: its files with their content, and its directories."""
        outside = list((self.root / WORK).rglob("*"))
        return {p: p.read_bytes() for p in outside if p.is_file()}, {p for p in outside if p.is_dir()}

    def put_back(self, kept):
        """.shop/work/ of the main checkout as it was before the worker started: changed and deleted files restored,
        files and directories added removed (r6)."""
        files, dirs = kept
        for path in list((self.root / WORK).rglob("*")):
            if path.is_dir() and path not in dirs:
                shutil.rmtree(path, ignore_errors=True)
            elif path.is_file() and path not in files:
                path.unlink()
        for path, content in files.items():
            if not path.is_file() or path.read_bytes() != content:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)

    def delivery(self):
        path = self.root / ".shop" / "delivery.toml"
        return tomllib.loads(path.read_text()) if path.is_file() else {}

    def tools(self, stage, agent):
        """The stage's list, less a bare Write or Edit (r13), with `Skill(<skill>)` for each skill the agent's definition
        lists (r12)."""
        tools = [t for t in self.delivery().get("allowed_tools", {}).get(stage, TOOLS[stage]) if t not in ("Write", "Edit")]
        definition = SCRIPTS.parent / "agents" / (agent + ".md")
        skills = workqueue.frontmatter(definition.read_text())[0].get("skills") if definition.is_file() else None
        return tools + ["Skill(%s)" % s for s in skills or [] if "Skill(%s)" % s not in tools]

    def trees_dir(self):
        """`.shop/worktrees/`, unless the repository is inside the plugin's own directory (this plugin delivering its own
        work): claude refuses every write under a `--plugin-dir` as a sensitive file, so there the worktrees go in a
        temporary directory outside it, removed when the run ends."""
        plugin = SCRIPTS.parent.resolve()
        if self.root != plugin and plugin not in self.root.parents:
            return self.root / ".shop" / "worktrees"
        if self.outside is None:
            self.outside = Path(tempfile.mkdtemp(prefix="work-run-%s-" % self.initiative))
        return self.outside

    def worktree(self, name, label, branch=None):
        """A worktree of the initiative branch's head for one worker: on `branch`, else detached."""
        tree = self.trees_dir() / label
        if branch:
            git(self.root, "worktree", "add", "-q", "-b", branch, str(tree), "HEAD")
        else:
            git(self.root, "worktree", "add", "-q", "--detach", str(tree), "HEAD")
        self.trees.append(tree)
        scratch = tree / ".shop" / "scratch"
        scratch.mkdir(parents=True, exist_ok=True)
        (scratch / ".gitignore").write_text("*\n")     # the scratch directory ignores itself, whatever the repository does
        return tree

    def remove(self, tree):
        if tree in self.trees:
            self.trees.remove(tree)
            subprocess.run(["git", "worktree", "remove", "--force", str(tree)], cwd=self.root, capture_output=True)

    def worker(self, name, stage, agent, tree, branch=None, extra=()):
        """Start one worker in `tree` and wait for it; its result as a dict, or the reason there is none.

        The worker writes in its worktree's .shop/scratch/<k>-<stage>/; work run copies that into the main checkout's
        run directory, .shop/work/<initiative>/runs/<work-item>/<k>-<stage>/, and reads the result from there."""
        label, kept_at = self.run_dir(name, stage)
        here = tree / ".shop" / "scratch" / label
        here.mkdir(parents=True)
        brief = self.brief(name, stage, agent, here, tree, branch, extra)
        session = str(uuid.uuid4())
        self.log(**{"work-item": name, "stage": stage, "agent": agent, "session": session, "event": "start"})
        kept = self.snapshot()
        done = subprocess.run([self.claude, "-p", "Read the brief file %s and do what it says." % brief,
                               "--agent", AGENT_PREFIX + agent, "--plugin-dir", str(SCRIPTS.parent),
                               "--session-id", session, "--output-format", "json",
                               "--permission-mode", "acceptEdits", "--allowedTools", ",".join(self.tools(stage, agent))],
                              cwd=tree, capture_output=True, text=True)
        self.put_back(kept)
        shutil.copytree(here, kept_at)
        (kept_at / "session.json").write_text(done.stdout)
        self.log(**{"work-item": name, "stage": stage, "agent": agent, "session": session, "event": "end"})
        result = kept_at / "result.json"
        if not result.is_file():
            return None, "%s gave no result file (%s)" % (agent, here / "result.json")
        try:
            data = json.loads(result.read_text())
        except ValueError:
            data = None
        if not isinstance(data, dict):
            return None, "%s's result file %s is not a JSON object" % (agent, self.rel(result))
        self.keep_named(data, tree, here, kept_at)
        questions = data.get("questions")
        if isinstance(questions, str):
            data["questions"] = [questions]
        elif questions is not None and not isinstance(questions, list):
            return None, "%s's result file %s gives its questions as %s, not a list of questions" % (
                agent, self.rel(result), json.dumps(questions))
        return data, None

    def keep_named(self, data, tree, here, kept_at):
        """Copy into the run directory each file of the worktree the result names outside the worker's run directory,
        before the worktree is removed (r15): a field's value that is the path of such a file, absolute or relative to
        the worktree."""
        for field, value in data.items():
            if field in ("status", "summary") or not isinstance(value, str) or not value.strip():
                continue
            path = (tree / value).resolve()
            if path.is_file() and path.is_relative_to(tree.resolve()) and not path.is_relative_to(here.resolve()):
                shutil.copy2(path, kept_at / path.name)

    def outcome(self, agent, data, failure):
        """None for DONE, else the question it puts to the person (r5)."""
        if failure:
            return failure
        if data.get("status") == "DONE":
            return None
        asked = [q if isinstance(q, str) else json.dumps(q) for q in data.get("questions") or []]
        return "; ".join(asked) or "%s gave %s: %s" % (agent, data.get("status"), data.get("summary", ""))

    def tests(self):
        return dict(TESTS, **self.delivery().get("tests", {}))

    def suite_record(self, tree, suite):
        """work run's own whole-suite run in `tree`, as the line `Suite: <N> passed, <M> failed at <hash> in <s> s`."""
        began = time.monotonic()
        done = subprocess.run(shlex.split(suite), cwd=tree, capture_output=True, text=True)
        seconds = time.monotonic() - began
        out = done.stdout + done.stderr
        summary = out.strip().splitlines()[-1] if out.strip() else ""

        def count(word):
            found = re.search(r"(\d+) %s\b" % word, summary)
            return int(found.group(1)) if found else 0
        failing = [l.split(" ", 1)[1].split(" - ")[0] for l in out.splitlines() if l.startswith("FAILED ")]
        head = git(tree, "rev-parse", "--short", "HEAD").stdout.strip()
        line = "Suite: %d passed, %d failed at %s in %.0f s" % (count("passed"), count("failed"), head, seconds)
        return line + ("; failing: %s" % ", ".join(failing) if failing else "")

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
        deleted (r18)."""
        self.move(name, "ready", "claimed")
        tests = self.tests()
        tree = self.worktree(name, name, "work/" + name)
        record = self.suite_record(tree, tests["suite"])
        self.log(**{"work-item": name, "stage": "implement", "event": "suite", "record": record})
        try:
            data, failure = self.worker(name, "implement", "bdd-implementer", tree, "work/" + name,
                                        [("Suite record", record)])
            question = self.outcome("bdd-implementer", data, failure)
            if question is None:
                done = subprocess.run(["git", "rebase", "-q", self.branch], cwd=tree, capture_output=True, text=True)
                if done.returncode != 0:
                    question = "`git rebase %s` failed on %s's branch work/%s:\n%s" % (
                        self.branch, name, name, (done.stdout + done.stderr).strip())
            if question is None:
                changed = self.under_work(tree, name)
                if changed:
                    question = ("bdd-implementer's branch work/%s changed %s under .shop/work/, which only work run "
                                "writes; work run put it back on the branch and did not merge it" % (name, ", ".join(changed)))
            if question is None:
                for cmd in (shlex.split(tests["work_item"].format(work_item=name)), shlex.split(tests["suite"])):
                    done = subprocess.run(cmd, cwd=tree, capture_output=True, text=True)
                    if done.returncode != 0:
                        question = "`%s` failed on %s's branch work/%s:\n%s" % (
                            " ".join(cmd), name, name, (done.stdout + done.stderr).strip())
                        break
            if question is not None:
                self.move(name, "claimed", "awaiting-ruling", question)
                return
            git(self.root, "merge", "--ff-only", "work/" + name)
            self.move(name, "claimed", "done")
        finally:
            self.remove(tree)
        git(self.root, "branch", "-q", "-d", "work/" + name)     # merged, so no longer needed; once its worktree is gone (r18)

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
        if all(s == "green" for _, s in statuses):
            return 0
        return 3 if any(s == "awaiting-ruling" for _, s in statuses) else 1


def run(root, initiative):
    return Run(root, initiative).run()
