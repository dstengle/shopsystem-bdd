"""features/work-queue.feature's steps of `work note` (r19-r21): the ledger Given, the line-break When and the Thens."""
import datetime

from pytest_bdd import given, parsers, then, when

from .work_queue_answer_steps import BREAKS
from .work_queue_git_steps import git

LEDGER = ".shop/work/i1/ledger.md"


@given(parsers.parse("an initiative {ident} under .shop/work/ whose ledger .shop/work/{ident2}/ledger.md has one line"))
def with_ledger(repo, ident, ident2):
    from .test_work_queue import initiative, write
    initiative(repo, ident)
    write(repo, ".shop/work/%s/ledger.md" % ident, "- 2026-10-01: the first note\n")


@when(parsers.parse("the session runs `work note i1` with a line of two lines broken by {line_break}"))
def note_of_two_lines(repo, run, context, line_break):
    from .test_work_queue import snapshot
    context["before"] = snapshot(repo)
    context["done"] = run("work", "note", "i1", "line one" + BREAKS[line_break] + "line two")


@then(".shop/work/i1/ledger.md has two lines, the first as it was")
def ledger_two_lines(repo, context):
    lines = (repo / LEDGER).read_text().splitlines(keepends=True)
    assert context["done"].returncode == 0, context["done"]
    assert len(lines) == 2 and lines[0] == context["before"][LEDGER], lines


@then(parsers.parse('its last line has the text "{text}", with the date the command was run'))
def ledger_last_line(repo, text):
    last = (repo / LEDGER).read_text().splitlines()[-1]
    assert last.endswith(text) and datetime.date.today().isoformat() in last, last


@then("work exits with an error, saying that a note is one line")
def refuses_multiline_note(context):
    done = context["done"]
    assert done.returncode != 0, done
    assert "Traceback" not in done.stderr and "a note is one line" in done.stderr, done.stderr


@then(".shop/work/i1/ledger.md is as it was")
def ledger_as_it_was(repo, context):
    assert (repo / LEDGER).read_text() == context["before"][LEDGER]


@then("main's last commit is the one it was")
def commit_is_the_same(repo, context):
    assert git(repo, "rev-parse", "main").strip() == context["head"]
