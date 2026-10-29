"""features/requests.feature's steps of requests r25: three requesters, each raising a request and taking it through the same
`work` commands. The three share one repository (see requests_world_steps); taking in what has been sent runs no command,
as nothing is sent between repositories here."""
import re
import shlex

from pytest_bdd import given, parsers, then, when

from .requests_steps import request_rel, status_of
from .requests_world_steps import run_as
from .requests_write_steps import GOOD

STATUSES = ["open", "awaiting-asker", "awaiting-upstream", "accepted", "delivered"]
WORK_COMMANDS = {"request", "outcome", "ask", "reply", "turn", "resolve", "show"}


@given("a file lines.md with one line in strict EARS in each of the repositories of the asker ctx-a, the product level p1"
       " and the upstream ctx-u")
def one_line(repo):
    (repo / "lines.md").write_text(GOOD[0] + "\n")


def argv_of(step, ident, asker):
    """The `work` arguments a step of the table runs for request `ident` raised by `asker`; None when it runs no command."""
    step = step.replace("<its asker>", asker).replace("<the request>", ident)
    if step.startswith("takes in"):
        return None
    if found := re.fullmatch(r'asks the question "(.+)" on line (\d+) of the request', step):
        return ["ask", ident, found.group(2), found.group(1)]
    if found := re.fullmatch(r'answers that question with "(.+)" in its own repository', step):
        return ["reply", ident, "1", found.group(1)]
    found = re.fullmatch(r"runs `work ([^`]+)`( in its own repository)?(?:, giving (\S+) for line (\d+), found in the version (\S+))?",
                         step)
    argv = shlex.split(found.group(1))
    return argv + ["--line", found.group(4), found.group(3), found.group(5)] if found.group(3) else argv


@when(parsers.re(r"the asker (?P<a>\S+), the product level (?P<p>\S+) and the upstream (?P<u>\S+) each raise a request of their"
                 r" own, and each request is taken through these steps, each step run as the same work command for every request"))
def each_raises(repo, run, context, datatable, a, p, u):
    context["upstream"] = u
    context["trace"] = []
    for who, name in (("the asker %s" % a, a), ("the product level %s" % p, p), ("the upstream %s" % u, u)):
        ident, rows = None, []
        for side, step in datatable[1:]:
            args = argv_of(step, ident or "<the request>", name)
            role = who if side == "asker" else "the upstream %s" % u
            done = run_as(repo, run, context, role, args) if args else None
            if args and args[0] == "request":
                ident = done.stdout.strip()
            rows.append({"command": args[0] if args else None, "code": done.returncode if done else None,
                         "out": done.stdout if done else "", "status": status_of(repo, ident) if ident else None,
                         "turn": turn_of(repo, ident) if ident else None})
        context["trace"].append(rows)


def turn_of(repo, ident):
    return re.search(r"(?m)^turn: (.*)$", (repo / request_rel(ident)).read_text()).group(1)


@then("each step exits successfully for each of the three requests")
def each_exits(context):
    assert all(row["code"] in (None, 0) for rows in context["trace"] for row in rows), context["trace"]


@then("each step was done by one command of work's set, the same command for the three requests")
def each_one_command(context):
    commands = [[row["command"] for row in rows] for rows in context["trace"]]
    assert commands[0] == commands[1] == commands[2], commands
    assert all(command in WORK_COMMANDS | {None} for command in commands[0]), commands


def went(rows):
    """The (status, turn) the request was in after each step, a repeat of the one before left out."""
    found = []
    for row in rows:
        pair = (row["status"], row["turn"])
        if row["status"] and (not found or found[-1] != pair):
            found.append(pair)
    return found


@then(parsers.parse("each of the three requests' status went {order}, in that order"))
def status_went(context, order):
    for rows in context["trace"]:
        assert [status for status, _ in went(rows)] == order.split(", "), rows


@then(parsers.parse("each of the three requests' turn went {order}, in that order"))
def turn_went(context, order):
    for rows in context["trace"]:
        assert ["the %s's" % turn for _, turn in went(rows)] == order.split(", "), rows


@then(parsers.parse("for each of the three requests, work show <the request> prints that request with delivered and the asker's turn"))
def show_prints(context):
    for rows in context["trace"]:
        shown = [row for row in rows if row["command"] == "show"][-1]
        assert shown["out"].splitlines()[0].split()[1:] == ["delivered", "asker"], shown
