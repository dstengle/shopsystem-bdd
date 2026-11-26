"""An amended item lifted from the workspaces of its batch and its task and laid there again (batches r185, b747), each
handler taking only a step of g185's scenario (`mine`): the laying service swapped for batches_handlers_laying's
stand-in (`$SHOPSYSTEM_LAYING`, its requests recorded in the outside folder's `laying-calls.jsonl`) before `work batch
amend` runs, which batches_handlers_amend's When runs over batches_world's batch. A Then of a lift or a lay of the item
i1 from (in) a workspace waits until a later Then says whose workspace it is (`the batch b1 has the workspace w1`: the
batch's worktree, `batch-1` in the worktrees directory; `the task t1 has the workspace w2`: the task's,
`batch-1-t1`); each is then read off the stand-in's records: the request of the item in that workspace, a lay after
the lift."""
import sys
from pathlib import Path

import batch_git

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
parts = F.parts
GROUP = "g185"


def _laying():
    return next(m for m in list(sys.modules.values())
                if str(getattr(m, "__file__", "") or "").endswith("/batches_handlers_laying.py"))


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "batches" and GROUP in found.tags


def stand_in(step):
    """Before `work batch amend`: the stand-in wired in, answering as the in-process adapter does."""
    if not mine(step):
        return
    env = step.context.setdefault("env", {})
    env.update(SHOPSYSTEM_LAYING=str(_laying().STAND_IN),
               STAND_IN_LAYING_CALLS=str(T.outside(step) / "laying-calls.jsonl"))


T.BEFORE_RUN.append(stand_in)


def _asked(step, operation, workspace):
    """The indexes of the stand-in's requests of `operation` of the item i1 in `workspace`."""
    return [k for k, c in enumerate(_laying().calls(step)) if c["operation"] == operation
            and c.get("item") == B.ident("i1") and str((step.repo / c["workspace"]).resolve()) == workspace]


def _check(step, operation, name):
    """The request of `operation` in the workspace `name` stands for was recorded, a lay after the lift."""
    workspace = step.context["relaid"]["of"][name]
    asked = _asked(step, operation, workspace)
    assert asked, (operation, workspace, _laying().calls(step), step.context["result"].stderr)
    if operation == "lay":
        lifted = _asked(step, "lift", workspace)
        assert lifted and asked[-1] > lifted[0], _laying().calls(step)


def _relaid(step):
    return step.context.setdefault("relaid", {"of": {}, "waiting": []})


@_laying().first("ThenDoes", "lift")
@_laying().first("ThenDoes", "lay")
def requested(step):
    """`the batches service lifts (lays) the item i1 from (in) the workspace w1`: checked once w1 is known."""
    if not mine(step) or "result" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    name, relaid = parts(step)[-1][1], _relaid(step)
    if name in relaid["of"]:
        _check(step, step.term, name)
    else:
        relaid["waiting"].append((step.term, name))


@_laying().first("ThenDoes", "has")
def has(step):
    """`the batch b1 has the workspace w1`, `the task t1 has the workspace w2`: the batch's worktree, the task's; each
    request waiting on it checked."""
    if not mine(step) or "result" not in step.context:
        return False
    (k1, n1), (_, n2) = parts(step)
    trees = batch_git.trees_dir(step.repo)
    batch = T.batch_name(step, "b1")
    tree = trees / batch if k1 == "batch" else trees / ("%s-%s" % (batch, T.task_id(step, n1)))
    relaid = _relaid(step)
    relaid["of"][n2] = str(tree.resolve())
    for operation, name in [w for w in relaid["waiting"] if w[1] == n2]:
        _check(step, operation, name)
    relaid["waiting"] = [w for w in relaid["waiting"] if w[1] != n2]
