"""features/work-queue.feature's Then step of `work answer` (r13): the answer, dated, under the work-item's `## Answers`."""
import datetime

from pytest_bdd import given, parsers, then, when

BREAKS = {"a newline": "\n"}
BREAKS.update({"U+%04X, the %s" % (ord(c), n): c for c, n in [
    ("\x0b", "vertical tab"), ("\x0c", "form feed"), ("\r", "carriage return"), ("\x85", "next-line control"),
    (" ", "line separator"), (" ", "paragraph separator")]})


@when(parsers.parse("the session runs `work answer w1` with an answer of two lines broken by {line_break}"))
def answer_of_two_lines(repo, run, context, line_break):
    from .test_work_queue import snapshot
    context["before"] = snapshot(repo)
    context["done"] = run("work", "answer", "w1", "line one" + BREAKS[line_break] + "line two")


@when(parsers.parse('the session runs `work answer w1 "{text}"`, saying that the answer asks for a change'))
def answer_asking_change(repo, run, context, text):
    from .test_work_queue import snapshot
    context["before"] = snapshot(repo)
    context["done"] = run("work", "answer", "w1", text, "--change")


@when(parsers.parse('the session runs `work answer w1 "{text}"`, saying that the answer accepts the work-item as it is'))
def answer_accepting(repo, run, context, text):
    from .test_work_queue import snapshot
    context["before"] = snapshot(repo)
    context["done"] = run("work", "answer", "w1", text, "--accept")


@when(parsers.parse('the session runs `work answer w1 "{text}"`, saying neither that the answer asks for a change '
                    'nor that it accepts the work-item as it is'))
def answer_saying_neither(repo, run, context, text):
    from .test_work_queue import snapshot
    context["before"] = snapshot(repo)
    context["done"] = run("work", "answer", "w1", text)


@then("work exits with an error, saying that the answer must say whether it asks for a change or accepts the work-item as it is")
def refuses_answer_without_verdict(context):
    done = context["done"]
    assert done.returncode != 0, done
    assert "Traceback" not in done.stderr and "must say whether it asks for a change" in done.stderr, done.stderr


@given(parsers.re(r"an initiative (?P<ident>i\d+) under \.shop/work/ whose capability-proposal (?P<name>\w+) is (?P<status>[\w-]+)$"))
def initiative_with_proposal(repo, ident, name, status):
    """A capability-proposal in the given status, with a question and no log.jsonl line."""
    from .test_work_queue import initiative, item_text, write
    initiative(repo, ident)
    text = item_text(name, status, ident, "capability-proposal") + "\n## Questions\n\n- Which reading?\n"
    write(repo, ".shop/work/%s/%s.md" % (ident, name), text)


@then("work exits with an error, saying that an answer is one line")
def refuses_multiline_answer(context):
    done = context["done"]
    assert done.returncode != 0, done
    assert "Traceback" not in done.stderr and "an answer is one line" in done.stderr, done.stderr


@then(parsers.parse('{rel} has under its `## Answers` the text "{text}", with the date the command was run'))
def has_answer(repo, context, rel, text):
    assert context["done"].returncode == 0, (context["done"].stdout, context["done"].stderr)
    body = (repo / rel).read_text()
    assert "\n## Answers\n" in body, body
    section = body.split("\n## Answers\n", 1)[1].split("\n## ", 1)[0]
    assert [l for l in section.splitlines() if l.strip()] == ["- %s: %s" % (datetime.date.today().isoformat(), text)], body
