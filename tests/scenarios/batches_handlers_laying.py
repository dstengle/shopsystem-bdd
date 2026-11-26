"""Handlers of batches' scenarios of the laying service (r179-r184, b611), each taking only a step of a scenario of
one of its groups (`mine`). The laying service is swapped for the stand-in adapter tests/scenarios/stand_in_laying.py
(`$SHOPSYSTEM_LAYING`), which records each request in the outside folder's `laying-calls.jsonl` and makes it of the
in-process adapter, before every `work batch` command such a scenario runs (batches_world's BEFORE_RUN). The Given of
the core's request (`the batches service lays the item i1 in the workspace w1`) says which request the When's reply is
on; the When (`the laying service completes the request to lay ...`, `... fails the request to check ...`) runs the
command whose request it is with the stand-in so answering: `work batch start` of a lay or a check, the item i1 made
`ready` with readiness_world's passing line, or `work batch park` of a lift, i1 `in-batch` in batches_world's batch
b1. A rule a requirement of i1 violates is a code of the stand-in's failure (`v_la<n>`), one it does not violate a
code the failure leaves out. The workspace of the batch is its worktree, `batch-1` in the worktrees directory. The
Thens read the requests the stand-in recorded, the batch branch's commits and what `work batch` printed."""
import json
import sys
from pathlib import Path

import batch_git

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
GROUPS = {"g179", "g180", "g181", "g182", "g183", "g184"}
STAND_IN = Path(__file__).resolve().parent / "stand_in_laying.py"
REPLIES = {"complete": "complete", "fail": "fail"}


def _module(name):
    return next(m for m in list(sys.modules.values()) if (getattr(m, "__file__", None) or "").endswith("/" + name))


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "batches" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("laying", {"rules": {}, "violated": []})


def first(template, term):
    """`four`, the handler put first in its key's chain."""
    def mark(fn):
        four(template, term, "batches")(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


def calls(step):
    path = T.outside(step) / "laying-calls.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()] if path.is_file() else []


def stand_in(step):
    """Before a `work batch` command of one of the groups: the stand-in wired in, recording its requests."""
    if not mine(step):
        return
    w = world(step)
    env = step.context.setdefault("env", {})
    env.update(SHOPSYSTEM_LAYING=str(STAND_IN), STAND_IN_LAYING_CALLS=str(T.outside(step) / "laying-calls.jsonl"),
               STAND_IN_LAYING_REPLY=w.get("reply", ""), STAND_IN_LAYING_ON=w.get("request", ""),
               STAND_IN_LAYING_RULES=",".join(w["violated"]))


T.BEFORE_RUN.append(stand_in)


@first("GivenDoes", "lay")
@first("GivenDoes", "lift")
@first("GivenDoes", "check")
def given_request(step):
    """`the batches service lays (lifts, checks) the item i1 in (from) the workspace w1`: the request replied to."""
    if not mine(step):
        return False
    world(step)["request"] = step.term


@first("GivenDoes", "violate")
@first("GivenDoesNot", "violate")
def given_violates(step):
    """`the requirement r3 violates the rule r2`: a rule the stand-in's failure names; `does not violate`: one it
    leaves out."""
    if not mine(step):
        return False
    w = world(step)
    rule = parts(step)[-1][1]
    code = w["rules"].setdefault(rule, "v_la%d" % (len(w["rules"]) + 1))
    if step.template == "GivenDoes":
        w["violated"].append(code)


@first("WhenHappens", "complete")
@first("WhenHappens", "fail")
def replies(step):
    """`the laying service completes (fails) the request to lay (check, lift) the item i1 ...`: the command whose
    request it is, run with the stand-in so answering."""
    if not mine(step):
        return False
    w = world(step)
    w["reply"] = REPLIES[step.term]
    if w.get("request") == "lift":
        B.write_item(step, "i1", status="in-batch")
        T.prepare(step)
        T.ensure_batch(step)
        w["head"] = T.git(step, "rev-parse", T.batch_name(step, "b1")).strip()
        T.run_batch(step, "park", T.batch_name(step, "b1"), B.ident("i1"), "--question",
                    _module("batches_handlers_more.py").QUESTION)
        return None
    B.write_item(step, "i1", status="ready")
    T.before_start(step)
    T.prepare(step)
    T.run_batch(step, "start")


def _workspace(step):
    return str((batch_git.trees_dir(step.repo) / "batch-1").resolve())


def _asked(step, operation):
    """The requests of `operation` of the item i1 in the batch's workspace the stand-in recorded, by their index."""
    return [k for k, c in enumerate(calls(step)) if c["operation"] == operation and c["item"] == B.ident("i1")
            and str((step.repo / c["workspace"]).resolve()) == _workspace(step)]


@first("ThenDoes", "lay")
@first("ThenDoes", "lift")
@first("ThenDoes", "check")
def then_requests(step):
    """`the batches service lays (lifts, checks) the item i1 in (from) the workspace w1`: the stand-in recorded the
    request of the item in the batch's workspace; a check after the lay it completed (r180)."""
    if not mine(step) or "result" not in step.context:
        return False
    assert _asked(step, step.term), (step.text, calls(step), step.context["result"].stderr)
    if step.term == "check":
        laid = [k for k, c in enumerate(calls(step)) if c["operation"] == "completed" and c.get("of") == "lay"]
        assert laid and _asked(step, "check")[-1] > laid[0], calls(step)


@first("ThenDoes", "has")
def then_has(step):
    """`the batch b2 has the workspace w1`: the workspace the stand-in was asked to lay in is the batch's."""
    if not mine(step) or [k for k, _ in parts(step)] != ["batch", "workspace"]:
        return False
    assert _asked(step, "lay"), (_workspace(step), calls(step))


@first("ThenDoes", "reopen")
def then_reopens(step):
    """`the batches service reopens the item i1`: given back `shaped` once the stand-in failed its check."""
    if not mine(step) or "result" not in step.context:
        return False
    done = step.context["result"]
    assert _asked(step, "check") and done.returncode == 0, (calls(step), done.stdout, done.stderr)
    assert B.status_of(step, B.ident("i1")) == "shaped", done.stdout


@first("ThenDoes", "name")
@first("ThenDoesNot", "name")
def then_names(step):
    """`the batches service names the rule r2` (does not name `r6`): its code in what `work batch start` printed."""
    if not mine(step) or "result" not in step.context or parts(step)[-1][0] != "rule":
        return False
    code, out = world(step)["rules"][parts(step)[-1][1]], step.context["result"].stdout
    assert (code in out) != (step.template == "ThenDoesNot"), (step.text, code, out)


@first("ThenDoes", "keep")
@first("ThenDoes", "write")
@first("ThenDoes", "commit")
@first("ThenDoes", "cite")
def then_kept(step):
    """`the batches service keeps the kept change k1` and `the kept change k1 cites the item i1`: once the stand-in
    recorded the completion of the request, the batch branch's head a new commit citing the item."""
    if not mine(step) or "result" not in step.context or not {"kept change", "commit"} & {k for k, _ in parts(step)}:
        return False
    done, w = step.context["result"], world(step)
    assert done.returncode == 0, (done.stdout, done.stderr)
    completed = [c for c in calls(step) if c["operation"] == "completed" and c.get("of") == w.get("request")]
    assert completed and completed[0]["item"] == B.ident("i1"), calls(step)
    branch = T.batch_name(step, "b1")
    head = T.git(step, "rev-parse", branch).strip()
    assert head != w.get("head"), head
    assert "Item: %s" % B.ident("i1") in T.git(step, "log", "-1", "--format=%B", branch).splitlines(), \
        T.git(step, "log", "-1", "--format=%B", branch)
