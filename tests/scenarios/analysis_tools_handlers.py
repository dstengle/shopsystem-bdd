"""analysis-tools' handlers (design §14.3): the Givens build a Python project, its interpreters, analysis tools,
coverage map and files in the scenario's repository; every `tools ...` command of the generated feature runs
`scripts/tools` there (with the stand-in interpreter of analysis_tools_world.py where a Given set one up); the Thens
read what it printed and what the stand-in was asked to do.

An analysis tool named `a<n>` stands for the n-th of analysis_tools_world.NAMES; one named with a code is that tool.
"""
import json
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
TESTS = ("test_total", "test_sum")
TEST_CART = "".join("\n\ndef %s():\n    assert total([1]) == 1\n" % t for t in TESTS)
FINDING = "src/cart.py:1:1: F401 unused import"


def bare(word):
    return word.strip("`")


def tool_of(name):
    found = re.fullmatch(r"a([1-9]\d*)", name)
    return w.NAMES[int(found.group(1)) - 1] if found else bare(name)


def outside(step):
    return step.fixtures("tmp_path_factory").mktemp("outside").resolve()


def files(step):
    return step.context.setdefault("files", {})


def stand_in(step):
    """The stand-in interpreter's config; asking for it means `tools` runs under the stand-in."""
    return w.interpreter(step.context)


# --- Givens ---

@handler("GivenK_A", "Python interpreter")
def given_interpreter(step):
    stand_in(step).update(venv=step.values[0] == "`virtualenv`")


@handler("GivenK_C", "Python interpreter")
def given_interpreter_present(step):
    """`the Python interpreter <path> is [not] present`: <path>'s file is made, or is left out; `tools` finds it."""
    name, ctx = bare(step.names[0]), step.context
    ctx["discover"] = True
    if step.text.endswith(" is not present"):
        return
    if name in (".venv/bin/python", "venv/bin/python") and not (step.repo / name).exists():
        w.fake(step.repo / name.split("/")[0])
    elif name == "$VIRTUAL_ENV/bin/python" and "env_dir" not in ctx:
        ctx["env_dir"] = outside(step)
        w.fake(ctx["env_dir"])
        ctx.setdefault("env", {})["VIRTUAL_ENV"] = str(ctx["env_dir"])


@handler("GivenK_A", "analysis tool")
def given_tool(step):
    config, tool = stand_in(step), tool_of(step.names[0])
    presence = bare(step.values[0])
    if presence in ("missing", "uninstallable"):
        config.setdefault("missing", []).append(tool)
        config.setdefault("block", []).append(tool)
    if presence == "uninstallable":
        config.update(pip_fails=True, pip_error="e1\ne2\nerror: no matching distribution for %s" % tool)


@handler("GivenK", "coverage map")
def given_map(step):
    """A coverage map is made only when it is present (GivenK_C)."""


@handler("GivenK_C", "coverage map")
def given_map_present(step):
    step.context["map"] = not step.text.endswith(" is not present")


@handler("GivenK", "test")
def given_test(step):
    files(step)["tests/test_%s.py" % bare(step.names[0])] = (
        "from cart import total\n\n\ndef test_%s():\n    assert total([1]) == 1\n" % bare(step.names[0]))


@handler("GivenK_C", "test")
def given_failing(step):
    name = bare(step.names[0])
    assert step.text.endswith(" is failing"), step.text
    files(step)["tests/test_%s.py" % name] = "def test_%s():\n    assert False\n" % name


@handler("GivenCodeText", "Python file")
def given_python_file(step):
    files(step)[bare(step.names[0])] = step.docstring + "\n"


@handler("GivenCode", "dependency file")
def given_dependency_file(step):
    files(step)[bare(step.names[0])] = step.quoted[0].strip('"') + "\n"


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


def runs_tools(step):
    ctx, repo = step.context, step.repo
    tests = {} if any(k.startswith("tests/") for k in files(step)) else {
        "tests/test_cart.py": "from cart import total" + TEST_CART}
    w.started(repo, {**tests, **files(step)})
    grammar_stub(step)
    flags = ctx.get("flags", [])
    argv = shlex.split(bare(step.command))[1:] + [f for f in flags if f != "--python"]
    if "--python" in flags and "python" not in ctx:
        ctx["python"] = w.fake(outside(step) / "py")
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


# --- Thens ---

def output(step, err=False):
    done = step.context["result"]
    return done.stdout + (done.stderr if err else "")


def expected(step, np):
    """What one noun phrase of a Then names in the output, as a list (empty when it names nothing to look for)."""
    ctx, name = step.context, re.search(r"(`[^`]+`|\b[A-Za-z]+[1-9]\d*)$", np)
    name = name.group(1) if name else None
    interpreters = {"`--python`": ctx.get("python"), "`sys.executable`": sys.executable,
                    "`$VIRTUAL_ENV/bin/python`": ctx.get("env_dir", pathlib.Path("/")) / "bin" / "python"}
    if name in interpreters or name in ("`.venv/bin/python`", "`venv/bin/python`"):
        return [str(interpreters.get(name) or step.repo / bare(name))]
    if np.startswith("the Python interpreter"):
        return ["python: "]
    if np.startswith("the analysis tool"):
        return [tool_of(name)]
    if np.startswith("the test"):
        return [TESTS[int(name[1:]) - 1]]
    if np.startswith("the Python file") and not name.startswith("`"):
        return [f for f in files(step) if not f.startswith("tests/")]
    if np.startswith("the map commit"):
        return [ctx.get("map_commit") or ctx["head"]]
    if np.startswith("the number of"):
        return []
    if np.startswith('"'):
        return [np.strip('"')]
    return [bare(name) if name else bare(np)]


@handler("ThenPrints", "`tools`")
def prints(step):
    out = output(step, err=True)
    for np in step.nps:
        for want in expected(step, np):
            if step.context.get("json") and re.fullmatch(r"\S+\.py:\d+", want):
                want = '"path": "%s", "line": %s' % tuple(want.split(":"))
            assert want in out, (np, want, out)
        if np.startswith("the number of") and step.context.get("json"):
            assert any(isinstance(v, int) for v in _values(json.loads(step.context["result"].stdout))), out
        elif np.startswith("the number of"):
            assert re.search(r"\b\d+\b", out), out


def _values(data):
    if isinstance(data, dict):
        for v in data.values():
            yield from _values(v)
    elif isinstance(data, list):
        for v in data:
            yield from _values(v)
    else:
        yield data


@handler("ThenPrintsNot", "`tools`")
def prints_not(step):
    out = [line for line in output(step).splitlines() if line.startswith("python: ")]
    for np in step.nps:
        assert all(want not in " ".join(out) for want in expected(step, np)), (np, out)


@handler("ThenExitsOk", "`tools`")
def exits_ok(step):
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr
    assert "Traceback" not in done.stderr


@handler("ThenExitsErr", "`tools`")
def exits_err(step):
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr
    assert "Traceback" not in done.stderr
    for np in step.nps:
        for want in expected(step, np):
            assert want in output(step, err=True), (np, want, output(step, err=True))


@handler("ThenDoes", "install")
@handler("ThenDoesNot", "install")
def installs(step):
    done = w.pip_calls(step.context["python"])
    for np in step.nps:
        if np == "`gf-rgl`":
            rgl = pathlib.Path(step.context["env"]["XDG_DATA_HOME"]) / "shopsystem-bdd" / "gf-rgl-20250812"
            assert "gf-rgl 20250812 built" in output(step), output(step, err=True)
            assert (rgl / "alltenses" / "AllEng.gfo").is_file() and (rgl / "release").is_file(), output(step, True)
        elif step.template == "ThenDoesNot":
            assert tool_of(np.split()[-1]) not in done, (np, done)
        elif np.startswith("`"):
            assert bare(np) in done, (np, done)
        else:
            assert tool_of(np.split()[-1]) in done, (np, done)


@handler("ThenDoes", "replace")
def replaces_map(step):
    at = step.repo / (w.MAP + ".at")
    assert (step.repo / w.MAP).is_file() and at.is_file(), output(step, err=True)
    assert at.read_text().strip() == step.context["head"]
    if "first_map" in step.context:
        assert step.context["head"] != step.context["first_map"]
