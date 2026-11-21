"""Handlers of the virtual environment a batch's tests run by (b449, batches r77, reviews r6): "the worktree w1 holds
the virtual environment v1", a task's workspace (its worktree) or the batch's (the checkout the batch is run from)
holding `.venv/bin/python`, ignored by git. `.shop/delivery.toml` names no `[batch] tests`, so `work` runs its
default `python3 -m pytest ...`; the virtual environment's python is a stand-in that runs that pytest with a test
that passes (the scenario that succeeds in the workspace, or one of its own), while `python3` on PATH, run in the
world's repository with no tests, does not pass."""
import shlex
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts


@four("GivenDoes", "holds", "backlog", "batches")
def holds_venv(step):
    (k1, workspace), (k2, _) = parts(step)
    if k1 != "worktree" or k2 != "virtual environment":
        return False
    step.context["venv"] = workspace
    step.context["delivery"] = ""


@four("GivenK", "virtual environment", "backlog", "batches")
def given_venv(step):
    """The virtual environment, made where a workspace holds it."""


def place(step):
    """The directory of the workspace that holds the virtual environment: its task's worktree, else the checkout."""
    task = step.context.get("git_branches", {}).get(step.context["venv"], {}).get("task")
    if task is None:
        return step.repo
    found = step.context["given"]["task"][task]
    return step.repo / ".shop" / "worktrees" / ("%s-%s" % (T.batch_name(step, found["batch"]), T.task_id(step, task)))


def make_venv(step):
    if "venv" not in step.context:
        return
    test = T.outside(step) / "passing" / "test_passing.py"
    if not step.context.get("passing"):
        test = T.outside(step) / "venv" / "test_venv.py"
        test.parent.mkdir(exist_ok=True)
        test.write_text("def test_venv():\n    pass\n")
    python = place(step) / ".venv" / "bin" / "python"
    python.parent.mkdir(parents=True, exist_ok=True)
    python.write_text('#!/bin/sh\nexec %s "$@" -p no:cacheprovider %s\n' % (shlex.quote(sys.executable),
                                                                            shlex.quote(str(test))))
    python.chmod(0o755)
    exclude = step.repo / ".git" / "info" / "exclude"
    exclude.parent.mkdir(exist_ok=True)
    with exclude.open("a") as out:
        out.write("/.venv/\n")


T.BEFORE_RUN.append(make_venv)
