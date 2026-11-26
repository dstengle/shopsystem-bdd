"""The batch brief (capability batches r14; item b55): what `work batch start` writes, once it has laid the batch, for
the one fresh agent that runs the batch from `work batch resume` to `awaiting-merge`, at
`.shop/worktrees/batch-<n>-driver/brief.md` beside the review folders, never committed.

It names the batch and its base checkout, each task with its worktree, branch, item and requirement ids, the skill the
agent follows (building-a-batch) by its poll loop on `work batch next` and what each step it names asks (b787), each
task's acceptance tests run with the plugin's pytest plugin (`-p work_items`), and, for a context's first batch (a laid
capability with no test module, or a domain model with no `spec/adapters/cli.toml`), how its first task makes the step
bindings, the program and the adapter contract (b389), the command prefix every push and gh call takes when `[batch]
push` of `.shop/delivery.toml` gives one, the rules every subagent is given (the plugin's own, then each batch rule of
`[batch] rules`, the context's own setup, which the plugin's code never keeps: b75), where the agent stops and what it
replies, with the batch summary in the batch summary form (batch_summary, b580). The session that started the batch
dispatches the agent with the brief's path as its whole prompt."""
from pathlib import Path

import backlog_chore
import backlog_items
import backlog_lines
import batch_plan
import batch_summary
from batch_git import SCRIPTS, delivery, trees_dir
from plumbing.shop_files import Refused

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
    ("Never use `git stash`: every worktree shares one stash list, so two tasks' stashes swap; to see a test "
     "red, put files back with `git checkout <commit> -- <path>` or a scratch copy."),
    "Don't push and don't run `shop work` commands that commit.",
    "A scenario that passes before it is built (an XPASS) means a test step is too loose: say so in the reply.",
    ("There is no brief or result file: reply with what was built and its commits, or with one question, never a "
     "guess. `shop work batch done` runs the whole suite in the worktree and refuses with its last lines."),
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


def batch_rules(root):
    """`[batch] rules` of `.shop/delivery.toml`: the context's own batch rules, each a text, in order (none when it
    gives none)."""
    given = delivery(root).get("batch", {}).get("rules", [])
    if not isinstance(given, list) or not all(isinstance(r, str) for r in given):
        raise Refused("work batch start: .shop/delivery.toml: [batch] rules is not a list of texts")
    return [r for r in given if r.strip()]


def _tasks(root, batch, picked):
    out = []
    for task, item in zip(batch.tasks, picked):
        ids = backlog_lines.ids(backlog_lines.read(item, backlog_items.rel_of(item.name)))
        caps = sorted({i.split("#")[0] for i in ids})
        tests = "; ".join("`PYTHONPATH=%s python3 -m pytest -p work_items -q %s -m \"%s\"`" % (
            SCRIPTS, _module(c), " or ".join("r%s" % i.split("#r")[1] for i in ids if i.startswith(c + "#")))
            for c in caps) or "none"
        unbound = [_module(c) for c in caps if not (root / _module(c)).exists()]
        chore = ["- %s" % said for said in backlog_chore.said(item)]       # in place of ids (b316)
        out += ["### %s %s" % (task.task, backlog_items.label(item)), "",
                "- Worktree: %s (made by `shop work batch resume`)" % (trees_dir(root) / ("%s-%s" % (batch.name, task.task))),
                "- Branch: %s" % task.branch,
                "- Item file: %s" % (Path(root) / backlog_items.rel_of(item.name)),
                *(chore or ["- Requirement ids: %s" % (", ".join(ids) or "none"),
                            "- Acceptance tests (in the worktree): %s" % tests,
                            *(["- Step bindings: none yet; this task writes %s (see `## A fresh context`)"
                               % ", ".join(unbound)] if unbound else [])]),
                "- Subagent description: `%s %s %s`" % (batch.name, task.task, item.name), ""]
    return out


def _module(cap):
    """The test module that binds a capability's generated feature."""
    return "tests/scenarios/test_%s.py" % cap.replace("-", "_")


LOOP = (
    ("prepare task", "`shop work batch resume`, which gives each pending task its worktree."),
    ("build task", ("one subagent for every task in its `tasks` list at once, each in its task's worktree, with its "
                    "task below and the rules every subagent is given.")),
    ("finish task", "`shop work batch done` of its task; a refusal goes back to the task's subagent."),
    ("fix task", ("the task's subagent fixes its branch (the conflict or the failed tests named), then `shop work batch "
                  "review`.")),
    ("look at failure", ("the failed tests looked at and fixed on the batch's branch or a task's, then `shop work batch "
                         "review`.")),
    ("submit batch", "`shop work batch review`, which merges, tests, pushes and opens the draft pull request."),
    ("review change", ("`shop work batch brief`, a fresh `shopsystem-bdd:pr-reviewer` given the brief's path alone, its "
                       "reply saved byte for byte at the findings file it names.")),
    ("fix finding", ("one subagent in the finding's task's worktree, each commit citing `Item:` and `Finding:`, then "
                     "`shop work batch review`.")),
    ("park item", "`shop work batch park` of the item with its subagent's question."),
    ("abandon batch", "`shop work batch abandon`: every item is `needs-input`."),
    ("stop", "the batch is `awaiting-merge` (or no longer building): reply as `## What you reply` says."),
)


FRESH = (
    ("A context's first batch builds what its tests run against, and nothing of it is laid by `shop work batch start`. "
     "The first task whose item needs a piece makes it; a later task that needs it too merges that task's branch "
     "into its own (its commits cite the earlier in-batch item, which `done` accepts)."),
    ("- Step bindings: one test module a capability, `tests/scenarios/test_<capability>.py`, binding "
     "`features/<capability>.feature` with pytest-bdd's `scenarios(...)` and one step definition a step text; "
     "`shop features vocab` lists the step grammar's shapes (the functions ending in `Step`) and %s, step 6, shows a "
     "whole module. `tests/scenarios/conftest.py` (from `shop migrate init`) and `-p work_items` make an `unbuilt:` id's "
     "scenario a strict xfail." % (SCRIPTS.parent / "docs" / "getting-started.md")),
    ("- The program: the command-line program the lines' operations are requested of, with its argparse "
     "subcommands and options; a When step runs it, a Then reads its exit, output and the files it kept."),
    ("- The adapter contract `spec/adapters/cli.toml`: `[programs]` names the program's path, and each "
     "`[operations.\"<service>.<operation>\"]` of the domain model the lines request maps it to its `command` and "
     "its `parameters` to options; `shop spec check` holds it to the model and the program both ways (v_a1-v_a4), and "
     "`shop spec annotate` writes each operation's governing requirements into it (`shop spec annotate --check` in the "
     "suite). Without the file `shop spec annotate` and its `--check` do nothing and say nothing."),
    ("- `shop work batch review` pushes the batch branch and opens a draft pull request: the repository needs a remote "
     "and gh logged in to it (a remote and gh), or the review is refused."),
)


def _fresh(root, picked):
    """Whether the brief says how a context's first batch makes its bindings, program and contract: a laid
    capability with no test module, or a domain model with no CLI adapter contract."""
    caps = {i.split("#")[0] for item in picked
            for i in backlog_lines.ids(backlog_lines.read(item, backlog_items.rel_of(item.name)))}
    unbound = any(not (root / _module(c)).exists() for c in caps)
    return unbound or ((root / "spec" / "model").is_dir() and not (root / "spec" / "adapters" / "cli.toml").exists())


def text(root, batch, picked, unwritten=(), superseded=()):
    """The batch brief of `batch`, whose tasks are the items `picked`, in order; `unwritten`, each catalogue problem
    that kept the lay from writing it (batch_catalogues, b333); `superseded`, each decision the lay superseded
    (decision_successor's `said`, b741)."""
    root, push = Path(root).resolve(), push_prefix(root)
    out = ["# %s: the batch brief" % batch.name, "",
           "You run %s, from `shop work batch resume` until its pull request is `awaiting-merge`, as the one fresh agent "
           "of this batch: you dispatch its task, fix and review subagents yourself." % batch.name, "",
           "- Batch: %s (`%s`)" % (batch.name, batch_plan.rel_of(batch.name)),
           "- Base checkout: %s, on %s: run every `shop work batch` command there, never in a task's worktree" % (
               root, batch.base),
           "- Batch branch: %s, its worktree %s" % (batch.branch, trees_dir(root) / batch.name),
           "- Scripts: %s" % SCRIPTS, "",
           "## The loop", "",
           "Follow the skill `%s`, steps 3 to 7, by its poll: run `shop work batch next %s --json` from the base "
           "checkout, do the step its `instruction` names, report it through the command its content gives, and ask "
           "again, until it says `stop`." % (SKILL, batch.name), "",
           *["- `%s`: %s" % step for step in LOOP], "",
           "Conclude every review with `shop work batch reviewed %s --reply <the reviewer's transcript>`. A task "
           "subagent's completion may reach the session that started you instead of you: if one seems quiet, check its "
           "branch and ask `shop work batch next` again. Never end your turn while a subagent is still running." % (
               batch.name), "",
           "## Tasks", ""]
    out += _tasks(root, batch, picked)
    if _fresh(root, picked):
        out += ["## A fresh context", "", FRESH[0], "", *FRESH[1:], ""]
    out += ["## The lay's bookkeeping", "",
            ("The lay's commit wrote each laid line's corpus block, took out each retired id's and wrote the "
             "catalogues again (b333): a block's form is the parser's, so the task whose item changes the grammar "
             "reads it against the line and corrects it."), ""]
    out += ["- Not written, for the task of the item that brings it to mend: %s" % p for p in unwritten]
    out += [""] if unwritten else []
    out += ["- Superseded by the lay, its retirement leaving the decision unenforced: %s" % s for s in superseded]
    out += [""] if superseded else []
    out += ["## Push", "",
            ("Run every git push and gh call as `%s <command>`; `work` pushes its own commits." % push) if push else
            "`.shop/delivery.toml` gives no `[batch] push`: git push and gh run as they are; `work` pushes its own "
            "commits.", "",
            "## The rules every subagent is given", ""]
    out += ["- %s" % r for r in (*RULES, *batch_rules(root))]
    out += ["", "## Where you stop", "",
            ("At `-> awaiting-merge`, once the pull request is clean and marked ready. You never merge the pull "
             "request, and never run `shop work batch merged` nor `shop measure batch`: the session that started you does, "
             "after the person merges it. A question you cannot settle goes onto its item with `shop work batch park`, "
             "never to the person."), "",
            "## What you reply", "",
            ("At `stop`: the pull request's URL, each item delivered in it and each item parked with its question, in a few "
             "lines; or, if the batch was abandoned, that and why; and any new gap of `shop work batch next`, a step it "
             "named wrongly or did not name. Then the batch summary, in the batch summary form "
             "below (b580): each figure as far as the batch has run, its cost and tokens summed from what your "
             "subagents and your own session report, its times from the batch's commits and the test runs `shop work "
             "batch done` and `review` timed; a figure you cannot read written `%s`." % batch_summary.UNKNOWN), "",
            "### The batch summary form", "", *batch_summary.form()]
    return "\n".join(out) + "\n"


def write(root, batch, picked, unwritten=(), superseded=()):
    """The batch brief of `batch` written; its path."""
    where = path(root, batch.name)
    where.parent.mkdir(parents=True, exist_ok=True)
    where.write_text(text(root, batch, picked, unwritten, superseded), encoding="utf-8")
    return where
