#!/usr/bin/env python3
"""A stand-in `claude` for supervision's scenarios: it takes `claude -p <prompt> --agent <agent> --session-id <uuid>
--allowedTools <list> ...`, reads the brief file its prompt names and does what a script tells it to, as a worker would;
no model runs. Like the real claude under -p, it runs a Bash command only when --allowedTools lets it
(`Bash(<pattern>)`, `*` matching anything), and refuses any other; it loads a skill only when the list has
`Skill(<skill>)`; and, as under --permission-mode acceptEdits, it writes a file outside its working directory only
when the list has a bare `Write`.

The script is the JSON file $STUB_CLAUDE_PLAN: an object whose keys are agents without the plugin's prefix
(`code-scout`), or "default", or a round's kind after "round:" (`round:apply`, read from the brief's `# <kind> of <name>`
heading, taking precedence over the agent's), or a question after "question:" (`question:Which module?`, read from the
brief's `Question:` line, taking precedence over all of those), each an object of:
  status     the result file's status (default "DONE"); with `result` "none" no result file is written, with
             "not-json" one that is not JSON;
  subtype    how the session ends, as claude's JSON output gives it (default "success"; "error_max_turns" at its
             turn limit, "error_during_execution" in an error; any but "success" with `is_error` true), with
             `num_turns` its turns (default 1; 26 at the turn limit, as the real CLI gives for a cap of 25);
  exit       the exit code of the session (default 0, or 1 when `subtype` is not "success", as the real CLI exits);
  stdout     the text the session prints, in place of its JSON result (`subtype` and `num_turns` then unused);
  fields     {field: value}, more fields of the result file (a planner's `fileset`);
  touch      a list of paths, files created first, wherever they are (no tool of the worker's: the world changing
             while it works, as a remote that starts refusing pushes);
  questions  the result file's questions;
  write      {path: text}, written relative to the worker's working directory (as a worker that edits files); a path
             outside it is refused unless --allowedTools has a bare Write;
  notes      {file name: text}, written in the result file's directory (the worker's run directory);
  commit     {path: text, or null to delete it}, written relative to the working directory and committed there
             (by `git add -A -- <paths>` and `git commit -q -m ...`, each a Bash command); `{work_item}` in a path is
             the name of the work-item the brief names;
  meet       a number n: before anything else, wait until $STUB_CLAUDE_CALLS has the starts of n workers of this
             agent, this one's included (up to a minute, so a worker nobody joins still ends);
  meet_all   a number n: the same for the starts of n workers of any agent;
  meet_agents a list of agents (`code-scout`): the same for the start of a worker of each;
  hold       {work-item: {"log": a log.jsonl, "work_item": another work-item}}: the worker of that work-item ends,
             as work run sees it, only once the log has the end of the other work-item's implementer;
  watch      a list of files: the worker's start is followed by a `seen` record of what each holds then;
  skills     a list of skills to load (`shopsystem-bdd:bdd-red-green`), first;
  run        a list of Bash commands (argument lists), run in the working directory, last;
  names      {result field: path}, a file the result names (`report`), given in the result by its absolute path, the
             path taken relative to the working directory;
  elsewhere  {"root": a directory, "commit": {path: text}} or {"root": ..., "write": {path: text}}: while this worker
             runs, another session (not the worker, so no tool of its own and nothing recorded) writes these files
             relative to that directory, first, and commits them there unless given as `write`.
It refuses an --agent the --plugin-dir has no agents/<agent>.md for. As the real claude does, it refuses to write any
file (a `write` path, the result file) under its --plugin-dir, as a sensitive file: the write is recorded as refused
(`Write`) and nothing is written.
It keeps a transcript of its session, `projects/stand-in/<session id>.jsonl`, in $CLAUDE_CONFIG_DIR when that is set.
Each start and end, and each Bash command, skill load or write outside the working directory run or refused (its `tool`,
`Bash`, `Skill` or `Write`), is appended to $STUB_CLAUDE_CALLS, one JSON object a line, so
a scenario can read who was started, with what arguments and brief, in which directory and in what order.
"""
import fnmatch
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys
import time

VALUED = ("--agent", "--plugin-dir", "--session-id", "--output-format", "--permission-mode", "--allowedTools", "--allowed-tools",
          "--max-turns")


def option(argv, name):
    return argv[argv.index(name) + 1] if name in argv else None


def prompt(argv):
    """The positional argument: the prompt (-p takes none)."""
    rest, skip = [], False
    for arg in argv:
        if skip:
            skip = False
        elif arg in VALUED:
            skip = True
        elif not arg.startswith("-"):
            rest.append(arg)
    return " ".join(rest)


def allowed(argv, tool):
    """The patterns --allowedTools gives `tool`: `Bash(git status*)` gives Bash `git status*`."""
    tools = (option(argv, "--allowedTools") or "").split(",")
    return [t[len(tool) + 1:-1] for t in tools if t.startswith(tool + "(") and t.endswith(")")]


def bash(argv, command):
    """Run `command` if --allowedTools allows it as Bash; record that it ran or was refused."""
    line = shlex.join(command)
    if any(fnmatch.fnmatchcase(line, pattern) for pattern in allowed(argv, "Bash")):
        done = subprocess.run(command, capture_output=True, text=True, check=command[0] == "git")
        record({"event": "ran", "tool": "Bash", "command": line, "code": done.returncode,
                "output": done.stdout + done.stderr})
        return True
    record({"event": "refused", "tool": "Bash", "command": line})
    return False


def skill(argv, name):
    """Load the skill `name` if --allowedTools has `Skill(<name>)`; record that it was loaded (ran) or refused."""
    record({"event": "ran" if name in allowed(argv, "Skill") else "refused", "tool": "Skill", "command": name})


def plugin_refuses(argv, path):
    """True, recorded as refused, when `path` lies under the --plugin-dir: claude writes nothing there."""
    plugin = option(argv, "--plugin-dir")
    if plugin and pathlib.Path(path).resolve().is_relative_to(pathlib.Path(plugin).resolve()):
        record({"event": "refused", "tool": "Write", "command": str(path)})
        return True
    return False


def wait_until(done):
    """Wait, up to a minute, until `done()` holds: a signal, polled, never a fixed sleep."""
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline and not done():
        time.sleep(0.05)


def started_agents():
    """The agent of each start in the record."""
    with open(os.environ["STUB_CLAUDE_CALLS"]) as calls:
        lines = [json.loads(line) for line in calls if line.endswith("\n")]     # a line still being written waits
    return [c["agent"] for c in lines if c["event"] == "start"]


def meet(agent, n):
    """Wait until the record has the starts of `n` workers of `agent`."""
    wait_until(lambda: started_agents().count(agent) >= n)


def meet_all(n):
    """Wait until the record has the starts of `n` workers, of any agent."""
    wait_until(lambda: len(started_agents()) >= n)


def meet_agents(names):
    """Wait until the record has the start of a worker of each of the agents `names`."""
    wait_until(lambda: all(any(a.split(":", 1)[-1] == n for a in started_agents()) for n in names))


def ended_in(log, work_item):
    """Whether the log `log` (work run's log.jsonl) has the end of the implementer of `work_item`."""
    path = pathlib.Path(log)
    lines = []
    for line in path.read_text().splitlines() if path.exists() else []:
        try:
            lines.append(json.loads(line))
        except ValueError:     # a line being written, or the file being put back
            pass
    return any(l.get("work-item") == work_item and l.get("stage") == "implement" and l.get("event") == "end" for l in lines)


def keep_transcript(session):
    """A transcript of the session in the store $CLAUDE_CONFIG_DIR names, as Claude Code keeps one."""
    store = os.environ.get("CLAUDE_CONFIG_DIR")
    if store:
        (pathlib.Path(store) / "projects" / "stand-in").mkdir(parents=True, exist_ok=True)
        (pathlib.Path(store) / "projects" / "stand-in" / (session + ".jsonl")).write_text(
            json.dumps({"sessionId": session, "type": "user"}) + "\n")


def record(entry):
    with open(os.environ["STUB_CLAUDE_CALLS"], "a") as out:
        out.write(json.dumps(entry) + "\n")


def main(argv):
    brief_path = pathlib.Path(re.search(r"(/\S*brief\.md)", prompt(argv)).group(1))
    brief = brief_path.read_text()
    agent = option(argv, "--agent")
    session = option(argv, "--session-id")
    plugin = option(argv, "--plugin-dir")
    if plugin and not (pathlib.Path(plugin) / "agents" / (agent.split(":", 1)[-1] + ".md")).is_file():
        print("stand-in claude: no agent %s in --plugin-dir %s" % (agent, plugin), file=sys.stderr)
        return 1
    record({"event": "start", "argv": argv, "cwd": os.getcwd(), "brief": brief, "brief_path": str(brief_path),
            "agent": agent, "session": session})
    plan = json.loads(pathlib.Path(os.environ["STUB_CLAUDE_PLAN"]).read_text())
    short = agent.split(":", 1)[-1]
    kind = re.search(r"^# (\w+) of ", brief, re.M)
    asked = re.search(r"^Question: (.*)$", brief, re.M)
    step = {**plan.get("default", {}), **plan.get(short, {}), **(plan.get("round:" + kind.group(1), {}) if kind else {}),
            **(plan.get("question:" + asked.group(1), {}) if asked else {})}
    result = pathlib.Path(next(line.split(":", 1)[1].strip() for line in brief.splitlines() if line.startswith("Result file:")))
    work_item = pathlib.Path(next((line.split(":", 1)[1].strip() for line in brief.splitlines()
                                   if line.startswith("Work-item:")), "none")).stem
    if step.get("watch"):     # what these files hold as the worker starts, in its start record
        record({"event": "seen", "agent": agent, "seen": {w: (pathlib.Path(w).read_text() if pathlib.Path(w).exists()
                                                             else "") for w in step["watch"]}})
    for path in step.get("touch", []):
        pathlib.Path(path).touch()
    if step.get("meet"):
        meet(agent, step["meet"])
    if step.get("meet_all"):
        meet_all(step["meet_all"])
    if step.get("meet_agents"):
        meet_agents(step["meet_agents"])
    if step.get("commit"):
        step["commit"] = {rel.replace("{work_item}", work_item): text for rel, text in step["commit"].items()}
    if step.get("elsewhere"):
        other = pathlib.Path(step["elsewhere"]["root"])
        files = step["elsewhere"].get("commit") or step["elsewhere"]["write"]
        for rel, text in files.items():
            (other / rel).parent.mkdir(parents=True, exist_ok=True)
            (other / rel).write_text(text)
        if "commit" in step["elsewhere"]:
            subprocess.run(["git", "add", "--", *files], cwd=other, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-q", "-m", "another session's commit"], cwd=other, check=True,
                           capture_output=True)
    for name in step.get("skills", []):
        skill(argv, name)
    for rel, text in step.get("write", {}).items():
        path = pathlib.Path(rel).resolve()
        if plugin_refuses(argv, path):
            continue
        if not path.is_relative_to(pathlib.Path.cwd().resolve()):
            done = "Write" in (option(argv, "--allowedTools") or "").split(",")
            record({"event": "ran" if done else "refused", "tool": "Write", "command": str(path)})
            if not done:
                continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    for name, text in step.get("notes", {}).items():
        (result.parent / name).write_text(text)
    if step.get("commit"):
        for rel, text in step["commit"].items():
            if text is None:
                pathlib.Path(rel).unlink()
            else:
                pathlib.Path(rel).parent.mkdir(parents=True, exist_ok=True)
                pathlib.Path(rel).write_text(text)
        if bash(argv, ["git", "add", "-A", "--", *step["commit"]]):
            bash(argv, ["git", "commit", "-q", "-m", "%s: %s" % (short, ", ".join(step["commit"]))])
    for command in step.get("run", []):
        bash(argv, command)
    if plugin_refuses(argv, result):
        pass
    elif step.get("result") == "not-json":
        result.write_text("not json\n")
    elif step.get("result") != "none":
        named = {field: str(pathlib.Path(rel).resolve()) for field, rel in step.get("names", {}).items()}
        result.write_text(json.dumps(dict({"status": step.get("status", "DONE"), "summary": "the stand-in's %s" % short,
                                           "questions": step.get("questions", [])}, **named, **step.get("fields", {}))))
    hold = step.get("hold", {}).get(work_item)
    if hold:     # this worker ends only once work run's log has the end of another work-item's
        wait_until(lambda: ended_in(hold["log"], hold["work_item"]))
    keep_transcript(session)
    subtype = step.get("subtype", "success")
    if "stdout" in step:
        print(step["stdout"])
    else:
        print(json.dumps({"type": "result", "subtype": subtype, "is_error": subtype != "success", "session_id": session,
                          "num_turns": step.get("num_turns", 26 if subtype == "error_max_turns" else 1),
                          "total_cost_usd": 0, "result": "stand-in"}))
    record({"event": "end", "agent": agent, "session": session})
    return step.get("exit", 0 if subtype == "success" else 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
