"""analysis-tools' steps for --json: one object in place of the lines (r53-r56)."""
import json

from pytest_bdd import given, parsers, then

from .analysis_tools_probe_steps import a_python_project
from .analysis_tools_project import (
    CART_ALL,
    TEST_DISCOUNT,
    TEST_ONLY_TOTAL,
    TEST_TOTAL,
    commit,
    interpreter,
    mapped,
    put,
    real,
)

SOURCE = CART_ALL + "\n\ndef refund(order):\n    return -order\n\n\ndef export():\n    return 2\n"


def printed(context):
    return json.loads(context["result"].stdout)


@given(parsers.parse("a map made at commit {label} in which no test executed the functions {first} and {second} in src/cart.py"))
def map_with_two_lost(run, repo, context, label, first, second):
    real()
    a_python_project(repo, context)
    put(repo, {"src/cart.py": SOURCE.replace("refund", first).replace("export", second), "tests/test_cart.py": TEST_ONLY_TOTAL})
    mapped(run, repo, context)
    context["commits"][label] = context["map_commit"]


@given(parsers.parse("a Python project with the tests test_total and test_discount at commit {label}"))
def two_tests_at_commit(repo, context, label):
    real()
    a_python_project(repo, context)
    put(repo, {"tests/test_cart.py": TEST_TOTAL + TEST_DISCOUNT})
    interpreter(context)
    context["commits"][label] = commit(repo)


@then("tools prints one JSON object")
def prints_one_object(context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert isinstance(printed(context), dict)


@then(parsers.parse("the object gives the tests test_total and test_checkout, their count {count:d} and commit {label}"))
def gives_tests(context, count, label):
    assert printed(context) == {"tests": ["tests/test_cart.py::test_total", "tests/test_checkout.py::test_checkout"],
                                "count": count, "of": 5, "commit": context["commits"][label]}


@then(parsers.parse("the object gives the functions {first} and {second}, their count {count:d} and commit {label}"))
def gives_functions(context, first, second, count, label):
    found = printed(context)
    assert [(f["path"], f["name"]) for f in found["functions"]] == [("src/cart.py", first), ("src/cart.py", second)]
    assert (found["count"], found["commit"]) == (count, context["commits"][label])


@then("the object gives the references in src/checkout.py and tests/test_cart.py")
def gives_references(context):
    places = [(ref["path"], ref["line"]) for ref in printed(context)["references"]]
    assert ("src/checkout.py", 5) in places and ("tests/test_cart.py", 5) in places


@then("the object gives the summary: the number of references it gives, 1 production file, 1 test file, and src/cart.py as where total is defined")
def gives_summary(context):
    found = printed(context)
    summary = found["summary"]
    assert (summary["references"], summary["production_files"], summary["test_files"]) == (len(found["references"]), 1, 1)
    assert [place.split(":")[0] for place in summary["defined"]] == ["src/cart.py"]


@then(parsers.parse("the object gives commit {label} and the test count {count:d}"))
def gives_commit_and_count(context, label, count):
    assert printed(context) == {"commit": context["commits"][label], "tests": count}
