"""tools: ruff, vulture and import-linter over the paths given or changed (check)."""
import os
import subprocess

from tools_env import TOOLS, Refused, probed


def cmd_check(args):
    python, why, found = probed(args)
    paths = args.paths
    if args.base:
        done = subprocess.run(["git", "diff", "--name-only", "--diff-filter=d", args.base, "--", "*.py"],
                              capture_output=True, text=True)
        if done.returncode:
            raise Refused(done.stderr.strip())
        paths = done.stdout.split()
    reported = False
    contracts = os.path.isfile(".importlinter") or (
        os.path.isfile("pyproject.toml") and "[tool.importlinter" in open("pyproject.toml", encoding="utf-8").read())
    runs = (("ruff", "ruff", [python, "-m", "ruff", "check", "--output-format=concise"] + paths, bool(paths)),
            ("vulture", "vulture", [python, "-m", "vulture", "--min-confidence", "80"] + paths, bool(paths)),
            ("import-linter", "import-linter", [os.path.join(os.path.dirname(python), "lint-imports")], contracts))
    for name, package, command, applies in runs:
        print("== %s ==" % name)
        if not found[package]:
            print("missing: %s" % next(tool[3] for tool in TOOLS if tool[0] == name))
        elif not applies:
            print("nothing to check" if name != "import-linter" else "the project states no import contracts")
        else:
            done = subprocess.run(command, capture_output=True, text=True)
            print((done.stdout + done.stderr).strip() or "clean")
            reported = reported or done.returncode != 0
    return 1 if reported else 0
