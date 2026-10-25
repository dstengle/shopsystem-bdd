"""supervision's steps about the measurement of a finished initiative and its analysis: what the branch reviewer's result
lists, `measure initiative` run by `work run`, and the session of analyzing-a-batch it starts."""
from pytest_bdd import given, parsers, then

from .supervision_proposal_steps import drafted
from .supervision_world import git, log_lines, starts

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


@given(parsers.re(r"every worker gives DONE, and the branch reviewer's result gives (?P<outcome>[A-Z_]+), with no question$"))
def reviewer_gives_no_question(plan, outcome):
    plan["default"] = {"status": "DONE"}
    plan["bdd-branch-reviewer"] = {"status": outcome, "questions": []}


@then("no work-item was drafted in i1 for the kept branch review")
def nothing_drafted(repo, context):
    found = drafted(repo)
    assert found == [], (found, context["done"].stderr)


@given("every worker gives DONE, the branch reviewer's result lists nothing to fix now, and the analyzing-a-batch "
       "session writes an analysis file of i1 and ends at its turn limit")
def analyst_turn_limit(plan):
    reviewer_lists_nothing(plan)
    plan["batch-analyst"] = {"notes": {"analysis.md": ANALYSIS}, "subtype": "error_max_turns"}


def analysts(repo):
    return [c for c in starts(repo) if c["agent"] == ANALYST]


@then("a session of analyzing-a-batch was started for i1 once `measure initiative` had written i1's measurement")
def analyst_started(repo, context):
    found, called = measurement(repo), analysts(repo)
    assert len(found) == 1 and len(called) == 1, (found, called, context["done"].stderr)
    assert str(found[0]) in called[0]["brief"], called[0]["brief"]


@then("`work run` ran no `measure initiative` on i1 after the branch review was kept")
def measured_not(repo, context):
    ended = [l for l in log_lines(repo) if l.get("stage") == "branch-review" and l.get("event") == "end"]
    found = measurement(repo)
    assert len(ended) == 1 and found == [], (ended, found, context["done"].stderr)


@then("`work run` ran no `measure initiative` on i1")
def measured_never(repo, context):
    assert measurement(repo) == [] and "measure initiative" not in context["done"].stderr, (
        measurement(repo), context["done"].stderr)


@then("i1's analysis record is not there")
def analysis_not_there(repo, context):
    records = sorted((repo / ".shop/records").glob("*-i1-analysis.md")) if (repo / ".shop/records").is_dir() else []
    assert records == [], (records, context["done"].stderr)


@then("the initiative branch has a commit of i1's measurement and i1's analysis record")
def records_committed(repo, context):
    found = [str(p.relative_to(repo)) for p in measurement(repo) + sorted((repo / ".shop/records").glob("*-i1-analysis.md"))]
    assert len(found) == 2, (found, context["done"].stdout, context["done"].stderr)
    for path in found:
        assert git(repo, "ls-files", "--", path).strip() == path, (path, context["done"].stderr)
        assert git(repo, "log", "--format=%H", "--", path).split(), path


@then("nothing under .shop/records/ is left uncommitted")
def records_clean(repo):
    assert git(repo, "status", "--porcelain", "--untracked-files=all", "--", ".shop/records").strip() == ""


@then("i1's analysis record is there")
def analysis_there(repo, context):
    records = sorted((repo / ".shop/records").glob("*-i1-analysis.md"))
    assert [r.read_text() for r in records] == [ANALYSIS], (records, context["done"].stderr)
