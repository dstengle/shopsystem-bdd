"""supervision's steps about an initiative `work run` sets done (r105, r109): the work-items and the request the Givens write,
and the Thens that read the initiative's status and its commit."""
from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_world import commit_all, fields, git, item_text, log_lines, write

INITIATIVE = ".shop/work/i1/initiative.md"


@given(parsers.re(r"i1 is started and its work-items w1 is (?P<s1>green|withdrawn) and w2 is (?P<s2>green|withdrawn)$"))
def started_with_items(repo, s1, s2):
    write(repo, INITIATIVE, "---\nid: %s\nkind: initiative\nstatus: started\n---\n" % full("initiative", "i1"))
    write(repo, ".shop/work/i1/w1.md", item_text("w1", s1))
    write(repo, ".shop/work/i1/w2.md", item_text("w2", s2))
    commit_all(repo, "i1 is started with w1 %s and w2 %s" % (s1, s2))


@given("i1's kept branch review lists nothing to fix now, and i1's measurement and analysis record are committed on the "
       "initiative branch")
def review_and_records_committed(repo, plan):
    plan["bdd-branch-reviewer"] = {"questions": []}
    write(repo, ".shop/records/measurements/2026-10-01-i1.md", "# measurement of i1\n")
    write(repo, ".shop/records/2026-10-01-i1-analysis.md", "# analysis of i1\n")
    commit_all(repo, "i1's measurement and analysis record")


@given(parsers.re(r'i1 is started, has neither a capability-proposal nor a work-item, and its glossary-proposal g1 is approved, '
                  r'its adds naming the term "(?P<term>[^"]+)"$'))
def started_glossary_only(repo, term):
    write(repo, INITIATIVE, "---\nid: %s\nkind: initiative\nstatus: started\n---\n" % full("initiative", "i1"))
    write(repo, ".shop/work/i1/g1.md", "---\nid: %s\nkind: glossary-proposal\npart_of: %s\nstatus: approved\nadds: [term/%s]\n"
          "changes: []\nremoves: []\ndate: 2026-10-15\n---\n" % (full("glossary-proposal", "g1"), full("initiative", "i1"), term))
    commit_all(repo, "i1 is started with an approved glossary-proposal")


@given(parsers.re(r'spec/index\.md\'s Glossary holds the term "(?P<term>[^"]+)", committed on the initiative branch$'))
def glossary_committed(repo, term):
    write(repo, "spec/index.md", "# Index\n\n## Glossary\n\n- **%s**: a thing.\n" % term)
    commit_all(repo, "spec/index.md's Glossary holds %s" % term)


@given("i1 is started and its work-item w1 is ready")
def started_with_ready(repo):
    write(repo, INITIATIVE, "---\nid: %s\nkind: initiative\nstatus: started\n---\n" % full("initiative", "i1"))
    write(repo, ".shop/work/i1/w1.md", item_text("w1", "ready"))
    commit_all(repo, "i1 is started with w1 ready")


@then("i1's transition to done was made after w1's transition to green, before `work run` exited")
def done_after_green(repo, context):
    lines = log_lines(repo)
    green = [n for n, l in enumerate(lines) if l.get("work-item") == "w1" and l.get("after") == "green"]
    done = [n for n, l in enumerate(lines) if l.get("work-item") == "i1" and l.get("after") == "done"]
    assert green and done and green[0] < done[0], (lines, context["done"].stdout, context["done"].stderr)


@given("a request q2 kept in this context, whose asker is this context, that names i1 and is delivered")
def delivered_request(repo):
    write(repo, ".shop/work/requests/q2.md", "---\nid: %s\nkind: request\nasker: internal\npart_of: %s\nstatus: delivered\n"
          "turn: upstream\n---\n\n# q2\n\n## Lines\n1. Line 1 text.\n" % (full("request", "q2"), full("initiative", "i1")))
    commit_all(repo, "a delivered request that names i1")


@then("i1 is not done")
def i1_is_not_done(repo, context):
    assert fields(repo / INITIATIVE)["status"] != "done", (context["done"].stdout, context["done"].stderr)


@then("i1 is done")
def i1_is_done(repo, context):
    assert fields(repo / INITIATIVE)["status"] == "done", (context["done"].stdout, context["done"].stderr)


@then("the initiative branch has a commit of i1 with its status done")
def done_committed(repo, context):
    assert "\nstatus: done\n" in git(repo, "show", "HEAD:" + INITIATIVE), context["done"].stderr
    assert git(repo, "log", "-1", "--format=%H", "-S", "status: done", "--", INITIATIVE).split(), context["done"].stderr


@then("i1's file is not left uncommitted")
def i1_file_clean(repo):
    assert git(repo, "status", "--porcelain", "--", INITIATIVE).strip() == ""
