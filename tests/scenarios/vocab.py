"""The step vocabulary in pytest-bdd (design §14.3): one step definition for each keyword, matching a step the step
grammar 4 reads (vocab4), dispatching to the handler `lookup` finds, and the checks of the observable
universal conditions after every generated scenario (design §8.4: U12, a refused command changes nothing; U13, a
commit a command makes in a repository with a remote is pushed, but under a remote the scenario made unpushable; U16,
`--json` prints one JSON object; U11, U4 and U8 before b240's rewording, decisions 0086-0088).

Each text is parsed once a process. `install(namespace, root, tests_dir)`
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

if __package__:
    from . import vocab4
else:   # loaded by path, as `features vocab --check` loads it
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import vocab4
    sys.path.pop(0)

HANDLERS, CLAIMS = {}, defaultdict(set)
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
    None."""
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


def _git(repo, *args):
    done = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else None


def branch_head(repo):
    """(branch, its commit) checked out in `repo`, or None outside git or on a detached HEAD."""
    branch = (Path(repo) / ".git").exists() and _git(repo, "symbolic-ref", "-q", "--short", "HEAD")
    return (branch, _git(repo, "rev-parse", "HEAD")) if branch else None


def unpushed(repo, before):
    """The remote a run's commit on the branch checked out is not pushed to (U13), or None: none when the run made no
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
    """The U12, U13 and U16 failures of a scenario's runs, each record {args, returncode, stdout, changed, unpushed};
    U13 is not asked under an unpushable remote."""
    out = []
    for r in records:
        command = " ".join(map(str, r["args"]))
        if r["returncode"] == 0 and r.get("unpushed") and not unpushable:
            out.append("U13: `%s` committed and did not push the commit to %s" % (command, r["unpushed"]))
        if r["returncode"] != 0 and r["changed"]:
            out.append("U12: `%s` was refused (exit %d) and changed %s" % (command, r["returncode"],
                                                                         ", ".join(r["changed"])))
        if r["returncode"] == 0 and "--json" in map(str, r["args"]):
            try:
                one = isinstance(json.loads(r["stdout"]), dict)
            except ValueError:
                one = False
            if not one:
                out.append("U16: `%s` printed something other than one JSON object" % command)
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
