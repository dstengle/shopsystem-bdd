"""features/analysis-tools.feature, bound to scripts/tools.

A Given describes the project and the interpreter in `repo` and `context`; the When runs `tools` once, and the
Then steps read what it printed. The interpreter is a stand-in (FAKE) that answers as its config says and logs
what it is asked to run, except where a scenario needs the real coverage map or jedi: then it is this Python.
"""
import importlib.util
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("analysis-tools.feature")

HAVE = all(importlib.util.find_spec(name) for name in ("coverage", "pytest_cov", "jedi", "pytest"))
MAP = ".shop/scratch/tools/coverage"
NAMES = ("coverage", "pytest-cov", "jedi", "ast-grep", "ruff", "vulture", "import-linter", "hypothesis")

CART = """\"\"\"The cart.\"\"\"


def refund(order):
    return -order


def total(items):
    \"\"\"Sum the items.\"\"\"
    return sum(items)


class Cart:
    def total(self, items):
        return sum(items)
"""
CART_ALL = "def total(items):\n    return sum(items)\n"
OTHER = "def other():\n    return 1\n"
TEST_TOTAL = "from cart import Cart, total\n\n\ndef test_total():\n    assert Cart().total([1, 2]) == 3\n    assert total([1]) == 1\n"
TEST_ONLY_TOTAL = "from cart import total\n\n\ndef test_total():\n    assert total([1]) == 1\n"
TEST_DISCOUNT = "\n\ndef test_discount():\n    assert Cart().total([4]) == 4\n"
TEST_CHECKOUT = "from cart import Cart\n\n\ndef test_checkout():\n    assert Cart().total([5]) == 5\n"

# stands in for an interpreter (and for lint-imports) beside it: answers as the config beside it says
FAKE = r"""import json, os, runpy, sys
here = os.path.dirname(os.path.abspath(__file__))
config = json.load(open(os.path.join(here, "fake.json")))
tool, args = os.path.basename(sys.argv[0]), sys.argv[1:]
REAL = %r


def note(*words):
    with open(config["log"], "a") as log:
        log.write(json.dumps([tool, *words]) + "\n")


def reply(text, failing=True):
    if text:
        print(text)
    sys.exit(1 if text and failing else 0)


if tool == "lint-imports":
    note(*args)
    reply(config.get("import-linter", ""))
if args[:1] == ["-c"]:
    found = {name: (None if name in config["missing"] else "1.0") for name in args[2:]}
    print(json.dumps(dict(found, virtualenv=config["venv"])))
    sys.exit(0)
if args[:3] == ["-m", "pip", "install"]:
    note(*args[1:])
    if config["pip_fails"]:
        sys.stderr.write(config["pip_error"])
        sys.exit(1)
    sys.exit(0)
if args[:1] == ["-m"] and args[1] in ("ruff", "vulture"):
    note(*args[1:])
    reply(config.get(args[1], ""))
if args[:2] == ["-m", "pytest"]:
    note(*args[1:])
    if config["pytest"] == "noop":
        reply(config["pytest_out"], failing=False)
    os.execv(REAL, [REAL] + args)
for blocked in config["block"]:
    sys.modules[blocked] = None
sys.executable = os.path.abspath(sys.argv[0])
sys.argv = args
runpy.run_path(args[0], run_name="__main__")
""" % sys.executable


# --- the project ---

def git(root, *args):
    done = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=root,
                          capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    return done.stdout.strip()


def commit(root, message="m"):
    git(root, "add", "-A")
    git(root, "commit", "-q", "--allow-empty", "-m", message)
    return git(root, "rev-parse", "--short", "HEAD")


def put(root, files):
    """Write these files into the project and commit them; return the commit."""
    for name, text in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(text)
    return commit(root)


def started(root, files=None):
    """The project as a git repository with a pytest.ini and src/cart.py, once; these files added."""
    if not (root / ".git").exists():
        git(root, "init", "-q")
        files = {"pytest.ini": "[pytest]\ntestpaths = tests\npythonpath = src\n", "src/cart.py": CART, **(files or {})}
    return put(root, files or {})


def real():
    if not HAVE:
        pytest.skip("coverage, pytest-cov and jedi are needed")


# --- the interpreter ---

@pytest.fixture
def outside(tmp_path_factory):
    """A new empty directory outside the project."""
    return lambda: tmp_path_factory.mktemp("outside").resolve()


def fake(where, **config):
    """An interpreter at <where>/bin/python that answers as a virtualenv with the tools it is told to have,
    logs what it is asked to run in <where>/calls.log, and runs the rest as the real one."""
    (where / "bin").mkdir(parents=True)
    config = {"missing": [], "venv": True, "pip_fails": False, "pip_error": "", "pytest": "run",
              "pytest_out": "", "block": [], **config, "log": str(where / "calls.log")}
    (where / "bin" / "fake.json").write_text(json.dumps(config))
    for name in ("python", "lint-imports"):
        (where / "bin" / name).write_text("#!%s\n%s" % (sys.executable, FAKE))
        (where / "bin" / name).chmod(0o755)
    return where / "bin" / "python"


def interpreter(context):
    """The config of the stand-in interpreter, made on first use."""
    return context.setdefault("fake", {})


def missing_tools(context, tools, venv=True):
    names = tools.split(" and ")
    interpreter(context).update(missing=names, block=names, venv=venv)


def calls(python):
    log = pathlib.Path(python).parent.parent / "calls.log"
    return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []


def pip_calls(python):
    return [call[3] for call in calls(python) if call[:3] == ["python", "pip", "install"]]


def under_heading(stdout, name):
    return stdout.split("== %s ==\n" % name)[1].split("== ")[0].strip()


# --- running tools ---

def invoke(run, repo, context, argv, outside=None):
    """Run tools in the project: with the stand-in or the --python given, or the real one; its map made first if wanted."""
    if "fake" in context and "python" not in context:
        context["python"] = fake(outside(), **context["fake"])
    option = []
    if "python" in context or not context.get("discover"):
        option = ["--python", str(context.get("python", sys.executable))]
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    env.update(context.get("env", {}))
    return run("tools", *option, *argv, cwd=repo, env=env)


def mapped(run, repo, context):
    done = invoke(run, repo, context, ["map"])
    assert done.returncode == 0, done.stderr
    context["map_commit"] = git(repo, "rev-parse", "--short", "HEAD")


@given("a Python project in the current directory")
@given("a Python project")
def a_python_project(repo, context):
    started(repo)
    context["commits"] = {}


@given("a project with no Python in it")
def no_python(repo, context):
    (repo / "main.go").write_text("package main\n")


@given(parsers.re(r"the project has (?P<which>.+?), and \$VIRTUAL_ENV points at /opt/env(?P<rest>.*)"))
def virtualenvs(repo, context, outside, which, rest):
    a_python_project(repo, context)
    context["discover"] = True
    if "neither" not in which and "no .venv" not in which:
        fake(repo / ".venv")
    if "neither" not in which:
        fake(repo / "venv")
    env_dir = outside()
    if "has no bin/python" in rest:
        (env_dir / "bin").mkdir()
    else:
        fake(env_dir)
    context["env"] = {"VIRTUAL_ENV": str(env_dir)}
    context["env_dir"] = env_dir


@given(parsers.parse("a Python project whose interpreter has every tool but {tool}"))
def all_but(repo, context, tool):
    a_python_project(repo, context)
    missing_tools(context, tool)


@given(parsers.parse("a Python project whose interpreter is a virtualenv missing {tools}"))
def venv_missing(repo, context, tools):
    a_python_project(repo, context)
    missing_tools(context, tools)


@given(parsers.parse("a Python project whose interpreter is not a virtualenv and is missing {tools}"))
def no_venv_missing(repo, context, tools):
    a_python_project(repo, context)
    missing_tools(context, tools, venv=False)


@given(parsers.parse("a Python project whose interpreter is missing {tools}"))
def interpreter_missing(repo, context, tools):
    a_python_project(repo, context)
    missing_tools(context, tools)


@given(parsers.parse("a Python project whose interpreter {kind} and has every tool"))
def all_present(repo, context, kind):
    a_python_project(repo, context)
    interpreter(context).update(venv=kind == "is a virtualenv")


@given("a Python project with a pyproject.toml and a requirements.txt")
def with_dependency_files(repo, context):
    started(repo, {"pyproject.toml": "[project]\nname = 'cart'\n", "requirements.txt": "pytest\n"})
    context["commits"] = {}


@given("its interpreter is a virtualenv missing jedi and vulture")
def its_interpreter_missing(context):
    missing_tools(context, "jedi and vulture")


@given(parsers.parse("installing {tool} with pip fails"))
def pip_fails(context, tool):
    interpreter(context).update(pip_fails=True, pip_error="e1\ne2\ne3\ne4\ne5\nerror: no matching distribution")


@given(parsers.parse("{tool} installs with pip"))
def pip_works(context, tool):
    interpreter(context).update(pip_fails=False)


@given("a Python project with the tests test_total and test_discount")
def with_two_tests(repo, context):
    a_python_project(repo, context)
    put(repo, {"tests/test_cart.py": TEST_TOTAL + TEST_DISCOUNT})
    interpreter(context)


@given(parsers.parse("a map of {count:d} tests made at commit {label}"))
def map_of(context, count, label):
    context["commits"] = {}
    context["planned"] = (count, label)


# what each form of target makes executable: the call both tests make, and the other tests that would show the form ignored
OTHERS = [("test_other_%d" % n, "from other import other", "other()") for n in range(3)]
REFUND = ("test_refund", "from cart import refund", "refund(1)")
PLAIN = ("test_plain", "from cart import total", "total([1])")
FORMS = (("the file", "Cart().total([1])", OTHERS), ("the function", "total([1])", [REFUND] + OTHERS[:2]),
         ("the method", "Cart().total([1])", [PLAIN, REFUND] + OTHERS[:1]), ("lines", "total([1])", [REFUND] + OTHERS[:2]))


@given(parsers.parse("test_total and test_checkout executed {target} and no other test did"))
def executed_target(run, repo, context, target):
    real()
    count, label = context["planned"]
    call, extras = next((call, extras) for form, call, extras in FORMS if target.startswith(form))
    assert 2 + len(extras) == count
    files = {"tests/test_cart.py": "from cart import Cart, total\n\n\ndef test_total():\n    assert %s\n" % call,
             "tests/test_checkout.py": "from cart import Cart, total\n\n\ndef test_checkout():\n    assert %s\n" % call,
             "tests/test_extra.py": "".join("%s\n\n\ndef %s():\n    assert %s\n\n\n" % (imp, name, body)
                                            for name, imp, body in extras),
             "src/other.py": OTHER}
    started(repo, files)
    mapped(run, repo, context)
    context["commits"][label] = context["map_commit"]


@given("a map in which two tests in tests/test_cart.py and one test in tests/test_checkout.py executed src/cart.py")
def by_file_map(run, repo, context):
    real()
    a_python_project(repo, context)
    put(repo, {"tests/test_cart.py": TEST_TOTAL + TEST_DISCOUNT, "tests/test_checkout.py": TEST_CHECKOUT})
    mapped(run, repo, context)


@given("a map has been made")
def a_map_has_been_made(run, repo, context):
    real()
    a_python_project(repo, context)
    put(repo, {"tests/test_cart.py": TEST_TOTAL})
    mapped(run, repo, context)


@given(parsers.parse("no test in the map executed the function {name}"))
def nothing_executed(run, repo, context, name):
    put(repo, {"src/cart.py": CART + "\n\ndef %s():\n    return 0\n" % name})
    mapped(run, repo, context)
    context["unexecuted"] = name


@given(parsers.parse("src/cart.py has no function named {name}"))
def no_function_named(repo, context, name):
    assert "def %s" % name not in (repo / "src" / "cart.py").read_text()
    context["absent"] = name


@given("a Python project for which no map has been made")
def no_map(repo, context):
    real()
    a_python_project(repo, context)


@given("a map in which no test executed the function refund in src/cart.py or the function export in src/report.py")
def refund_export_map(repo, context):
    real()
    a_python_project(repo, context)
    put(repo, {"src/cart.py": "def total(items):\n    return sum(items)\n\n\ndef refund(order):\n    return -order\n",
               "src/report.py": "def build():\n    return 1\n\n\ndef export():\n    return 2\n"})


@given("every other function in those files was executed by a test")
def the_others_executed(run, repo, context):
    put(repo, {"tests/test_cart.py": "from cart import total\nfrom report import build\n\n\n"
                                     "def test_total():\n    assert total([1]) == 1\n    assert build() == 1\n"})
    mapped(run, repo, context)


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


@given(parsers.parse("{tool} reports a finding and the other tools report nothing"))
def reports(context, tool):
    interpreter(context)[tool] = "%s found something" % tool
    context["reporting"] = tool


@given("`--python` names an interpreter that fails when run")
def broken_interpreter(outside, context):
    broken = outside() / "broken"
    broken.write_text("#!/bin/sh\necho 'boom: cannot start' >&2\nexit 3\n")
    broken.chmod(0o755)
    context["python"] = broken


@given("a Python project with a map made at an earlier commit")
def earlier_map(run, repo, context):
    real()
    a_python_project(repo, context)
    put(repo, {"tests/test_cart.py": TEST_TOTAL,
               "tests/test_old.py": "from cart import total\n\n\ndef test_old():\n    assert total([1])\n"})
    mapped(run, repo, context)
    earlier = invoke(run, repo, context, ["tests-of", "src/cart.py"]).stdout
    assert "test_old" in earlier


@given(parsers.parse("the project is at commit {label} and its suite {outcome}"))
def new_commit(repo, context, label, outcome):
    (repo / "tests" / "test_old.py").unlink()
    context["last_line"] = "1 passed"
    if outcome != "passes":
        (repo / "tests" / "test_broken.py").write_text("def test_broken():\n    assert False\n")
        context["last_line"] = "1 failed, 1 passed"
    context["commits"][label] = commit(repo)


@given("a Python project in which running the suite under coverage leaves no map")
def leaves_no_map(repo, context):
    a_python_project(repo, context)
    interpreter(context).update(pytest="noop", pytest_out="collected nothing at all")


@given(parsers.parse("a map made at commit {label} in which no test executed {count:d} functions in src/cart.py"))
def map_with_lost(run, repo, context, label, count):
    real()
    a_python_project(repo, context)
    text = CART_ALL + "".join("\n\ndef lost_%d():\n    return %d\n" % (n, n) for n in range(count))
    put(repo, {"src/cart.py": text, "tests/test_cart.py": TEST_ONLY_TOTAL})
    mapped(run, repo, context)
    context["commits"][label] = context["map_commit"]
    context["source"] = text


@given("the project has no file src/gone.py")
def no_gone(repo):
    assert not (repo / "src" / "gone.py").exists()


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


@given("a Python project that states no import contracts")
def no_contracts(repo, context):
    a_python_project(repo, context)
    interpreter(context)["import-linter"] = "would fail"


@given("a Python project in which ruff prints nothing for src/cart.py")
def ruff_silent(repo, context):
    a_python_project(repo, context)
    interpreter(context)


# --- the agent runs tools ---

@when(parsers.parse("the agent runs `tools {args}`"))
def agent_runs(run, repo, context, outside, args):
    for label, commit_ in context.get("commits", {}).items():
        args = args.replace(label, commit_)
    if "--python /opt/py/bin/python" in args:  # the option goes before the command, where invoke puts it
        context["py"] = context["python"] = fake(outside() / "py")
        args = args.replace("--python /opt/py/bin/python", "")
    argv = shlex.split(args)
    context["args"] = argv
    context["result"] = invoke(run, repo, context, argv, outside)


@then(parsers.parse("it exits {code:d}"))
def exits(run, repo, context, outside, code):
    result = context["result"]
    assert result.returncode == code, result
    assert "Traceback" not in result.stderr
    if "absent" in context:  # r11: a function the file does not have
        assert result.stdout == ""
        assert result.stderr == "tools: src/cart.py has no function named %s\n" % context["absent"]
        assert invoke(run, repo, context, ["tests-of", "src/cart.py:total"], outside).returncode == 0
    if "unexecuted" in context:  # r11: a function no test executed
        assert "0 of the 1 tests in the map executed" in result.stdout
    if context.get("defines_nothing"):  # r15
        assert result.stdout == ""


def lines(context):
    return context["result"].stdout.splitlines()


# r1
@then(parsers.parse("tools prints the path of {interpreter}"))
def prints_interpreter(repo, context, interpreter):
    expected = {"/opt/py/bin/python": lambda: context["py"],
                "the .venv/bin/python under the current directory": lambda: repo / ".venv" / "bin" / "python",
                "the venv/bin/python under the current directory": lambda: repo / "venv" / "bin" / "python",
                "/opt/env/bin/python": lambda: context["env_dir"] / "bin" / "python",
                "the interpreter running the script": lambda: pathlib.Path(sys.executable)}[interpreter]()
    assert lines(context)[-1].startswith("python: %s (" % expected), lines(context)[-1]


@then(parsers.parse("it says the interpreter came from {source}"))
def says_source(context, source):
    last = lines(context)[-1]
    assert last.endswith("(%s)" % source) if source != "neither" else "(no virtualenv found" in last, last


# r2
@then("tools says in one line that no analysis tools are known for its language")
def no_tools_known(context):
    stderr = context["result"].stderr
    assert "no analysis tools are known for this project's language" in stderr
    assert len(stderr.strip().splitlines()) == 1


# r3
@then("tools prints one line for each tool")
def line_each(context):
    assert len(lines(context)) == len(NAMES) + 1
    assert [line.split()[0] for line in lines(context)[:-1]] == list(NAMES)


@then("each installed tool's line gives its name and version")
def installed_lines(context):
    for line in lines(context)[:-1]:
        if not line.startswith("vulture"):
            assert line == "%s 1.0" % line.split()[0]


@then("vulture's line says it is missing and what it is for")
def vulture_missing(context):
    assert re.search(r"^vulture missing: \S.+$", "\n".join(lines(context)), re.M)


@then("the interpreter is printed after the tools")
def interpreter_last(context):
    assert lines(context)[-1] == "python: %s (--python)" % context["python"]


# r4
@then("tools prints exactly one line, and it begins `Probe: tools -> `")
def one_probe_line(context):
    assert len(lines(context)) == 1
    assert re.match(r"^Probe: tools -> coverage \S+, pytest-cov \S+, jedi \S+, .*hypothesis \S+$", lines(context)[0])


# r5
@then(parsers.parse("{tools} are installed into the interpreter with pip"))
def installed_with_pip(context, tools):
    assert context["result"].returncode == 0, context["result"].stderr
    assert pip_calls(context["python"]) == tools.split(" and ")


@then("pyproject.toml and requirements.txt are unchanged")
def dependency_files_unchanged(repo):
    assert (repo / "pyproject.toml").read_text() == "[project]\nname = 'cart'\n"
    assert (repo / "requirements.txt").read_text() == "pytest\n"
    assert git(repo, "status", "--porcelain") == ""


# r6
@then("the install is refused because the interpreter is not a virtualenv")
def install_refused(context):
    assert context["result"].returncode == 1
    assert "is not a virtualenv" in context["result"].stdout


@then(parsers.parse("{tool} is still missing from the interpreter"))
def still_missing(run, repo, context, outside, tool):
    assert pip_calls(context["python"]) == []
    assert "%s missing" % tool in invoke(run, repo, context, ["probe", "--log"], outside).stdout


# r7, r18
@then(parsers.parse("tools prints {tool}, what it is for and what the workflow does without it"))
def explains_one(context, tool):
    assert re.search(r"(?m)^%s is missing\.\n  It is for: .+\.\n  Without it: .+\.\n" % tool, context["result"].stdout)


@then("it prints the command that failed with the end of its error")
def failed_command(context):
    stdout = context["result"].stdout
    assert re.search(r"(?m)^jedi is missing\.\n  It is for: .+\.\n  Without it: .+\.\n"
                     r"  Tried: %s -m pip install jedi\n" % re.escape(str(context["python"])), stdout)
    assert "error: no matching distribution" in stdout
    assert "e1" not in stdout
    assert pip_calls(context["python"]) == ["jedi"]


# r8
@then("the suite is run once under coverage with a context for each test")
def suite_once(context):
    runs = [call for call in calls(context["python"]) if call[:2] == ["python", "pytest"]]
    assert len(runs) == 1
    assert "--cov-context=test" in runs[0]
    context["pytest_run"] = runs[0]


@then("only test_total is run")
def only_test_total(repo, run, context):
    assert context["pytest_run"][-2:] == ["-k", "test_total"]
    assert "1 passed" in context["result"].stdout
    listed = run("tools", "--python", sys.executable, "tests-of", "src/cart.py", cwd=repo).stdout
    assert listed.splitlines()[0] == "tests/test_cart.py::test_total"
    assert "test_discount" not in listed


@then(parsers.parse("the map is kept in `{path}`"))
def map_kept(repo, path):
    assert path == MAP
    assert (repo / path).is_file()


# r9
@then("tools prints test_total and test_checkout, one a line")
def prints_two(context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert lines(context)[:-1] == ["tests/test_cart.py::test_total", "tests/test_checkout.py::test_checkout"]


@then(parsers.parse("it says that is {n:d} of the map's {total:d} tests"))
def says_share(context, n, total):
    assert lines(context)[-1].startswith("%d of the %d tests in the map executed %s (" % (n, total, context["args"][-1]))


@then(parsers.parse("it gives commit {label}"))
def gives_commit(context, label):
    assert lines(context)[-1].endswith("(map made at %s)" % context["commits"][label])


# r10
@then("tools prints tests/test_cart.py with 2 and tests/test_checkout.py with 1")
def by_file(context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert lines(context)[:2] == ["tests/test_cart.py 2", "tests/test_checkout.py 1"]


@then("it prints no test names")
def no_test_names(context):
    assert "::" not in context["result"].stdout
    assert "test_total" not in context["result"].stdout


# r12, r26
@then("the command is refused because no map has been made")
def refused_no_map(context):
    assert context["result"].returncode == 1
    assert "no map" in context["result"].stderr


@then("it says to make one with `tools map`")
def make_one(context):
    assert context["result"].stderr == "tools: no map: make one with tools map\n"


# r13
@then("tools prints refund and export")
def prints_refund_export(context):
    assert lines(context)[:-1] == ["src/cart.py:5 refund", "src/report.py:5 export"]


@then("it prints no other function")
def no_other_function(context):
    assert len(lines(context)) == 3
    assert lines(context)[-1].startswith("2 functions no test executed")


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


# r18
@then(parsers.parse("for {first} and for {second} tools prints the tool, what it is for, what the workflow does "
                    "without it and that the interpreter is not a virtualenv"))
def explains_not_venv(context, first, second):
    for name in (first, second):
        assert re.search(r"(?m)^%s is missing\.\n  It is for: .+\.\n  Without it: .+\.\n  Tried: %s is not a virtualenv"
                         % (name, re.escape(str(context["python"]))), context["result"].stdout)


@then("nothing is installed into the interpreter")
def nothing_installed(context):
    assert pip_calls(context["python"]) == []


# r19, r20
@then("tools says every tool is present")
def all_present_said(context):
    assert context["result"].stdout == "every tool is present\n"
    assert pip_calls(context["python"]) == []


@then(parsers.parse("tools prints that {tool} is installed"))
def says_installed(context, tool):
    assert context["result"].returncode == 0, context["result"].stderr
    assert context["result"].stdout == "%s installed\n" % tool


# r21
@then("the command is refused because the interpreter does not run")
def refused_not_running(context):
    assert context["result"].returncode == 1


@then("it names the interpreter and the end of its error")
def names_interpreter(context):
    assert context["result"].stderr == "tools: %s does not run: boom: cannot start\n" % context["python"]


# r22
def probe_entries(context):
    line = context["result"].stdout
    assert line.startswith("Probe: tools -> ") and line.endswith("\n")
    return dict(entry.rsplit(" ", 1) for entry in line[len("Probe: tools -> "):].strip().split(", "))


@then("the line names each installed tool with its version")
def log_versions(context):
    entries = probe_entries(context)
    assert list(entries) == list(NAMES)
    assert all(version == "1.0" for name, version in entries.items() if name != "vulture")


@then("it names vulture as `missing`")
def log_vulture(context):
    assert probe_entries(context)["vulture"] == "missing"


# r23
@then(parsers.parse("the earlier map is replaced by one made at commit {label}"))
def map_replaced(run, repo, context, outside, label):
    later = invoke(run, repo, context, ["tests-of", "src/cart.py"], outside).stdout
    assert "test_old" not in later
    assert "(map made at %s)" % context["commits"][label] in later


@then(parsers.parse("tools prints pytest's last line, where the map is and commit {label}"))
def prints_map_line(context, label):
    assert lines(context)[0].startswith(context["last_line"]), lines(context)
    assert lines(context)[1] == "map: %s, at %s" % (MAP, context["commits"][label])


# r24
@then("the command is refused because no map was made")
def refused_no_map_made(repo, context):
    assert context["result"].returncode == 1
    assert not (repo / MAP.replace("coverage", "coverage.at")).exists()


@then("it names the command it ran and the end of its output")
def names_command(context):
    assert re.match(r"^tools: no map was made by: %s -m pytest -q .*--cov-context=test --cov-report=\n"
                    r"collected nothing at all\n$" % re.escape(str(context["python"])), context["result"].stderr)


# r25
@then("tools prints each of those functions as `<path>:<line> <name>`")
def lost_functions(context):
    source = context["source"].splitlines()
    count = len(lines(context)) - 1
    want = ["src/cart.py:%d lost_%d" % (source.index("def lost_%d():" % n) + 1, n) for n in range(count)]
    assert lines(context)[:-1] == want


@then(parsers.parse("it says {count:d} functions no test executed and gives commit {label}"))
def says_count(context, count, label):
    assert lines(context)[-1] == "%d functions no test executed, in the map made at %s" % (
        count, context["commits"][label])
    assert len(lines(context)) - 1 == count


# r27, r28
@then(parsers.parse("the command is refused because {tool} is missing from the interpreter"))
def refused_missing_tool(context, tool):
    assert context["result"].returncode == 1
    assert context["result"].stderr == "tools: %s is missing from %s: tools install\n" % (tool, context["python"])


@then("it says to run `tools install`")
def says_install(context):
    assert "tools install" in context["result"].stderr


# r29
@then("the command is refused")
def refused(context):
    assert context["result"].returncode == 1
    assert context["result"].stdout == ""


@then("it names src/gone.py")
def names_gone(context):
    assert context["result"].stderr == "tools: src/gone.py is not a file\n"


# r31
def checked(context):
    return [call for call in calls(context["python"]) if call[:2] in (["python", "ruff"], ["python", "vulture"])]


@then("tools checks src/cart.py")
def checks_cart(context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert len(checked(context)) == 2
    for call in checked(context):
        assert [a for a in call[2:] if "." in a and not a.startswith("-")] == ["src/cart.py"]


@then("it does not check README.md, src/old.py or src/report.py")
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
@then("under the ruff heading and under the vulture heading tools says there is nothing to check")
def nothing_to_check(context):
    assert under_heading(context["result"].stdout, "ruff") == "nothing to check"
    assert under_heading(context["result"].stdout, "vulture") == "nothing to check"


@then("neither ruff nor vulture makes it exit 1")
def neither_fails(context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert checked(context) == []


# r34
@then("under the import-linter heading tools says the project states no import contracts")
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
