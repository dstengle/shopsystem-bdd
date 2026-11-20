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
"""
import pathlib
import re

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
    for mark in tags(spec_root(config)):     # a scenario's tags are marks (b419)
        config.addinivalue_line("markers", "%s: scenario of %s" % (mark, mark))


def pytest_collection_modifyitems(config, items):
    # imported here, after a tree's conftest has put its own scripts first (b198)
    import spec_unbuilt

    spec_unbuilt.mark(items, spec_root(config))     # an unbuilt requirement's scenario is a strict xfail
