"""Handlers of features/backlog.feature's upstream branch and task branch (b57, r20, r21): a repository whose `main`
tracks `trunk` of its remote `origin`, and one whose branch checked out is a task's, `batch-1-b1`, the branch of the
task `t1` of `batch-1` in the plan committed on `main`. Each is made once the repository is in git, before the run
(backlog_world.run_work's `before_run`)."""
import sys

local = sys.modules["shop_work_queue_world"].local
W = sys.modules["shop_work_queue_world"]

TRUNK = "trunk"
TASK_BRANCH = "batch-1-b1"
PLAN = ("---\nid: batch/ex.com/prod/ctx/batch-1\nkind: batch\nstatus: building\nbase: main\nforked_from: %s\n"
        "branch: batch-1\npull_request:\n---\n\n# batch-1\n\n## Tasks\n\n| task | item | status | branch |\n"
        "|---|---|---|---|\n| t1 | b1 | running | %s |\n" % ("0" * 40, TASK_BRANCH))


def track(step):
    """`main` pushed to `trunk` of a bare remote `origin`, and tracking it there."""
    bare_repo = step.request.getfixturevalue("tmp_path_factory").mktemp("upstream") / "origin.git"
    W.git(bare_repo.parent, "init", "-q", "--bare", str(bare_repo))
    W.git(step.repo, "remote", "add", "origin", str(bare_repo))
    W.git(step.repo, "push", "-q", "origin", "main:refs/heads/%s" % TRUNK)
    W.git(step.repo, "config", "branch.main.remote", "origin")
    W.git(step.repo, "config", "branch.main.merge", "refs/heads/%s" % TRUNK)


def task_branch(step):
    W.git(step.repo, "checkout", "-q", "-b", TASK_BRANCH)


def tasked_plan(step):
    path = step.repo / ".shop" / "batches" / "1" / "plan.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(PLAN)


@local("GivenK_C", "repository")
def repository_is(step):
    word = step.text.rsplit(" is ", 1)[1]
    if word == "tracking":
        step.context.setdefault("before_run", []).append(track)
    elif word == "tasked":
        tasked_plan(step)
        step.context.setdefault("before_run", []).append(task_branch)
        step.context.setdefault("task_branches", {})["t1"] = TASK_BRANCH
    else:
        return False


@local("ThenExitsErr", "task")
def refused_naming_task(step):
    """The run exited non-zero, naming the task whose branch the `tasked` Given checked out: its id, its batch and its
    branch."""
    done = step.context["result"]
    assert done.returncode != 0, done.stdout
    said = done.stdout + done.stderr
    branch = step.context["task_branches"][step.names[0]]
    assert "task %s of batch-1" % step.names[0] in said and branch in said, (step.text, said)


@local("ThenDoes", "upstream branch")
def keeps_upstream(step):
    """The upstream branch is the one the `tracking` Given set: `main` still tracks `trunk` of `origin`, and the run's
    commit reached `trunk` there and made no `main` beside it."""
    if step.term != "keep":
        return False
    step.context.setdefault("upstreams", {})[step.names[0]] = TRUNK
    assert W.git(step.repo, "config", "branch.main.remote").strip() == "origin"
    assert W.git(step.repo, "config", "branch.main.merge").strip() == "refs/heads/%s" % TRUNK
    there = W.git(step.repo, "ls-remote", "origin").split("\n")
    heads = {line.split()[1]: line.split()[0] for line in there if line.strip()}
    assert heads.get("refs/heads/%s" % TRUNK) == W.head(step.repo), (heads, W.head(step.repo))
    assert "refs/heads/main" not in heads, heads
