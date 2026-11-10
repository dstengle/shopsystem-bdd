"""Handlers of features/batches.feature in grammar 4 (b240, b158): the Givens of the batches, tasks, commits, pull
requests, review folders, scenarios and requirements batches_world.py builds, said with has, holds, cites, passes and
fails, each in world_four's chain beside the backlog's (backlog_handlers4.py), over the world functions of
batches_handlers*.py."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")


def _module(stem):
    """A handler module of the glob, by its file's stem."""
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and m.__file__.endswith("/%s.py" % stem))


@four("GivenDoes", "holds", *BOTH)
def holds_given(step):
    """A batch holds an item (in it, `in-batch` unless a Given says otherwise); a git branch holds a requirement (the
    world lays the item's lines on the batch's branch)."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) == ("batch", "item"):
        T.given(step, "batch", n1)
        T.given(step, "item", n2)["batch"] = n1
        if not B.item_rel(step.context, n2):
            B.write_item(step, n2)
        if T.status_of(step, n2) == "idea":
            B.write_item(step, n2, status="in-batch")
    elif (k1, k2) != ("git branch", "requirement"):
        return False


@four("GivenDoes", "has", *BOTH)
def has_given(step):
    (k1, n1), (k2, n2) = parts(step)
    if k1 == "batch" and k2 in ("pull request", "review folder", "task"):
        T.given(step, "batch", n1)
        T.given(step, k2, n2)["batch"] = n1
    elif (k1, k2) == ("item", "task"):
        T.given(step, "task", n2).update(item=n1, batch=T.given(step, "item", n1).get("batch", "b1"))
    elif (k1, k2) == ("item", "scenario"):
        step.context.setdefault("scenario_of", {})[n2] = n1
    elif (k1, k2) == ("item", "requirement"):
        step.context.setdefault("proposed", {})[n2] = n1
    elif (k1, k2) == ("git branch", "commit"):
        task = step.context["git_branches"][n1]["task"]
        T.given(step, "task", task).setdefault("item", T.OWN_IN)
        T.given(step, "commit", n2)["item"] = step.context["given"]["task"][task]["item"]
    elif (k1, k2) not in (("task", "worktree"), ("batch", "git branch")):
        return False


@four("GivenK", "worktree", *BOTH)
def given_worktree(step):
    """The task's worktree, which the world makes for a running task."""


@four("GivenDoes", "cite", *BOTH)
def cites_given(step):
    """A commit cites the item (a commit of the item's branch), or cites no item (its message has no `Item:` line)."""
    commit = parts(step)[0][1]
    if step.nps[0] == "no item":
        T.given(step, "commit", commit)["uncited"] = True
    else:
        T.given(step, "commit", commit)["item"] = parts(step)[1][1]


@four("GivenDoes", "pass", *BOTH)
@four("GivenDoesNot", "pass", *BOTH)
@four("GivenDoes", "fail", *BOTH)
def passes_given(step):
    """An item passes the readiness bar (the lines `work batch start` gives a ready item) or does not (a line that
    does not parse); a scenario of an item fails or passes in the worktree of the task (the batch's tests)."""
    k, name = parts(step)[0]
    if k == "item":
        if step.template == "GivenDoesNot":
            sys.modules["shop_readiness_world"].give_lines(step, name, sys.modules["shop_readiness_world"].FAILING)
    else:
        item = step.context["scenario_of"][name]
        step.context["failing" if step.term == "fail" else "passing"] = item


@four("WhenRuns", "`work batch park`", *BOTH)
def batch_park(step):
    item = step.names[-1]
    batch = T.given(step, "item", item).get("batch", "b1")
    T.prepare(step)
    T.ensure_batch(step)
    T.run_batch(step, "park", T.batch_name(step, batch), B.ident(item), "--question",
                _module("batches_handlers_more").QUESTION)


@four("WhenHappens", "merge", *BOTH)
def merges(step):
    return _module("batches_handlers_more").merges_pull_request(step)


@four("ThenDoes", "set", *BOTH)
@four("ThenDoesNot", "set", *BOTH)
def sets(step):
    """The plan's status of the batch, or the task's row, is (is not) the value."""
    np = step.nps[0]
    if not np.startswith("the status of the "):
        return False
    k, name = F.kind(np[len("the status of the "):])
    if k not in ("batch", "task"):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    got = T.plan_field(step, name, "status") if k == "batch" else T.task_row(step, name)[0]
    wanted = step.text.rsplit(" to ", 1)[1].strip("`")
    assert (got != wanted) if step.template == "ThenDoesNot" else (got == wanted), (step.text, got)
