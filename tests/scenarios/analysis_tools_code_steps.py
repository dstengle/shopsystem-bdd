"""analysis-tools' steps for references and checks: refs and check (r14-r17, r31-r35)."""
import re
import subprocess

from pytest_bdd import given, parsers, then

from .analysis_tools_probe_steps import a_python_project
from .analysis_tools_project import CART, CART_ALL, calls, git, interpreter, lines, put, real, started, under_heading


@given(parsers.parse("a Python project that defines the function total in src/cart.py and refers to it {count:d} times"))
def refers_n_times(repo, context, count):
    real()
    a_python_project(repo, context)
    uses = "".join("    cart.total([%d])\n" % n for n in range(count))
    put(repo, {"src/cart.py": CART_ALL, "src/checkout.py": "import cart\n\n\ndef pay():\n" + uses + "    return 0\n"})


@given("a Python project that defines the function total in src/cart.py")
def defines_total(repo, context):
    real()
    a_python_project(repo, context)
    put(repo, {"src/cart.py": CART_ALL})


@given(parsers.parse("{path} imports total and calls it"))
def imports_and_calls(repo, path):
    call = "total([1])"
    body = ("def test_total():\n    assert %s == 1\n" if path.startswith("tests") else "def pay():\n    return %s\n") % call
    put(repo, {path: "from cart import total\n\n\n" + body})


@given(parsers.parse("{path} imports total under the alias cart_total and calls cart_total"))
def imports_alias(repo, path):
    put(repo, {path: "from cart import total as cart_total\n\n\ndef show():\n    return cart_total([2])\n"})


@given("a Python project in which nothing is defined as `nowhere`")
def nothing_defined(repo, context):
    real()
    a_python_project(repo, context)
    assert "nowhere" not in CART
    context["defines_nothing"] = True


@given("a Python project with import contracts")
def with_contracts(repo, context):
    started(repo, {".importlinter": "[importlinter]\n"})
    context["commits"] = {}
    interpreter(context)


@given(parsers.parse("{tool} prints a finding and the other tools print nothing"))
def reports(context, tool):
    interpreter(context)[tool] = "%s found something" % tool
    context["reporting"] = tool


@given(parsers.parse("a Python project in git with base commit {label}"))
def with_base(repo, context, label):
    a_python_project(repo, context)
    interpreter(context)
    context["commits"][label] = put(repo, {"src/old.py": "B = 1\n", "src/report.py": "C = 1\n", "README.md": "one\n"})


@given(parsers.parse("since {label} src/cart.py and README.md have changed and src/old.py has been deleted"))
def since(repo, context, label):
    (repo / "src" / "old.py").unlink()
    put(repo, {"src/cart.py": "A = 2\n", "README.md": "two\n"})


@given(parsers.parse("a Python project in git with no ref named {ref}"))
def no_ref(repo, context, ref):
    a_python_project(repo, context)
    interpreter(context)
    assert subprocess.run(["git", "rev-parse", "--verify", "-q", ref], cwd=repo, capture_output=True).returncode != 0


@given(parsers.parse("a Python project in git whose Python files are unchanged since base commit {label}"))
def unchanged_since(repo, context, label):
    a_python_project(repo, context)
    interpreter(context).update(ruff="would fail", vulture="would fail")
    context["commits"][label] = git(repo, "rev-parse", "--short", "HEAD")


@given("a Python project that declares no import contracts")
def no_contracts(repo, context):
    a_python_project(repo, context)
    interpreter(context)["import-linter"] = "would fail"


@given("a Python project in which ruff prints nothing for src/cart.py")
def ruff_silent(repo, context):
    a_python_project(repo, context)
    interpreter(context)


# r14, r30
@then("tools prints each reference as `path:line`")
def refs_as_path_line(context):
    assert context["result"].returncode == 0, context["result"].stderr
    for line in lines(context)[:-1]:
        assert re.match(r"^\S+:\d+$", line)


@then("the references printed include the calls in src/checkout.py, src/report.py and tests/test_cart.py")
def refs_include(context):
    for call in ("src/checkout.py:5", "src/report.py:5", "tests/test_cart.py:5"):
        assert call in lines(context)[:-1]


@then(parsers.parse("then it prints one summary line giving the number of references printed, "
                    "{prod:d} production files, {test:d} test file, and {path} as where {name} is defined"))
def summary(context, prod, test, path, name):
    refs = lines(context)[:-1]
    assert lines(context)[-1] == "%d references to %s, in %d production and %d test files; defined at %s:1" % (
        len(refs), name, prod, test, path)


@then("tools names src/cart.py as where total is defined")
def names_definition(context):
    assert lines(context)[-1].endswith("defined at src/cart.py:1")


@then("the definition is not counted as a reference")
def definition_not_counted(context):
    assert "src/cart.py:1" not in lines(context)[:-1]


@then(parsers.parse("{count:d} references are printed"))
def n_refs(context, count):
    assert len(lines(context)) - 1 == count
    assert lines(context)[-1] == "%d reference%s to total, in %d production and 0 test files; defined at src/cart.py:1" % (
        count, "" if count == 1 else "s", 1 if count else 0)


# r16
@then("tools prints a heading for ruff, for vulture and for import-linter")
def headings(context):
    for name in ("ruff", "vulture", "import-linter"):
        assert "== %s ==\n" % name in context["result"].stdout


@then("ruff and vulture are run over src/cart.py and import-linter over the project")
def run_over(context):
    done = {call[0] if call[0] != "python" else call[1]: call for call in calls(context["python"])
            if call[:2] != ["python", "pip"]}
    assert done["ruff"][-1:] == ["src/cart.py"]
    assert done["vulture"][-1:] == ["src/cart.py"]
    assert done["lint-imports"] == ["lint-imports"]


@then(parsers.parse("{tool}'s finding is under {heading}'s heading"))
def finding_under(context, tool, heading):
    assert tool == heading == context["reporting"]
    for name in ("ruff", "vulture", "import-linter"):
        assert under_heading(context["result"].stdout, name) == ("%s found something" % name if name == tool else "clean")


# r17
@then(parsers.parse("under the {tool} heading tools says {same} is missing"))
def heading_missing(context, tool, same):
    assert re.search(r"^missing: \S.+$", under_heading(context["result"].stdout, tool))
    assert tool not in [call[1] for call in calls(context["python"]) if len(call) > 1]


# r31
def checked(context):
    return [call for call in calls(context["python"]) if call[:2] in (["python", "ruff"], ["python", "vulture"])]


@then("tools examines src/cart.py")
def checks_cart(context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert len(checked(context)) == 2
    for call in checked(context):
        assert [a for a in call[2:] if "." in a and not a.startswith("-")] == ["src/cart.py"]


@then("it does not examine README.md, src/old.py or src/report.py")
def does_not_check(context):
    for call in checked(context):
        assert not {"README.md", "src/old.py", "src/report.py"} & set(call)


# r32
@then(parsers.parse("the command is refused because git cannot compare the working tree with {ref}"))
def refused_git(repo, context, ref):
    assert context["result"].returncode == 1
    assert context["result"].stdout == ""
    wanted = subprocess.run(["git", "diff", "--name-only", "--diff-filter=d", ref, "--", "*.py"], cwd=repo,
                            capture_output=True, text=True).stderr.strip()
    assert ref in wanted
    context["git_error"] = wanted


@then("it prints git's error")
def prints_git_error(context):
    assert context["result"].stderr == "tools: %s\n" % context["git_error"]


# r33
@then("under the ruff heading and under the vulture heading tools says `nothing to check`")
def nothing_to_check(context):
    assert under_heading(context["result"].stdout, "ruff") == "nothing to check"
    assert under_heading(context["result"].stdout, "vulture") == "nothing to check"


@then("neither ruff nor vulture makes it exit 1")
def neither_fails(context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert checked(context) == []


# r34
@then("under the import-linter heading tools says `the project states no import contracts`")
def says_no_contracts(context):
    assert under_heading(context["result"].stdout, "import-linter") == "the project states no import contracts"
    assert context["result"].returncode == 0


@then("import-linter is not run")
def linter_not_run(context):
    assert [c for c in calls(context["python"]) if c[0] == "lint-imports"] == []


# r35
@then("under the ruff heading tools says it is clean")
def ruff_clean(context):
    assert under_heading(context["result"].stdout, "ruff") == "clean"


# r49
@then("it says nothing in the project is defined as nowhere")
def says_nothing_defined(context):
    assert context["result"].stderr == "tools: nothing in the project is defined as nowhere\n"
