"""Handlers of features/backlog.feature's remote (b51, r18): a remote the scenario gives, which backlog_world.py adds
to the repository as `main`'s upstream remote once it is in git, and one that refuses every push. Under an unpushable
remote the scenario is not checked against U4 (vocab.py), which such a remote cannot keep."""
import sys

from vocab import handler

local = sys.modules["shop_work_queue_world"].local


@handler("GivenK", "remote")
def given_remote(step):
    step.context.setdefault("remotes", {}).setdefault(step.names[0], False)


@handler("GivenK_C", "remote")
def given_unpushable(step):
    assert step.text.endswith(" is unpushable"), step.text
    step.context.setdefault("remotes", {})[step.names[0]] = True
    step.request.node._shop_unpushable = True


@local("ThenPrints", "remote")
def prints_remote(step):
    """The run succeeded and said, beside what it prints, that its commit is not pushed to the remote, by the
    remote's name and git's reason."""
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    said = done.stdout + done.stderr
    assert "not pushed: %s: " % step.names[0] in said, (step.text, said)
