"""features/requests.feature's steps about the same work commands taking every request through one lifecycle (requests r25):
the asker ctx-a, the product level p1 and the upstream ctx-u each raise a request, and a table of steps takes each one through
the lines of work, each step run in the repository of the side that does it."""
import re
import shlex

from pytest_bdd import given, parsers, then, when

from . import requests_world_steps as world
from .requests_world_steps import GOOD, home

REQUESTERS = ["ctx-a", "p1", "ctx-u"]
COMMANDS = {"request", "take-in", "ask", "turn", "reply", "outcome", "resolve", "show"}


@given("a file lines.md with one line in strict EARS in each of the repositories of the asker ctx-a, the product level p1 "
       "and the upstream ctx-u")
def a_line_in_each_repository(repo, context):
    for name in ("ctx-a", "p1"):
        world.asker_repo(repo, context, name)
    for path in (repo, *context["askers"].values()):
        (path / "lines.md").write_text(GOOD[0] + "\n")


def argv_of(step, name, request):
    """The `work` arguments of a step of the table, `name` being the requester and `request` the name of its request."""
    if step.startswith("takes in"):
        return ["take-in"]
    asks = re.fullmatch(r'asks the question "(.*)" on line (\d+) of the request', step)
    if asks:
        return ["ask", request, asks.group(2), asks.group(1)]
    answers = re.fullmatch(r'answers that question with "(.*)" in its own repository', step)
    if answers:
        return ["reply", request, "1", answers.group(1)]
    runs = re.fullmatch(r"runs `work (.+?)`(, giving .*)?(?: in its own repository)?", step)
    argv = shlex.split(runs.group(1).replace("<its asker>", name).replace("<the request>", request or ""))
    if runs.group(2):
        version = runs.group(2).rsplit("version ", 1)[1]
        for ident, line in re.findall(r"(\S+#r\d+) for line (\d+)", runs.group(2)):
            argv += ["--line", line, ident, version]
    return argv


@when("the asker ctx-a, the product level p1 and the upstream ctx-u each raise a request of their own, and each request is "
      "taken through these steps, each step run as the same work command for every request")
def each_request_through_the_steps(repo, run, context, datatable):
    context["flow"] = {}
    for name in REQUESTERS:
        trail, codes, commands, request, out = [], [], [], None, None
        for side, step in datatable[1:]:
            path = home(repo, context) if side == "upstream" or name == "ctx-u" else context["askers"][name]
            argv = argv_of(step, name, request)
            done = run("work", *argv, cwd=path)
            codes.append(done.returncode)
            commands.append(argv[0])
            out = done.stdout
            if argv[0] == "request":
                request = done.stdout.strip()
            text = world.local_text(repo, context, request) if request else None
            if text:
                state = tuple(re.search(r"(?m)^%s: (.*)$" % f, text).group(1) for f in ("status", "turn"))
                if not trail or trail[-1][0] != state[0]:
                    trail.append(state)
            assert done.returncode == 0, (name, step, done)
        context["flow"][name] = {"codes": codes, "commands": commands, "trail": trail, "request": request, "shown": out}


@then("each step exits successfully for each of the three requests")
def each_step_succeeds(context):
    assert all(code == 0 for flow in context["flow"].values() for code in flow["codes"]), context["flow"]


@then("each step was done by one command of work's set, the same command for the three requests")
def same_command(context):
    by_request = [flow["commands"] for flow in context["flow"].values()]
    assert by_request[0] == by_request[1] == by_request[2] and set(by_request[0]) <= COMMANDS, by_request


@then(parsers.parse("each of the three requests' status went {words}, in that order"))
def statuses_went(context, words):
    assert [f["trail"] for f in context["flow"].values()]
    for flow in context["flow"].values():
        assert [s for s, _ in flow["trail"]] == words.split(", "), flow["trail"]


@then(parsers.parse("each of the three requests' turn went {words}, in that order"))
def turns_went(context, words):
    for flow in context["flow"].values():
        assert [t for _, t in flow["trail"]] == [w.removeprefix("the ").removesuffix("'s") for w in words.split(", ")], flow["trail"]


@then("for each of the three requests, work show <the request> prints that request with delivered and the asker's turn")
def show_prints_delivered(context):
    for flow in context["flow"].values():
        assert re.search(r"(?m)^%s delivered asker$" % flow["request"], flow["shown"]), flow["shown"]
