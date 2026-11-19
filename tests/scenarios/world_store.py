"""The store's domain words in the scenarios (the domain contract design, §7 "Domain words for the store's acts"): a
shared store that does not answer or rejects a change, and a store that rejects a change, made as the CLI's
handlers made them before the reword: the remote that does not answer or refuses every push (backlog_handlers_remote),
the repository whose every commit is refused (requests_handlers_commit). "names this shared store": the run said its
change is not shared there, by the remote's name. Each a `local` of its template, passing on any other step."""
import sys

W = sys.modules["shop_work_queue_world"]
SHARED = "r1"       # the remote a shared store is made as


def _module(stem):
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and m.__file__.endswith("/%s.py" % stem))


@W.local("GivenK_A")
def given_store(step):
    value = step.values[0].strip("`") if step.values else None
    if step.attribute == "availability" and step.kind == "shared store":
        remote = _module("backlog_handlers_remote")
        condition = {"unreachable": "silent", "rejecting": "unpushable"}[value]
        step.context.setdefault("remotes", {})[SHARED] = remote.PRE_RECEIVE[condition]
        if condition == "silent":
            step.request.getfixturevalue("monkeypatch").setenv("SHOPSYSTEM_PUSH_TIMEOUT", str(remote.TIMEOUT))
        step.request.node._shop_unpushable = True
    elif step.attribute == "store" and value == "rejecting":
        step.context.setdefault("before_run", []).append(_module("requests_handlers_commit").uncommittable)
    else:
        return False


@W.local("ThenDoes")
def names_shared_store(step):
    if step.term != "name" or step.nps != ["this shared store"]:
        return False
    done = step.context["result"]
    said = done.stdout + done.stderr
    assert "not pushed: %s: " % SHARED in said, (step.text, said)
