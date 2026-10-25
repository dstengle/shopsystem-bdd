"""supervision's steps about the requests whose asker is this context, which `work run` reads at its end (r9, r82, r101)."""
from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_world import commit_all, write


def request_q2(repo, status, turn, questions="", answers=""):
    write(repo, ".shop/work/requests/q2.md",
          "---\nid: %s\nkind: request\nasker: internal\nstatus: %s\nturn: %s\n---\n\n# q2\n\n## Lines\n1. Line 1 text.\n\n"
          "## Questions\n%s\n## Answers\n%s\n## Outcomes\n\n## Resolution\n" % (full("request", "q2"), status, turn, questions, answers))
    commit_all(repo, "a request this context asked")


@given("a request q2 whose asker is this context, awaiting-upstream, its turn the upstream's")
def asked_awaiting_upstream(repo):
    request_q2(repo, "awaiting-upstream", "upstream")


@given(parsers.parse('a request q2 kept in this context whose asker is this context, awaiting-asker, its turn the '
                     'asker\'s, with the question "{question}" and no answer'))
def asked_awaiting_asker(repo, question):
    request_q2(repo, "awaiting-asker", "asker", "1. line 1: %s\n" % question)


@then(parsers.parse('`work run` prints q2 with the question "{question}"'))
def prints_q2_question(context, question):
    out = context["done"].stdout.splitlines()
    assert any("q2" in l.split() for l in out) and any(question in l for l in out), context["done"]
