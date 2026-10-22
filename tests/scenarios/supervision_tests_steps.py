"""supervision's steps about the tests `work run` runs: the commands, the --work-item they are given, and what the
whole suite before a merge counts as expected."""
from pytest_bdd import given, parsers, then

from .supervision_world import DELIVERY, calls, commit_all, git, item_text, log_lines, work_commits, write


@given(".shop/delivery.toml gives [tests] with `python3 tests.py --work-item w1` for the work-item's scenarios and "
       "`python3 tests.py` for the suite")
def delivery_tests(repo):
    assert (repo / ".shop/delivery.toml").read_text() == DELIVERY


@then("`work run` ran `python3 tests.py --work-item w1` for w1's scenarios and `python3 tests.py` for the suite")
def ran_delivery_tests(repo, context):
    ran = [c["argv"] for c in calls(repo, ("tests",))]
    assert ["--work-item", "w1"] in ran and [] in ran, (ran, context["done"].stderr)
    assert all(argv in (["--work-item", "w1"], []) for argv in ran), ran
    assert calls(repo, ("pytest",)) == [], calls(repo, ("pytest",))


@given(".shop/delivery.toml gives no [tests]")
def no_tests(repo):
    (repo / ".shop/delivery.toml").unlink()
    commit_all(repo, "no [tests]")


@then("each pytest command `work run` ran for w1, for its scenarios and for the whole suite, was given --work-item w1")
def pytest_given_work_item(repo, context):
    ran = calls(repo, ("pytest",))
    suites = [c for c in ran if "--whole-suite" in c["args"]]
    assert suites and len(suites) < len(ran), (ran, context["done"].stderr)
    assert all(c["work_item"] == "w1" for c in ran), ran


@then("the implementer's `python3 -m pytest -q` ran with --work-item w1")
def worker_pytest(repo, context):
    ran = [c for c in calls(repo, ("pytest",)) if c["args"] == ["-q"]]
    assert len(ran) == 1 and ran[0]["work_item"] == "w1", (calls(repo, ("pytest",)), context["done"].stderr)


@given(parsers.parse("every worker gives DONE, the planner's result giving a `fileset` of {first} and {second}"))
def planner_fileset(plan, first, second):
    plan["default"] = {"status": "DONE"}
    plan["bdd-planner"] = {"fields": {"fileset": [first, second]}}


@then(parsers.parse("the commit of w1's transition to planned writes `fileset:` {first} and {second} into "
                    ".shop/work/i1/w1.md"))
def fileset_written(repo, context, first, second):
    made = [sha for sha, subject in work_commits(repo) if subject == "work: w1 researched -> planned"]
    assert len(made) == 1, (work_commits(repo), context["done"].stderr)
    text = git(repo, "show", "%s:.shop/work/i1/w1.md" % made[0])
    assert "\nfileset: [%s, %s]\n" % (first, second) in text, text


THING_FEATURE = """Feature: Thing

  @r1
  Scenario: it answers
    Given a thing
    Then it answers

  @r2
  Scenario: it waits
    Given a thing
    Then it waits
"""
THING_STEPS = """from pytest_bdd import given, scenarios, then

scenarios("../features/thing.feature")


@given("a thing")
def a_thing():
    pass


@then("it answers")
def answers():
    pass


@then("it waits")
def waits():
    assert False, "it does not wait yet"
"""


@given(parsers.parse("i1's work-item w1 is ready, accepting thing#r1, w2 is drafted, w3 is green and w4 is withdrawn"))
def four_items(repo):
    for name, status in (("w1", "ready"), ("w2", "drafted"), ("w3", "green"), ("w4", "withdrawn")):
        text = item_text(name, status).replace("accepts: [thing#r1]", "accepts: [%s]" % ("thing#r1" if name == "w1" else "thing#r3"))
        write(repo, ".shop/work/i1/%s.md" % name, text)
    commit_all(repo, "four work-items")


@given('features/thing.feature has the scenario "it waits", tagged @r2, which fails')
def thing_waits(repo):
    """A pytest-bdd suite: "it answers" (@r1, w1's) passes and "it waits" (@r2) fails; work run's own commands run it."""
    write(repo, "features/thing.feature", THING_FEATURE)
    write(repo, "tests/test_thing.py", THING_STEPS)
    (repo / ".shop/delivery.toml").unlink()
    commit_all(repo, "the thing's suite")


@given(parsers.parse("thing#r2 is accepted by {who}"))
def r2_accepted(repo, who):
    names = [] if who == "no work-item" else who.replace(" only", "").split(" and ")
    for name in names:
        path = repo / (".shop/work/i1/%s.md" % name)
        path.write_text(path.read_text().replace("accepts: [", "accepts: [thing#r2, "))
    commit_all(repo, "thing#r2 accepted")


@then(parsers.parse('the whole suite `work run` ran before w1\'s merge counted "it waits" as {counted}'))
def counted_as(repo, context, counted):
    records = [l["record"] for l in log_lines(repo) if l.get("event") == "suite" and l.get("stage") == "merge"
               and l.get("work-item") == "w1"]
    assert len(records) == 1, (log_lines(repo), context["done"].stdout, context["done"].stderr)
    failing = records[0].partition("; failing: ")[2].partition("; expected: ")[0]
    expected = records[0].partition("; expected: ")[2]
    assert ("test_it_waits" in expected, "test_it_waits" in failing) == (
        (True, False) if counted == "expected" else (False, True)), records[0]
