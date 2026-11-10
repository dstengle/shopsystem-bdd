"""analysis-tools' project and stand-in interpreter, for analysis_tools_handlers.py: the files a Given writes, the FAKE
interpreter that answers as its config says and logs what it is asked to run, and how a handler runs `tools` in the
project."""
import json
import os
import pathlib
import subprocess
import sys

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


# --- the interpreter ---

def fake(where, log=None, **config):
    """An interpreter at <where>/bin/python that answers as a virtualenv with the tools it is told to have,
    logs what it is asked to run in `log` (default <where>/calls.log), and runs the rest as the real one."""
    (where / "bin").mkdir(parents=True)
    config = {"missing": [], "venv": True, "pip_fails": False, "pip_error": "", "pytest": "run",
              "pytest_out": "", "block": [], **config, "log": str(log or where / "calls.log")}
    (where / "bin" / "fake.json").write_text(json.dumps(config))
    for name in ("python", "lint-imports"):
        (where / "bin" / name).write_text("#!%s\n%s" % (sys.executable, FAKE))
        (where / "bin" / name).chmod(0o755)
    return where / "bin" / "python"


def interpreter(context):
    """The config of the stand-in interpreter, made on first use."""
    return context.setdefault("fake", {})


def calls(python):
    log = pathlib.Path(json.loads((pathlib.Path(python).parent / "fake.json").read_text())["log"])
    return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []


def pip_calls(python):
    return [call[3] for call in calls(python) if call[:3] == ["python", "pip", "install"]]


# --- the RGL ---

def rgl_source(gf, where, env):
    """A gf-rgl source tree at <where>, one empty module of each the RGL's build compiles, named to `tools install` by
    $SHOPSYSTEM_GF_RGL_SRC; the stand-in GF at <gf> made the real one, which builds it in a moment."""
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))
    import tools_grammar
    real = tools_grammar.gf_binary({k: v for k, v in os.environ.items() if k != "XDG_DATA_HOME"})
    assert real, "no gf to build the RGL with: run `python3 scripts/tools install`"
    gf.write_text('#!/bin/sh\nexec %s "$@"\n' % real)
    (where / "src" / "prelude").mkdir(parents=True)
    (where / "src" / "prelude" / "Prelude.gf").write_text("resource Prelude = { oper SS : Type = {s : Str} ; }\n")
    for module in tools_grammar.RGL_MODULES:
        path = where / "src" / (module + ".gf")
        path.parent.mkdir(exist_ok=True)
        name = path.stem
        (path.parent / (name + "Abs.gf")).write_text("abstract %sAbs = { cat C ; }\n" % name)
        path.write_text("concrete %s of %sAbs = open Prelude in { lincat C = SS ; }\n" % (name, name))
    env["SHOPSYSTEM_GF_RGL_SRC"] = str(where)


# --- running tools ---

def invoke(run, repo, context, argv, outside=None):
    """Run tools in the project: with the stand-in (at `.venv` of the project, which tools finds, when `fake_at` says
    so) or the --python given, or the real one; its map made first if wanted."""
    if "fake" in context and "python" not in context:
        at = context.get("fake_at")
        log = outside() / "calls.log" if at else None    # the log of a stand-in in the project kept out of it
        context["python"] = fake(at or outside(), log=log, **context["fake"])
        context["discover"] = context.get("discover") or bool(at)
    option = []
    if not context.get("discover"):
        option = ["--python", str(context.get("python", sys.executable))]
    env = {k: v for k, v in os.environ.items() if k not in ("VIRTUAL_ENV", "PYTEST_ADDOPTS", "SHOPSYSTEM_GF")}
    env.update(context.get("env", {}))
    return run("tools", *option, *argv, cwd=repo, env=env)


def mapped(run, repo, context, outside=None):
    done = invoke(run, repo, context, ["map"], outside)
    assert done.returncode == 0, done.stderr
    context["map_commit"] = git(repo, "rev-parse", "--short", "HEAD")


