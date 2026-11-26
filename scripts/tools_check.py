"""tools: ruff, vulture and import-linter over the paths given or changed (check): with no paths, the Python files
the branch checked out changed against `--base`, else its kept changes since it forked from its base branch (`base`),
`main` or the branch the `base` of `.shop/delivery.toml` names (b490). import-linter runs with `scripts/` on its path
when `.importlinter` names a root package there (b614)."""
import configparser
import os
import shutil
import subprocess
import tomllib
from pathlib import Path

from tools_env import TOOLS, Refused, probed


def base():
    """The base branch of the repository: the `base` of `.shop/delivery.toml`, else `main`."""
    path = Path(".shop/delivery.toml")
    try:
        named = tomllib.loads(path.read_text(encoding="utf-8")).get("base") if path.is_file() else None
    except tomllib.TOMLDecodeError as err:
        raise Refused("%s: %s" % (path, err)) from None
    return named if isinstance(named, str) and named else "main"


def linter(python):
    """`lint-imports` beside the interpreter, else the one on PATH (a user install's, b614), else beside it."""
    beside = os.path.join(os.path.dirname(python), "lint-imports")
    return beside if os.path.isfile(beside) else shutil.which("lint-imports") or beside


def linter_env():
    """The environment import-linter runs in: `scripts/` first on PYTHONPATH when a root package `.importlinter`
    names is a folder of it (the plumbing, b614), else the environment as it is."""
    config = configparser.ConfigParser()
    try:
        config.read(".importlinter", encoding="utf-8")
    except configparser.Error:
        return None
    named = config.get("importlinter", "root_packages", fallback="").split()
    named += config.get("importlinter", "root_package", fallback="").split()
    if not any(Path("scripts", name.split(".")[0]).is_dir() for name in named):
        return None
    paths = [os.path.abspath("scripts")] + [p for p in os.environ.get("PYTHONPATH", "").split(os.pathsep) if p]
    return dict(os.environ, PYTHONPATH=os.pathsep.join(paths))


def cmd_check(args):
    python, _why, found = probed(args)
    paths = args.paths
    if args.base or not paths:
        since = args.base or base() + "...HEAD"   # the base branch: the kept changes since the fork, not its later tip
        done = subprocess.run(["git", "diff", "--name-only", "--diff-filter=d", since, "--", "*.py"],
                              capture_output=True, text=True)
        if done.returncode:
            raise Refused(done.stderr.strip())
        paths = done.stdout.split()
    reported = False
    contracts = os.path.isfile(".importlinter") or (
        os.path.isfile("pyproject.toml") and "[tool.importlinter" in Path("pyproject.toml").read_text(encoding="utf-8"))
    runs = (("ruff", "ruff", [python, "-m", "ruff", "check", "--output-format=concise"] + paths, bool(paths)),
            ("vulture", "vulture", [python, "-m", "vulture", "--min-confidence", "80"] + paths, bool(paths)),
            ("import-linter", "import-linter", [linter(python)], contracts))
    for name, package, command, applies in runs:
        print("== %s ==" % name)
        if not found[package]:
            print("missing: %s" % next(tool[3] for tool in TOOLS if tool[0] == name))
            reported = True
        elif not applies:
            print("nothing to check" if name != "import-linter" else "the project states no import contracts")
        else:
            env = linter_env() if name == "import-linter" else None
            done = subprocess.run(command, capture_output=True, text=True, env=env)
            print((done.stdout + done.stderr).strip() or "clean")
            reported = reported or done.returncode != 0
    return 1 if reported else 0
