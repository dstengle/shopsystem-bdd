"""features/work-queue.feature's Then step of `work answer` (r13): the answer, dated, under the work-item's `## Answers`."""
import datetime

from pytest_bdd import parsers, then


@then(parsers.parse('{rel} has under its `## Answers` the text "{text}", with the date the command was run'))
def has_answer(repo, context, rel, text):
    assert context["done"].returncode == 0, (context["done"].stdout, context["done"].stderr)
    body = (repo / rel).read_text()
    assert "\n## Answers\n" in body, body
    section = body.split("\n## Answers\n", 1)[1].split("\n## ", 1)[0]
    assert [l for l in section.splitlines() if l.strip()] == ["- %s: %s" % (datetime.date.today().isoformat(), text)], body
