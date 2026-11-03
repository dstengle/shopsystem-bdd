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
TEST_FAILS = "def test_fails():\n    assert False\n"


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

@handler("GivenK", "Python interpreter")
@handler("GivenK_A", "Python interpreter")
def given_interpreter(step):
    name, ctx = bare(step.names[0]), step.context
    if step.values:
        stand_in(step).update(venv=step.values[0] == "`virtualenv`")
        return
    if name == "--python":
        ctx["python"] = w.fake(outside(step) / "py")
        return
    ctx["discover"] = True
    if name in (".venv/bin/python", "venv/bin/python") and not (step.repo / name).exists():
        w.fake(step.repo / name.split("/")[0])
    elif name == "$VIRTUAL_ENV/bin/python" and "env_dir" not in ctx:
        ctx["env_dir"] = outside(step)
        w.fake(ctx["env_dir"])
        ctx.setdefault("env", {})["VIRTUAL_ENV"] = str(ctx["env_dir"])


@handler("GivenK", "analysis tool")
@handler("GivenK_A", "analysis tool")
def given_tool(step):
    config, tool = stand_in(step), tool_of(step.names[0])
    presence = bare(step.values[0]) if step.values else "installed"
    if presence in ("missing", "uninstallable"):
        config.setdefault("missing", []).append(tool)
        config.setdefault("block", []).append(tool)
    if presence == "uninstallable":
        config.update(pip_fails=True, pip_error="e1\ne2\nerror: no matching distribution for %s" % tool)


@handler("GivenK", "coverage map")
def given_map(step):
    step.context["map"] = True


@handler("GivenK", "test")
def given_test(step):
    name = bare(step.names[0])
    if name == "test_fails":
        files(step)["tests/test_fails.py"] = TEST_FAILS
    else:
        files(step)["tests/test_%s.py" % name] = "from cart import total\n\n\ndef test_%s():\n    assert total([1]) == 1\n" % name


@handler("GivenK", "Python file")
def given_test_file(step):
    files(step)[bare(step.names[0])] = w.TEST_TOTAL + w.TEST_DISCOUNT


@handler("GivenCodeText", "Python file")
def given_python_file(step):
    files(step)[bare(step.names[0])] = step.docstring + "\n"


@handler("GivenCode", "dependency file")
def given_dependency_file(step):
    files(step)[bare(step.names[0])] = step.quoted[0].strip('"') + "\n"


@handler("GivenK", "function")
def given_function(step):
    assert "def %s" % bare(step.names[0]) in w.CART


@handler("GivenK", "reference")
def given_reference(step):
    path, line = bare(step.names[0]).split(":")
    files(step)[path] = "from cart import total\n" + "\n" * (int(line) - 2) + "print(total([1]))\n"


@handler("GivenK", "finding")
def given_finding(step):
    stand_in(step)["ruff"] = "src/cart.py:1:1: %s unused import" % bare(step.names[0])


# --- the command ---

def grammar_stub(step):
    """GF stands installed under a fresh XDG_DATA_HOME, so `tools install` never downloads it in a scenario."""
    data = outside(step)
    gf = data / "shopsystem-bdd" / "gf-3.12" / "bin" / "gf"
    gf.parent.mkdir(parents=True)
    gf.write_text("#!/bin/sh\necho 'Grammatical Framework (GF) version 3.12.0'\n")
    gf.chmod(0o755)
    step.context.setdefault("env", {})["XDG_DATA_HOME"] = str(data)


def runs_tools(step):
    ctx, repo = step.context, step.repo
    tests = {} if any(k.startswith("tests/") for k in files(step)) else {"tests/test_cart.py": w.TEST_ONLY_TOTAL}
    w.started(repo, {**tests, **files(step)})
    grammar_stub(step)
    if ctx.get("map"):
        w.mapped(step.run, repo, ctx, lambda: outside(step))
        ctx["first_map"] = ctx["map_commit"]
        w.put(repo, {"src/later.py": "def later():\n    return 2\n"})
    flags = [f for f in ctx.get("flags", []) if f != "--python"]
    argv = shlex.split(bare(step.command))[1:] + flags
    ctx["json"] = "--json" in flags
    ctx["result"] = w.invoke(step.run, repo, ctx, argv, lambda: outside(step))
    ctx["head"] = w.git(repo, "rev-parse", "--short", "HEAD")


for _command in sorted(set(re.findall(r"When the person runs (`tools[^`]*`)", FEATURE.read_text()))):
    handler("WhenRuns", _command)(runs_tools)


# --- Thens ---

def output(step, err=False):
    done = step.context["result"]
    return done.stdout + (done.stderr if err else "")


def expected(step, np):
    """What one noun phrase of a Then names in the output, or None when it names nothing to look for."""
    ctx, name = step.context, re.search(r"(`[^`]+`|\b[a-z]+[1-9]\d*)$", np)
    name = name.group(1) if name else None
    if np.startswith("the Python interpreter"):
        paths = {"`--python`": ctx.get("python"), "`sys.executable`": sys.executable,
                 "`$VIRTUAL_ENV/bin/python`": ctx.get("env_dir", pathlib.Path("/")) / "bin" / "python"}
        return str(paths.get(name) or (step.repo / bare(name) if name else "python: "))
    if np.startswith("the analysis tool"):
        return tool_of(name)
    if np.startswith("the test"):
        return "test_" + bare(name) if not bare(name).startswith("test_") else bare(name)
    if np == "the map commit":
        return ctx.get("map_commit") or ctx["head"]
    if np.startswith("the number of"):
        return None
    if np.startswith('"'):
        return np.strip('"')
    return bare(name) if name else bare(np)


@handler("ThenPrints", "`tools`")
def prints(step):
    out = output(step, err=True)
    for np in step.nps:
        want = expected(step, np)
        if want and step.context.get("json") and re.fullmatch(r"\S+\.py:\d+", want):
            want = '"path": "%s", "line": %s' % tuple(want.split(":"))
        assert want is None or want in out, (np, want, out)
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
        assert expected(step, np) not in " ".join(out), (np, out)


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
        want = expected(step, np)
        assert want is None or want in output(step, err=True), (np, want, output(step, err=True))


@handler("ThenDoes", "install")
@handler("ThenDoesNot", "install")
def installs(step):
    done = w.pip_calls(step.context["python"])
    for np in step.nps:
        if step.template == "ThenDoesNot":
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
    if step.names:
        assert step.context["head"] != step.context["first_map"]
