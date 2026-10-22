"""supervision's steps about the tests `work run` runs: the commands, the --work-item they are given, and what the
whole suite before a merge counts as expected."""
from pytest_bdd import given, parsers, then

from .supervision_world import DELIVERY, calls, commit_all


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
