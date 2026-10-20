"""tools: the coverage map, made and read (map, tests-of, untested)."""
import ast
import os
import re
import subprocess
import sys

from tools_env import Refused, interpreter

MAP = os.path.join(".shop", "scratch", "tools", "coverage")


def head():
    done = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return done.stdout.strip() or "no commit"


def cmd_map(args):
    python, _ = interpreter(args)
    os.makedirs(os.path.dirname(MAP), exist_ok=True)
    for name in os.listdir(os.path.dirname(MAP)):
        if name.startswith("coverage"):
            os.remove(os.path.join(os.path.dirname(MAP), name))
    env = dict(os.environ, COVERAGE_FILE=os.path.abspath(MAP))
    command = [python, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--cov=.", "--cov-context=test",
               "--cov-report="] + args.pytest
    done = subprocess.run(command, env=env, capture_output=True, text=True)
    lines = done.stdout.strip().splitlines()
    if not os.path.isfile(MAP):
        raise Refused("no map was made by: %s\n%s" % (" ".join(command), "\n".join((lines + done.stderr.splitlines())[-6:])))
    with open(MAP + ".at", "w") as handle:
        handle.write(head() + "\n")
    print("%s\nmap: %s, at %s" % (lines[-1] if lines else "", MAP, head()))
    return 0


def read_map():
    try:
        import coverage
    except ImportError:
        raise Refused("coverage is missing from %s: tools install" % sys.executable)
    if not os.path.isfile(MAP):
        raise Refused("no map: make one with tools map")
    data = coverage.CoverageData(basename=os.path.abspath(MAP))
    data.read()
    with open(MAP + ".at") as handle:
        return data, handle.read().strip()


def functions(path):
    """Every function and method in a file: (dotted name, first line, last line)."""
    with open(path, encoding="utf-8") as handle:
        tree = ast.parse(handle.read(), path)
    found = []

    def walk(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = prefix + child.name
                if not isinstance(child, ast.ClassDef):
                    body = child.body[0].lineno if child.body else child.lineno
                    found.append((name, child.lineno, child.end_lineno, body))
                walk(child, name + ".")
    walk(tree, "")
    return found


def executed(data, path):
    """{line: the tests that executed it} for one file."""
    by_line = data.contexts_by_lineno(os.path.abspath(path))
    return {line: {c.split("|")[0] for c in contexts if c} for line, contexts in by_line.items()}


def cmd_tests_of(args):
    data, at = read_map()
    path, _, name = args.target.partition(":")
    if not os.path.isfile(path):
        raise Refused("%s is not a file" % path)
    lines = executed(data, path)
    if name:
        span = re.match(r"^(\d+)(?:-(\d+))?$", name)
        if span:
            spans = [(int(span.group(1)), int(span.group(2) or span.group(1)))]
        else:
            spans = [(first, last) for found, _, last, first in functions(path) if found == name or found.endswith("." + name)]
        if not spans:
            raise Refused("%s has no function named %s" % (path, name))
        lines = {line: tests for line, tests in lines.items() if any(a <= line <= b for a, b in spans)}
    tests = sorted(set().union(*lines.values())) if lines else []
    ran = len({c.split("|")[0] for c in data.measured_contexts() if c})
    if args.by_file:
        files = {}
        for test in tests:
            files[test.split("::")[0]] = files.get(test.split("::")[0], 0) + 1
        for name_, count in sorted(files.items()):
            print("%s %d" % (name_, count))
    else:
        for test in tests:
            print(test)
    print("%d of the %d tests in the map executed %s (map made at %s)" % (len(tests), ran, args.target, at))
    return 0 if tests else 1


def cmd_untested(args):
    data, at = read_map()
    count = 0
    for path in args.files:
        lines = executed(data, path)
        for name, line, last, first in functions(path):
            if not any(lines.get(n) for n in range(first, last + 1)):
                count += 1
                print("%s:%d %s" % (path, line, name))
    print("%d function%s no test executed, in the map made at %s" % (count, "" if count == 1 else "s", at))
    return 0
