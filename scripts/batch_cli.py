"""The batches' commands of `work` (capability batches): `work batch <command>`'s parsers, what each prints, and their
dispatch, so that scripts/work stays small. An item is named by its label, a batch as `batch-<n>`, a task as
`t<k> <item label>` (design goal 10)."""
import json

import backlog_items
import batch_brief
import batch_close
import batch_plan
import batch_review
import batch_reviewed
import batch_start
import batch_tasks
from shop_files import Refused


def add_parsers(sub):
    p = sub.add_parser("batch", help="build ready items together in a batch: one branch, one task an item, one pull request")
    cmds = p.add_subparsers(dest="batch_cmd", required=True)
    cmds.add_parser("start", help="pick the ready, unblocked, passing items in rank order and start a batch of them")
    s = cmds.add_parser("status", help="where a batch stands (default: the open one): its items and its tasks")
    s.add_argument("batch", nargs="?")
    s.add_argument("--json", action="store_true", help="print one JSON object instead of lines")
    s = cmds.add_parser("resume", help="give each pending task its worktree and print what each running task builds")
    s.add_argument("batch")
    s = cmds.add_parser("done", help="set a running task done, once its ids are built and the tests pass in its worktree")
    s.add_argument("batch")
    s.add_argument("task")
    s = cmds.add_parser("park", help="set an item of the batch needs-input with its question; the rest carries on")
    s.add_argument("batch")
    s.add_argument("item")
    s.add_argument("--question", required=True)
    s.add_argument("--discard", action="store_true", help="discard the uncommitted changes of the item's worktree")
    cmds.add_parser("merged", help="record the merge of a batch's pull request: its in-batch items delivered"
                    ).add_argument("batch")
    s = cmds.add_parser("abandon", help="abandon a batch: its pull request closed, its in-batch items ready again")
    s.add_argument("batch")
    s.add_argument("--discard", action="store_true", help="discard the uncommitted changes of its task worktrees")
    s = cmds.add_parser("review", help="merge the in-batch items into the batch branch, test, push and publish its pull request")
    s.add_argument("batch")
    cmds.add_parser("reviewed", help="record the findings file (pr-reviewer's reply, saved): back to building, or awaiting-merge"
                    ).add_argument("batch")
    cmds.add_parser("brief", help="write the brief of the next review of a batch's pull request, for pr-reviewer"
                    ).add_argument("batch")


def _item(root, name):
    try:
        return backlog_items.find(root, name)
    except Refused:
        return None


def task_label(root, task):
    item = _item(root, task.item)
    return "%s %s" % (task.task, backlog_items.label(item) if item else "%s (missing)" % task.item)


def status_text(root, batch):
    out = ["%s %s, base %s, pull request %s" % (batch.name, batch.status, batch.base, batch.pull_request or "-"),
           "plan: %s" % batch_plan.rel_of(batch.name)]
    if batch.pull_request:      # a batch with no pull request has no review to show (plan 4's lines kept)
        out.append(batch_reviewed.status_line(root, batch))
    for task in batch.tasks:
        item = _item(root, task.item)
        out.append("  %s %s" % (backlog_items.label(item), item.status) if item else "  %s missing" % task.item)
    out += ["  %s: %s, branch %s" % (task_label(root, t), t.status, t.branch) for t in batch.tasks]
    return "\n".join(out)


def as_json(root, batch):
    items = [(t.item, _item(root, t.item)) for t in batch.tasks]
    return {"batch": {"name": batch.name, "status": batch.status, "base": batch.base,
                      "pull_request": batch.pull_request, "plan": batch_plan.rel_of(batch.name),
                      "items": [{"id": n, "title": i.title if i else None, "status": i.status if i else None}
                                for n, i in items],
                      "tasks": [{"task": t.task, "item": t.item, "status": t.status, "branch": t.branch}
                                for t in batch.tasks], **batch_reviewed.as_json(root, batch)}}


def status(args):
    if args.batch is not None:
        batch = batch_plan.find(args.root, args.batch)
    else:
        batch = batch_plan.open_batch(args.root) or next(iter(reversed(batch_plan.batches(args.root))), None)
    if batch is None:
        print(json.dumps({"batch": None}) if args.json else "there is no batch in %s/" % batch_plan.BATCHES.as_posix())
        return 0
    print(json.dumps(as_json(args.root, batch)) if args.json else status_text(args.root, batch))
    return 0


def start(args):
    batch, pick = batch_start.start(args.root)
    print(batch_start.said(args.root, batch, pick))
    return 0


def resume(args):
    batch, out = batch_tasks.resume(args.root, args.batch)
    print(batch_tasks.resume_said(args.root, batch, out))
    return 0


def done(args):
    task = batch_tasks.done(args.root, args.batch, args.task)
    print("%s %s: done" % (args.batch, batch_tasks.task_label(args.root, task)))
    return 0


def park(args):
    item = batch_tasks.park(args.root, args.batch, args.item, args.question, args.discard)
    print("%s %s -> needs-input: %s" % (args.batch, backlog_items.label(item), item.question))
    return 0


def review(args):
    url = batch_review.review(args.root, args.batch)
    print("next: work batch brief %s, the pr-reviewer on it, then work batch reviewed %s" % (args.batch, args.batch))
    print(url)
    return 0


def brief(args):
    path, removed = batch_brief.brief(args.root, args.batch)
    for name in removed:
        print("removed an old %s" % name)
    print(path)
    return 0


def reviewed(args):
    print(batch_reviewed.said(args.root, batch_reviewed.reviewed(args.root, args.batch)))
    return 0


def merged(args):
    batch = batch_close.merged(args.root, args.batch)
    print("%s merged" % batch.name)
    return 0


def abandon(args):
    batch = batch_close.abandon(args.root, args.batch, args.discard)
    print("%s abandoned" % batch.name)
    return 0


def cmd_batch(args):
    return {"start": start, "status": status, "resume": resume, "done": done, "park": park, "review": review,
            "brief": brief, "reviewed": reviewed, "merged": merged, "abandon": abandon}[args.batch_cmd](args)


COMMANDS = {"batch": cmd_batch}
