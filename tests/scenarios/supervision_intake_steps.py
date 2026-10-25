"""supervision's steps about the intake round `work run` starts for a request this context is the upstream of."""
import re

from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_world import calls, commit_all, git, scripts_in, starts, write

REQUEST = ".shop/work/requests/q1.md"
JUDGED = ("accepted", "refused")


@given(parsers.re(r"a request q1 of which this context is the upstream, (?P<status>[\w-]+), its turn the upstream's, "
                  r"with two lines$"))
def upstream_request(repo, status):
    write(repo, REQUEST, "---\nid: %s\nkind: request\nasker: internal\nstatus: %s\nturn: upstream\n---\n\n# q1\n\n"
          "## Lines\n1. Line 1 text.\n2. Line 2 text.\n\n## Outcomes\n\n## Resolution\n" % (full("request", "q1"), status))
    commit_all(repo, "a request this context is the upstream of")


@given("the intake round writes a line outcome for each of q1's lines and passes the turn with `work turn`")
def intake_writes(plan):
    work = ["python3", scripts_in("{scripts}/work")]
    commands = [work + ["outcome", "q1", str(n), word] for n, word in enumerate(JUDGED, 1)]
    plan["initiative-round"] = {"status": "DONE", "run": commands + [work + ["turn", "q1"]]}


@then("an `initiative-round` session of the kind intake was started, given q1")
def intake_started(repo, context):
    found = [c for c in starts(repo) if c["agent"].endswith("initiative-round") and "# intake of q1" in c["brief"]
             and "Kind: intake" in c["brief"] and REQUEST in c["brief"]]
    assert len(found) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)


@then("each of q1's lines has a line outcome, and q1's turn is its asker's")
def lines_have_outcomes(repo, context):
    text = (repo / REQUEST).read_text()
    outcomes = text.split("\n## Outcomes\n", 1)[1].split("\n## ", 1)[0].split()
    assert outcomes == ["1.", "accepted", "2.", "refused"], (text, context["done"].stderr, calls(repo, ("ran", "refused")))
    assert "\nturn: asker\n" in text, text


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
