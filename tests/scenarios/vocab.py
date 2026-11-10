"""The step vocabulary in pytest-bdd (design §14.3): one step definition for each (keyword, template, kind) of the
context's Steps grammar, dispatching to the handler `features_vocab.lookup` finds, and the checks of the observable
universal conditions after every generated scenario (design §8.4: U11, a refused command changes nothing; U4, a commit
a command makes in a repository with a remote is pushed, but under a remote the scenario made unpushable; U8,
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


def _git(repo, *args):
    done = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else None


def branch_head(repo):
    """(branch, its commit) checked out in `repo`, or None outside git or on a detached HEAD."""
    branch = (Path(repo) / ".git").exists() and _git(repo, "symbolic-ref", "-q", "--short", "HEAD")
    return (branch, _git(repo, "rev-parse", "HEAD")) if branch else None


def unpushed(repo, before):
    """The remote a run's commit on the branch checked out is not pushed to (U4), or None: none when the run made no
    commit there or the repository has no remote for the branch (its upstream's, else `origin`). The commit is looked
    for on the branch's upstream branch there (`branch.<b>.merge`), else on the branch of its own name."""
    after = branch_head(repo)
    if after is None or after == before:
        return None
    branch, head = after
    remote = _git(repo, "config", "branch.%s.remote" % branch) or "origin"
    if remote not in (_git(repo, "remote") or "").split():
        return None
    upstream = (_git(repo, "config", "branch.%s.merge" % branch) or branch).removeprefix("refs/heads/")
    return None if _git(repo, "rev-parse", "-q", "--verify", "refs/remotes/%s/%s" % (remote, upstream)) == head else remote


def u_problems(records, unpushable=False):
    """The U11, U4 and U8 failures of a scenario's runs, each record {args, returncode, stdout, changed, unpushed}; U4
    is not asked under an unpushable remote."""
    out = []
    for r in records:
        command = " ".join(map(str, r["args"]))
        if r["returncode"] == 0 and r.get("unpushed") and not unpushable:
            out.append("U4: `%s` committed and did not push the commit to %s" % (command, r["unpushed"]))
        if r["returncode"] != 0 and r["changed"]:
            out.append("U11: `%s` was refused (exit %d) and changed %s" % (command, r["returncode"],
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
        before, at = (snapshot(repo), branch_head(repo)) if record else (None, None)
        done = subprocess.run([sys.executable, str(Path(scripts) / script), *map(str, args)], capture_output=True,
                              text=True, cwd=cwd or repo, **kwargs)
        if record:
            after = snapshot(repo)
            changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
            request.node.__dict__.setdefault("_shop_runs", []).append(
                {"args": [script, *args], "returncode": done.returncode, "stdout": done.stdout, "changed": changed,
                 "unpushed": unpushed(repo, at)})
        return done
    return _run


def pytest_bdd_step_error(request):
    request.node._shop_failed = True


def pytest_bdd_after_scenario(request):
    if getattr(request.node, "_shop_failed", False) or not generated(request.node):
        return
    problems = u_problems(request.node.__dict__.get("_shop_runs", []),
                          getattr(request.node, "_shop_unpushable", False))
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
            _read[key] = _read4(root, keyword, text)
    return _read[key]


def _read4(root, keyword, text):
    """A step only the step grammar 4 reads (a codified-2 capability's): (4, template, kind), which is no row's key, so
    the catch-all definition of its keyword takes it; None when grammar 4 does not read it either."""
    import features_vocab4
    try:
        call = features_vocab4.step(root, keyword, text)
    except Exception:  # noqa: BLE001  (a context with no grammar 4 reads no step in it)
        return None
    return (4, call.template, call.kind)


class VocabParser:
    """A pytest-bdd step parser for one (keyword, template, kind); with `catch_all`, for any step the grammar
    reads whose (template, kind) has no definition of its own."""

    def __init__(self, root, row, own, catch_all=False):
        self.root, self.keyword, self.key, self.own, self.catch_all = root, row.keyword, (row.template, row.kind), \
            own, catch_all
        self.name = "vocab %s %s %s" % (row.keyword, row.template, row.kind)
        self.words = [] if catch_all else [_words(row)]

    def is_matching(self, name):
        if self.words and not any(all(w.strip() in name for w in words) for words in self.words):
            return False
        got = read(self.root, self.keyword, name)
        return got is not None and (got == self.key or (self.catch_all and (self.keyword,) + got not in self.own))

    def parse_arguments(self, name):
        return {"text": name}


def _words(row):
    """The fixed words of a row's pattern: a quick test before the grammar reads a step."""
    return [w for w in re.split(r"\{[nx]\d+\}", row.pattern) if w.strip()]


def call_of(root, keyword, text):
    """A step's Call, read in the Steps grammar, else in the step grammar 4 (`_read4`)."""
    try:
        return features_vocab.step(features_vocab.load(root), keyword, text)
    except features_vocab.StepError:
        import features_vocab4
        return features_vocab4.step(root, keyword, text)


def _step_function(root, keyword):
    def step_function(text, request, docstring=None, datatable=None):
        call = call_of(root, keyword, text)
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
        key = (row.keyword, row.template, row.kind)
        if key in chosen:   # one definition for each key, matching the text of any of its rows
            chosen[key].words.append(_words(row))
        chosen.setdefault(key, VocabParser(root, row, own))
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
