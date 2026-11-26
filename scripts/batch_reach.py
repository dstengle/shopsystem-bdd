"""The tests a task's change reaches (b456, batches r78): `work batch done` runs only them, `work batch review` the
whole suite.

A capability's scenario test `tests/scenarios/test_<capability>.py` is reached when the item holds a requirement id
of the capability, or a kept change of the task (a commit on its branch since the batch's lines commit) touches the
capability's feature `features/<capability>.feature` or the test itself. A test of `tests/scripts/` is reached when
the change touches it, or touches a module it names: a file of `scripts/` or a helper of `tests/scripts/` whose stem
the test's text holds as a word, a module of a package also after its package's dotted name (`plumbing.shop_files`,
b771) (a helper that names a touched module counting as touched), or whose stem's first part opens the test's name (`batch_tasks.py` reaches `test_batch_*.py`). Every other test is run. A change to a
`conftest.py` or `pytest.ini` reaches every test.

The tests not reached are given to the pytest plugin `work_items` as `$SHOPSYSTEM_UNREACHED`, one path a line
relative to where the tests run, which it leaves out of collection whatever `[batch] tests` names (`work_items`)."""
import re
from pathlib import Path

ENV = "SHOPSYSTEM_UNREACHED"
EVERYTHING = ("conftest.py", "pytest.ini")


def touched(git, tree, since, branch):
    """The paths the commits on `branch` after `since` change."""
    return set(filter(None, git(tree, "diff", "--name-only", since, branch).stdout.splitlines()))


def _scenario_tests(tree, capabilities, changed):
    found = []
    for spec in sorted((Path(tree) / "spec" / "capabilities").glob("*.md")):
        cap = spec.stem
        test = "tests/scenarios/test_%s.py" % cap.replace("-", "_")
        reached = cap in capabilities or {test, "features/%s.feature" % cap} & changed
        if (Path(tree) / test).is_file() and not reached:
            found.append(test)
    return found


def _names(text, module):
    """Whether `text` names `module`, a (package, stem) pair, as a word not after a dot, or after its package's name
    and a dot."""
    package, stem = module
    after = r"|(?<=(?<![\w.])%s\.)" % re.escape(package) if package else ""
    return re.search(r"(?:(?<![\w.])%s)%s(?!\w)" % (after, re.escape(stem)), text) is not None


def _module(path):
    """A changed file's (package, stem): its package the dotted folders between `scripts/` and it ("" when none)."""
    parts = Path(path).parts
    return ".".join(parts[1:-1]) if parts[0] == "scripts" else "", Path(path).name.removesuffix(".py")


def _script_tests(tree, changed):
    here = Path(tree) / "tests" / "scripts"
    stems = {_module(p) for p in changed
             if p.startswith("scripts/") or (p.startswith("tests/scripts/") and p.count("/") == 2)}
    helpers = [p for p in sorted(here.glob("*.py")) if not p.name.startswith("test_")]
    stems |= {("", p.stem) for p in helpers if any(_names(p.read_text(), s) for s in stems)}
    found = []
    for test in sorted(here.glob("test_*.py")):
        rel = test.relative_to(tree).as_posix()
        text = test.read_text()
        reached = rel in changed or any(_names(text, s) or test.stem.startswith("test_%s" % s[1].split("_")[0])
                                        for s in stems)
        if not reached:
            found.append(rel)
    return found


def unreached(git, tree, since, branch, ids):
    """The test files of `tree` the task's change does not reach, its item holding the requirement ids `ids`
    (`<capability>#r<n>`); none when the change touches a `conftest.py` or `pytest.ini`."""
    changed = touched(git, tree, since, branch)
    if any(Path(p).name in EVERYTHING for p in changed):
        return []
    capabilities = {i.split("#")[0] for i in ids}
    return _scenario_tests(tree, capabilities, changed) + _script_tests(tree, changed)


def laid(tree, capabilities):
    """The test files of `tree` but the scenario tests of `capabilities` (b488): what `work batch start`'s run of the
    laid lines' scenarios (batch_laid) leaves out."""
    return _scenario_tests(tree, set(capabilities), set()) + _script_tests(tree, set())
