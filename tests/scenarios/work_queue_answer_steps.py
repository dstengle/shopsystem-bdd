"""features/work-queue.feature's Then step of `work answer` (r13): the answer, dated, under the work-item's `## Answers`."""
import datetime

from pytest_bdd import parsers, then, when


@when("the session runs `work answer w1` with an answer of two lines")
def answer_of_two_lines(repo, run, context):
    from .test_work_queue import snapshot
    context["before"] = snapshot(repo)
    context["done"] = run("work", "answer", "w1", "line one\nline two")


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
