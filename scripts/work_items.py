"""The plugin's pytest plugin: on every run, a scenario of a requirement its codified capability lists in `unbuilt:`
is a strict xfail (spec_unbuilt). Standard library and pytest only.

It keeps the name of plugin 0.30's `--work-item` plugin, whose options went with `work run` in 0.31.0 (workflow
simplification plan 9, D14), because `batch_tasks`' default test command and consumers' `[batch] tests` load it as
`-p work_items`, the scripts directory on PYTHONPATH; this repository's conftest.py loads it the same way.

It imports `spec_unbuilt` (and with it `spec_read`) only in its collection hook, not at load (b198): `-p work_items`
loads it before a tree's conftest.py runs, and the conftest puts the tree's own scripts first on sys.path, so the
spec modules that mark a tree's scenarios are the tree's, not those of the plugin's scripts on PYTHONPATH.

Each @g<n> and @r<n> tag of the context's features/*.feature is registered as a mark (b419), so that a context's
scenarios run with no PytestUnknownMarkWarning; registering a mark this repository's conftest registers too is
harmless. A context founded by `migrate init` loads this plugin from its tests/scenarios/conftest.py.

Under `work batch done`, each test file `$SHOPSYSTEM_UNREACHED` names (one path a line, relative to where pytest was
started: the tests the task's change does not reach, batch_reach, b456) is left out of collection, and a run that
then collects nothing passes.

Under `work batch start` (batch_laid, b488), `$SHOPSYSTEM_LAID` names the laid lines' requirement ids
(`<capability>#r<n>`, one a line): every scenario but an unbuilt one of those ids is deselected, and each that passes
(non-strict, so an expected failure that passes is passed with its xfail reason) is written to the file
`$SHOPSYSTEM_LAID_REPORT` names, one line `<its ids, comma separated>\t<its title>`, by the process that reports it
(the controller under xdist, never a worker).
"""
import os
import pathlib
import re

UNREACHED = "SHOPSYSTEM_UNREACHED"      # batch_reach.ENV
LAID, LAID_REPORT = "SHOPSYSTEM_LAID", "SHOPSYSTEM_LAID_REPORT"     # batch_laid's
_WORKER = False

TAG = re.compile(r"(?<![\w@])@([rg][1-9]\d*)(?![\w-])")


def spec_root(config):
    """The nearest directory at or above where pytest was started that has spec/capabilities/, else pytest's root."""
    start = pathlib.Path(config.invocation_params.dir).resolve()
    for here in (start, *start.parents):
        if (here / "spec" / "capabilities").is_dir():
            return here
    return pathlib.Path(config.rootpath)


def tags(root):
    """Every g<n> and r<n> a tag of a feature under `root`/features/ names, in order."""
    found = set()
    for path in sorted((pathlib.Path(root) / "features").glob("*.feature")):
        for line in path.read_text().splitlines():
            if line.strip().startswith("@"):
                found |= set(TAG.findall(line))
    return sorted(found, key=lambda m: (m[0], int(m[1:])))


def pytest_configure(config):
    global _WORKER
    _WORKER = hasattr(config, "workerinput")        # an xdist worker (its environment may be inherited by a child)
    for mark in tags(spec_root(config)):     # a scenario's tags are marks (b419)
        config.addinivalue_line("markers", "%s: scenario of %s" % (mark, mark))


def pytest_collection_modifyitems(config, items):
    # imported here, after a tree's conftest has put its own scripts first (b198)
    import spec_unbuilt

    spec_unbuilt.mark(items, spec_root(config))     # an unbuilt requirement's scenario is a strict xfail
    if os.environ.get(LAID):
        _keep_laid(config, items)


def _unbuilt_ids(item):
    marker = item.get_closest_marker("xfail")
    reason = str(marker.kwargs.get("reason", "")) if marker else ""
    return set(reason.removeprefix("unbuilt: ").split(", ")) if reason.startswith("unbuilt: ") else set()


def _keep_laid(config, items):
    """Only the unbuilt scenarios of the ids `$SHOPSYSTEM_LAID` names kept, each with its title as a user property."""
    wanted = set(filter(None, os.environ[LAID].split()))
    kept, gone = [], []
    for item in items:
        if _unbuilt_ids(item) & wanted:
            scenario = item.function.__scenario__
            item.user_properties.append(("scenario", scenario.name))
            kept.append(item)
        else:
            gone.append(item)
    if gone:
        config.hook.pytest_deselected(items=gone)
        items[:] = kept


def pytest_runtest_logreport(report):
    path = os.environ.get(LAID_REPORT)
    reason = getattr(report, "wasxfail", None)
    if not path or _WORKER or report.when != "call" or not report.passed or not reason:
        return
    title = dict(report.user_properties).get("scenario", report.nodeid)
    with open(path, "a", encoding="utf-8") as out:
        out.write("%s\t%s\n" % (str(reason).removeprefix("unbuilt: "), title))


def _unreached(config):
    start = pathlib.Path(config.invocation_params.dir).resolve()
    return {(start / p).resolve() for p in os.environ.get(UNREACHED, "").splitlines() if p.strip()}


def pytest_ignore_collect(collection_path, config):
    if UNREACHED in os.environ and pathlib.Path(collection_path).resolve() in _unreached(config):
        return True
    return None


def pytest_sessionfinish(session, exitstatus):
    if os.environ.get(UNREACHED) and exitstatus == 5:      # every test left out: nothing the change reaches failed
        session.exitstatus = 0
