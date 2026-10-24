"""features/work-queue.feature's steps of `work start` (r22) and of an initiative's done (r23): the requests kept under
.shop/work/requests/ that the Givens write, and the Thens that read the new initiative."""
import re

from pytest_bdd import given, parsers, then

from .conftest import full


def request_text(status, asker="internal", origin="part_of: initiative/x"):
    return ("---\nid: %s\nkind: request\nasker: %s\n%s\nstatus: %s\nturn: upstream\n---\n\n# Show the queue\n\n## Lines\n"
            "1. The system shall show the queue.\n" % (full("request", "q1"), asker, origin, status))


@given(parsers.parse("a request q1 that is accepted, whose origins are {first} and {second}"))
def accepted_request(repo, first, second):
    from .test_work_queue import write
    write(repo, ".shop/work/requests/q1.md", request_text("accepted", origin="source: [%s, %s]" % (first, second)))


@given(parsers.parse("a request q1 kept in this context, whose asker is {asker}, names {ident} and is {status}"))
def kept_request(repo, asker, ident, status):
    from .test_work_queue import write
    who = "internal" if asker == "this context" else "missingmass.io/shopsystem/other"
    write(repo, ".shop/work/requests/q1.md", request_text(status, who, "part_of: " + full("initiative", ident)))


@given("no request kept in this context names i1")
def no_request():
    pass


def new_initiatives(repo, context):
    return sorted(p.parent for p in (repo / ".shop/work").glob("*/initiative.md")
                  if str(p.relative_to(repo)) not in context["before"])


@then(".shop/work/ has one new initiative, its initiative.md a proposed initiative of kind capability-change")
def one_new_initiative(repo, context):
    from .test_work_queue import fields
    found = new_initiatives(repo, context)
    assert len(found) == 1, found
    data = fields(found[0] / "initiative.md")
    assert (data.get("kind"), data.get("status")) == ("capability-change", "proposed"), data
    context["new"] = found[0]


@then("it fulfils q1, and its source is o1 and o2")
def fulfils_q1(context):
    from .test_work_queue import fields
    data = fields(context["new"] / "initiative.md")
    assert data.get("fulfils") == full("request", "q1"), data
    assert re.findall(r"\w+", data.get("source", "")) == ["o1", "o2"], data


@then("work prints that initiative's id")
def prints_new_id(context):
    assert context["done"].stdout.strip() == re.match(r"i\d+", context["new"].name).group(0), context["done"]


@then(".shop/work/i1/ is as it was")
def i1_as_it_was(repo, context):
    now = {k: v for k, v in _files(repo).items() if k.startswith(".shop/work/i1/")}
    assert now == {k: v for k, v in context["before"].items() if k.startswith(".shop/work/i1/")}


def _files(repo):
    from .test_work_queue import snapshot
    return snapshot(repo)
