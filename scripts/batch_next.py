"""`work batch next <batch>` (b683, b692, batches r141, r143-r148): the batches service's poll, the next step of a
batch said to its driver (whatever runs the batch: an agent from the batch brief, a script, a headless runner), so
that any driver loops on it and reports each step's result through the batch's other operations.

A batch step is its instruction and what it is about: `prepare task` (a pending task, reported through `work batch
resume`, which makes its worktree), `build task` (a running task whose branch holds no commit citing its item since
the batch's lines commit, with the batch brief), `finish task` (a running task whose branch holds one), `submit
batch`, `review change` (the next review's folder and the findings file in it, `findings.md`, where the reviewer's
reply is saved for `work batch reviewed`), `fix finding` (an open `fix now` finding no commit cites yet), `park item`
(a failed task) or `stop`. One step is picked, the first that applies in this order: stop, review change, fix
finding, park item, finish or build task (running), prepare task (pending), submit batch (`pick`). Only the tasks of
an item still `in-batch` count; a building batch with none of them stops. Each step names the command its result is
reported through (`report`). The step is printed as lines, and is the content of a `returned` response (the envelope
under `--json`)."""
from pathlib import Path

import backlog_items
import batch_driver
import batch_findings
import batch_fix
import batch_git
import batch_plan
import batch_tasks
from domain_envelope import Response
from shop_files import Refused

INSTRUCTIONS = ("prepare task", "build task", "finish task", "submit batch", "review change", "fix finding", "park item", "stop")


def _in_batch(root, task):
    try:
        return backlog_items.find(root, task.item).status == "in-batch"
    except Refused:
        return False


def _unfixed(root, batch):
    """The open `fix now` findings with no commit on their item's branch citing them since the last review."""
    cited = batch_fix.for_finding(root, batch)
    return [f for f in batch_findings.open_findings(root, batch.name) if not cited.get(f.fid)]


def _cites(root, since, branch, item):
    """Whether a commit on `branch` after `since` has an `Item: <item>` trailer."""
    out = batch_git.git(root, "log", "--format=%(trailers:key=Item,valueonly,separator=%x2c)", "%s..%s" % (
        since, branch)).stdout
    return item in {c.strip() for line in out.splitlines() for c in line.split(",")}


def _built(root, batch, tasks):
    """The ids of the running tasks whose branch holds a commit citing the task's item since the batch's lines commit:
    the kept change its subagent reported."""
    running = [t for t in tasks if t.status == "running"]
    try:
        since = batch_tasks.lines_commit(root, batch) if running else None
    except Refused:
        return set()
    found = set()
    for task in running:
        try:
            if _cites(root, since, task.branch, task.item):
                found.add(task.task)
        except Refused:          # no such branch yet: nothing built on it
            pass
    return found


def pick(batch, tasks, unfixed, built=()):
    """(instruction, task or None, finding or None): the first step that applies, in the service's order. `tasks` are
    the batch's tasks of in-batch items, `unfixed` its open findings to fix, `built` the ids of its running tasks whose
    branch holds a kept change citing their item."""
    if batch.status not in ("building", "in-review"):
        return "stop", None, None
    if batch.status == "in-review":
        return "review change", None, None
    if unfixed:
        return "fix finding", None, unfixed[0]
    for status, instruction in (("failed", "park item"), ("running", None), ("pending", "prepare task")):
        task = next((t for t in tasks if t.status == status), None)
        if task is not None:
            return instruction or ("finish task" if task.task in built else "build task"), task, None
    return ("submit batch", None, None) if tasks else ("stop", None, None)


def report(batch, instruction, task, finding):
    """The command the step's result is reported through, or None for `stop`."""
    name = batch.name
    return {"prepare task": "shop work batch resume %s" % name,
            "build task": "a commit on %s citing Item: %s, then shop work batch done %s %s" % (
                task.branch if task else "", task.item if task else "", name, task.task if task else ""),
            "finish task": "shop work batch done %s %s" % (name, task.task if task else ""),
            "park item": "shop work batch park %s %s --question <question>" % (name, task.item if task else ""),
            "submit batch": "shop work batch review %s" % name,
            "review change": "shop work batch brief %s, the reply saved as the findings file, then shop work batch "
                             "reviewed %s" % (name, name),
            "fix finding": "a commit on %s citing Finding: %s, then shop work batch review %s" % (
                next((t.branch for t in batch.tasks if finding and t.item == finding.item), ""), finding.fid if finding else "", name),
            }.get(instruction)


def _task(task):
    return {"task": task.task, "item": task.item, "status": task.status, "branch": task.branch}


def poll(root, name):
    """The batch step of the batch `name`, as a dict: its batch, status, instruction, the task, batch brief, review
    folder, findings file (where `work batch reviewed` reads the reviewer's reply) and review finding it is about (None where it is about none) and the command to report through."""
    batch = batch_plan.find(root, name)
    tasks = [t for t in batch.tasks if _in_batch(root, t)]
    unfixed = _unfixed(root, batch) if batch.status == "building" else []
    instruction, task, finding = pick(batch, tasks, unfixed, _built(root, batch, tasks))
    folder = None
    if instruction == "review change":
        folder = str(batch_findings.scratch(root, batch, len(batch_findings.reviews(root, batch)) + 1).resolve())
    return {"batch": batch.name, "status": batch.status, "instruction": instruction,
            "task": _task(task) if task else None,
            "batch brief": str(batch_driver.path(root, batch.name)) if instruction == "build task" else None,
            "review folder": folder,
            "findings file": str(Path(folder) / "findings.md") if folder else None,
            "review finding": {"finding": finding.fid, "title": finding.title, "item": finding.item,
                               "where": finding.where} if finding else None,
            "report": report(batch, instruction, task, finding)}


def text(step):
    lines = ["%s %s: %s" % (step["batch"], step["status"], step["instruction"])]
    if step["task"]:
        t = step["task"]
        lines.append("task: %s %s (%s), branch %s" % (t["task"], t["item"], t["status"], t["branch"]))
    if step["review finding"]:
        f = step["review finding"]
        lines.append("review finding: %s %s (%s, %s)" % (f["finding"], f["title"], f["item"], f["where"] or "-"))
    for key in ("batch brief", "review folder", "findings file", "report"):
        if step[key]:
            lines.append("%s: %s" % (key, step[key]))
    return "\n".join(lines) + "\n"


def cmd_next(args):
    found = poll(args.root, args.batch)
    if not args.json:
        print(text(found), end="")
    return Response("returned", found)
