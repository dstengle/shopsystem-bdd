"""supervision's steps about a scenario that fails each time it is run: its one second run, alone, before a merge is
refused (r219), and the question that gives both its runs (r220)."""
import re

from pytest_bdd import given, then

from .supervision_world import commit_all, log_lines, write

ALWAYS_FEATURE = """Feature: Thing

  @r1
  Scenario: it closes
    Given a thing
    Then it closes
"""
ALWAYS_STEPS = """from pytest_bdd import given, scenarios, then

scenarios("../features/thing.feature")


@given("a thing")
def a_thing():
    pass


@then("it closes")
def closes(request):
    args = request.config.invocation_params.args
    with open(%r, "a") as runs:
        runs.write(("alone" if any("::" in str(a) for a in args) else "with") + "\\n")
    assert False, "it does not close"
"""


@given("the work-item's scenario \"it closes\", tagged @r1, fails on the implementer's branch each time it is run")
def closes_never(repo):
    """A pytest-bdd suite whose "it closes" fails in every run and notes in `closes.runs` how it was run."""
    write(repo, "features/thing.feature", ALWAYS_FEATURE)
    write(repo, "tests/test_thing.py", ALWAYS_STEPS % str(repo / "closes.runs"))
    (repo / ".shop/delivery.toml").unlink()
    commit_all(repo, "the scenario that never closes")


def runs_of(repo):
    path = repo / "closes.runs"
    return path.read_text().split() if path.exists() else []


@then("\"it closes\" was run once more, alone, after its run with w1's scenarios and before the merge of w1's branch "
      "was refused")
def closes_run_alone(repo, context):
    runs = runs_of(repo)
    assert runs[-1:] == ["alone"] and "with" in runs, (runs, context["done"].stderr)
    text = (repo / ".shop/work/i1/w1.md").read_text()
    assert "status: awaiting-answer" in text, text
    assert not [l for l in log_lines(repo) if l.get("event") == "merged"], log_lines(repo)


@then("\"it closes\" was run no other time")
def closes_run_no_other(repo, context):
    runs = runs_of(repo)
    assert runs.count("alone") == 1, (runs, context["done"].stderr)


@then("w1's ## Questions holds a question giving both runs of \"it closes\": its run with w1's scenarios and its "
      "second run, alone")
def question_gives_both_runs(repo, context):
    text = (repo / ".shop/work/i1/w1.md").read_text()
    held = text.partition("## Questions")[2]
    commands = re.findall(r"`([^`]+)`", held)
    first = [c for c in commands if "::" not in c and "--work-item w1" in c]
    second = [c for c in commands if "::" in c and "test_it_closes" in c]
    assert first and second, (commands, held)
    assert "it does not close" in held.partition(second[0])[2], held
