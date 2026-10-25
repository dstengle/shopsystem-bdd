"""supervision's steps about an initiative `work run` sets done (r105, r109): the work-items and the request the Givens write,
and the Thens that read the initiative's status and its commit."""
from pytest_bdd import given, then

from .conftest import full
from .supervision_world import commit_all, fields, git, item_text, log_lines, write

INITIATIVE = ".shop/work/i1/initiative.md"


@given("i1 is started and its work-items w1 is green and w2 is withdrawn")
def started_with_items(repo):
    write(repo, INITIATIVE, "---\nid: %s\nkind: initiative\nstatus: started\n---\n" % full("initiative", "i1"))
    write(repo, ".shop/work/i1/w1.md", item_text("w1", "green"))
    write(repo, ".shop/work/i1/w2.md", item_text("w2", "withdrawn"))
    commit_all(repo, "i1 is started with w1 green and w2 withdrawn")


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
