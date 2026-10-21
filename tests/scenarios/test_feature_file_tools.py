"""features/feature-file-tools.feature, bound to scripts/features: every scenario of the file, by `scenarios()`.

A Given writes the feature files, test modules and trees a scenario names into `repo`; the When runs `features`
once and keeps the files as they were (`context["before"]`); the Then steps read what it printed and what it left.
The steps live in feature_file_tools_*_steps.py, beside what they share (feature_file_tools_files.py).
"""
import shlex

import pytest
from pytest_bdd import parsers, scenarios, then, when

from .feature_file_tools_check_steps import *  # noqa: F401,F403  the steps are fixtures pytest-bdd finds by their names here
from .feature_file_tools_edit_steps import *  # noqa: F401,F403
from .feature_file_tools_files import snapshot
from .feature_file_tools_given_steps import *  # noqa: F401,F403
from .feature_file_tools_refusal_steps import *  # noqa: F401,F403
from .feature_file_tools_tree_steps import *  # noqa: F401,F403

scenarios("feature-file-tools.feature")


# --- the checks every scenario ends with --------------------------------------------------------------------

@pytest.fixture(autouse=True)
def whole_output(context):
    """After each scenario: features never crashed, and a listing had exactly the lines the scenario said it lists."""
    yield
    result = context.get("result")
    if result is not None:
        assert "Traceback" not in result.stderr
    if "listed" in context:
        assert sorted(result.stdout.splitlines()) == sorted(context["listed"])


# --- When -------------------------------------------------------------------------------------------------------

def invoke(run, repo, context, argv):
    context["before"] = snapshot(repo)
    context["result"] = run("features", *argv)


@when(parsers.re(r"the agent runs features (?P<args>.+?)(?: without --(?:dir|tests|file))?"))
def agent_runs(run, repo, context, args):
    invoke(run, repo, context, shlex.split(args))


@when("the agent runs that edit")
def agent_runs_edit(run, repo, context):
    invoke(run, repo, context, context["edit"])



@when('the agent deprecates "Apply a code" for a new title written over two lines')
def agent_deprecates_two_lines(run, repo, context):
    invoke(run, repo, context, ["deprecate", "Apply a code", "--for", "Apply a voucher\n  Scenario: Injected"])

# --- Then: what a listing printed -------------------------------------------------------------------------------

@then(parsers.re(r'the output lists (?P<path>\S+) with "(?P<title>[^"]+)"'))
def output_lists(context, path, title):
    result = context["result"]
    assert result.returncode == 0, result.stderr
    line = "%s: %s" % (path, title)
    assert line in result.stdout.splitlines(), result.stdout
    context.setdefault("listed", []).append(line)


@then(parsers.re(r'the output does not list "(?P<one>[^"]+)"(?: or "(?P<two>[^"]+)")?'))
def output_does_not_list(run, repo, context, one, two):
    for text in (one, two):
        if text:
            assert text not in context["result"].stdout
    if one == "Phantom":  # r1: the docstring's scenario is not found by its title either
        done = run("features", "list", "--title", "Phantom")
        assert (done.returncode, done.stdout) == (1, "")


@then("nothing is printed")
def nothing_printed(context):
    assert context["result"].stdout == ""


@then(parsers.parse("it exits {code:d}"))
def exits(context, code):
    result = context["result"]
    assert result.returncode == code, result
    assert "Traceback" not in result.stderr


# --- Then: counting (r4) ----------------------------------------------------------------------------------------

@then("it prints 5 scenarios for cart, 1 for slice-1, 3 for slice-2 and 2 for r3")
def counts_by_tag(context):
    result = context["result"]
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[:-1] == ["cart 5", "r3 2", "slice-1 1", "slice-2 3"]


@then("it prints a total of 6")
def counts_total(context):
    assert context["result"].stdout == "cart 5\nr3 2\nslice-1 1\nslice-2 3\ntotal 6\n"
