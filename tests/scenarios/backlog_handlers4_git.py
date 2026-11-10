"""Handlers of features/backlog.feature's git in grammar 4 (b240, b158): a remote that rejects the push of `work
idea` or does not answer it (backlog_handlers_remote.py's hooks), a git branch of a task that this repository checks
out, and a git branch whose upstream branch has a different branch name (backlog_handlers_upstream.py's repositories),
each made once the repository is in git."""
import sys

F = sys.modules["shop_world_four"]
four, parts = F.four, F.parts
W = sys.modules["shop_work_queue_world"]

BOTH = ("backlog", "batches")



def _module(stem):
    """A handler module of the glob, by its file's stem."""
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and m.__file__.endswith("/%s.py" % stem))


def _remote(step, condition):
    remote = _module("backlog_handlers_remote")
    name = parts(step)[0][1]
    step.context.setdefault("remotes", {})[name] = remote.PRE_RECEIVE[condition]
    if condition == "silent":
        step.request.getfixturevalue("monkeypatch").setenv("SHOPSYSTEM_PUSH_TIMEOUT", str(remote.TIMEOUT))
    step.request.node._shop_unpushable = True


@four("GivenDoes", "reject", *BOTH)
def rejects(step):
    _remote(step, "unpushable")


@four("GivenDoesNot", "answer", *BOTH)
def answers_not(step):
    _remote(step, "silent")


@four("GivenK", "git branch", *BOTH)
def given_branch(step):
    step.context.setdefault("git_branches", {}).setdefault(step.names[0], {})


@four("GivenDoes", "has", *BOTH)
def branch_has(step):
    """A task's git branch, a git branch's upstream branch, a branch name: recorded for the check out."""
    (k1, n1), (k2, n2) = parts(step)
    if k1 == "task" and k2 == "git branch":
        step.context["git_branches"][n2]["task"] = n1
    elif k1 == "git branch" and k2 == "upstream branch":
        step.context["git_branches"][n1]["upstream"] = n2
    elif k2 != "branch name":
        return False


@four("GivenDoes", "check out", *BOTH)
def checks_out(step):
    """This repository checks out a task's git branch (`batch-1-b1`, its plan on main) or one that tracks an upstream
    branch of another name (`main` tracking `trunk`); which, the Givens after it say, so it is made before the run."""
    upstream = _module("backlog_handlers_upstream")
    found = step.context["git_branches"][parts(step)[1][1]]

    def made(step):
        if "task" in found:
            upstream.tasked_plan(step)
            W.init(step.repo)
            upstream.task_branch(step)
        else:
            assert "upstream" in found, found
            upstream.track(step)
    step.context.setdefault("before_run", []).append(made)


@four("ThenDoes", "keep", *BOTH)
def keeps(step):
    upstream = _module("backlog_handlers_upstream")
    if parts(step)[1][0] != "upstream branch":
        return False
    upstream.keeps_upstream(step)
