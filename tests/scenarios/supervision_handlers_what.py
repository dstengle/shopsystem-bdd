"""Handlers of features/supervision.feature (design §14.3), the Thens on how `work run` exited, what it printed and
that a refused run changed nothing."""
import re
import sys

from vocab import handler

W, B, P = (sys.modules["shop_supervision_" + n] for n in ("world", "build", "plans"))


def where(step):
    done = step.context.get("result")
    return (done.returncode, done.stdout[-3000:], done.stderr[-3000:]) if done else "no run"


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
