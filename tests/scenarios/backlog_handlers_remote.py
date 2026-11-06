"""Handlers of features/backlog.feature's remote (b51, r18; b56, r19): a remote the scenario gives, which
backlog_world.py adds to the repository as `main`'s upstream remote once it is in git with the pre-receive hook given
here: one that refuses every push, and a silent one, whose hook sleeps longer than the push's timeout (bounded, so a
push with no timeout still ends). Under either the scenario is not checked against U4 (vocab.py), which such a remote
cannot keep."""
import sys

from vocab import handler

local = sys.modules["shop_work_queue_world"].local

TIMEOUT = 2      # seconds a push waits under a silent remote ($SHOPSYSTEM_PUSH_TIMEOUT)
SILENCE = 20     # seconds a silent remote's hook sleeps: past the timeout, never forever


@handler("GivenK", "remote")
def given_remote(step):
    step.context.setdefault("remotes", {}).setdefault(step.names[0], None)


PRE_RECEIVE = {
    "unpushable": "#!/bin/sh\necho 'this remote takes no push' >&2\nexit 1\n",
    "silent": "#!/bin/sh\nsleep %d\nexit 0\n" % SILENCE,
}


@handler("GivenK_C", "remote")
def given_condition(step):
    """An unpushable remote refuses every push; a silent one answers none within the push's timeout, set short."""
    condition = step.text.rsplit(" is ", 1)[-1]
    assert condition in PRE_RECEIVE, step.text
    step.context.setdefault("remotes", {})[step.names[0]] = PRE_RECEIVE[condition]
    if condition == "silent":
        step.request.getfixturevalue("monkeypatch").setenv("SHOPSYSTEM_PUSH_TIMEOUT", str(TIMEOUT))
    step.request.node._shop_unpushable = True


@local("ThenPrints", "remote")
def prints_remote(step):
    """The run succeeded and said, beside what it prints, that its commit is not pushed to the remote, by the
    remote's name and git's reason."""
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    said = done.stdout + done.stderr
    assert "not pushed: %s: " % step.names[0] in said, (step.text, said)
