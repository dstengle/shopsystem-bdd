"""design-model-check's interpreters: one without clingo (r12), and the search for one that has it (r55)."""
import os
import sys

from pytest_bdd import given, then

from .conftest import SCRIPTS


# HIDE_CLINGO on PYTHONPATH hides clingo from an interpreter, as the fixture harness does.
HIDE_CLINGO = 'raise ImportError("clingo is hidden for this test")\n'


@given("an interpreter without the clingo package")
def no_clingo(world, repo, context):
    world.good()
    world.write("hidden/clingo.py", HIDE_CLINGO)
    env = {k: v for k, v in os.environ.items() if k not in ("SHOPSYSTEM_MODEL_PYTHON", "SHOPSYSTEM_MODEL_REEXEC")}
    env.update(PYTHONPATH=str(repo / "hidden"), PATH=str(repo / "empty"))
    context["env"] = env


# === the search for an interpreter with clingo (r12, r55) =========================================================

PROBE = "-c import clingo"
TRIED_ALWAYS = ["/usr/local/bin/python3", "/usr/bin/python3"]


def _fake_python(world, dirname, behaviour="find"):
    """A python3 in <dirname> that logs each call. find: runs the real interpreter without the hiding PYTHONPATH;
    probe-only: says yes to the probe but runs the real interpreter with clingo still hidden; lack: has no clingo."""
    real = sys.executable
    body = {"find": 'exec /usr/bin/env -u PYTHONPATH "%s" "$@"' % real,
            "probe-only": 'if [ "$1" = "-c" ]; then exit 0; fi\nexec "%s" "$@"' % real,
            "lack": "exit 1"}[behaviour]
    p = world.write("%s/python3" % dirname, '#!/bin/sh\necho "%s: $*" >> "%s"\n%s\n' % (dirname, world.root / "calls.log", body))
    p.chmod(0o755)
    return p


def _search_env(world, path_dirs, **extra):
    """The environment of the interpreter without clingo: clingo hidden, PATH as given."""
    env = {k: v for k, v in os.environ.items() if k not in ("SHOPSYSTEM_MODEL_PYTHON", "VIRTUAL_ENV", "SHOPSYSTEM_MODEL_REEXEC")}
    env["PYTHONPATH"] = str(world.root / "hidden")
    env["PATH"] = os.pathsep.join(str(world.root / d) for d in path_dirs)
    env.update(extra)
    return env


def _calls(world):
    log = world.root / "calls.log"
    return log.read_text().splitlines() if log.exists() else []


def _check_calls(world):
    return [c for c in _calls(world) if str(SCRIPTS / "model") in c]


@given("an interpreter that cannot import clingo")
def interpreter_without_clingo(world, context):
    world.good()
    world.write("hidden/clingo.py", HIDE_CLINGO)
    context["env"] = _search_env(world, ["empty"])


@given("on PATH, in order, a virtualenv's python3 that has clingo, a python3 without it and two python3s with it")
def path_of_four(world, context):
    for d, behaviour in (("venv/bin", "find"), ("lacks", "lack"), ("bin", "find"), ("later", "find")):
        _fake_python(world, d, behaviour)
    context["env"] = _search_env(world, ["venv/bin", "lacks", "bin", "later"], VIRTUAL_ENV=str(world.root / "venv"))


@given("a python3 on PATH that says it has clingo but runs `model check` without it")
def path_of_liar(world, context):
    _fake_python(world, "bin", "probe-only")
    context["env"] = _search_env(world, ["bin"])


@given("no python3 that can, whether PATH has none or $SHOPSYSTEM_MODEL_PYTHON and PATH name ones without it")
def no_python_with_clingo(world, context):
    _fake_python(world, "lacks", "lack")
    nowhere = world.root / "nowhere/python3"
    # the case run by the When has no interpreter on PATH; the other is run by the Then steps (see _tried_cases)
    context["cases"] = [("no interpreter on PATH", [], context["env"]),
                        ("interpreters that lack it", [str(nowhere), str(world.root / "lacks/python3")],
                         _search_env(world, ["lacks"], SHOPSYSTEM_MODEL_PYTHON=str(nowhere)))]


@then("it asks the one without clingo, then the first with it, and tries again under that one")
def asks_in_order(world, context):
    out = context["result"].stdout
    assert "0 violations" in out, out
    assert _calls(world) == ["lacks: " + PROBE, "bin: " + PROBE, "bin: %s --root %s check" % (SCRIPTS / "model", world.root)], _calls(world)


@then("it never asks the virtualenv's python3 or the second with clingo")
def never_asks(world):
    assert not [c for c in _calls(world) if c.startswith(("venv/bin:", "later:"))], _calls(world)


@then("when $SHOPSYSTEM_MODEL_PYTHON names a python3 with clingo, it tries again under that one")
def explicit_python(world, context):
    _fake_python(world, "chosen")
    (world.root / "calls.log").unlink(missing_ok=True)
    env = _search_env(world, ["bin"], SHOPSYSTEM_MODEL_PYTHON=str(world.root / "chosen/python3"))
    result = world.model("check", env=env, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "0 violations" in result.stdout
    assert _calls(world) == ["chosen: " + PROBE, "chosen: %s --root %s check" % (SCRIPTS / "model", world.root)], _calls(world)


@then("`model check` tries again under that python3 once")
def runs_again_once(world, context):
    assert "clingo" in context["result"].stdout
    assert len(_check_calls(world)) == 1, _calls(world)


def _each_case(world, context):
    """The When's result and the other case's, run here: (name, result, interpreters tried) for each."""
    if "second" not in context:
        context["second"] = world.model("check", env=context["cases"][1][2], timeout=60)
    return [(context["cases"][0][0], context["result"], context["cases"][0][1]),
            (context["cases"][1][0], context["second"], context["cases"][1][1])]


@then("it names clingo and pip install clingo")
def names_pip_install(world, context):
    for name, result, _ in _each_case(world, context):
        assert "clingo" in result.stdout, name
        assert "pip install clingo" in result.stdout, name


@then("it names each interpreter it tried, /usr/local/bin/python3 and /usr/bin/python3 among them")
def names_interpreters_tried(world, context):
    for name, result, tried in _each_case(world, context):
        assert result.returncode == 2, (name, result.stdout + result.stderr)
        named = result.stdout.split("it tried has it:", 1)[1].split("\n", 1)[0]
        assert [p.strip() for p in named.rstrip(".").split(",")] == tried + TRIED_ALWAYS, (name, named)
    assert _check_calls(world) == [], _calls(world)
