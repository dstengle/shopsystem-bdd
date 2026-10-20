#!/usr/bin/env python3
"""A stand-in `claude` for supervision's scenarios: it takes `claude -p <prompt> --agent <agent> --session-id <uuid>
--allowedTools <list> ...`, reads the brief file its prompt names and does what a script tells it to, as a worker would;
no model runs. Like the real claude under -p, it runs a Bash command only when --allowedTools lets it
(`Bash(<pattern>)`, `*` matching anything), and refuses any other.

The script is the JSON file $STUB_CLAUDE_PLAN: an object whose keys are agents without the plugin's prefix
(`code-scout`), or "default", each an object of:
  status     the result file's status (default "DONE"); with `result` "none" no result file is written, with
             "not-json" one that is not JSON;
  questions  the result file's questions;
  write      {path: text}, written relative to the worker's working directory (as a worker that edits files);
  notes      {file name: text}, written in the result file's directory (the worker's run directory);
  commit     {path: text, or null to delete it}, written relative to the working directory and committed there
             (by `git add -A -- <paths>` and `git commit -q -m ...`, each a Bash command);
  run        a list of Bash commands (argument lists), run in the working directory, last.
Each start and end, and each Bash command run or refused, is appended to $STUB_CLAUDE_CALLS, one JSON object a line, so
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

VALUED = ("--agent", "--plugin-dir", "--session-id", "--output-format", "--permission-mode", "--allowedTools", "--allowed-tools")


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


def bash(argv, command):
    """Run `command` if --allowedTools allows it as Bash; record that it ran or was refused."""
    line = shlex.join(command)
    allowed = [t[5:-1] for t in (option(argv, "--allowedTools") or "").split(",") if t.startswith("Bash(") and t.endswith(")")]
    if any(fnmatch.fnmatchcase(line, pattern) for pattern in allowed):
        subprocess.run(command, check=True, capture_output=True)
        record({"event": "ran", "command": line})
        return True
    record({"event": "refused", "command": line})
    return False


def record(entry):
    with open(os.environ["STUB_CLAUDE_CALLS"], "a") as out:
        out.write(json.dumps(entry) + "\n")


def main(argv):
    brief_path = pathlib.Path(re.search(r"(/\S*brief\.md)", prompt(argv)).group(1))
    brief = brief_path.read_text()
    agent = option(argv, "--agent")
    session = option(argv, "--session-id")
    record({"event": "start", "argv": argv, "cwd": os.getcwd(), "brief": brief, "brief_path": str(brief_path),
            "agent": agent, "session": session})
    plan = json.loads(pathlib.Path(os.environ["STUB_CLAUDE_PLAN"]).read_text())
    short = agent.split(":", 1)[-1]
    step = dict(plan.get("default", {}), **plan.get(short, {}))
    result = pathlib.Path(next(line.split(":", 1)[1].strip() for line in brief.splitlines() if line.startswith("Result file:")))
    for rel, text in step.get("write", {}).items():
        pathlib.Path(rel).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(rel).write_text(text)
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
    if step.get("result") == "not-json":
        result.write_text("not json\n")
    elif step.get("result") != "none":
        result.write_text(json.dumps({"status": step.get("status", "DONE"), "summary": "the stand-in's %s" % short,
                                      "questions": step.get("questions", [])}))
    print(json.dumps({"type": "result", "subtype": "success", "is_error": False, "session_id": session,
                      "num_turns": 1, "total_cost_usd": 0, "result": "stand-in"}))
    record({"event": "end", "agent": agent, "session": session})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
