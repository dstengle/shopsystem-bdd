"""tools: the project's interpreter and the tools in it, probed and installed (probe, install)."""
import json
import os
import subprocess
import sys

import shop_refused

# name, pip package, what it is for, what the workflow does without it
TOOLS = (
    ("coverage", "coverage", "which tests execute a function, and which code no test executes",
     "the scout searches for the tests a decision breaks, and a guard may rest on no test"),
    ("pytest-cov", "pytest-cov", "the coverage map made with a context for each test",
     "there is no map: the same as coverage missing"),
    ("jedi", "jedi", "exact references to a name, through imports and aliases",
     "where a change lands is counted by text search, and the count is a floor"),
    ("ast-grep", "ast-grep-cli", "search by the shape of code: a call that relies on a default, a broad except",
     "the consequence sweep searches by text and misses what text cannot say"),
    ("ruff", "ruff", "lint, line length, unused imports", "reviewers read for them"),
    ("vulture", "vulture", "code with no caller left", "reviewers find it by reading, after a removal"),
    ("import-linter", "import-linter", "the module map's import rules as checked contracts",
     "reviewers read the imports against CLAUDE.md"),
    ("hypothesis", "hypothesis", "the project's invariants as property tests", "invariants are probed by hand in review"),
)
PINS = {"ruff": "0.17.0"}  # the one version of each of these `install` puts in
VERSIONS = ("import json, sys\nfrom importlib import metadata\nout = {}\n"
            "for name in sys.argv[1:]:\n    try:\n        out[name] = metadata.version(name)\n"
            "    except metadata.PackageNotFoundError:\n        out[name] = None\n"
            "out['virtualenv'] = sys.prefix != sys.base_prefix\nprint(json.dumps(out))\n")


class Refused(shop_refused.Refused):
    pass


def interpreter(args):
    if args.python:
        return args.python, "--python"
    return project_python(".")


def project_python(root):
    """(interpreter, how found): the project's virtualenv under `root` (`.venv`, `venv`, then `$VIRTUAL_ENV`), else the
    interpreter running this script."""
    candidates = [os.path.join(root, ".venv/bin/python"), os.path.join(root, "venv/bin/python")]
    if os.environ.get("VIRTUAL_ENV"):
        candidates.append(os.path.join(os.environ["VIRTUAL_ENV"], "bin", "python"))
    for path in candidates:
        if os.path.isfile(path):
            return os.path.abspath(path), "the project's virtualenv"
    return sys.executable, "no virtualenv found: the interpreter running this script"


def is_python_project():
    marks = ("pyproject.toml", "setup.py", "setup.cfg", "pytest.ini", "requirements.txt", "tox.ini")
    if any(os.path.isfile(mark) for mark in marks):
        return True
    return any(name.endswith(".py") for _, _, names in os.walk(".") for name in names)


def versions(python):
    done = subprocess.run([python, "-c", VERSIONS] + [package for _, package, _, _ in TOOLS],
                          capture_output=True, text=True)
    if done.returncode:
        raise Refused("%s does not run: %s" % (python, done.stderr.strip()[-300:]))
    return json.loads(done.stdout)


def probed(args):
    if not is_python_project():
        raise Refused("no analysis tools are known for this project's language (looked for Python): "
                      "agents search by text, and say so")
    python, why = interpreter(args)
    return python, why, versions(python)


def cmd_probe(args):
    import tools_grammar
    python, why, found = probed(args)
    grammar, binary = tools_grammar.probed()
    missing = [name for name, package, _, _ in TOOLS if not found[package]]
    missing += [name for name, version in grammar.items() if version is None]
    if getattr(args, "json", False):
        print(json.dumps({"python": python, "source": why, "grammar": grammar,
                          "tools": {name: found[package] for name, package, _, _ in TOOLS}}))
    elif args.log:
        print("Probe: tools -> " + ", ".join(
            "%s %s" % (name, found[package] or "missing") for name, package, _, _ in TOOLS))
    else:
        for name, package, what, _ in TOOLS:
            print("%s %s" % (name, found[package]) if found[package] else "%s missing: %s" % (name, what))
        print("python: %s (%s)" % (python, why))
        print("\n".join(tools_grammar.probe_lines(grammar, binary)))
    return 1 if missing else 0


def cmd_install(args):
    """The analysis tools into the project's interpreter, then the grammar tools; exit 1 when either fails."""
    import tools_grammar
    analysis = install_analysis(args)
    try:
        tools_grammar.install()
    except tools_grammar.Refused as why:
        print("the grammar tools are not installed: %s" % why)
        return 1
    return analysis


def install_analysis(args):
    python, why, found = probed(args)
    missing = [tool for tool in TOOLS if not found[tool[1]]]
    if not missing:
        print("every tool is present")
        return 0
    failed = {}
    if not found["virtualenv"]:
        failed = {tool[0]: ("%s is not a virtualenv (%s): nothing is installed into it" % (python, why), "")
                  for tool in missing}
    else:
        for name, package, _, _ in missing:
            requirement = "%s==%s" % (package, PINS[name]) if name in PINS else package
            command = [python, "-m", "pip", "install", requirement]
            done = subprocess.run(command, capture_output=True, text=True)
            if done.returncode:
                failed[name] = (" ".join(command), "\n".join(done.stderr.strip().splitlines()[-4:]))
            else:
                print("%s installed" % name)
    for name, _, what, without in missing:
        if name in failed:
            command, error = failed[name]
            print("%s is missing.\n  It is for: %s.\n  Without it: %s.\n  Tried: %s\n  %s"
                  % (name, what, without, command, error.replace("\n", "\n  ")))
    return 1 if failed else 0
