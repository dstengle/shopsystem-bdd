"""The step vocabulary in pytest-bdd (design §14.3): one step definition for each keyword, matching a step the step
grammar 4 reads (vocab4), dispatching to the handler `lookup` finds, and the checks of the observable
universal conditions after every generated scenario: U17, a refused request names a reason and changes nothing;
U20, a run on a task's branch keeps no change there (b60); and the store's check of the decision "Git is the store and the isolation" (U13 retired into it), a request's kept
commit shared to its upstream remote, but under a remote the scenario made unpushable (store_git).

Each text is parsed once a process. `install(namespace, root, tests_dir)`
puts the definitions, the default fixtures (`repo`, `context`, `run`) and the hooks into a conftest's namespace, and
imports the handlers (`world_*.py`, `*_handlers*.py`) by glob.

This module is also the handler registry. It is importable as `vocab` however it was loaded, so a handler module
writes `from vocab import handler`, and `features vocab --check` reads the same registry.
"""
import hashlib
import importlib.util
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.append(str(SCRIPTS))
import store_git
from plumbing import shop_files

if __name__ in sys.modules:   # a loader by path puts the module in sys.modules first, as importlib's recipe does
    sys.modules.setdefault("vocab", sys.modules[__name__])

if __package__:
    from . import vocab4
else:   # loaded by path, as `features vocab --check` loads it
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import vocab4
    sys.path.pop(0)

HANDLERS, CLAIMS = {}, defaultdict(set)
origin = vocab4.requested.origin     # the capability a scenario's group moved from, which handlers know it by
FOUR_CHAINS, FOUR_RUN = {}, {}     # world_four's chains of grammar 4's handlers, and the runner of each


def handler(template, term=None):
    """`@handler("GivenK_A", "initiative")`: the function that runs every step of that template and term; with no
    term, the fallback for the template. It is called with the step's `features_vocab4.Call`."""
    def mark(fn):
        CLAIMS[(template, term)].add("%s:%d" % (fn.__code__.co_filename, fn.__code__.co_firstlineno))
        HANDLERS.setdefault((template, term), fn)
        return fn
    return mark


def lookup(template, term):
    """The handler of (template, term), else the template's fallback, else world_four's chain of the key, else
    None; a request's step by the key it is taken to (requested.lookup_key)."""
    if not (HANDLERS.get((template, term)) or FOUR_RUN.get((template, term))):
        template, term = vocab4.requested.lookup_key(lambda key: key in HANDLERS or key in FOUR_CHAINS,
                                                     template, term)
    return HANDLERS.get((template, term)) or HANDLERS.get((template, None)) or FOUR_RUN.get((template, term))


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


def u_problems(records, unpushable=False):
    """The U17 failures of a scenario's runs (a refused request names a reason and changes nothing), and the store's:
    a request's kept commit shared to its upstream remote (store_git, the decision "Git is the store and the
    isolation", into which U13 retired), not asked under an unpushable remote. Each record {args, returncode, stdout,
    stderr, changed, unshared}."""
    out = []
    for r in records:
        command = " ".join(map(str, r["args"]))
        if r["returncode"] == 0 and r.get("unshared") and not unpushable:
            out.append("store: `%s` kept a commit not shared to %s" % (command, r["unshared"]))
        if r.get("task") and r.get("kept"):
            out.append("U20: `%s` kept a change on the branch of %s" % (command, r["task"]))
        if r["returncode"] != 0 and r["changed"]:
            out.append("U17: `%s` was refused (exit %d) and changed %s" % (command, r["returncode"],
                                                                         ", ".join(r["changed"])))
        elif r["returncode"] != 0 and not ((r.get("stderr") or "") + r["stdout"]).strip():   # the CLI says why on either
            out.append("U17: `%s` was refused (exit %d) and named no reason" % (command, r["returncode"]))
    return out


def tasked(repo, at):
    """U20's part of a run's record: the task whose branch was checked out at `at` (a store_git head, taken before
    the run), else None, and whether a commit was kept on that branch since."""
    task = shop_files.task_of(repo, at[0]) if at else None
    now = store_git.head(repo)
    return {"task": task, "kept": bool(task) and now is not None and now[0] == at[0] and now[1] != at[1]}


def runner(repo, request, scripts=SCRIPTS):
    """`run("spec", "check", ...)`: a script of the plugin run with this Python in the repository; in a generated
    scenario each run is recorded for the U checks."""
    def _run(script, *args, cwd=None, **kwargs):
        record = generated(request.node)
        before, at = (snapshot(repo), store_git.head(repo)) if record else (None, None)
        done = subprocess.run([sys.executable, str(Path(scripts) / script), *map(str, args)], capture_output=True,
                              text=True, cwd=cwd or repo, **kwargs)
        if record:
            after = snapshot(repo)
            changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
            request.node.__dict__.setdefault("_shop_runs", []).append(
                {"args": [script, *args], "returncode": done.returncode, "stdout": done.stdout,
                 "stderr": done.stderr, "changed": changed, "unshared": store_git.unshared(repo, at), **tasked(repo, at)})
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


def _step_function(root, keyword):
    def step_function(text, request, docstring=None, datatable=None):
        call = vocab4.step(root, keyword, text, request)
        if call is None:
            pytest.fail("not read in the step grammar 4 (is its capability codified-2?): %s" % text, pytrace=False)
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
    """One step definition for each keyword (vocab4's)."""
    vocab4.register(namespace, root, _step_function, _marker)


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
