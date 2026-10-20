#!/usr/bin/env python3
"""A stand-in `claude` for supervision's scenarios: it takes `claude -p <brief file> --agent <agent> --session-id <uuid>
...`, reads its brief and does what a script tells it to, as a worker would; no model runs.

The script is the JSON file $STUB_CLAUDE_PLAN: an object whose keys are agents without the plugin's prefix
(`code-scout`), or "default", each an object of:
  status     the result file's status (default "DONE"); with `result` "none" no result file is written, with
             "not-json" one that is not JSON;
  questions  the result file's questions;
  write      {path: text}, written relative to the worker's working directory (as a worker that edits files);
  notes      {file name: text}, written in the result file's directory (the worker's run directory);
  commit     {path: text}, written relative to the working directory and committed there.
Each start and end is appended to $STUB_CLAUDE_CALLS, one JSON object a line, so a scenario can read who was started,
with what arguments and brief, in which directory and in what order.
"""
import json
import os
import pathlib
import subprocess
import sys


def option(argv, name):
    return argv[argv.index(name) + 1] if name in argv else None


def record(entry):
    with open(os.environ["STUB_CLAUDE_CALLS"], "a") as out:
        out.write(json.dumps(entry) + "\n")


def main(argv):
    brief_path = pathlib.Path(option(argv, "-p"))
    brief = brief_path.read_text()
    agent = option(argv, "--agent")
    session = option(argv, "--session-id")
    record({"event": "start", "argv": argv, "cwd": os.getcwd(), "brief": brief, "agent": agent, "session": session})
    plan = json.loads(pathlib.Path(os.environ["STUB_CLAUDE_PLAN"]).read_text())
    short = agent.split(":", 1)[-1]
    step = dict(plan.get("default", {}), **plan.get(short, {}))
    result = pathlib.Path(next(line.split(":", 1)[1].strip() for line in brief.splitlines() if line.startswith("Result file:")))
    for rel, text in step.get("write", {}).items():
        pathlib.Path(rel).write_text(text)
    for name, text in step.get("notes", {}).items():
        (result.parent / name).write_text(text)
    if step.get("commit"):
        for rel, text in step["commit"].items():
            pathlib.Path(rel).write_text(text)
        subprocess.run(["git", "add", "-A", "--", *step["commit"]], check=True)
        subprocess.run(["git", "commit", "-q", "-m", "%s: %s" % (short, ", ".join(step["commit"]))], check=True)
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
