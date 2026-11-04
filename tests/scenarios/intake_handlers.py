"""Handlers of features/intake.feature (plan 3, Tasks 3 and 4): `work intake` and `work outcome` run with no input on
the requests world_nodes.py and readiness_world.py write and the items backlog_world.py writes. The steps whose key
another capability claims reach these through work_queue_world's `local` table, so test_intake.py binds with
`bind_all`; each returns False for a step that is not about intake, which then goes on to the registry."""
import importlib.util
import sys
from pathlib import Path

import workqueue_request
from vocab import handler


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
R = shared("shop_readiness_world", "readiness_world.py")
local = W.local
B.OF_GIVENS["request line"] = lambda step: R.link_request(step, *step.names)


@handler("WhenRuns", "`work intake`")
def work_intake(step):
    step.context["taken_in"] = step.names[-1]
    B.run_work(step, "intake", step.names[-1], **R.NO_INPUT)


@local("GivenK_C", "request line")
def given_settled(step):
    """settled: the line's outcome `accepted`; not settled: none. Any other condition (unparsed) is requests'."""
    word = step.text.split(" is ", 1)[1]
    if word not in ("settled", "not settled"):
        return False
    outcome = "accepted" if word == "settled" else None
    step.context.setdefault("lines", {})[step.names[0]] = outcome
    if step.names[0] in step.context.get("line_of", {}):
        R.write_request(step, outcome)


@handler("ThenR", "asked by")
def asked_by(step):
    """The item's `asked_by` is the asker of the request the run took in, and that asker is not this context."""
    item = B.item_file(step, step.names[0])
    request = step.repo / W.node_rel(step.context, step.context["taken_in"])
    asker = W.field(request, "asker")
    assert W.field(item, "asked_by") == asker, (step.text, W.field(item, "asked_by"), asker)
    assert asker not in workqueue_request.own_askers(step.repo) and asker != "internal", (step.text, asker)


@local("ThenExitsErr", "request line")
def refused_naming_line(step):
    """Exit 1 (not a usage error), naming the line as `work` names it: `line <n> of request q<m>`."""
    done = step.context["result"]
    assert done.returncode == 1, (done.returncode, done.stdout, done.stderr)
    said = step.context["says"][step.names[0]]
    assert said in done.stderr, (said, done.stderr)
