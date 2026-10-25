"""features/requests.feature's steps about `work request` (requests r1 to r5): the upstream that takes a request in, the
lines file the asker gives, and what the upstream keeps afterwards."""
import json
import re
import shlex

from pytest_bdd import given, parsers, then, when

from .conftest import INDEX
from .requests_steps import request_rel, sections
from .work_queue_git_steps import init

GOOD = ["The queue shall show each item.", "While idle, when a request arrives, the system shall answer it."]
FAULTS = {
    "is in none of EARS's patterns": "Show the queue to the caller.",
    "puts its When clause before a While clause": "When a request arrives, while idle, the system shall answer it.",
    "has an If clause with no then": "If a request arrives the system shall answer it.",
    "has two shalls": "When a request arrives, the system shall answer and the system shall log it.",
    "has two sentences": "The system shall answer it. Then the system logs it.",
}


def kept(repo):
    return sorted((repo / ".shop" / "work" / "requests").glob("q*.md"))


@given("an upstream that keeps no request")
def upstream_keeps_none(repo):
    (repo / "spec").mkdir()
    (repo / "spec" / "index.md").write_text(INDEX)
    init(repo)


@given("a file lines.md with two lines in strict EARS")
def lines_in_strict_ears(repo):
    (repo / "lines.md").write_text("\n".join(GOOD) + "\n")


@given(parsers.parse("a file lines.md whose line 1 is in strict EARS and whose line 2 {fault}"))
def lines_with_a_fault(repo, fault):
    (repo / "lines.md").write_text(GOOD[0] + "\n" + FAULTS[fault] + "\n")


@when(parsers.re(r"the asker runs `work (?P<args>[^`]+)`"))
def the_asker_runs(run, context, args):
    context["done"] = run("work", *shlex.split(args))


@then("the upstream keeps one new request, whose status is open and whose turn is the upstream's")
def keeps_one_open(repo, context):
    assert [p.name for p in kept(repo)] == ["q1.md"], context["done"]
    text = (repo / request_rel("q1")).read_text()
    assert "status: open\n" in text and "turn: upstream\n" in text


@then("the upstream keeps one new request")
def keeps_one(repo, context):
    assert [p.name for p in kept(repo)] == ["q1.md"], context["done"]


@then(parsers.parse('its delegation is "{text}"'))
def delegation_is(repo, text):
    found = re.search(r"(?m)^delegation: (.*)$", (repo / request_rel("q1")).read_text())
    assert found, "no delegation field"
    value = found.group(1)
    assert (json.loads(value) if value.startswith('"') else value) == text


@then("its lines are the two lines of lines.md and its asker is ctx-a")
def lines_and_asker(repo):
    assert sections(repo, "q1")["Lines"] == ["%d. %s" % (n, line) for n, line in enumerate(GOOD, 1)]
    assert "asker: ctx-a\n" in (repo / request_rel("q1")).read_text()


@then(parsers.re(r"its (?P<field>origins|job-thread) (?:are|is) (?P<named>.+)"))
def names_origin(repo, field, named):
    text = (repo / request_rel("q1")).read_text()
    if field == "origins":
        assert re.search(r"(?m)^source: \[o1, o2\]$", text), text
    else:
        assert re.search(r"(?m)^part_of: t1$", text), text


@then("work prints that request's id")
def prints_id(context):
    assert context["done"].stdout.strip() == "q1"


@then("the command is refused, naming line 2")
def refused_naming_line_2(context):
    assert "line 2" in context["done"].stderr, context["done"]


@then("the command is refused because the request names neither an origin nor a job-thread")
def refused_no_origin(context):
    err = context["done"].stderr
    assert "neither an origin" in err and "job-thread" in err, context["done"]


@then("it exits with an error")
def exits_with_an_error(context):
    assert context["done"].returncode != 0, context["done"]


@then("the upstream keeps no request")
def keeps_no_request(repo):
    assert kept(repo) == []


@then(parsers.parse("{ident}'s lines are as they were"))
def lines_as_they_were(repo, ident):
    assert sections(repo, ident)["Lines"] == ["1. line 1", "2. line 2"]


@then(parsers.parse("{ident} gives line {n} the line outcome {word}"))
def gives_outcome(repo, ident, n, word):
    assert "%s. %s" % (n, word) in sections(repo, ident)["Outcomes"]


@then(parsers.parse("{ident} has no resolution"))
def has_no_resolution(repo, ident):
    assert sections(repo, ident)["Resolution"] == []


def add_sections(repo, context, ident, question, answer=None):
    """Append the upstream's question on line 1 (and the asker's answer to it) to the request, as work writes them."""
    path = repo / request_rel(ident)
    text = path.read_text().rstrip("\n") + "\n\n## Questions\n1. line 1: %s\n\n## Answers\n" % question
    path.write_text(text + ("1. %s\n" % answer if answer else ""))
    context["written"] = path.read_text()
    context["questions"], context["answers"] = sections(repo, ident)["Questions"], sections(repo, ident)["Answers"]


@given(parsers.parse('{ident} holds the upstream\'s question "{question}" on line 1 and the asker\'s answer "{answer}" to it'))
def holds_question_and_answer(repo, context, ident, question, answer):
    add_sections(repo, context, ident, question, answer)


@given(parsers.parse('{ident} holds the upstream\'s question "{question}" on line 1'))
def holds_question(repo, context, ident, question):
    add_sections(repo, context, ident, question)


@when(parsers.parse('the upstream asks the question "{question}" on line {n} of {ident}'))
def the_upstream_asks(run, context, question, n, ident):
    context["done"] = run("work", "ask", ident, n, question)


@when(parsers.parse('the asker answers that question with "{answer}"'))
def the_asker_answers(run, context, answer):
    context["done"] = run("work", "reply", "q1", "1", answer)


@then(parsers.parse('{ident} holds the question "{question}" on line {n}'))
def holds_the_question(repo, ident, question, n):
    assert "line %s: %s" % (n, question) in [e.split(". ", 1)[1] for e in sections(repo, ident)["Questions"]]


@then(parsers.parse('{ident} holds the answer "{answer}" to the question "{question}"'))
def holds_the_answer(repo, ident, answer, question):
    found = sections(repo, ident)
    number = next(e.split(". ", 1)[0] for e in found["Questions"] if e.endswith(": " + question))
    assert "%s. %s" % (number, answer) in found["Answers"]


@then(parsers.parse("{ident}'s questions are as they were"))
def questions_as_they_were(repo, context, ident):
    assert sections(repo, ident)["Questions"] == context["questions"]


@then(parsers.parse("{ident}'s answers are as they were"))
def answers_as_they_were(repo, context, ident):
    assert sections(repo, ident)["Answers"] == context["answers"]
