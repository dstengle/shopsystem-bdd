"""Handlers of features/intake.feature (plan 3, Tasks 3 and 4) and of `work outcome accepted` in
features/requests.feature (r38): `work outcome` run with no input on the requests world_nodes.py and readiness_world.py
write, each on its issue (requests_world.py), and the items backlog_world.py writes. The steps whose key
another capability claims reach these through work_queue_world's `local` table, so test_intake.py binds with
`bind_all`; each returns False for a step that is not about intake, which then goes on to the registry."""
import importlib.util
import re
import sys
from pathlib import Path

import request_text
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
Q = shared("shop_requests_world", "requests_world.py")
local = W.local
B.OF_GIVENS["request line"] = lambda step: R.link_request(step, *step.names)


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


@local("ThenExitsErr", "request line")
def refused_naming_line(step):
    """Exit 1 (not a usage error), naming the line as `work` names it: `line <n> of request q<m>`."""
    done = step.context["result"]
    assert done.returncode == 1, (done.returncode, done.stdout, done.stderr)
    said = step.context["says"][step.names[0]]
    assert said in done.stderr, (said, done.stderr)


# What each word of `work outcome` is run with (D12).
OPTIONS = {"accepted": ["--into", "work-queue"], "rewritten": ["--line", R.COUNTER],
           "refused": ["--reason", "Out of this context's scope"]}


@handler("WhenRuns", "`work outcome accepted`")
@handler("WhenRuns", "`work outcome rewritten`")
@handler("WhenRuns", "`work outcome refused`")
def work_outcome(step):
    """`work outcome q<n> <k> <word>` on the line a Given placed, with the word's option, over the codified spec (the
    accepted line goes into one of its capabilities, a counter-proposal parses in its grammar). A line no Given placed
    in a request is line 1 of the world's request q9, in the words a Given said it has; the request is on its issue.
    An option a Given made absent, or the step runs it without (`--reason`), is left out."""
    if step.names[-1] not in step.context.get("line_of", {}):
        R.write_request(step)
        step.context.setdefault("line_of", {})[step.names[-1]] = (R.REQUEST, 1)
        said = step.context.get("says", {}).get(step.names[-1])
        if said and step.context.get("unparsed"):
            path = step.repo / W.node_rel(step.context, R.REQUEST)
            path.write_text(path.read_text().replace("1. %s\n" % R.PASSING, "1. %s\n" % said, 1))
    request, number = step.context["line_of"][step.names[-1]]
    word = step.term.strip("`").split()[-1]
    R.codify(step)
    path = step.repo / W.node_rel(step.context, request)
    Q.with_issue(step, path)
    step.context["before"] = {"status": W.field(path, "status"), "side": W.field(path, "turn")}
    gone = set(step.context.get("absent", ())) | {o.strip("`") for o in getattr(step, "without", None) or ()}
    options = OPTIONS[word] if OPTIONS[word][0] not in gone else []
    B.run_work(step, "outcome", request, str(number), word, *options, env=Q.env(step), **R.NO_INPUT)


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
    got = request_text.entries(path.read_text(), "Outcomes")
    has = "%d. %s" % (number, step.values[0].strip("`")) in got
    assert (not has) if " is not " in step.text else has, (step.text, got)


@local("ThenDoes", "request line")
def writes_line(step):
    """The request's `## Lines` gained an entry in the last run; the name is bound to its number."""
    if step.term != "write" or not step.context.get("line_of"):
        return False
    path, _ = request_of(step, next(iter(step.context["line_of"])))
    rel = path.relative_to(step.repo).as_posix()
    assert rel in W.runs(step)[-1]["changed"], (step.text, W.runs(step)[-1]["changed"])
    had = request_text.entries(W.git(step.repo, "show", "%s:%s" % (step.context["head"], rel)), "Lines")
    now = request_text.entries(path.read_text(), "Lines")
    assert len(now) == len(had) + 1, (step.text, had, now)
    step.context["line_of"][step.names[0]] = (step.context["line_of"][next(iter(step.context["line_of"]))][0],
                                              int(now[-1].split(".", 1)[0]))


@local("ThenDoes", "reason")
def writes_reason(step):
    """The last run wrote the line's reason under its request's `## Reasons`, where there was none before."""
    if step.term != "write" or not step.context.get("line_of"):
        return False
    path, number = request_of(step, next(iter(step.context["line_of"])))
    rel = path.relative_to(step.repo).as_posix()
    assert rel in W.runs(step)[-1]["changed"], (step.text, W.runs(step)[-1]["changed"])
    had = request_text.entries(W.git(step.repo, "show", "%s:%s" % (step.context["head"], rel)), "Reasons")
    now = request_text.entries(path.read_text(), "Reasons")
    said = "%d. %s" % (number, OPTIONS["refused"][1])
    assert said not in had and said in now, (step.text, had, now)


# Grammar 4 (b240 phase 15): the rows and verbs of the codified-2 feature, each a `local` handler that returns False
# for a step that is not about intake.

@local("GivenK_A", "request line")
def line_is_not(step):
    """`the request line r1 is not `accepted``: the line has no outcome when it had that one; "is v" is requests'."""
    if " is not " not in step.text:
        return False
    lines = step.context.setdefault("lines", {})
    if lines.get(step.names[0]) == step.values[0].strip("`"):
        lines[step.names[0]] = None
        if step.names[0] in step.context.get("line_of", {}):
            R.write_request(step, None)


@local("GivenDoes")
def has_line(step):
    """`the item i1 has the request line r1`: the line of the item's request (R.link_request); `the request r2 has
    the request line r1`: line 1 of the world's request q9, the request r2 its file."""
    if step.term != "has" or not step.text.startswith(("the item ", "the request ")) \
            or " has the request line " not in step.text:
        return False
    owner, line = step.names
    if step.text.startswith("the item "):
        return R.link_request(step, line, owner)
    R.write_request(step, step.context.get("lines", {}).get(line))
    step.context.setdefault("line_of", {})[line] = (R.REQUEST, 1)
    step.context["nodes"][owner] = step.context["nodes"][R.REQUEST]


def last_request(step):
    return request_of(step, next(iter(step.context["line_of"])))


@local("ThenDoes")
def sets_line(step):
    """`work` sets the line outcome of the request line r1 to v (its `## Outcomes` entry), the side of the request r2
    to v (its `turn:`)."""
    if step.term != "set" or not step.context.get("line_of"):
        return False
    value = step.values[0].strip("`")
    if step.nps[0].startswith("the side of "):
        path, _ = last_request(step)
        assert W.field(path, "turn") == value, (step.text, W.field(path, "turn"))
        return None
    path, number = request_of(step, step.names[0])
    got = request_text.entries(path.read_text(), "Outcomes")
    assert "%d. %s" % (number, value) in got, (step.text, got)


@local("ThenDoes")
def request_has_line(step):
    """`the request r2 has the request line r3`: the request's `## Lines` gained an entry, which r3 names."""
    if step.term != "has" or " has the request line " not in step.text or not step.context.get("line_of"):
        return False
    path, _ = last_request(step)
    rel = path.relative_to(step.repo).as_posix()
    had = request_text.entries(W.git(step.repo, "show", "%s:%s" % (step.context["head"], rel)), "Lines")
    now = request_text.entries(path.read_text(), "Lines")
    assert len(now) == len(had) + 1, (step.text, had, now)
    step.context["line_of"][step.names[1]] = (step.context["line_of"][next(iter(step.context["line_of"]))][0],
                                              int(now[-1].split(".", 1)[0]))


@handler("ThenDoes", "counter")
def counters(step):
    """`the request line r3 counters the request line r1`: `<n>. <m>` under the request's `## Counter-proposals`."""
    new, old = (request_of(step, n) for n in step.names)
    got = request_text.entries(new[0].read_text(), "Counter-proposals")
    assert "%d. %d" % (old[1], new[1]) in got, (step.text, got)


@local("ThenDoes")
def reason_for(step):
    """`the reason r3 is for the request line r1`: the line's entry under its request's `## Reasons`, new in the
    last run; the comment c1 `is on the request r2`: what `work posts the comment c1` reads."""
    if step.term == "on" and step.text.startswith("the comment "):
        return None
    if step.term != "for" or not step.context.get("line_of"):
        return False
    path, number = request_of(step, step.names[1])
    rel = path.relative_to(step.repo).as_posix()
    had = request_text.entries(W.git(step.repo, "show", "%s:%s" % (step.context["head"], rel)), "Reasons")
    now = request_text.entries(path.read_text(), "Reasons")
    said = "%d. %s" % (number, OPTIONS["refused"][1])
    assert said not in had and said in now, (step.text, had, now)
    step.context["reason_of"] = path


@local("ThenDoes")
def writes_in_request(step):
    """`work` writes the request line r3 (the reason r3): the last run changed the request that holds it."""
    if step.term != "write" or not step.context.get("line_of") or not re.match(r"the (request line|reason) ", step.nps[0]):
        return False
    path, _ = last_request(step)
    assert path.relative_to(step.repo).as_posix() in W.runs(step)[-1]["changed"], (step.text, W.runs(step)[-1])
