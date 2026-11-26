"""Handlers of a batch polled by its driver (batches r135-r141, b683): over batches_world's batch (its tasks, review
folders, and batches_handlers_finding's review with its `fix now` findings), the batch brief a Given gives the batch
written where `work batch start` writes it (batch_driver's `path`), `work batch next <batch> --json` run, and the
Thens, first in their chains, read the batch step off the envelope's content: its instruction, and the task, batch
brief, review folder or review finding it returns. A scenario of an item that breaks in the batch's workspace once
every task is done (r149, b696) is a submit the whole suite refused: `work batch review` run before the poll with
`[batch] tests` that fail naming the item's scenario test, as pytest's short summary names it."""
import json
import re
import sys
from pathlib import Path

import batch_broken
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


@first("GivenDoes", "cite")
def none_cites(step):
    """`no kept change cites the item i1`: its task's branch holds no commit after the batch's lines commit."""
    if not (step.subject or "").startswith("no "):
        return False
    kind, name = parts(step)[-1]
    assert kind == "item", step.text
    T.given(step, "item", name)["unbuilt"] = True


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


def failing_suite(step, item):
    """`[batch] tests` that fail naming the scenario test of the item's group (titled as the item is)."""
    test = "tests/scenarios/test_work_queue.py::%s" % batch_broken.test_name(step.context["item_fields"][item]["title"])
    return "[batch]\ntests = '''python3 -c \"print('FAILED %s - broken'); raise SystemExit(1)\"'''\n" % test


def refused_submit(step, batch):
    """The batch's submit refused by its whole-suite run, when the scenario of an item breaks and every task is done."""
    tasks = step.context["given"].get("task", {}).values()
    if not tasks or any(t.get("status") != "done" for t in tasks):
        return
    done = T.run_batch(step, "review", T.batch_name(step, batch))
    assert done.returncode != 0 and "FAILED" in done.stderr, (done.stdout, done.stderr)


RANK = {"failed": 0, "running": 1, "pending": 2}
PARKED = "i91"


def polled_world(step):
    """Under a poll (b702): the item of a running task no kept change cites is unbuilt (a Given of a kept change citing
    it builds it), and a task the scenario says the service does not return, of a status whose step comes before the
    step its Thens expect, is the task of a parked item, which the poll does not count, so that the line's precondition
    (no task of the batch is that status) holds of the batch's in-batch items."""
    if not step.context.get("polling"):
        return
    text = " ".join(W.scenario_texts(step))
    tasks, items = step.context["given"]["task"], step.context["given"]["item"]
    for name, found in items.items():
        cited = re.search(r"\bthe kept change [a-z]+\d+ cites the item %s\b" % name, text)
        if not cited and any(t["item"] == name and t["status"] == "running" for t in tasks.values()):
            found["unbuilt"] = True
    wanted = re.search(r"instruction of the batch step [a-z]+\d+ is `(\w+) task`", text)
    rank = {"park": 0, "build": 1, "finish": 1, "prepare": 2}.get(wanted.group(1) if wanted else None)
    for name in re.findall(r"\bdoes not return the task ([a-z]+\d+)\b", text):
        found = tasks.get(name)
        if found and rank is not None and RANK.get(found["status"], 3) < rank:
            B.write_item(step, PARKED, title="an item parked in the batch", status="needs-input")
            items.setdefault(PARKED, {"batch": found["batch"]})
            found["item"] = PARKED


T.BEFORE_BATCH.append(polled_world)


@four("WhenRuns", "`work batch next`", *BOTH)
def batch_next(step):
    step.context["polling"] = True
    failing = step.context.get("failing")
    if failing:
        step.context["delivery"] = failing_suite(step, failing)
    T.prepare(step)
    T.ensure_batch(step)
    batch = next(n for n in step.names if n in step.context["given"]["batch"])
    if failing:
        refused_submit(step, batch)
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
    task, one of the step's `tasks`), `... the batch brief b2` (its path), `... the review folder r1` (its path), `... the findings file f1` (its
    path, `findings.md` in the review folder returned), `... the review finding r2`."""
    if "polled" not in step.context:
        return False
    content = _step(step)
    kind, name = parts(step)[-1]
    if kind == "batch step":
        assert content["instruction"] in INSTRUCTIONS, (step.text, content)
        step.context.setdefault("batch_steps", {})[name] = content
    elif kind == "task":
        assert T.task_id(step, name) in [t["task"] for t in content["tasks"]], (step.text, content)
    elif kind == "batch brief":
        assert content["batch brief"] == step.context["briefs"][name], (step.text, content)
    elif kind == "review folder":
        want = Path(step.context["review_folders"][name]).resolve()
        assert content["review folder"] and Path(content["review folder"]) == want, (step.text, content)
    elif kind == "findings file":
        want = Path(content["review folder"] or "") / "findings.md"
        assert content.get("findings file") and Path(content["findings file"]) == want, (step.text, content)
        step.context.setdefault("findings_files", {})[name] = content["findings file"]
    elif kind == "review finding":
        assert content["review finding"] and content["review finding"]["finding"] == _fid(step, name), (
            step.text, content)
    else:
        return False


@first("ThenPrintsNot", "`work`")
def returns_not(step):
    """`the batches service does not return the task t5`: none of the step's `tasks` is the plan's task (b702)."""
    if "polled" not in step.context:
        return False
    kind, name = parts(step)[-1]
    if kind != "task":
        return False
    content = _step(step)
    assert T.task_id(step, name) not in [t["task"] for t in content["tasks"]], (step.text, content)


@four("ThenK_A", "batch step", *BOTH)
def instruction_is(step):
    """`the instruction of the batch step b2 is `stop``: the batch step returned says it."""
    content = step.context.get("batch_steps", {}).get(step.names[0])
    assert content is not None, ("no batch step returned", step.text)
    assert content["instruction"] == step.values[0].strip("`"), (step.text, content)


@first("ThenDoes", "holds")
def folder_holds(step):
    """`the review folder r1 holds the findings file f1`: the findings file returned is `findings.md` in r1's path."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("review folder", "findings file") or "polled" not in step.context:
        return False
    found = step.context.get("findings_files", {}).get(n2)
    assert found, ("no findings file returned", step.text)
    assert Path(found) == Path(step.context["review_folders"][n1]).resolve() / "findings.md", (step.text, found)
