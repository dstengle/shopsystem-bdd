"""analysis-tools' Givens and When (design §14.3), its steps in grammar 4: the Givens build a Python project, its
interpreters, analysis tools, coverage map and files in the scenario's repository; every `tools ...` command of the
generated feature runs `scripts/tools` there (with the stand-in interpreter of analysis_tools_world.py where a Given
set one up). The Thens are analysis_tools_handlers_thens.py's.

What an instance stands for is kept in the context's `named` (an instance name to the text that names it in the
output), which world_cli's refuse and name read too: an analysis tool `a<n>` is the n-th of
analysis_tools_world.NAMES unless a Given binds it to another; one named with a code is that tool.
"""
import pathlib
import re
import shlex
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

from vocab import handler

from scenarios import analysis_tools_world as w

FEATURE = HERE.parents[1] / "features" / "analysis-tools.feature"
TEST_CART = "from cart import total\n\n\ndef test_cart():\n    assert total([1]) == 1\n"
USES = "from cart import refund\n\n\ndef back(order):\n    return refund(order)\n\n\ndef again(order):\n    return refund(order)\n"
FINDING = "src/cart.py:1:1: F401 unused import"
LIMIT = "10"
# the functions of src/cart.py: the one a test calls, the one no test calls, and one no file has
FUNCTIONS = {"executed": "total", "untested": "refund", "nowhere": "nowhere"}


def bare(word):
    return word.strip("`")


def named(step):
    return step.context.setdefault("named", {})


def tool_of(step, name):
    found = re.fullmatch(r"a([1-9]\d*)", name)
    if name in named(step):
        return named(step)[name]
    return w.NAMES[int(found.group(1)) - 1] if found else bare(name)


def outside(step):
    return step.fixtures("tmp_path_factory").mktemp("outside").resolve()


def files(step):
    return step.context.setdefault("files", {})


def stand_in(step):
    """The stand-in interpreter's config; asking for it means `tools` runs under the stand-in."""
    return w.interpreter(step.context)


def name_of(np):
    """The instance name or code a noun phrase ends in, else None."""
    found = re.search(r"(`[^`]+`|\b[A-Za-z]+[1-9]\d*)$", np)
    return found.group(1) if found else None


def function(step, name, kind):
    """The function `name` stands for, bound to `kind` of FUNCTIONS the first time."""
    named(step).setdefault(name, FUNCTIONS[kind])


# --- instances and values ---

@handler("GivenK", "analysis tool")
def given_a_tool(step):
    """An analysis tool a<n> is the n-th of NAMES until a Given says which it is."""
    named(step).setdefault(step.names[0], tool_of(step, step.names[0]))


for _kind in ("log line", "coverage map", "Python file", "function", "identifier", "reference",
              "finding", "file", "size limit"):
    handler("GivenK", _kind)(lambda step: None)     # an instance is made by what the Givens say of it


@handler("GivenK", "test")
def given_test(step):
    name = bare(step.names[0])
    files(step)["tests/test_%s.py" % name] = "from cart import total\n\n\ndef test_%s():\n    assert total([1]) == 1\n" % name
    named(step)[name] = "test_%s" % name


@handler("GivenK_A", "test")
def given_failing(step):
    name = bare(step.names[0])
    assert step.values == ["`failing`"], step.text
    files(step)["tests/test_%s.py" % name] = "def test_%s():\n    assert False\n" % name


@handler("GivenK_A", "analysis tool")
def given_tool(step):
    """`the analysis tool a1 is v`, `` `ruff` is v `` or `no analysis tool is v`: the stand-in has it or lacks it."""
    config, presence = stand_in(step), bare(step.values[0])
    if step.text.startswith("no "):
        return
    tool = tool_of(step, step.names[0]) if step.names else bare(step.text.split(" is ")[0])
    if presence in ("missing", "uninstallable"):
        config.setdefault("missing", []).append(tool)
        config.setdefault("block", []).append(tool)
    if presence == "uninstallable":
        config.update(pip_fails=True, pip_error="e1\ne2\nerror: no matching distribution for %s" % tool)


@handler("GivenK_A", "Python interpreter")
def given_environment(step):
    """`the dot-venv interpreter is v`: the stand-in at `.venv/bin/python`, a virtualenv or the system's."""
    stand_in(step).update(venv=step.values[0] == "`virtualenv`")
    step.context["fake_at"] = step.repo / ".venv"


@handler("GivenCode", "dependency manifest")
def given_manifest(step):
    files(step)[bare(step.names[0])] = step.quoted[0].strip('"') + "\n"


# --- what holds ---

INTERPRETERS = {"the dot-venv interpreter": ".venv", "the venv interpreter": "venv",
                "the active-virtualenv interpreter": "$VIRTUAL_ENV"}


@handler("GivenDoes", "holds")
@handler("GivenDoesNot", "holds")
def given_holds(step):
    """This file system holds an interpreter (made where tools looks, or left out), this repository holds a coverage
    map (or none), a Python file holds a test, a file holds a finding."""
    ctx, np = step.context, step.nps[0]
    if step.subject == "this file system":
        ctx["discover"] = True
        where = INTERPRETERS[np]
        if step.template == "GivenDoesNot":
            return
        if where == "$VIRTUAL_ENV":
            ctx["env_dir"] = outside(step)
            w.fake(ctx["env_dir"])
            ctx.setdefault("env", {})["VIRTUAL_ENV"] = str(ctx["env_dir"])
        elif not (step.repo / where).exists():
            w.fake(step.repo / where)
    elif step.subject == "this repository":
        ctx["map"] = not np.startswith("no ")
    elif np.startswith("the test"):
        named(step)[step.names[0]] = "tests/test_%s.py" % bare(step.names[1])
    else:
        named(step)[step.names[0]], named(step)[step.names[1]] = FINDING.split(":")[0], FINDING


@handler("GivenDoes", "execute")
def given_executes(step):
    """A test executes the function f1 (src/cart.py's `total`), or no test does (its `refund`)."""
    function(step, step.names[-1], "untested" if step.subject.startswith("no ") else "executed")


@handler("GivenDoes", "has")
def given_has(step):
    """A Python file has a function (src/cart.py), no Python file has one (a name no file defines), an analysis tool
    has a finding (`ruff`, whose finding the stand-in prints)."""
    if step.subject.startswith("no "):
        function(step, step.names[-1], "nowhere")
    elif step.nps[0].startswith("the function"):
        named(step)[step.names[0]] = "src/cart.py"
    else:
        named(step)[step.names[0]] = "ruff"
        stand_in(step)["ruff"] = FINDING


@handler("GivenDoes", "define")
def given_defines(step):
    """A Python file defines the identifier (src/cart.py's `refund`, used twice in src/shop.py), or none does."""
    if step.subject.startswith("no "):
        named(step)[step.names[-1]] = "nowhere"
        return
    named(step).update({step.names[0]: "src/cart.py", step.names[1]: "refund"})
    files(step)["src/shop.py"] = USES


@handler("GivenDoes", "to")
def given_reference(step):
    """The n-th reference to the identifier is the n-th use of it in src/shop.py."""
    lines = [n for n, line in enumerate(USES.splitlines(), 1) if "refund(" in line]
    made = step.context.setdefault("references", [])
    made.append(step.names[0])
    named(step)[step.names[0]] = "src/shop.py:%d" % lines[len(made) - 1]


@handler("GivenDoes", "exceed")
def given_exceeds(step):
    """A Python file over the size limit (src/big.py, of 20 lines over a limit of 10), or none over the default."""
    if step.subject.startswith("no "):
        return
    files(step)["src/big.py"] = "x = 1\n" * 20
    named(step).update({step.names[0]: "src/big.py", step.names[1]: LIMIT})


# --- the command ---

def grammar_stub(step):
    """GF and the RGL stand installed under a fresh XDG_DATA_HOME, so `tools install` never downloads them in a
    scenario; an RGL that is `missing` is not there, and is built from w.rgl_source with the real GF."""
    data = outside(step)
    gf = data / "shopsystem-bdd" / "gf-3.12" / "bin" / "gf"
    gf.parent.mkdir(parents=True)
    gf.write_text("#!/bin/sh\necho 'Grammatical Framework (GF) version 3.12.0'\n")
    gf.chmod(0o755)
    step.context.setdefault("env", {})["XDG_DATA_HOME"] = str(data)
    if "gf-rgl" in step.context.get("fake", {}).get("missing", []):
        w.rgl_source(gf, outside(step), step.context["env"])
    else:
        rgl = data / "shopsystem-bdd" / "gf-rgl-20250812"
        rgl.mkdir()
        (rgl / "release").write_text("20250812\n")


def target(step, argv):
    """The command's argument for the instance it runs on: an interpreter for --python, a function as
    `src/cart.py:<name>`, a file's path, an identifier, a size limit; nothing when it runs on none."""
    if not step.names:
        return []
    name = step.names[0]
    if argv[-1] == "--python":
        step.context["python"] = str(w.fake(outside(step) / "py"))
        named(step)[name] = "python: %s" % step.context["python"]
        return [step.context["python"]]
    if argv[0] == "tests-of":
        function(step, name, "executed")
        return ["src/cart.py:%s" % named(step)[name]]
    named(step).setdefault(name, "refund" if argv[0] == "refs" else "src/cart.py")
    return [named(step)[name]]


def runs_tools(step):
    ctx, repo = step.context, step.repo
    tests = {} if any(k.startswith("tests/") for k in files(step)) else {"tests/test_cart.py": TEST_CART}
    w.started(repo, {**tests, **files(step)})
    grammar_stub(step)
    argv = shlex.split(bare(step.command))[1:]
    argv += target(step, argv)
    if argv[0] == "check":
        stand_in(step).setdefault("ruff", FINDING)
    if ctx.get("map"):
        w.mapped(step.run, repo, ctx, lambda: outside(step))
        ctx["first_map"] = ctx["map_commit"]
        w.put(repo, {"src/later.py": "def later():\n    return 2\n"})
    ctx["json"] = "--json" in argv
    ctx["result"] = w.invoke(step.run, repo, ctx, argv, lambda: outside(step))
    ctx["head"] = w.git(repo, "rev-parse", "--short", "HEAD")


for _command in sorted(set(re.findall(r"When the person runs (`tools[^`]*`)", FEATURE.read_text()))):
    handler("WhenRuns", _command)(runs_tools)
