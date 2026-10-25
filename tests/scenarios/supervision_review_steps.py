"""supervision's steps about the branch review: the commits a kept branch review has read, what the branch reviewer's
session leaves, and what `work run` keeps and logs of it."""
from pytest_bdd import given, parsers, then

from .supervision_world import commit_all, git, item_text, log_lines, starts, write

REVIEWS = ".shop/work/i1/runs/branch-review"
FINDINGS = "# findings\nNothing found.\n"
REVIEWER = "shopsystem-bdd:bdd-branch-reviewer"


def kept_review(repo):
    """A branch review kept in the initiative, as work run keeps one: its directory with the brief (naming the head it
    read up to) and its findings, committed."""
    head = git(repo, "rev-parse", "HEAD").strip()
    write(repo, REVIEWS + "/1/brief.md", "# branch review of i1\n\nInitiative branch: main\nHead: %s\n" % head)
    write(repo, REVIEWS + "/1/findings.md", FINDINGS)
    commit_all(repo, "work: branch review 1")


@given(parsers.re(r"every worker gives DONE, and the branch reviewer (?P<does>ends|writes findings\.md beside its brief)$"))
def reviewer_does(plan, does):
    plan["default"] = {"status": "DONE"}
    plan["bdd-branch-reviewer"] = {"notes": {"findings.md": FINDINGS}} if does != "ends" else {}


@given("i1's work-item w1 is green and a kept branch review has read every commit on the initiative branch")
def green_and_reviewed(repo):
    write(repo, ".shop/work/i1/w1.md", item_text("w1", "green"))
    commit_all(repo, "work-items")
    kept_review(repo)


@given("i1's work-item w2 was added after that review and is drafted")
def added_after(repo):
    write(repo, ".shop/work/i1/w2.md", item_text("w2", "drafted"))
    commit_all(repo, "w2 added")


@given("a kept branch review has read every commit on the initiative branch, and its own commit is the initiative "
       "branch's last")
def reviewed_last(repo):
    kept_review(repo)


@given("the initiative branch holds a commit of notes.txt that no kept branch review has read")
def unread_notes(repo):
    write(repo, "notes.txt", "notes\n")
    commit_all(repo, "notes.txt")


def reviewer_calls(repo):
    return [c for c in starts(repo) if c["agent"] == REVIEWER]


@then("a directory under .shop/work/i1/runs/branch-review/ holds the branch reviewer's brief and its findings.md, as it "
      "wrote them")
def review_kept(repo, context):
    kept = sorted((repo / REVIEWS).glob("*/brief.md"))
    assert len(kept) == 1 and len(reviewer_calls(repo)) == 1, (kept, context["done"].stderr)
    assert kept[0].read_text() == reviewer_calls(repo)[0]["brief"]
    assert (kept[0].parent / "findings.md").read_text() == FINDINGS


@then("the initiative branch has a commit of the branch reviewer's directory under .shop/work/i1/runs/branch-review/, "
      "its findings.md included")
def review_committed(repo, context):
    committed = git(repo, "log", "main", "--name-only", "--format=", "--", REVIEWS).split()
    assert any(p.startswith(REVIEWS + "/") and p.endswith("/findings.md") for p in committed), (committed, context["done"].stderr)
    assert any(p.startswith(REVIEWS + "/") and p.endswith("/brief.md") for p in committed), committed


@then("nothing under .shop/work/i1/runs/branch-review/ is left uncommitted")
def review_clean(repo):
    assert git(repo, "status", "--porcelain", "--untracked-files=all", "--", REVIEWS) == ""


@then("log.jsonl has, for the branch reviewer, a start line and then an end line, each with the time, the stage "
      "branch-review, the agent bdd-branch-reviewer and the session id claude was given")
def review_logged(repo, context):
    lines = [l for l in log_lines(repo) if l.get("stage") == "branch-review" and l.get("event") in ("start", "end")]
    given = [c["argv"][c["argv"].index("--session-id") + 1] for c in reviewer_calls(repo)]
    assert [l["event"] for l in lines] == ["start", "end"] and len(given) == 1, (lines, context["done"].stderr)
    for line in lines:
        assert line.get("time") and line["agent"] == "bdd-branch-reviewer" and line["session"] == given[0], line


@then("before each of w1's four workers was started, and before the branch reviewer was started, `work run` had "
      "verified that it can push the initiative branch to the remote")
def verified_before_all(repo, context):
    lines = [l for l in log_lines(repo) if l.get("event") in ("start", "push verified")
             and l.get("work-item", "w1") == "w1"]
    starts_at = [i for i, l in enumerate(lines) if l["event"] == "start"]
    assert len(starts_at) == 5, (lines, context["done"].stderr)
    assert lines[starts_at[-1]].get("stage") == "branch-review", lines
    for before, at in zip([-1] + starts_at, starts_at):
        assert any(l["event"] == "push verified" for l in lines[before + 1:at]), lines


@then("no session of bdd-branch-reviewer was started")
def no_reviewer(repo, context):
    assert reviewer_calls(repo) == [], context["done"].stderr
