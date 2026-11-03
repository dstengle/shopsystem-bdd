"""The step vocabulary in pytest-bdd (design §14.3): one step definition for each (keyword, template, kind) of the
context's Steps grammar, dispatching to the handler `features_vocab.lookup` finds, and the checks of the observable
universal conditions after every generated scenario (design §8.4: U3, a refused command changes nothing; U8,
`--json` prints one JSON object).

A step definition matches a step when the Steps grammar reads the step's text as its (template, kind); a cheap test
of the pattern's words comes first, and each text is parsed once a process. `install(namespace, root, tests_dir)`
puts the definitions, the default fixtures (`repo`, `context`, `run`) and the hooks into a conftest's namespace, and
imports the handlers (`world_*.py`, `*_handlers*.py`) by glob.

This module is also the handler registry. It is importable as `vocab` however it was loaded, so a handler module
writes `from vocab import handler`, and `features vocab --check` reads the same registry.
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.append(str(SCRIPTS))
if __name__ in sys.modules:   # a loader by path puts the module in sys.modules first, as importlib's recipe does
    sys.modules.setdefault("vocab", sys.modules[__name__])

import features_vocab

_read, HANDLERS, CLAIMS = {}, {}, defaultdict(set)


def handler(template, term=None):
    """`@handler("GivenK_A", "initiative")`: the function that runs every step of that template and term; with no
    term, the fallback for the template. It is called with the step's `features_vocab.Call`."""
    def mark(fn):
        CLAIMS[(template, term)].add("%s:%d" % (fn.__code__.co_filename, fn.__code__.co_firstlineno))
        HANDLERS.setdefault((template, term), fn)
        return fn
    return mark


def lookup(template, term):
    """The handler of (template, term), else the template's fallback, else None."""
    return HANDLERS.get((template, term)) or HANDLERS.get((template, None))


def load_handlers(tests_dir):
    """Import every world_*.py and *_handlers*.py under tests_dir, each once."""
    tests_dir = Path(tests_dir)
    for path in sorted(tests_dir.glob("world_*.py")) + sorted(tests_dir.glob("*_handlers*.py")):
        name = "shop_handlers_%s" % hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:12]
        if name not in sys.modules:
            spec = importlib.util.spec_from_file_location(name, path)
            sys.modules[name] = module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)


def duplicates():
    """Each key two handlers claim, naming where they are."""
    return ["two handlers claim %s%s: %s" % (t, " " + term if term else "", ", ".join(sorted(where)))
            for (t, term), where in sorted(CLAIMS.items(), key=lambda kv: (kv[0][0], kv[0][1] or ""))
            if len(where) > 1]


def marks(root):
    """Every r<n> and g<n> a capability file of the spec names: the marks of the scenarios' tags."""
    found = set()
    for path in sorted((Path(root) / "spec" / "capabilities").glob("*.md")):
        found |= set(re.findall(r"(?<![\w#])([rg][1-9]\d*)(?!\w)", path.read_text()))
    return sorted(found, key=lambda m: (m[0], int(m[1:])))


def generated(node):
    """True for a scenario of a generated feature: its tags carry a group mark g<n>."""
    return any(re.fullmatch(r"g[1-9]\d*", m.name) for m in node.iter_markers())


def snapshot(repo):
    """{path: digest} of every file under the repository but .git."""
    repo = Path(repo)
    return {p.relative_to(repo).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(repo.rglob("*")) if p.is_file() and ".git" not in p.relative_to(repo).parts}


def u_problems(records):
    """The U3 and U8 failures of a scenario's runs, each record {args, returncode, stdout, changed}."""
    out = []
    for r in records:
        command = " ".join(map(str, r["args"]))
        if r["returncode"] != 0 and r["changed"]:
            out.append("U3: `%s` was refused (exit %d) and changed %s" % (command, r["returncode"],
                                                                         ", ".join(r["changed"])))
        if r["returncode"] == 0 and "--json" in map(str, r["args"]):
            try:
                one = isinstance(json.loads(r["stdout"]), dict)
            except ValueError:
                one = False
            if not one:
                out.append("U8: `%s` printed something other than one JSON object" % command)
    return out


def runner(repo, request, scripts=SCRIPTS):
    """`run("model", "check", ...)`: a script of the plugin run with this Python in the repository; in a generated
    scenario each run is recorded for the U checks."""
    def _run(script, *args, cwd=None, **kwargs):
        record = generated(request.node)
        before = snapshot(repo) if record else None
        done = subprocess.run([sys.executable, str(Path(scripts) / script), *map(str, args)], capture_output=True,
                              text=True, cwd=cwd or repo, **kwargs)
        if record:
            after = snapshot(repo)
            changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
            request.node.__dict__.setdefault("_shop_runs", []).append(
                {"args": [script, *args], "returncode": done.returncode, "stdout": done.stdout, "changed": changed})
        return done
    return _run


def pytest_bdd_step_error(request):
    request.node._shop_failed = True


def pytest_bdd_after_scenario(request):
    if getattr(request.node, "_shop_failed", False) or not generated(request.node):
        return
    problems = u_problems(request.node.__dict__.get("_shop_runs", []))
    if problems:
        pytest.fail("\n".join(problems), pytrace=False)


def read(root, keyword, text):
    """(template, kind) of a step's text under its keyword, or None; once a process for each text."""
    key = (str(root), keyword, text)
    if key not in _read:
        try:
            call = features_vocab.step(features_vocab.load(root), keyword, text)
            _read[key] = (call.template, call.kind)
        except features_vocab.StepError:
            _read[key] = None
    return _read[key]


class VocabParser:
    """A pytest-bdd step parser for one (keyword, template, kind); with `catch_all`, for any step the grammar
    reads whose (template, kind) has no definition of its own."""

    def __init__(self, root, row, own, catch_all=False):
        self.root, self.keyword, self.key, self.own, self.catch_all = root, row.keyword, (row.template, row.kind), \
            own, catch_all
        self.name = "vocab %s %s %s" % (row.keyword, row.template, row.kind)
        self.words = [] if catch_all else [w for w in re.split(r"\{[nx]\d+\}", row.pattern) if w.strip()]

    def is_matching(self, name):
        if not all(w.strip() in name for w in self.words):
            return False
        got = read(self.root, self.keyword, name)
        return got is not None and (got == self.key or (self.catch_all and (self.keyword,) + got not in self.own))

    def parse_arguments(self, name):
        return {"text": name}


def _step_function(root, keyword):
    def step_function(text, request, docstring=None, datatable=None):
        call = features_vocab.step(features_vocab.load(root), keyword, text)
        call.docstring, call.datatable, call.fixtures = docstring, datatable, request.getfixturevalue
        found = sys.modules["vocab"].lookup(call.template, call.term)
        if found is None:
            pytest.fail("no handler for %s %s: %s" % (call.template, call.term, text), pytrace=False)
        return found(call)
    return step_function


def _marker(context):
    """The fixture pytest-bdd finds a step definition by, as its own `step` decorator makes it."""
    def step_function_marker():
        return context
    step_function_marker._pytest_bdd_step_context = context
    return step_function_marker


def register(namespace, root):
    """One step definition for each (keyword, template, kind) row, and a catch-all for each keyword."""
    from pytest_bdd.steps import StepFunctionContext
    rows = features_vocab.rows(features_vocab.load(root))
    own = {(r.keyword, r.template, r.kind) for r in rows}
    chosen = {}
    for row in rows:
        chosen.setdefault((row.keyword, row.template, row.kind), VocabParser(root, row, own))
    for row in rows:
        if row.kind is None:
            chosen.setdefault((row.keyword, "*"), VocabParser(root, row, own, catch_all=True))
    for n, parser in enumerate(chosen.values()):
        context = StepFunctionContext(type=parser.keyword, step_func=_step_function(root, parser.keyword),
                                      parser=parser)
        marker = _marker(context)
        name = "pytestbdd_stepdef_%s_vocab_%d" % (parser.keyword, n)
        namespace[name] = pytest.fixture(name=name)(marker)


@pytest.fixture
def repo(tmp_path):
    return tmp_path


@pytest.fixture
def context():
    return {}


@pytest.fixture
def run(repo, request):
    return runner(repo, request)


def install(namespace, root, tests_dir):
    """Make a conftest's namespace the vocabulary's: step definitions, default fixtures and hooks (a name the
    conftest defines itself is kept), the marks of the spec, and the handlers under tests_dir."""
    for name, value in (("repo", repo), ("context", context), ("run", run),
                        ("pytest_bdd_step_error", pytest_bdd_step_error),
                        ("pytest_bdd_after_scenario", pytest_bdd_after_scenario)):
        namespace.setdefault(name, value)

    def pytest_configure(config):
        for mark in marks(root):
            config.addinivalue_line("markers", "%s: scenario of %s" % (mark, mark))
    namespace.setdefault("pytest_configure", pytest_configure)
    try:
        register(namespace, root)
    except Exception as err:  # noqa: BLE001  (no grammar tools: only generated scenarios fail, on their steps)
        sys.stderr.write("vocab: no step definitions (%s)\n" % err)
    sys.modules["vocab"].load_handlers(tests_dir)
