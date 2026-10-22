"""`work run`'s workers (capability supervision): the tools a stage's worker is given, the worktree it runs in, the
`claude -p` session itself, and what its result file says. Standard library only; a part of supervise.Run."""
import datetime
import json
import os
import shutil
import subprocess
import tempfile
import tomllib
import uuid
from pathlib import Path

import workqueue
from supervise_faults import Fault, session_end
from workqueue import Refused

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
# Python (r14). The scripts are the ones a stage's agent and skills run, each by name: never `work`, with which a worker
# could move statuses as work run does, nor any other of the plugin's scripts.
STAGE_SCRIPTS = ("features", "model", "tools")
PYTHON = ["Bash(python3 -m pytest*)", *("Bash(python3 %s/%s *)" % (SCRIPTS, s) for s in STAGE_SCRIPTS)]
READER = ["Read", "Glob", "Grep", *PYTHON, "Bash(git status*)", "Bash(git diff*)", "Bash(git log*)", "Bash(git show*)"]
TOOLS = {
    "research": READER,
    "plan": ["Read", "Glob", "Grep"],
    "implement": ["Read", "Glob", "Grep", *PYTHON, "Bash(git add *)", "Bash(git commit *)", "Bash(git status*)",
                  "Bash(git diff*)"],
    "review": READER,
}
# A stage's limit of turns: the researcher's is 25 (r19).
MAX_TURNS = {"research": 25}
ROLE = {"code-scout": "researcher", "bdd-planner": "planner", "bdd-implementer": "implementer",
        "bdd-task-reviewer": "reviewer", "bdd-branch-reviewer": "branch reviewer"}
# Set in each worker's environment: a `work run` that finds it was started by a worker (r21).
WORKER = "SHOPSYSTEM_WORK_RUN_WORKER"


class GitFailed(Refused):
    """A git command that failed: work run's refusal before any stage (r10), the work-item's fault during one (r41)."""


def git(root, *args):
    """Run git in `root`; a git that fails raises GitFailed, with git's first line of complaint."""
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if done.returncode != 0:
        said = (done.stderr.strip() or done.stdout.strip() or "exit %d" % done.returncode).splitlines()[0]
        raise GitFailed("git %s failed: %s" % (" ".join(args), said))
    return done


def with_scripts(plugin=False, work_item=None):
    """The environment with the plugin's scripts directory last on PYTHONPATH, so `-p work_items` finds the plugin's
    `--work-item` and a module of the project's own named as one of the scripts still comes first; with `plugin`, that
    pytest plugin loaded by every pytest run too (PYTEST_PLUGINS), and with `work_item`, `--work-item <it>` given to
    every pytest run (PYTEST_ADDOPTS), as for a worker."""
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(p for p in (env.get("PYTHONPATH"), str(SCRIPTS)) if p)
    if plugin:
        env["PYTEST_PLUGINS"] = ",".join(p for p in (env.get("PYTEST_PLUGINS"), "work_items") if p)
        env[WORKER] = work_item or "the branch review"      # a `work run` started from here refuses (r21)
    if work_item:      # every pytest a worker runs selects its work-item's scenarios (r22)
        env["PYTEST_ADDOPTS"] = " ".join(p for p in (env.get("PYTEST_ADDOPTS"), "--work-item " + work_item) if p)
    return env


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


class Workers:
    """The part of supervise.Run that starts workers and reads what they leave. Two implementers may run at once
    (r20), so what changes the main checkout or the run's list of worktrees holds `self.lock`; the worker itself does
    not."""

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

    def run_dir(self, name, stage):
        """The name of the stage's next run directory, `<k>-<stage>`, and its place in the main checkout."""
        runs = self.dir / "runs" / name
        k = len([p for p in runs.iterdir() if p.is_dir()]) + 1 if runs.is_dir() else 1
        return "%d-%s" % (k, stage), runs / ("%d-%s" % (k, stage))

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
        with self.lock:
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
        with self.lock:
            if tree in self.trees:
                self.trees.remove(tree)
                subprocess.run(["git", "worktree", "remove", "--force", str(tree)], cwd=self.root, capture_output=True)

    def worker(self, name, stage, agent, tree, branch=None, extra=()):
        """Start one worker in `tree` and wait for it; its result as a dict, or the reason there is none.

        The worker writes in its worktree's .shop/scratch/<k>-<stage>/; work run copies that into the main checkout's
        run directory, .shop/work/<initiative>/runs/<work-item>/<k>-<stage>/, and reads the result from there.
        What a worker changes under .shop/work/ is put back where the worker changed it (r6): a detached worktree's
        changes go with the worktree, a branch's are put back by `under_work`. A change left uncommitted there in the
        main checkout while the worker ran is put back too, and is the work-item's fault (r28); one committed there is
        someone else's, and kept."""
        self.verify_push(name, stage)
        with self.lock:
            label, kept_at = self.run_dir(name, stage)
            here = tree / ".shop" / "scratch" / label
            here.mkdir(parents=True)
            brief = self.brief(name, stage, agent, here, tree, branch, extra)
            session = str(uuid.uuid4())
            self.log(**{"work-item": name, "stage": stage, "agent": agent, "session": session, "event": "start"})
        done = self.session(stage, agent, brief, session, tree, name)
        with self.lock:
            changed = self.checkout_changes()
            shutil.copytree(here, kept_at)
            self.own.add(self.rel(kept_at))
            (kept_at / "session.json").write_text(done.stdout)
            self.log(**{"work-item": name, "stage": stage, "agent": agent, "session": session, "event": "end"})
        if changed:
            raise Fault("while its %s worked, %s changed in the repository's own checkout and not committed; work run "
                        "put %s back" % (ROLE[agent], ", ".join(changed), "it" if len(changed) == 1 else "them"))
        result = kept_at / "result.json"
        try:
            data = json.loads(result.read_text()) if result.is_file() else None
        except ValueError:
            data = None
        if not isinstance(data, dict):
            raise Fault("its %s wrote %s; %s" % (ROLE[agent], "a result file that is not JSON" if result.is_file()
                                                  else "no result file", session_end(done.stdout, done.returncode)))
        self.keep_named(data, tree, here, kept_at)
        questions = data.get("questions")
        if isinstance(questions, str):
            data["questions"] = [questions]
        elif questions is not None and not isinstance(questions, list):
            return None, "%s's result file %s gives its questions as %s, not a list of questions" % (
                agent, self.rel(result), json.dumps(questions))
        return data, None

    def session(self, stage, agent, brief, session, tree, work_item):
        """One `claude -p` session of `agent` in `tree`, given its brief (r2), its plugin (r11) and its stage's tools."""
        return subprocess.run([self.claude, "-p", "Read the brief file %s and do what it says." % brief,
                               "--agent", AGENT_PREFIX + agent, "--plugin-dir", str(SCRIPTS.parent),
                               "--session-id", session, "--output-format", "json",
                               "--permission-mode", "acceptEdits", "--allowedTools", ",".join(self.tools(stage, agent)),
                               *(["--max-turns", str(MAX_TURNS[stage])] if stage in MAX_TURNS else [])],
                              cwd=tree, capture_output=True, text=True, env=with_scripts(plugin=True, work_item=work_item))

    def keep_named(self, data, tree, here, kept_at):
        """Copy into the run directory each file of the worktree the result names outside the worker's run directory,
        before the worktree is removed (r15): a field's value that is the path of such a file, absolute or relative to
        the worktree."""
        for field, value in data.items():
            if field in ("status", "summary") or not isinstance(value, str) or not value.strip():
                continue
            path = (tree / value).resolve()
            if path.is_file() and path.is_relative_to(tree.resolve()) and not path.is_relative_to(here.resolve()):
                to = kept_at / path.name
                if to.exists():     # never over the run's own record (brief.md, result.json, session.json) or notes
                    to = kept_at / ("named-" + path.name)
                shutil.copy2(path, to)

    def outcome(self, agent, data, failure):
        """None for DONE, else the question it puts to the person (r5)."""
        if failure:
            return failure
        if data.get("status") == "DONE":
            return None
        asked = [q if isinstance(q, str) else json.dumps(q) for q in data.get("questions") or []]
        return "; ".join(asked) or "%s gave %s: %s" % (agent, data.get("status"), data.get("summary", ""))
