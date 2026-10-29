"""features/requests.feature's steps about a request kept as .shop/work/requests/<id>.md (requests r8 to r12).

A Given writes the request in the file form of the capability's Implementation section; a When runs `work`; the Thens
read the request's file back.
"""
import re
import shlex

from pytest_bdd import given, parsers, then, when

from .conftest import full
from .work_queue_git_steps import init

COUNTS = {"one": 1, "two": 2, "three": 3}


def request_rel(ident):
    return ".shop/work/requests/%s.md" % ident


def sections(repo, ident):
    """The request's `## <name>` sections, each as its list of entry lines."""
    text = (repo / request_rel(ident)).read_text()
    return {name: [line for line in body.splitlines() if line.strip()]
            for name, body in re.findall(r"(?ms)^## (\w+)\n(.*?)(?=^## |\Z)", text)}


def status_of(repo, ident):
    return re.search(r"(?m)^status: (.*)$", (repo / request_rel(ident)).read_text()).group(1)


def write_request(repo, context, ident, asker, status, turn, count, given):
    """Write the request in the file form, `given` being its line outcomes in order; keep its text as written."""
    lines = "".join("%d. line %d\n" % (n, n) for n in range(1, COUNTS[count] + 1))
    kept = "".join("%d. %s\n" % (n, word) for n, word in enumerate(given, 1))
    init(repo)     # the request commands commit what they change (r12)
    path = repo / request_rel(ident)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nid: %s\nkind: request\nasker: %s\nstatus: %s\nturn: %s\n---\n\n# %s\n\n## Lines\n%s\n"
                    "## Outcomes\n%s\n## Resolution\n" % (full("request", ident), asker, status or "open", turn, ident, lines, kept))
    context["written"] = path.read_text()


@given(parsers.re(r"a request (?P<ident>q\d+) from the asker (?P<asker>\S+)(?: whose status is (?P<status>[\w-]+) and)?"
                  r" whose turn is the (?P<turn>asker|upstream)'s, with (?P<count>one|two|three) lines? (?P<outcomes>.+)"))
def a_request(repo, context, ident, asker, status, turn, count, outcomes):
    given = [] if re.fullmatch(r"that (has|have) no line outcomes?", outcomes) else \
        re.split(r", | and ", outcomes.split(" are ")[-1].split(" is ")[-1])
    write_request(repo, context, ident, asker, status, turn, count, given)


@given(parsers.re(r"a request (?P<ident>q\d+) from the asker (?P<asker>\S+) whose turn is the (?P<turn>asker|upstream)'s,"
                  r" with two lines, line 1 with the line outcome (?P<first>\w+) and line 2 with (?P<second>.+)"))
def a_request_with_a_line_each(repo, context, ident, asker, turn, first, second):
    word = None if second == "no line outcome" else second.removeprefix("the line outcome ")
    write_request(repo, context, ident, asker, None, turn, "two", [first] + ([word] if word else []))


@when(parsers.re(r"the upstream runs `work (?P<args>[^`]+)`(?P<giving>, giving .*)?"))
def the_upstream_runs(repo, run, context, args, giving):
    argv = shlex.split(args)
    if giving and "the delegation" in giving:
        ident, text = re.fullmatch(r', giving (q\d+) and the delegation "(.*)"', giving).groups()
        argv += [ident, text]
    elif giving:
        version = giving.rsplit("version ", 1)[1]
        for ident, line in re.findall(r"(\S+#r\d+) for line (\d+)", giving):
            argv += ["--line", line, ident, version]
    context["done"] = run("work", *argv)


@then(parsers.parse("{ident}'s status is {status}"))
def status_is(repo, ident, status):
    actual = status_of(repo, ident)
    if status == "not accepted":
        assert actual != "accepted"
    else:
        assert actual == status


@then(parsers.re(r"(?P<ident>q\d+)'s resolution gives (?P<gives>.+), each found in (?P<version>\S+)"))
def resolution_gives(repo, ident, gives, version):
    expected = {n: "%s %s" % (req, version) for n, req in re.findall(r"line (\d+) (\S+?)(?: and |$)", gives)}
    kept = dict(entry.split(". ", 1) for entry in sections(repo, ident)["Resolution"])
    assert {k: kept.get(k) for k in expected} == expected, kept


@then(parsers.parse("it gives line {n} nothing"))
def gives_nothing(repo, n):
    assert n not in dict(entry.split(". ", 1) for entry in sections(repo, "q1")["Resolution"])


@then(parsers.parse("{ident} gives line {n} no line outcome"))
def gives_no_outcome(repo, ident, n):
    assert n not in dict(entry.split(". ", 1) for entry in sections(repo, ident)["Outcomes"])


@then(parsers.re(r"(?P<ident>q\d+)'s turn is the (?P<side>asker|upstream)'s"))
def turn_is(repo, ident, side):
    assert re.search(r"(?m)^turn: (.*)$", (repo / request_rel(ident)).read_text()).group(1) == side


@then("the command is refused because it is the asker's turn")
def refused_asker_turn(context):
    assert "asker's turn" in context["done"].stderr, context["done"]


@then(parsers.parse("{ident} is as it was"))
def as_it_was(repo, context, ident):
    assert (repo / request_rel(ident)).read_text() == context["written"]


@then("it exits successfully")
def exits_successfully(context):
    assert context["done"].returncode == 0, context["done"]
