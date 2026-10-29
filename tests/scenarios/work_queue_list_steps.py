"""features/work-queue.feature's steps of `work list` and `work show <target>` (r34-r39): requests under .shop/work/, the
record of requests an initiative raised, and what the two commands print."""
import json
import re

from pytest_bdd import given, parsers, then

from .conftest import PATH, full


@given(parsers.re(r"a request (?P<ident>q\d+) under \.shop/work/ that is (?P<status>[\w-]+)$"))
def request_with_status(repo, ident, status):
    from .test_work_queue import write
    write(repo, ".shop/work/requests/%s.md" % ident,
          "---\nid: %s\nkind: request\nasker: ctx-a\nstatus: %s\n---\n\n# %s\n" % (full("request", ident), status, ident))


@given(parsers.re(r"a request (?P<ident>q\d+) that (?P<initiative>i\d+) raised into the upstream (?P<upstream>[\w-]+), "
                  r"which is (?P<status>[\w-]+)$"))
def raised_request(repo, ident, initiative, upstream, status):
    from .test_work_queue import write
    write(repo, ".shop/work/%s/raised.jsonl" % initiative, json.dumps(
        {"upstream": upstream, "request": ident, "initiative": initiative, "status": status}) + "\n")


@given(parsers.re(r"(?P<ident>i\d+)'s work-item (?P<name>\w+) is awaiting-answer with the question \"(?P<question>[^\"]*)\" "
                  r"not yet answered$"))
def item_with_question(repo, ident, name, question):
    from .test_work_queue import item_text, write
    write(repo, ".shop/work/%s/%s.md" % (ident, name), item_text(name, "awaiting-answer", ident) + "\n## Questions\n- %s\n" % question)


def printed(context):
    assert context["done"].returncode == 0, context["done"]
    return [line.replace("/", " ").split() for line in context["done"].stdout.splitlines()]


@then(parsers.re(r"it prints (?P<pairs>\S+ with (?:(?!and the question).)+)$"))
def prints_pairs(context, pairs):
    lines = printed(context)
    for pair in pairs.replace(" and ", ", ").split(", "):
        name, status = pair.split(" with ")
        assert [w for w in lines if name in w and status in w], (name, status, context["done"].stdout)


@then(parsers.parse("work prints {ident} as waiting on {request}"))
def prints_waiting(context, ident, request):
    assert [w for w in printed(context) if w[:2] == ["initiative", ident] and "waiting" in w and request in w], context["done"].stdout


@then(parsers.parse("work prints {whose}'s status as {status}"))
def prints_status_as(context, whose, status):
    assert [w for w in printed(context) if whose in w and status in w], context["done"].stdout


@then(parsers.re(r'it prints the question "(?P<question>[^"]*)"$'))
def prints_question(context, question):
    assert question in context["done"].stdout, context["done"].stdout


@given("a request q1 kept in this context, whose asker is this context, that is delivered and in the asker's turn")
def request_kept_here(repo):
    from .test_work_queue import write
    write(repo, ".shop/work/requests/q1.md",
          "---\nid: %s\nkind: request\nasker: bounded-context/%s\nstatus: delivered\nturn: asker\n---\n\n# q1\n\n"
          "## Lines\n1. The first line.\n2. The second line.\n\n## Questions\n\n## Answers\n\n## Outcomes\n\n## Resolution\n"
          % (full("request", "q1"), PATH))


def fill(repo, section, *entries):
    path = repo / ".shop/work/requests/q1.md"
    path.write_text(path.read_text().replace("## %s\n" % section, "## %s\n%s" % (section, "".join(e + "\n" for e in entries)), 1))


@given("its line 1 has the line outcome accepted and its line 2 the line outcome refused")
def request_outcomes(repo):
    fill(repo, "Outcomes", "1. accepted", "2. refused")


@given(parsers.re(r'it has on line (?P<line>\d+) the question "(?P<question>[^"]*)" with the answer "(?P<answer>[^"]*)"$'))
def request_question(repo, line, question, answer):
    fill(repo, "Questions", "1. line %s: %s" % (line, question))
    fill(repo, "Answers", "1. %s" % answer)


@given("its resolution gives line 1 as thing#r7, delivered in version 0.23.0")
def request_resolution(repo):
    fill(repo, "Resolution", "1. thing#r7 0.23.0")


@then("it prints that it is the asker's turn")
def prints_asker_turn(context):
    assert "it is the asker's turn" in context["done"].stdout, context["done"].stdout


@then(parsers.re(r"it prints line (?P<a>\d+) with (?P<aw>\w+) and line (?P<b>\d+) with (?P<bw>\w+)$"))
def prints_line_outcomes(context, a, aw, b, bw):
    shown = context["done"].stdout.splitlines()
    for number, word in ((a, aw), (b, bw)):
        assert ["line %s: %s" % (number, word)] == [l.split(" - ")[0].strip() for l in shown if l.strip().startswith("line %s:" % number)], shown


@then(parsers.re(r'it prints the question "(?P<question>[^"]*)" and the answer "(?P<answer>[^"]*)"$'))
def prints_question_answer(context, question, answer):
    shown = context["done"].stdout
    assert re.search(r"(?m)^\s*question 1: .*%s" % re.escape(question), shown), shown
    assert re.search(r"(?m)^\s*answer 1: %s$" % re.escape(answer), shown), shown


@then("it prints its resolution, thing#r7 and 0.23.0")
def prints_resolution(context):
    assert re.search(r"(?m)^\s*resolution line 1: thing#r7 0\.23\.0$", context["done"].stdout), context["done"].stdout


@then(parsers.re(r"it gives (?P<pairs>\S+ with .+)$"))
def gives_pairs(context, pairs):
    shown = context["json"]
    found = {(i["initiative"], i["status"]) for i in shown["initiatives"]} | {(r["request"], r["status"]) for r in shown["requests"]}
    found |= {(w["work-item"], w["status"]) for w in shown["work-items"]}
    for pair in pairs.replace(" and ", ", ").split(", "):
        name, status = pair.split(" with ")
        assert (name, status) in found, (pair, shown)


@then(parsers.re(r"it gives (?P<whose>\w+)'s status as (?P<status>[\w-]+)(?:, and (?P<name>\w+) with (?P<wstatus>[\w-]+))?"
                 r" and the question \"(?P<question>[^\"]*)\"$"))
def gives_status_and_question(context, whose, status, name, wstatus, question):
    shown = context["json"]
    if name is None:
        assert (shown["work-item"], shown["status"], question in shown["questions"]) == (whose, status, True), shown
        return
    found = shown["initiatives"][0]
    assert (found["initiative"], found["status"]) == (whose, status), shown
    item = [i for i in found["work-items"] if i["work-item"] == name][0]
    assert item["status"] == wstatus and question in item["questions"], shown
