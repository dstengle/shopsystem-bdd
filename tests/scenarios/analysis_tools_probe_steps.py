"""analysis-tools' steps for finding the interpreter and probing and installing the tools (r1-r7, r18-r22)."""
import pathlib
import re
import subprocess
import sys

import pytest
from pytest_bdd import given, parsers, then

from .analysis_tools_project import NAMES, fake, git, interpreter, invoke, lines, missing_tools, pip_calls, started


@pytest.fixture
def outside(tmp_path_factory):
    """A new empty directory outside the project."""
    return lambda: tmp_path_factory.mktemp("outside").resolve()


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


@given("a Python project whose .venv is a virtualenv made from the interpreter running the script, without jedi")
def venv_from_running(repo, context):
    """A real virtualenv: its bin/python is a symlink to the running interpreter, but its packages are its own."""
    a_python_project(repo, context)
    subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(repo / ".venv")], check=True)
    context["discover"] = True
    context["refused_by"] = str(repo / ".venv" / "bin" / "python")


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


@given("`--python` names an interpreter that fails when run")
def broken_interpreter(outside, context):
    broken = outside() / "broken"
    broken.write_text("#!/bin/sh\necho 'boom: cannot start' >&2\nexit 3\n")
    broken.chmod(0o755)
    context["python"] = broken


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
@then("tools says that no analysis tools are known for its language")
def no_tools_known(context):
    stderr = context["result"].stderr
    assert "no analysis tools are known for this project's language" in stderr


# r3
@then("tools prints each tool")
def line_each(context):
    assert len(lines(context)) == len(NAMES) + 1
    assert [line.split()[0] for line in lines(context)[:-1]] == list(NAMES)


@then("each installed tool is printed with its version")
def installed_lines(context):
    for line in lines(context)[:-1]:
        if not line.startswith("vulture"):
            assert line == "%s 1.0" % line.split()[0]


@then("vulture is printed as missing, with what it is for")
def vulture_missing(context):
    assert re.search(r"^vulture missing: \S.+$", "\n".join(lines(context)), re.M)


@then("the interpreter's path is printed after the tools")
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


# r18
@then(parsers.parse("for {first} and for {second} tools says that the interpreter is not a virtualenv"))
def explains_not_venv(context, first, second):
    for name in (first, second):
        assert re.search(r"(?m)^%s is missing\.\n  It is for: .+\.\n  Without it: .+\.\n  Tried: %s is not a virtualenv"
                         % (name, re.escape(str(context["python"]))), context["result"].stdout)


@then("nothing is installed into the interpreter")
def nothing_installed(context):
    assert pip_calls(context["python"]) == []






# r21
@then("the command is refused because the interpreter does not start")
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
