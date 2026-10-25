"""supervision's steps about the measurement of a finished initiative and its analysis: what the branch reviewer's result
lists, `measure initiative` run by `work run`, and the session of analyzing-a-batch it starts."""
from pytest_bdd import given, then

from .supervision_world import log_lines, starts

MEASUREMENTS = ".shop/records/measurements"
ANALYST = "shopsystem-bdd:batch-analyst"
ANALYSIS = "# analysis of i1\nThe stand-in's analysis.\n"


def measurement(repo):
    return sorted((repo / MEASUREMENTS).glob("*-i1.md")) if (repo / MEASUREMENTS).is_dir() else []


@given("every worker gives DONE, and the branch reviewer's result lists nothing to fix now")
def reviewer_lists_nothing(plan):
    plan["default"] = {"status": "DONE"}
    plan["bdd-branch-reviewer"] = {"questions": []}


@then("`work run` ran `measure initiative` on i1 after the branch review was kept")
def measured_after_review(repo, context):
    ended = [l for l in log_lines(repo) if l.get("stage") == "branch-review" and l.get("event") == "end"]
    found = measurement(repo)
    assert len(ended) == 1 and len(found) == 1, (ended, found, context["done"].stderr)
    assert found[0].stat().st_mtime_ns >= (repo / ".shop/work/i1/runs/branch-review/1/brief.md").stat().st_mtime_ns


@given("every worker gives DONE, the branch reviewer's result lists nothing to fix now, and the analyzing-a-batch "
       "session writes i1's analysis record")
def analyst_writes_record(plan):
    reviewer_lists_nothing(plan)
    plan["batch-analyst"] = {"notes": {"analysis.md": ANALYSIS}}


def analysts(repo):
    return [c for c in starts(repo) if c["agent"] == ANALYST]


@then("a session of analyzing-a-batch was started for i1 once `measure initiative` had written i1's measurement")
def analyst_started(repo, context):
    found, called = measurement(repo), analysts(repo)
    assert len(found) == 1 and len(called) == 1, (found, called, context["done"].stderr)
    assert str(found[0]) in called[0]["brief"], called[0]["brief"]


@then("i1's analysis record is there")
def analysis_there(repo, context):
    records = sorted((repo / ".shop/records").glob("*-i1-analysis.md"))
    assert [r.read_text() for r in records] == [ANALYSIS], (records, context["done"].stderr)
