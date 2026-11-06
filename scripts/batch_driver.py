"""The batch brief (capability batches r14; item b55): what `work batch start` writes, once it has laid the batch, for
the one fresh agent that runs the batch from `work batch resume` to `awaiting-merge`, at
`.shop/worktrees/batch-<n>-driver/brief.md` beside the review folders, never committed.

It names the batch and its base checkout, each task with its worktree, branch, item and requirement ids, the skill
the agent follows (building-a-batch), the command prefix every push and gh call takes when `[batch] push` of
`.shop/delivery.toml` gives one, the rules every subagent is given, where the agent stops and what it replies. The
session that started the batch dispatches the agent with the brief's path as its whole prompt."""
from pathlib import Path

import backlog_items
import backlog_lines
import batch_plan
from batch_git import SCRIPTS, delivery, trees_dir
from shop_files import Refused

SKILL = "shopsystem-bdd:building-a-batch"

RULES = (
    ("Read the repository's CLAUDE.md in its worktree and follow it; the `tier: judgement` design-decisions "
     "(`grep -l '^tier: judgement' spec/decisions/*.md`) are followed in the code it writes."),
    "One scenario at a time, red first: see it fail on its Then line before writing its handler or code.",
    "Never edit a `.feature` file; an existing test is changed only in its setup.",
    "Take each id out of its capability's `unbuilt:` in the same commit that makes its scenario pass.",
    ("End every commit message with the line `Item: b<j>` (`git commit -m \"<subject>\" --trailer \"Item: b<j>\"`); a "
     "fix also `--trailer \"Finding: f<m>\"`, both in the message's last paragraph."),
    "Change nothing under `.shop/` (`.shop/backlog/`, `.shop/batches/` are the base checkout's batch commands' only).",
    ("Worktrees of older work (`.shop/worktrees/*` of other or earlier batches, `.claude/worktrees/`) are never "
     "reference material: the reference is the base branch and its own worktree."),
    "Don't chain `cp` and `rm` in one shell command; keep shell variables few.",
    "Don't push and don't run `work` commands that commit.",
    "A scenario that passes before it is built (an XPASS) means a test step is too loose: say so in the reply.",
    ("There is no brief or result file: reply with what was built and its commits, or with one question, never a "
     "guess. `work batch done` runs the whole suite in the worktree and refuses with its last lines."),
)


def path(root, name):
    """Where the batch brief of the batch `name` is written."""
    return (trees_dir(root) / ("%s-driver" % name) / "brief.md").resolve()


def push_prefix(root):
    """`[batch] push` of `.shop/delivery.toml`: the prefix every push and gh call takes, or None."""
    given = delivery(root).get("batch", {}).get("push")
    if given is not None and not isinstance(given, str):
        raise Refused("work batch start: .shop/delivery.toml: [batch] push is not a string")
    return given or None


def _tasks(root, batch, picked):
    out = []
    for task, item in zip(batch.tasks, picked):
        ids = backlog_lines.ids(backlog_lines.read(item, backlog_items.rel_of(item.name)))
        caps = sorted({i.split("#")[0] for i in ids})
        tests = "; ".join("`python3 -m pytest -q tests/scenarios/test_%s.py -m \"%s\"`" % (
            c.replace("-", "_"), " or ".join("r%s" % i.split("#r")[1] for i in ids if i.startswith(c + "#")))
            for c in caps) or "none"
        out += ["### %s %s" % (task.task, backlog_items.label(item)), "",
                "- Worktree: %s (made by `work batch resume`)" % (trees_dir(root) / ("%s-%s" % (batch.name, task.task))),
                "- Branch: %s" % task.branch,
                "- Item file: %s" % (Path(root) / backlog_items.rel_of(item.name)),
                "- Requirement ids: %s" % (", ".join(ids) or "none"),
                "- Acceptance tests (in the worktree): %s" % tests,
                "- Subagent description: `%s %s %s`" % (batch.name, task.task, item.name), ""]
    return out


def text(root, batch, picked):
    """The batch brief of `batch`, whose tasks are the items `picked`, in order."""
    root, push = Path(root).resolve(), push_prefix(root)
    out = ["# %s: the batch brief" % batch.name, "",
           "You run %s, from `work batch resume` until its pull request is `awaiting-merge`, as the one fresh agent "
           "of this batch: you dispatch its task, fix and review subagents yourself." % batch.name, "",
           "- Batch: %s (`%s`)" % (batch.name, batch_plan.rel_of(batch.name)),
           "- Base checkout: %s, on %s: run every `work batch` command there, never in a task's worktree" % (
               root, batch.base),
           "- Batch branch: %s, its worktree %s" % (batch.branch, trees_dir(root) / batch.name),
           "- Scripts: %s" % SCRIPTS, "",
           "## The skill", "",
           "Follow the skill `%s` from step 3 (Resume) to step 7's `-> awaiting-merge`: `work batch resume %s`, one "
           "subagent for each running task, all at once, `work batch done` or `park` as each returns, `work batch "
           "review`, then `work batch brief`, a fresh `shopsystem-bdd:pr-reviewer` and `work batch reviewed`, and the "
           "fix loop until the review is clean." % (SKILL, batch.name), "",
           "## Tasks", ""]
    out += _tasks(root, batch, picked)
    out += ["## Push", "",
            ("Run every git push and gh call as `%s <command>`; `work` pushes its own commits." % push) if push else
            "`.shop/delivery.toml` gives no `[batch] push`: git push and gh run as they are; `work` pushes its own "
            "commits.", "",
            "## The rules every subagent is given", ""]
    out += ["- %s" % r for r in RULES]
    out += ["", "## Where you stop", "",
            ("At `-> awaiting-merge`, once the pull request is clean and marked ready. You never merge the pull "
             "request, and never run `work batch merged` nor `measure batch`: the session that started you does, "
             "after the person merges it. A question you cannot settle goes onto its item with `work batch park`, "
             "never to the person."), "",
            "## What you reply", "",
            ("The pull request's URL, each item delivered in it and each item parked with its question, in a few "
             "lines; or, if the batch was abandoned, that and why.")]
    return "\n".join(out) + "\n"


def write(root, batch, picked):
    """The batch brief of `batch` written; its path."""
    where = path(root, batch.name)
    where.parent.mkdir(parents=True, exist_ok=True)
    where.write_text(text(root, batch, picked), encoding="utf-8")
    return where
