"""`work run <initiative>`: the supervisor that takes an initiative's work-items through their stages (capability
supervision). Standard library only.

For each stage it starts a fresh `claude -p` worker of that stage's agent, given one brief file, reads the outcome only
from the worker's result file and makes the move itself through workqueue.move; each move is its own commit of the
work-item's file, its run directory and log.jsonl. It takes no judgment: what is not DONE goes to the person as a
question.
"""
import datetime
import json
import os
import shlex
import subprocess
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


def git(root, *args, check=True):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=check)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


class Run:
    """One `work run` of one initiative in the repository at `root`."""

    def __init__(self, root, initiative):
        self.root = Path(root).resolve()
        self.initiative = initiative
        self.dir = self.root / WORK / initiative
        self.claude = os.environ.get("SHOPSYSTEM_WORK_CLAUDE") or "claude"

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

    def log(self, **line):
        with open(self.dir / "log.jsonl", "a") as out:
            out.write(json.dumps(dict(time=now(), **line)) + "\n")

    def commit(self, name, before, after):
        """A move's commit on the initiative branch: the work-item's file, its run directories and log.jsonl (r7)."""
        paths = [p for p in (self.dir / (name + ".md"), self.dir / "runs" / name, self.dir / "log.jsonl") if p.exists()]
        rels = [self.rel(p) for p in paths]
        git(self.root, "add", "--", *rels)
        git(self.root, "commit", "-q", "-m", "work: %s %s -> %s" % (name, before, after), "--", *rels)

    def move(self, name, before, after, question=None):
        workqueue.move(self.root, self.initiative, name, after, by=BY)
        if question:
            path = self.dir / (name + ".md")
            text = path.read_text()
            if "\n## Questions\n" not in text:
                text = text.rstrip("\n") + "\n\n## Questions\n"
            path.write_text(text + "- %s\n" % question.replace("\n", "\n  "))
        self.commit(name, before, after)

    def run_dir(self, name, stage):
        runs = self.dir / "runs" / name
        k = len([p for p in runs.iterdir() if p.is_dir()]) + 1 if runs.is_dir() else 1
        path = runs / ("%d-%s" % (k, stage))
        path.mkdir(parents=True)
        return path

    def brief(self, name, stage, agent, here):
        """The one brief file a worker is given: the work-item, the files to read and the result file (r2)."""
        item = self.dir / (name + ".md")
        data, _ = workqueue.frontmatter(item.read_text())
        read = [self.rel(item)]
        under = data.get("under")
        if isinstance(under, str) and under:
            read.append("spec/capabilities/%s.md" % under)
        runs = self.dir / "runs" / name
        read += [self.rel(p) for p in sorted(runs.iterdir()) if p.is_dir() and p != here] if runs.is_dir() else []
        path = here / "brief.md"
        path.write_text("# %s of %s\n\nWork-item: %s\nAgent: %s\n\nRead:\n%s\n\nRun directory: %s\nResult file: %s\n\n"
                        "Write your notes, plan, report or findings in the run directory and, last, the result file: "
                        "JSON with `status`, `summary` (under fifteen lines) and `questions`.\n"
                        % (stage, name, self.rel(item), agent, "".join("- %s\n" % r for r in read), here,
                           here / "result.json"))
        return path

    def snapshot(self, here):
        """The files under .shop/work/ outside the worker's run directory `here`."""
        return {p: p.read_bytes() for p in (self.root / WORK).rglob("*") if p.is_file() and here not in p.parents}

    def worker(self, name, stage, agent, cwd):
        """Start one worker and wait for it; its result as a dict, or the reason there is none."""
        here = self.run_dir(name, stage)
        brief = self.brief(name, stage, agent, here)
        session = str(uuid.uuid4())
        self.log(**{"work-item": name, "stage": stage, "agent": agent, "session": session, "event": "start"})
        kept = self.snapshot(here)
        done = subprocess.run([self.claude, "-p", str(brief), "--agent", AGENT_PREFIX + agent, "--session-id", session,
                               "--output-format", "json", "--permission-mode", "acceptEdits"],
                              cwd=cwd, capture_output=True, text=True)
        for path, content in kept.items():          # r6: a worker's change under .shop/work/ is put back
            if not path.is_file() or path.read_bytes() != content:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
        (here / "session.json").write_text(done.stdout)
        self.log(**{"work-item": name, "stage": stage, "agent": agent, "session": session, "event": "end"})
        result = here / "result.json"
        if not result.is_file():
            return None, "%s gave no result file (%s)" % (agent, self.rel(result))
        try:
            data = json.loads(result.read_text())
        except ValueError:
            data = None
        if not isinstance(data, dict):
            return None, "%s's result file %s is not a JSON object" % (agent, self.rel(result))
        return data, None

    def outcome(self, agent, data, failure):
        """None for DONE, else the question it puts to the person (r5)."""
        if failure:
            return failure
        if data.get("status") == "DONE":
            return None
        asked = [q if isinstance(q, str) else json.dumps(q) for q in data.get("questions") or []]
        return "; ".join(asked) or "%s gave %s: %s" % (agent, data.get("status"), data.get("summary", ""))

    def tests(self):
        path = self.root / ".shop" / "delivery.toml"
        given = tomllib.loads(path.read_text()).get("tests", {}) if path.is_file() else {}
        return dict(TESTS, **given)

    def implement(self, name):
        """ready -> claimed, the implementer in its worktree, and its branch merged only on passing tests (r4)."""
        self.move(name, "ready", "claimed")
        branch = git(self.root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        tree = self.root / ".shop" / "worktrees" / name
        git(self.root, "worktree", "add", "-q", "-b", "work/" + name, str(tree), "HEAD")
        data, failure = self.worker(name, "implement", "bdd-implementer", tree)
        question = self.outcome("bdd-implementer", data, failure)
        if question is None:
            tests = self.tests()
            for cmd in (["git", "rebase", "-q", branch], shlex.split(tests["work_item"].format(work_item=name)),
                        shlex.split(tests["suite"])):
                done = subprocess.run(cmd, cwd=tree, capture_output=True, text=True)
                if done.returncode != 0:
                    question = "`%s` failed on %s's branch work/%s:\n%s" % (
                        " ".join(cmd), name, name, (done.stdout + done.stderr).strip())
                    break
        if question is None:
            git(self.root, "merge", "-q", "--ff-only", "work/" + name)
            self.move(name, "claimed", "done")
        else:
            self.move(name, "claimed", "awaiting-ruling", question)

    def step(self, name, status):
        if status == "planned":
            self.move(name, "planned", "ready")
        elif status == "ready":
            self.implement(name)
        else:
            stage, agent, after = STAGES[status]
            data, failure = self.worker(name, stage, agent, self.root)
            question = self.outcome(agent, data, failure)
            self.move(name, status, after if question is None else "awaiting-ruling", question)

    def questions(self, name):
        """The lines of the work-item's `## Questions` section: its open questions."""
        text = (self.dir / (name + ".md")).read_text()
        return text.split("\n## Questions\n", 1)[1].splitlines() if "\n## Questions\n" in text else []

    def run(self):
        """Pull the work-items one worker at a time until none can move (r1); print where each stands (r9)."""
        self.check()
        while True:
            movable = [(n, s) for n, s in self.items() if s in MOVABLE]
            if not movable:
                break
            self.step(*movable[0])
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
