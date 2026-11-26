"""Handlers of a batch polled by its driver (batches r135-r141, b683): over batches_world's batch (its tasks, review
folders, and batches_handlers_finding's review with its `fix now` findings), the batch brief a Given gives the batch
written where `work batch start` writes it (batch_driver's `path`), `work batch next <batch> --json` run, and the
Thens, first in their chains, read the batch step off the envelope's content: its instruction, and the task, batch
brief, review folder or review finding it returns."""
import json
import sys
from pathlib import Path

import batch_driver
from batch_next import INSTRUCTIONS

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")


def first(template, term):
    """`four`, the handler put first in its key's chain."""
    def mark(fn):
        four(template, term, *BOTH)(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


@four("GivenK", "batch brief", *BOTH)
def given_brief(step):
    """The batch brief, written once its batch is (`briefed`)."""
    T.given(step, "batch brief", step.names[0])


@first("GivenDoes", "has")
def has_brief(step):
    """`the batch b1 has the batch brief b2`."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("batch", "batch brief"):
        return False
    T.given(step, "batch", n1)
    T.given(step, "batch brief", n2)["batch"] = n1


@four("GivenK_A", "review finding", *BOTH)
def given_triage(step):
    """`the triage of the review finding r2 is `fix now``: batches_handlers_finding records each as `fix now`."""
    assert step.values and step.values[0].strip("`") == "fix now", step.text


def briefed(step, name):
    """Each batch brief of the batch `name` written where `work batch start` writes it (T.AFTER_BATCH)."""
    for brief, found in step.context.get("given", {}).get("batch brief", {}).items():
        if found.get("batch") == name:
            path = batch_driver.path(step.repo, T.batch_name(step, name))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("the batch brief %s\n" % brief)
            step.context.setdefault("briefs", {})[brief] = str(path)


T.AFTER_BATCH.append(briefed)


@four("WhenRuns", "`work batch next`", *BOTH)
def batch_next(step):
    T.prepare(step)
    T.ensure_batch(step)
    batch = next(n for n in step.names if n in step.context["given"]["batch"])
    done = T.run_batch(step, "next", T.batch_name(step, batch), "--json")
    step.context["polled"] = json.loads(done.stdout) if done.returncode == 0 else None


def _step(step):
    polled = step.context["polled"]
    assert polled is not None, (step.text, step.context["result"].stderr)
    assert polled["outcome"] == "returned", (step.text, polled)
    return polled["content"]


def _fid(step, name):
    return step.context["given"]["review finding"][name]["fid"]


@first("ThenPrints", "`work`")
def returns(step):
    """`the batches service returns the batch step b2` (a batch step the content is), `... the task t1` (the plan's
    task), `... the batch brief b2` (its path), `... the review folder r1` (its path), `... the review finding r2`."""
    if "polled" not in step.context:
        return False
    content = _step(step)
    kind, name = parts(step)[-1]
    if kind == "batch step":
        assert content["instruction"] in INSTRUCTIONS, (step.text, content)
        step.context.setdefault("batch_steps", {})[name] = content
    elif kind == "task":
        assert content["task"] and content["task"]["task"] == T.task_id(step, name), (step.text, content)
    elif kind == "batch brief":
        assert content["batch brief"] == step.context["briefs"][name], (step.text, content)
    elif kind == "review folder":
        want = Path(step.context["review_folders"][name]).resolve()
        assert content["review folder"] and Path(content["review folder"]) == want, (step.text, content)
    elif kind == "review finding":
        assert content["review finding"] and content["review finding"]["finding"] == _fid(step, name), (
            step.text, content)
    else:
        return False


@four("ThenK_A", "batch step", *BOTH)
def instruction_is(step):
    """`the instruction of the batch step b2 is `stop``: the batch step returned says it."""
    content = step.context.get("batch_steps", {}).get(step.names[0])
    assert content is not None, ("no batch step returned", step.text)
    assert content["instruction"] == step.values[0].strip("`"), (step.text, content)
