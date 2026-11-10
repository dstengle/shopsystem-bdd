"""analysis-tools' Thens (design §14.3), its steps in grammar 4: they read what `tools` printed and how it exited, what
the stand-in interpreter was asked to run and the coverage map it left; a Then "X has the Y y1" binds y1 to what X has
in the scenario's project (a commit, a version, a pip command, a heading) for the Thens after it; "the number of Ks
..." is the count of the Ks in the scenario's project."""
import importlib.util
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

from vocab import handler

four = sys.modules["shop_world_four"].four   # loaded before the handlers, by the glob of world_*.py

from scenarios import analysis_tools_handlers as h
from scenarios import analysis_tools_world as w

SCRIPTS = HERE.parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.append(str(SCRIPTS))

import tools_env

PACKAGES = {name: package for name, package, _, _ in tools_env.TOOLS}
LOG = "Probe: tools -> "

# The CLI pack's refuse and name of analysis-tools' steps (world_cli's), ahead of the registry's (world_refusal's).
if "shop_world_cli" not in sys.modules:      # requests_handlers' `shared` loads it under this name too
    _spec = importlib.util.spec_from_file_location("shop_world_cli", HERE / "world_cli.py")
    sys.modules["shop_world_cli"] = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(sys.modules["shop_world_cli"])
CLI = sys.modules["shop_world_cli"]
four("ThenDoes", "refuse", "analysis-tools")(CLI.refuses)
four("ThenDoes", "name", "analysis-tools")(CLI.names)


def output(step, err=False):
    done = step.context["result"]
    return done.stdout + (done.stderr if err else "")


def interpreter(step, np):
    """The path an interpreter of the first-match rule is printed as, or None for another noun phrase."""
    return {"`.venv/bin/python`": step.repo / ".venv" / "bin" / "python",
            "`venv/bin/python`": step.repo / "venv" / "bin" / "python",
            "`$VIRTUAL_ENV/bin/python`": step.context.get("env_dir", pathlib.Path("/")) / "bin" / "python"}.get(np)


def number(step, np):
    """The number of Ks a noun phrase "the number of Ks ..." counts in the scenario's project."""
    name = h.name_of(np)
    if np.startswith("the number of tests in"):
        return sum(text.count("def test_") for path, text in h.files(step).items() if path.startswith("tests/")) or 1
    if np.startswith("the number of tests that execute"):
        return len(tests_calling(step, "%s(" % h.named(step)[name]))
    if np.startswith("the number of references to"):
        return sum("refund" in line for line in h.USES.splitlines())
    raise AssertionError("no number known of: %s" % np)


def expected(step, np):
    """What one noun phrase of a Then names in the output, as a string or an int (a count)."""
    found = interpreter(step, np)
    if found is not None:
        return "python: %s" % found
    if np.startswith("the number of "):
        return number(step, np)
    name = h.name_of(np)
    if np.startswith("the analysis tool"):
        return h.tool_of(step, name)
    if name in h.named(step):
        return h.named(step)[name]
    return h.bare(name or np)


def values(data):
    if isinstance(data, dict):
        for v in data.values():
            yield from values(v)
    elif isinstance(data, list):
        for v in data:
            yield from values(v)
    else:
        yield data


def printed(step, want):
    out = output(step, err=True)
    if isinstance(want, int):
        if step.context.get("json"):
            return want in values(json.loads(step.context["result"].stdout))
        return re.search(r"\b%d\b" % want, out) is not None
    if step.context.get("json") and re.fullmatch(r"\S+\.py:\d+", want):
        want = '"path": "%s", "line": %s' % tuple(want.split(":"))
    if step.context.get("json") and want.startswith("test_"):
        want = "::" + want
    return want in out


@handler("ThenPrints", "`tools`")
def prints(step):
    for np in step.nps:
        if np.startswith("the log line"):
            lines = [line for line in output(step).splitlines() if line.startswith(LOG)]
            assert len(lines) == 1 and all(name in lines[0] for name in w.NAMES), output(step, err=True)
            continue
        want = expected(step, np)
        assert printed(step, want), (np, want, output(step, err=True))


@handler("ThenPrintsNot", "`tools`")
def prints_not(step):
    for np in step.nps:   # "python: <path> (<how it was found>)"
        want = expected(step, np)
        assert not any(line.startswith(want + " ") for line in output(step).splitlines()), (np, output(step))


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
        assert printed(step, expected(step, np)), (np, output(step, err=True))


# --- what a thing has ---

def tests_calling(step, call):
    return [path for path, text in h.files(step).items() if path.startswith("tests/") and call in text] or (
        ["tests/test_cart.py"] if call == "total(" and not any(p.startswith("tests/") for p in h.files(step)) else [])


def has(step, owner, np):
    """What `owner` has, the thing `np` names, in the scenario's project."""
    ctx = step.context
    if np.startswith("the version"):
        return "%s==%s" % (h.bare(owner), tools_env.PINS[h.bare(owner)])
    if np.startswith("the pip command"):
        return "%s -m pip install %s" % (ctx["python"], PACKAGES[h.tool_of(step, h.name_of(owner))])
    if np.startswith("the commit"):
        return (step.repo / (w.MAP + ".at")).read_text().strip()
    if np.startswith("the heading"):
        return "== %s ==" % h.tool_of(step, h.name_of(owner))
    raise AssertionError("nothing known of what %s has: %s" % (owner, np))


@four("ThenDoes", "has", "analysis-tools")
def then_has(step):
    h.named(step)[step.names[-1]] = has(step, step.subject, step.nps[0])


@handler("ThenDoes", "pin")
def pins(step):
    """The plugin pins the version: `tools_env.PINS` holds it."""
    tool, version = h.named(step)[step.names[0]].split("==")
    assert tools_env.PINS.get(tool) == version, (tool, version, tools_env.PINS)


@handler("ThenDoes", "execute")
def executes(step):
    """The Python interpreter p1 executes `scripts/tools`: the one the scenario runs `tools` with, printed so."""
    h.named(step)[step.names[0]] = "python: %s" % sys.executable


@handler("ThenDoes", "make")
def makes_map(step):
    at = step.repo / (w.MAP + ".at")
    assert (step.repo / w.MAP).is_file() and at.is_file(), output(step, err=True)
    assert at.read_text().strip() == step.context["head"]


@handler("ThenDoes", "replace")
def replaces_map(step):
    makes_map(step)
    assert step.context["head"] != step.context.get("first_map"), output(step, err=True)


@handler("ThenDoes", "install")
def installs(step):
    for np in step.nps:
        if np == "`gf-rgl`":
            rgl = pathlib.Path(step.context["env"]["XDG_DATA_HOME"]) / "shopsystem-bdd" / "gf-rgl-20250812"
            assert "gf-rgl 20250812 built" in output(step), output(step, err=True)
            assert (rgl / "alltenses" / "AllEng.gfo").is_file() and (rgl / "release").is_file(), output(step, True)
            continue
        want = expected(step, np)
        assert PACKAGES.get(want, want) in w.pip_calls(step.context["python"]), (np, w.pip_calls(step.context["python"]))
