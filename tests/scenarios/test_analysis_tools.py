"""features/analysis-tools.feature, bound to scripts/tools.

A Given describes the project and the interpreter in `repo` and `context`; the When runs `tools` once, and the
Then steps read what it printed. The interpreter is a stand-in (FAKE) that answers as its config says and logs
what it is asked to run, except where a scenario needs the real coverage map or jedi: then it is this Python.
The steps are in analysis_tools_*_steps.py and the project and the stand-in in analysis_tools_project.py.
"""
import shlex

from pytest_bdd import parsers, scenarios, then, when

from .analysis_tools_code_steps import *  # noqa: F401,F403  the steps are fixtures pytest-bdd finds by their names here
from .analysis_tools_map_steps import *  # noqa: F401,F403
from .analysis_tools_probe_steps import *  # noqa: F401,F403
from .analysis_tools_project import fake, invoke

scenarios("analysis-tools.feature")


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
