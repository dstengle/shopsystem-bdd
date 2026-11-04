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


# What each word of `work outcome` is run with (D12).
OPTIONS = {"accepted": ["--into", "work-queue"], "refused": ["--reason", "out of scope"],
           "rewritten": ["--line", R.COUNTER]}


@handler("WhenRuns", "`work outcome accepted`")
@handler("WhenRuns", "`work outcome refused`")
@handler("WhenRuns", "`work outcome rewritten`")
def work_outcome(step):
    """`work outcome q<n> <k> <word>` on the line a Given placed, with the word's option, over the codified spec (the
    accepted line goes into one of its capabilities, a counter-proposal parses in its grammar)."""
    request, number = step.context["line_of"][step.names[-1]]
    word = step.term.strip("`").split()[-1]
    R.codify(step)
    path = step.repo / W.node_rel(step.context, request)
    step.context["before"] = {"status": W.field(path, "status"), "side": W.field(path, "turn")}
    step.context["reason_text"] = "out of scope" if word == "refused" else None
    B.run_work(step, "outcome", request, str(number), word, *OPTIONS[word], **R.NO_INPUT)


@local("GivenR", "request line")
def proposed_in(step):
    """`the request line r1 is proposed in the request q1`: the line is line 1 of q1; requests' handler runs too."""
    if step.term == "proposed in":
        step.context.setdefault("line_of", {})[step.names[0]] = (step.names[1], 1)
    return False


def request_of(step, line):
    request, number = step.context["line_of"][line]
    return step.repo / W.node_rel(step.context, request), number


@handler("ThenK_A", "request line")
def line_outcome(step):
    """The request's `## Outcomes` entry for the line's number is (is not) the value."""
    path, number = request_of(step, step.names[0])
    got = workqueue_request._entries(path.read_text(), "Outcomes")
    has = "%d. %s" % (number, step.values[0].strip("`")) in got
    assert (not has) if " is not " in step.text else has, (step.text, got)


@local("ThenDoes", "reason")
def writes_reason(step):
    """A file the last run changed holds the reason the run gave."""
    said = step.context.get("reason_text")
    if step.term != "write" or not said:
        return False
    hits = [rel for rel in W.runs(step)[-1]["changed"] if said in (step.repo / rel).read_text()]
    assert hits, (step.text, said, W.runs(step)[-1]["changed"])


@local("ThenDoes", "request line")
def writes_line(step):
    """The request's `## Lines` gained an entry in the last run; the name is bound to its number."""
    if step.term != "write" or not step.context.get("line_of"):
        return False
    path, _ = request_of(step, next(iter(step.context["line_of"])))
    rel = path.relative_to(step.repo).as_posix()
    assert rel in W.runs(step)[-1]["changed"], (step.text, W.runs(step)[-1]["changed"])
    had = workqueue_request._entries(W.git(step.repo, "show", "%s:%s" % (step.context["head"], rel)), "Lines")
    now = workqueue_request._entries(path.read_text(), "Lines")
    assert len(now) == len(had) + 1, (step.text, had, now)
    step.context["line_of"][step.names[0]] = (step.context["line_of"][next(iter(step.context["line_of"]))][0],
                                              int(now[-1].split(".", 1)[0]))
