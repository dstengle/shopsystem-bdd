"""features/requests.feature's steps of `work show` and `work status` (requests r13, r14): requests with a status and a
turn, dated observations, and what the two commands print."""
import re

from pytest_bdd import given, parsers, then, when

from .conftest import full


@given(parsers.re(r"a request (?P<ident>q\d+) from the asker (?P<asker>\S+) whose status is (?P<status>[\w-]+)"
                  r" and whose turn is the (?P<turn>asker|upstream)'s"))
def request_with_turn(repo, ident, asker, status, turn):
    path = repo / ".shop/work/requests" / (ident + ".md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nid: %s\nkind: request\nasker: %s\nstatus: %s\nturn: %s\n---\n\n# %s\n"
                    % (full("request", ident), asker, status, turn, ident))


@given(parsers.re(r"a request (?P<ident>q\d+) from the asker (?P<asker>\S+) whose origin is (?P<origin>o\d+)"))
def request_with_origin(repo, ident, asker, origin):
    path = repo / ".shop/work/requests" / (ident + ".md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nid: %s\nkind: request\nasker: %s\nsource: observation/%s\nstatus: open\nturn: upstream\n---\n\n# %s\n"
                    % (full("request", ident), asker, origin, ident))


@given(parsers.parse("observations o1, o2 and o3, each with its date"))
def observations(repo):
    path = repo / ".shop/records/observations.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Observations\n\n" + "".join(
        "## %s\nabout: %s\nby: someone\ndate: 2026-10-%02d\n\nSeen.\n\n" % (full("observation", "o%d" % n), "x", 10 + n)
        for n in (1, 2, 3)))


@given(parsers.re(r"an initiative (?P<ident>i\d+) under \.shop/work/ that is neither done nor abandoned, whose source is (?P<origin>o\d+)"))
def initiative_with_source(repo, ident, origin):
    path = repo / ".shop/work" / ident / "initiative.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nid: %s\nkind: initiative\nsource: [%s]\nstatus: started\n---\n"
                    % (full("initiative", ident), full("observation", origin)))


@when("the session runs `work show`")
def runs_show(run, context):
    context["done"] = run("work", "show")


@when("the session runs `work list`")
def runs_list(run, context):
    context["done"] = run("work", "list")


@then(parsers.re(r"work prints (?P<ident>q\d+) with (?P<status>[\w-]+) and the (?P<turn>asker|upstream)'s turn"))
def prints_request(context, ident, status, turn):
    assert any(re.search(r"\b%s\b" % ident, l) and status in l.split() and turn in l.split()
               for l in context["done"].stdout.splitlines()), context["done"].stdout


@then(parsers.re(r"it prints (?P<ident>q\d+) with (?P<status>[\w-]+) and the (?P<turn>asker|upstream)'s turn"))
def it_prints_request(context, ident, status, turn):
    prints_request(context, ident, status, turn)


@then("work prints o3 with its date")
def prints_o3(context):
    assert any(re.search(r"\bo3\b", l) and "2026-10-13" in l for l in context["done"].stdout.splitlines()), context["done"].stdout


@then("it gives neither o1 nor o2 as an observation nothing names")
def neither(context):
    assert not re.search(r"\bo[12]\b", context["done"].stdout), context["done"].stdout
