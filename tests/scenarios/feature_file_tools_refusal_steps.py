"""feature-file-tools' Thens for refused commands: what the refusal says and that no file changed."""
import re

from pytest_bdd import parsers, then

from .feature_file_tools_files import refused, rejected, snapshot


# --- Then: refusals ---------------------------------------------------------------------------------------------

@then("the command is rejected because the feature file has a Rule: block")
def rejected_rule(context):
    assert "Rule: blocks are not supported" in rejected(context)


@then(parsers.re(r"the refusal names (?P<names>.+)"))
def refusal_names(repo, context, names):
    reason = context["result"].stderr
    if names == "no file":
        assert not re.findall(r"features/\w+\.feature", reason)
        return
    if names == "tests/test_cart.py and line 20":
        assert "tests/test_cart.py:20" in reason
        return
    wanted = re.split(r", | and ", names)
    for name in wanted:
        assert name in reason
    if context.get("exact_files"):  # r10: every file with the title, no other
        assert re.findall(r"features/\w+\.feature", reason) == wanted
    if names == "tests/test_broken.py":
        assert "tests/test_broken.py does not parse" in reason


@then("the edit is rejected because features could not read the result, and every file is as it was")
def edit_rejected(repo, context):
    assert "Rule:" in rejected(context)
    assert "features/cart.feature" in rejected(context)  # r2: naming the file
    assert snapshot(repo) == context["before"]


@then("the edit is made")
def edit_made(run, repo, context):
    result = context["result"]
    assert result.returncode == 0, result.stderr
    assert "Scenario: " + context["title"] in (repo / "features" / "cart.feature").read_text()
    if context["result_wanted"].startswith("two"):
        listed = run("features", "list", "--title", "Apply a code")
        assert listed.stdout == "features/cart.feature: Apply a code\n" * 2


@then("the command is rejected because no file has the title")
def rejected_no_file_has_title(context):
    assert "no scenario titled 'Apply a code'" in rejected(context)


@then("the command is rejected because several files have the title")
def rejected_several_have_title(context):
    reason = rejected(context)
    assert "several" in reason
    assert "features/cart.feature, features/old.feature" in reason


@then("the command is rejected because the title is not in exactly one file")
def rejected_not_one(context):
    rejected(context)


@then("no file is changed")
def no_file_changed(repo, context):
    assert snapshot(repo) == context["before"]


@then("no test module is changed")
def no_module_changed(repo, context):
    assert snapshot(repo) == context["before"]


@then("the command is rejected as bad usage because the tag is not written r<n>")
def rejected_bad_usage(repo, context):
    result = context["result"]
    assert result.returncode == 2
    assert "r<n>" in result.stderr and "slice" not in result.stderr
    assert snapshot(repo) == context["before"]


@then("the command is rejected because the destination does not exist")
def rejected_no_destination(repo, context):
    assert "features/missing.feature does not exist" in rejected(context)


@then("the command is rejected because the destination is the scenario's own file")
def rejected_own_file(context):
    assert "is the scenario's own file" in rejected(context)


@then("the reason for the refusal is written to stderr")
def reason_on_stderr(context):
    result = context["result"]
    assert result.stdout == ""
    assert result.stderr == "features: 'Apply a code' is not tagged @deprecated: only a deprecated scenario is retired here\n"


@then("the command is rejected because the test module does not parse")
def rejected_unparsed(context):
    assert "does not parse" in rejected(context)


@then("the command is rejected because no scenario has the new title")
def rejected_no_new_title(context):
    assert "no scenario titled 'Apply a voucher'" in rejected(context)


@then("the command is rejected because several feature files have the new title")
def rejected_several_new_title(context):
    reason = rejected(context)
    assert "several" in reason
    assert "features/cart.feature, features/codes.feature" in reason


@then("the command is rejected because the binding's title is written over several lines")
def rejected_multiline(context):
    assert "tests/test_cart.py:20: the title is written over several lines" in rejected(context)


@then("the command is rejected because the file does not have the title")
def rejected_file_lacks_title(run, repo, context):
    assert "does not have" in rejected(context)
    for command in (("deprecate", "Voucher", "--for-removal"), ("retire", "Voucher"), ("move", "Voucher", "--to", "features/old.feature")):
        reason = refused(run, repo, *command, "--file", "features/cart.feature")
        assert "features/cart.feature" in reason and "does not have" in reason


@then("the command is rejected because the file has the title twice")
def rejected_file_twice(run, repo, context):
    assert "twice" in rejected(context)
    for command in (("deprecate", "Apply a code", "--for-removal"), ("move", "Apply a code", "--to", "features/old.feature")):
        reason = refused(run, repo, *command, "--file", "features/cart.feature")
        assert "features/cart.feature" in reason and "twice" in reason


@then("the command is rejected because the file is outside --dir")
def rejected_outside(run, repo, context):
    assert "outside" in rejected(context)
    for path in ("elsewhere/other.feature", "features/../elsewhere/other.feature"):
        for command in (("tag", "Apply a code", "r7"), ("deprecate", "Apply a code", "--for-removal"), ("retire", "Apply a code"),
                        ("move", "Apply a code", "--to", "features/codes.feature")):
            assert "outside" in refused(run, repo, *command, "--file", path)


@then("the command is rejected because a title is one line")
def rejected_two_line_title(context):
    assert "one line" in rejected(context)
