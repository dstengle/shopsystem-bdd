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

four = sys.modules["shop_world_four"].four   # loaded before the handlers, by the glob of world_*.py

from scenarios import analysis_tools_world as w

FEATURE = HERE.parents[1] / "features" / "analysis-tools.feature"
TEST_CART = "from cart import total\n\n\ndef test_cart():\n    assert total([1]) == 1\n"
USES = "from cart import refund\n\n\n" + "\n\n".join(
    "def back%d(order):\n    return refund(order)\n" % n for n in range(1, 5))   # four references to `refund`
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


for _kind in ("Python interpreter", "log line", "coverage map", "Python file", "function", "identifier", "reference",
              "finding", "file", "size limit"):
    handler("GivenK", _kind)(lambda step: None)     # an instance is made by what the Givens say of it


@handler("GivenK", "test")
def given_test(step):
    name = bare(step.names[0])
    files(step)["tests/test_%s.py" % name] = "from cart import total\n\n\ndef test_%s():\n    assert total([1]) == 1\n" % name
    named(step)[name] = "test_%s" % name


@handler("GivenDoes", "fail")
def given_failing(step):
    """The test t1 fails: its file asserts False."""
    name = bare(step.names[0])
    files(step)["tests/test_%s.py" % name] = "def test_%s():\n    assert False\n" % name


@handler("GivenK_A", "analysis tool")
def given_tool(step):
    """`the presence of the analysis tool a1 is v`, `the presence of `ruff` is v` or `no analysis tool whose presence
    is v exists`: the stand-in has it or lacks it."""
    config, presence = stand_in(step), bare(step.values[0])
    if step.text.startswith("no "):
        return
    tool = tool_of(step, step.names[0]) if step.names else bare(step.subject)
    if presence in ("missing", "uninstallable"):
        config.setdefault("missing", []).append(tool)
        config.setdefault("block", []).append(tool)
    if presence == "uninstallable":
        config.update(pip_fails=True, pip_error="e1\ne2\nerror: no matching distribution for %s" % tool)


@handler("GivenK_A", "Python interpreter")
def given_environment(step):
    """`this Python interpreter is v`, the one `tools` runs with: the stand-in at `.venv/bin/python`, which `tools`
    finds, a virtualenv or the system's."""
    stand_in(step).update(venv=step.values[0] == "`virtualenv`")
    step.context["fake_at"] = step.repo / ".venv"


@handler("GivenCode", "dependency file")
def given_manifest(step):
    files(step)[bare(step.names[0])] = step.quoted[0].strip('"') + "\n"


# --- what holds ---

INTERPRETERS = {"`.venv/bin/python`": ".venv", "`venv/bin/python`": "venv", "`$VIRTUAL_ENV/bin/python`": "$VIRTUAL_ENV"}


@four("GivenDoes", "exist", "analysis-tools")
@handler("GivenDoesNot", "exist")
def given_exists(step):
    """An interpreter of the first match exists (made where `tools` looks for it) or does not (left out); a coverage
    map exists (made before the command runs), or none does."""
    ctx, there = step.context, step.template == "GivenDoes" and not step.subject.startswith("no ")
    if step.subject.endswith("coverage map") or step.subject.startswith("the coverage map"):
        ctx["map"] = there
        return
    ctx["discover"] = True
    where = INTERPRETERS[step.subject.split()[1]]
    if not there:
        return
    if where == "$VIRTUAL_ENV":
        ctx["env_dir"] = outside(step)
        w.fake(ctx["env_dir"])
        ctx.setdefault("env", {})["VIRTUAL_ENV"] = str(ctx["env_dir"])
    elif not (step.repo / where).exists():
        w.fake(step.repo / where)


@four("GivenDoes", "holds", "analysis-tools")
def given_holds(step):
    """A coverage map holds a test (the test's file is in the project the map is made of), a Python file holds a
    test, a file holds a finding."""
    np = step.nps[0]
    if step.subject.startswith("the coverage map"):
        return
    if np.startswith("the test"):
        named(step)[step.names[0]] = "tests/test_%s.py" % bare(step.names[1])
    else:
        named(step)[step.names[0]], named(step)[step.names[1]] = FINDING.split(":")[0], FINDING


@handler("GivenDoes", "execute")
def given_executes(step):
    """A test executes the function f1 (src/cart.py's `total`), or no test does (its `refund`)."""
    function(step, step.names[-1], "untested" if step.subject.startswith("no ") else "executed")


@four("GivenDoes", "has", "analysis-tools")
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
    """A Python file over the size limit (src/big.py, of 20 lines over a limit of 10), or none over `300`."""
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
    """The command's argument for the instance it runs on: a function as `src/cart.py:<name>` (an identifier no file
    defines as `src/cart.py:nowhere`), a file's path, an identifier; nothing when it runs on none."""
    given = {v.split()[-1] for _, v in getattr(step, "options", []) if v}
    on = [n for n in step.names if n not in given]
    if not on:
        return []
    name = on[0]
    if argv[0] == "tests-of":
        function(step, name, "executed")
        return ["src/cart.py:%s" % named(step)[name]]
    named(step).setdefault(name, "refund" if argv[0] == "refs" else "src/cart.py")
    return [named(step)[name]]


def options(step):
    """Each option of the When with its argument: an interpreter for `--python` (a stand-in, which `tools` takes
    after the command), a size limit for `--limit`; `tools` looks for the interpreter itself without `--python`."""
    out = []
    for option, value in getattr(step, "options", []):
        out.append(bare(option))
        if bare(option) == "--python":
            step.context.update(python=str(w.fake(outside(step) / "py")), discover=True)
            named(step)[value.split()[-1]] = "python: %s" % step.context["python"]
            out.append(step.context["python"])
        elif value is not None:
            out.append(named(step).get(value.split()[-1], LIMIT))
    if "`--python`" in getattr(step, "without", []):
        step.context["discover"] = True
    return out


def runs_tools(step):
    ctx, repo = step.context, step.repo
    tests = {} if any(k.startswith("tests/") for k in files(step)) else {"tests/test_cart.py": TEST_CART}
    w.started(repo, {**tests, **files(step)})
    grammar_stub(step)
    argv = shlex.split(bare(step.command))[1:]
    argv += options(step) + target(step, argv)
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
