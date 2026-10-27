"""supervision's steps about the lines an integrate round gives into an upstream (r135) and the capability-proposal that
waits for the request raised with them (r136): the upstream catalogue is a repository beside the context's, named by
spec/index.md's `## Upstreams`; the record of what this context raised is .shop/work/i1/raised.jsonl."""
import json
import re
import subprocess

from pytest_bdd import given, parsers, then

from .conftest import INDEX, full
from .supervision_integrate_steps import entry
from .supervision_proposal_steps import DIR, drafted
from .supervision_world import commit_all, write

CATALOGUE = "bounded-context/ex.com/prod/catalogue"
KEPT = ".shop/work/i1/runs/i1/1-integrate/drafts/round-1/"


def catalogue(repo):
    """The repository of the upstream catalogue beside the context's, made once; the context's spec/index.md names it."""
    there = repo.parent / "catalogue-ctx"
    if not there.exists():
        write(there, "spec/index.md", "---\nid: %s\n---\n# catalogue\n" % CATALOGUE)
        for args in (("init", "-q", "-b", "main"), ("config", "user.name", "Someone"),
                     ("config", "user.email", "someone@example.com"), ("config", "commit.gpgsign", "false"),
                     ("add", "-A"), ("commit", "-q", "-m", "catalogue")):
            subprocess.run(["git", *args], cwd=there, check=True, capture_output=True)
        write(repo, "spec/index.md", INDEX + "\n## Upstreams\n\n- %s: ../catalogue-ctx/spec\n" % CATALOGUE)
        commit_all(repo, "spec/index.md names catalogue as an upstream")
    return there


def requests_of(there):
    return sorted((there / ".shop/work/requests").glob("q*.md"))


@given(parsers.re(r"the integrate round for i1 gives DONE with a change list that (?P<first>.+) on thing, and gives the lines "
                  r'of a request into the upstream catalogue: "(?P<line>[^"]+)"$'))
def integrate_gives_lines(repo, plan, first, line):
    catalogue(repo)
    plan["round:integrate"] = {"status": "DONE", "fields": {"changes": [entry("thing", first)],
                                                           "requests": [{"upstream": CATALOGUE, "lines": [line]}]}}


@then(parsers.re(r'`work request` was run for the upstream catalogue, with the line "(?P<line>[^"]+)" as its one line$'))
def request_run(repo, context, line):
    found = requests_of(repo.parent / "catalogue-ctx")
    assert len(found) == 1, (found, context["done"].stdout, context["done"].stderr)
    assert "## Lines\n1. %s\n" % line in found[0].read_text(), found[0].read_text()


@then(parsers.re(r'the request it wrote in catalogue is raised for q1 and gives the delegation "(?P<text>[^"]+)"$'))
def request_raised(repo, text):
    body = requests_of(repo.parent / "catalogue-ctx")[0].read_text()
    assert re.search(r"(?m)^raised_for: request/\S+/q1$", body) and "\ndelegation: %s\n" % json.dumps(text) in body, body


@given("i1 is started and fulfils the request q1, and i1's capability-proposal p1 is formulated, its adds naming thing#r1, "
       "and i1's capability-proposal p2 is formulated, its adds naming other#r4")
def two_formulated(repo):
    write(repo, DIR + "/initiative.md", "---\nid: %s\nkind: initiative\nstatus: started\nfulfils: q1\n---\n" % full("initiative", "i1"))
    write(repo, ".shop/work/requests/q1.md", "---\nid: %s\nkind: request\nasker: internal\nstatus: accepted\n---\n\n## Lines\n"
          "1. Line 1 text.\n\n## Outcomes\n1. accepted\n" % full("request", "q1"))
    for name, capability, ident in (("p1", "thing", "thing#r1"), ("p2", "other", "other#r4")):
        write(repo, "%s/%s.md" % (DIR, name), "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: formulated\n"
              "argues: [%s]\nadds: [%s]\nchanges: []\nremoves: []\ndate: 2026-10-15\n---\n"
              % (full("capability-proposal", name), full("initiative", "i1"), capability, ident))
    commit_all(repo, "two formulated capability-proposals")


@given(parsers.re(r'p1 was written by an integrate round that gave the lines of a request into the upstream catalogue: '
                  r'"(?P<line>[^"]+)", and p2 by an integrate round that gave no lines into an upstream$'))
def p1_from_round_with_lines(repo, context, line):
    context["line"] = line
    path = repo / DIR / "p1.md"
    path.write_text(path.read_text() + "\n# thing\n\nThe drafts of this proposal are in %s.\n" % KEPT)
    commit_all(repo, "p1 names the drafts of its integrate round")


@given(parsers.re(r'the request q2 in catalogue, with the line "(?P<line>[^"]+)" as its one line, is raised by i1 for q1 and '
                  r'is awaiting-upstream$'))
def q2_awaiting(repo, line):
    there = catalogue(repo)
    write(there, ".shop/work/requests/q2.md", "---\nid: request/ex.com/prod/catalogue/q2\nkind: request\n"
          "asker: bounded-context/ex.com/prod/ctx\nraised_for: request/ex.com/prod/ctx/q1\nstatus: awaiting-upstream\nturn: upstream\n---\n\n"
          "# q2\n\n## Lines\n1. %s\n" % line)
    commit_all(there, "q2")
    write(repo, DIR + "/raised.jsonl", json.dumps({"upstream": CATALOGUE, "request": "q2", "initiative": "i1",
                                                   "status": "open", "round": KEPT}) + "\n")
    commit_all(repo, "i1 raised q2 in catalogue")


@then("`work add` drafted no work-item part of p1")
def none_of_p1(repo, context):
    found = [n for n, f, _ in drafted(repo) if f["part_of"].endswith("/p1")]
    assert not found, (found, context["done"].stderr)


@then(parsers.parse("`work add` drafted one work-item in i1, part of p2: under other accepting other#r4"))
def one_of_p2(repo, context):
    found = [(f["under"], f["accepts"]) for _, f, _ in drafted(repo) if f["part_of"].endswith("/p2")]
    assert found == [("other", "[other#r4]")] and len(drafted(repo)) == 1, (found, context["done"].stderr)
