"""supervision's steps about the intake round `work run` starts for a request this context is the upstream of."""
import re

from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_world import calls, commit_all, git, scripts_in, starts, write

REQUEST = ".shop/work/requests/q1.md"


@given(parsers.re(r"a request q1 of which this context is the upstream, (?P<status>[\w-]+), its turn the upstream's, "
                  r"with two lines$"))
def upstream_request(repo, status):
    write(repo, REQUEST, "---\nid: %s\nkind: request\nasker: internal\nstatus: %s\nturn: upstream\n---\n\n# q1\n\n"
          "## Lines\n1. Line 1 text.\n2. Line 2 text.\n\n## Outcomes\n\n## Resolution\n" % (full("request", "q1"), status))
    commit_all(repo, "a request this context is the upstream of")


def round_with_question(plan, question):
    work = ["python3", scripts_in("{scripts}/work")]
    plan["initiative-round"] = {"status": "DONE", "questions": ["2. " + question],
                                "run": [work + ["outcome", "q1", "1", "accepted"], work + ["turn", "q1"]]}


@given("the intake round writes a line outcome for q1's line 1, gives a question on q1's line 2 and passes the turn with "
       "`work turn`")
def intake_questions(plan):
    round_with_question(plan, "What is meant by line 2?")


@given(parsers.parse('the intake round writes a line outcome for q1\'s line 1, gives the question "{question}" on q1\'s '
                     'line 2 and passes the turn with `work turn`'))
def intake_asks(plan, question):
    round_with_question(plan, question)


@then("an `initiative-round` session of the kind intake was started, given q1, its brief asking for each line's line "
      "outcome or a question on it and for the turn passed with `work turn`")
def intake_started(repo, context):
    found = [c for c in starts(repo) if c["agent"].endswith("initiative-round") and "# intake of q1" in c["brief"]
             and "Kind: intake" in c["brief"] and REQUEST in c["brief"] and "line outcome or a question on it" in c["brief"]
             and "/work turn q1" in c["brief"]]
    assert len(found) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)


@then("q1's line 1 has a line outcome, and q1's turn is its asker's")
def line_one_has_outcome(repo, context):
    text = (repo / REQUEST).read_text()
    outcomes = text.split("\n## Outcomes\n", 1)[1].split("\n## ", 1)[0].split()
    assert outcomes == ["1.", "accepted"], (text, context["done"].stderr, calls(repo, ("ran", "refused")))
    assert "\nturn: asker\n" in text, text


@then(parsers.parse('q1 holds the question "{question}" on its line 2'))
def q1_holds_question(repo, context, question):
    text = (repo / REQUEST).read_text()
    held = text.split("\n## Questions\n", 1)[1].split("\n## ", 1)[0].strip().splitlines()
    assert held == ["1. line 2: " + question], (text, context["done"].stderr)


def accepted_request(repo, name):
    write(repo, ".shop/work/requests/%s.md" % name, "---\nid: %s\nkind: request\nasker: internal\nstatus: accepted\n---\n\n"
          "# %s\n\n## Lines\n1. Line 1 text.\n\n## Outcomes\n1. accepted\n\n## Resolution\n" % (full("request", name), name))


@given("a request q1 of which this context is the upstream, accepted, that no initiative fulfils")
def accepted_unfulfilled(repo):
    accepted_request(repo, "q1")
    commit_all(repo, "q1 is accepted and no initiative fulfils it")


@given("a request q2 of which this context is the upstream, accepted, that i1 fulfils")
def accepted_fulfilled(repo):
    accepted_request(repo, "q2")
    write(repo, ".shop/work/i1/initiative.md", "---\nid: %s\nkind: initiative\nstatus: started\nfulfils: q2\n---\n"
          % full("initiative", "i1"))
    commit_all(repo, "i1 fulfils q2")


def fulfilling(repo, request):
    """The initiatives under .shop/work/ whose initiative.md names `request` as what it fulfils."""
    return [p.parent.name for p in sorted((repo / ".shop/work").glob("i*/initiative.md"))
            if re.search(r"^fulfils: (\S*/)?%s$" % request, p.read_text(), re.M)]


def start_commits(repo, request):
    return [s for s in git(repo, "log", "--format=%s").splitlines() if s.endswith(", fulfilling %s" % request)]


@then("`work start` was run for q1, and an initiative under .shop/work/ fulfils q1")
def started_for_q1(repo, context):
    where = (context["done"].stdout, context["done"].stderr)
    assert len(start_commits(repo, "q1")) == 1 and len(fulfilling(repo, "q1")) == 1, (fulfilling(repo, "q1"), where)


@then("`work start` was not run for q2, and i1 is the only initiative that fulfils q2")
def not_started_for_q2(repo, context):
    assert not start_commits(repo, "q2") and fulfilling(repo, "q2") == ["i1"], (fulfilling(repo, "q2"), context["done"].stderr)
