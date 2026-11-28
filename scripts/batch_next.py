"""`work batch next <batch>` (b683, b692, b702, batches r141, r143, r144, r147, r148, r152, r153): the batches
service's poll, the next step of a batch said to its driver (whatever runs the batch: an agent from the batch brief, a
script, a headless runner), so that any driver loops on it and reports each step's result through the batch's other
operations.

A batch step is its instruction and the tasks it is about: `prepare task` (every pending task, reported through `work
batch resume`, which makes their worktrees), `build task` (every running task whose branch holds no commit citing its
item since the batch's lines commit, with the batch brief, so that the driver builds them side by side), `finish task`
(a running task whose branch holds one), `submit batch`, `review change` (the next review's folder and the findings
file in it, `findings.md`, where the reviewer's reply is saved for `work batch reviewed`), `fix finding` (an open `fix
now` finding no commit cites yet), `park item` (a failed task), `fix task` (every task done, and the last whole-suite
run of `work batch review` failed: the task of the item whose change broke it, batch_broken, b696; or two tasks'
branches conflict in a file, which `work batch review` would refuse to merge: the later task, whose item's subagent
merges the earlier branch and settles it, and the files, batch_merge's `clashes`, b710), `look at failure`
(the same, but the tests are of no task's item: the failed tests and no task, b703), `abandon batch` (a building
batch every item of which is parked, `needs-input`: nothing is left to build, so its driver abandons it, b722) or
`stop`; a fix of the refused
submit (a commit on a task's branch since it, batch_broken's `fixed`, b713) makes it `submit batch` in place of `fix
task` for the failure and `look at failure`. One step is picked,
the first that applies in this order: stop, review change, abandon batch, fix finding, park item, finish task, build task, prepare
task, fix task (a conflict first), look at failure, submit batch (`pick`). Only the tasks of an item still `in-batch` count; a building
batch with none of them stops. Each step names the command its result is reported through (`report`). The step is
printed as lines, one `task:` line a task, and is the content of a `returned` response (the envelope under `--json`:
`tasks`, and the first of them as `task`)."""
from pathlib import Path

import backlog_items
import batch_broken
import batch_driver
import batch_findings
import batch_fix
import batch_git
import batch_merge
import batch_plan
import batch_tasks
from plumbing.domain_envelope import Response
from plumbing.shop_files import Refused

INSTRUCTIONS = ("prepare task", "build task", "finish task", "submit batch", "review change", "fix finding", "fix task",
                "look at failure", "park item", "abandon batch", "stop")


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
    """Whether a commit on `branch` after `since` has an `Item: <item>` trailer and no `Applied:` (or, before b874,
    `Laid:`) one: an amendment `work batch amend` applies cites the item but builds nothing (b698)."""
    out = batch_git.git(root, "log", "--format=%(trailers:key=Applied,valueonly,separator=%x2c)"
                        "%(trailers:key=Laid,valueonly,separator=%x2c)%x09"
                        "%(trailers:key=Item,valueonly,separator=%x2c)", "%s..%s" % (since, branch)).stdout
    rows = (line.split("\t", 1) for line in out.splitlines() if "\t" in line)
    return any(not laid.strip() and item in {c.strip() for c in cited.split(",")} for laid, cited in rows)


def _built(root, batch, tasks):
    """The ids of the running tasks whose branch holds a commit citing the task's item since the batch's lines commit:
    the kept change its subagent reported."""
    found = set()
    for task in [t for t in tasks if t.status == "running"]:
        try:
            if _cites(root, batch_tasks.lines_commit(root, batch, task), task.branch, task.item):
                found.add(task.task)
        except Refused:          # no such branch yet: nothing built on it
            pass
    return found


def _conflict(root, tasks):
    """(the later task, the earlier one, the files) of the first two tasks whose branches conflict, in plan order, or
    None."""
    for j, later in enumerate(tasks):
        for earlier in tasks[:j]:
            files = batch_merge.clashes(root, earlier.branch, later.branch)
            if files:
                return later, earlier, files
    return None


def _parked(root, batch):
    """Whether the batch holds items and every one of them is `needs-input` (b722)."""
    try:
        return bool(batch.tasks) and all(backlog_items.find(root, t.item).status == "needs-input" for t in batch.tasks)
    except Refused:
        return False


def pick(batch, tasks, unfixed, built=(), broken=None, kept=False, clash=None, parked=False):
    """(instruction, the tasks it is about, finding or None): the first step that applies, in the service's order.
    `tasks` are the batch's tasks of in-batch items, `unfixed` its open findings to fix, `built` the ids of its running
    tasks whose branch holds a kept change citing their item, `broken` the task to fix for a refused submit (or None),
    `kept` whether a refused submit's failed run is kept with no task to fix it (`look at failure`, b703), `clash`
    (later task, earlier task, files) of two task branches that conflict (b710), `parked` whether every item of the
    batch is `needs-input` (`abandon batch`, b722).
    `build task` and `prepare task` are about every task that takes the step, so that they are built side by side
    (b702); `finish task` (the first built running task), `park item` and `fix task` about one."""
    if batch.status not in ("building", "in-review"):
        return "stop", [], None
    if batch.status == "in-review":
        return "review change", [], None
    if parked:
        return "abandon batch", [], None
    if unfixed:
        return "fix finding", [], unfixed[0]
    failed = [t for t in tasks if t.status == "failed"]
    if failed:
        return "park item", failed[:1], None
    running = [t for t in tasks if t.status == "running"]
    finished = [t for t in running if t.task in built]
    if finished:
        return "finish task", finished[:1], None
    if running:
        return "build task", running, None
    pending = [t for t in tasks if t.status == "pending"]
    if pending:
        return "prepare task", pending, None
    if clash is not None:
        return "fix task", [clash[0]], None
    if broken is not None:
        return "fix task", [broken], None
    if kept:
        return "look at failure", [], None
    return ("submit batch", [], None) if tasks else ("stop", [], None)


def report(batch, instruction, tasks, finding, clash=None):
    """The command the step's result is reported through, or None for `stop`: of `build task`, one for each task."""
    name = batch.name
    task = tasks[0] if tasks else None
    if instruction == "fix task" and clash:
        return "%s merged into %s with %s settled, a commit citing Item: %s, then shop work batch review %s" % (
            clash[1].branch, clash[0].branch, ", ".join(clash[2]), clash[0].item, name)
    if instruction == "build task":
        return "; ".join("a commit on %s citing Item: %s, then shop work batch done %s %s" % (
            t.branch, t.item, name, t.task) for t in tasks)
    return {"prepare task": "shop work batch resume %s" % name,
            "finish task": "shop work batch done %s %s" % (name, task.task if task else ""),
            "park item": "shop work batch park %s %s --question <question>" % (name, task.item if task else ""),
            "submit batch": "shop work batch review %s" % name,
            "abandon batch": "shop work batch abandon %s" % name,
            "fix task": "a commit on %s citing Item: %s, then shop work batch review %s" % (
                task.branch if task else "", task.item if task else "", name),
            "look at failure": "the failed tests looked at and fixed on the batch's branch or a task's, "
                               "then shop work batch review %s" % name,
            "review change": "shop work batch brief %s, a fresh pr-reviewer on it, then shop work batch reviewed "
                             "%s --reply <its transcript> (the findings file read only when no transcript is found)"
                             % (name, name),
            "fix finding": "a commit on %s citing Finding: %s, then shop work batch review %s" % (
                next((t.branch for t in batch.tasks if finding and t.item == finding.item), ""), finding.fid if finding else "", name),
            }.get(instruction)


def _task(task):
    return {"task": task.task, "item": task.item, "status": task.status, "branch": task.branch}


def poll(root, name):
    """The batch step of the batch `name`, as a dict: its batch, status, instruction, the tasks it is about (`tasks`,
    the first of them `task`), batch brief, review
    folder, findings file (where `work batch reviewed` reads the reviewer's reply) and review finding it is about (None where it is about none) and the command to report through."""
    batch = batch_plan.find(root, name)
    tasks = [t for t in batch.tasks if _in_batch(root, t)]
    unfixed = _unfixed(root, batch) if batch.status == "building" else []
    done = batch.status == "building" and tasks and all(t.status == "done" for t in tasks) and not unfixed
    unfixed_run = done and not batch_broken.fixed(root, batch, tasks)     # a fix is submitted (b713)
    broken = batch_broken.task_of(root, batch, tasks) if unfixed_run else None
    clash = _conflict(root, tasks) if done else None
    kept = bool(unfixed_run and broken is None and batch_broken.failed(root, batch))
    instruction, picked, finding = pick(batch, tasks, unfixed, _built(root, batch, tasks), broken, kept, clash,
                                   batch.status == "building" and _parked(root, batch))
    folder = None
    if instruction == "review change":
        folder = str(batch_findings.scratch(root, batch, len(batch_findings.reviews(root, batch)) + 1).resolve())
    return {"batch": batch.name, "status": batch.status, "instruction": instruction,
            "task": _task(picked[0]) if picked else None,
            "tasks": [_task(t) for t in picked],
            "batch brief": str(batch_driver.path(root, batch.name)) if instruction == "build task" else None,
            "review folder": folder,
            "findings file": str(Path(folder) / "findings.md") if folder else None,
            "review finding": {"finding": finding.fid, "title": finding.title, "item": finding.item,
                               "where": finding.where} if finding else None,
            "failed tests": batch_broken.failed(root, batch) if instruction in ("fix task", "look at failure") else None,
            "files": clash[2] if clash and instruction == "fix task" else None,
            "report": report(batch, instruction, picked, finding, clash)}


def text(step):
    lines = ["%s %s: %s" % (step["batch"], step["status"], step["instruction"])]
    for t in step.get("tasks") or ([step["task"]] if step["task"] else []):
        lines.append("task: %s %s (%s), branch %s" % (t["task"], t["item"], t["status"], t["branch"]))
    if step["review finding"]:
        f = step["review finding"]
        lines.append("review finding: %s %s (%s, %s)" % (f["finding"], f["title"], f["item"], f["where"] or "-"))
    for path in step.get("files") or ():
        lines.append("file: %s" % path)
    for test in step.get("failed tests") or ():
        lines.append("failed test: %s" % test)
    for key in ("batch brief", "review folder", "findings file", "report"):
        if step[key]:
            lines.append("%s: %s" % (key, step[key]))
    return "\n".join(lines) + "\n"


def cmd_next(args):
    found = poll(args.root, args.batch)
    if not args.json:
        print(text(found), end="")
    return Response("returned", found)
