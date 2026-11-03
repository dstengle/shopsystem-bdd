"""Handlers of features/supervision.feature (design §14.3), the Thens on what `work run` committed and pushed, how it
exited, what it printed and that a refused run changed nothing."""
import re
import sys

from vocab import handler

W, B, P = (sys.modules["shop_supervision_" + n] for n in ("world", "build", "plans"))


def where(step):
    done = step.context.get("result")
    return (done.returncode, done.stdout[-3000:], done.stderr[-3000:]) if done else "no run"


def tracked(step, pattern):
    return [p for p in W.git(step.repo, "ls-files").splitlines() if re.search(pattern, p)]


def pushed(step):
    """The remote has the initiative branch's head, unless the scenario's remote refuses every push."""
    if "unpushable" in W.sv(step.context)["conds"].get("remote", set()):
        return True
    return W.git(W.remote_dir(step.repo), "rev-parse", "main").strip() == W.git(step.repo, "rev-parse", "main").strip()


COMMITTED = {"transition": r"^\.shop/work/i1/log\.jsonl$", "`branch review` stage": r"^\.shop/work/i1/runs/branch-review/\d+/",
             "measurement": r"^\.shop/records/measurements/.*i1", "draft": r"^\.shop/work/i1/runs/i1/\d+-integrate/drafts/",
             "feature": r"^features/work-queue\.feature$", "stage": r"^\.shop/work/i1/runs/w1/\d+-answer/"}


@handler("ThenCommits", "`work run`")
def then_commits(step):
    np = step.nps[-1]
    stage = re.fullmatch(r"the stage (s\d+)", np)
    if stage:     # a stage instance: by the kind its Givens or the Thens before gave it
        sv = W.sv(step.context)
        np = "the `%s` stage" % (sv["stages"].get(stage.group(1)) or sv.get("new", {}).get(stage.group(1), {}).get("kind"))
    if np.startswith("the initiative"):
        assert "\nstatus: done\n" in W.git(step.repo, "show", "main:.shop/work/i1/initiative.md"), where(step)
    else:
        key = next(k for k in COMMITTED if k in np)
        assert tracked(step, COMMITTED[key]), (np, W.git(step.repo, "ls-files"), where(step))
    if np.startswith("the transition"):
        moves = [l for l in W.log_lines(step.repo) if "after" in l]
        made = [s for s in W.git(step.repo, "log", "--format=%s", "main").splitlines() if s.startswith("work: ")]
        assert moves and len(made) >= len(moves), (moves, made)
    assert pushed(step), where(step)
    assert not W.git(step.repo, "status", "--porcelain", "--", ".shop/work").strip(), where(step)


def named(step, np):
    """The words an error naming `np` holds."""
    sv = W.sv(step.context)
    name = re.search(r"\b([a-z][a-z-]*\d+)$", np)
    if np.startswith("the stage"):
        return [sv["stages"][name.group(1)]]
    if np.startswith("the remote"):
        return ["push"]
    if np.startswith("the capability"):
        return ["nowhere"] if "strange" in sv["conds"].get("result", set()) else ["thing"]
    if np.startswith("the file"):
        return [np.split("`")[1]] if "`" in np else [name.group(1)]
    if np.startswith("the worker"):
        return ["worker"]
    if np.startswith("the reason"):
        return []
    return [name.group(1)] if name else []


@handler("ThenExitsErr", "`work run`")
def then_exits_err(step):
    done = step.context["result"]
    assert done.returncode != 0, where(step)
    assert "Traceback" not in done.stderr, done.stderr
    for word in named(step, step.nps[-1]):
        assert word in done.stdout + done.stderr, (word, where(step))


@handler("ThenExitsOk", "`work run`")
def then_exits_ok(step):
    assert step.context["result"].returncode == 0, where(step)


@handler("ThenPrints", "`work run`")
def then_prints(step):
    out = step.context["result"].stdout.splitlines()
    for np in step.nps:
        name = re.search(r"\b([a-z][a-z-]*\d+)$", np).group(1)
        status = W.field((step.repo / step.context["nodes"][name][1]).read_text(), "status")
        assert any(name in l.split() and status in l.split() for l in out), (name, status, out)


@handler("ThenChangesNothing", "`work run`")
def then_changes_nothing(step):
    assert W.state(step.repo) == step.context["before"], where(step)
