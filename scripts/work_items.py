"""The plugin's pytest plugin: on every run, a scenario of a requirement its codified capability lists in `unbuilt:`
is a strict xfail (spec_unbuilt). Standard library and pytest only.

It keeps the name of plugin 0.30's `--work-item` plugin, whose options went with `work run` in 0.31.0 (workflow
simplification plan 9, D14), because `batch_tasks`' default test command and consumers' `[batch] tests` load it as
`-p work_items`, the scripts directory on PYTHONPATH; this repository's conftest.py loads it the same way.

It imports `spec_unbuilt` (and with it `spec_read`) only in its collection hook, not at load (b198): `-p work_items`
loads it before a tree's conftest.py runs, and the conftest puts the tree's own scripts first on sys.path, so the
spec modules that mark a tree's scenarios are the tree's, not those of the plugin's scripts on PYTHONPATH.
"""
import pathlib


def spec_root(config):
    """The nearest directory at or above where pytest was started that has spec/capabilities/, else pytest's root."""
    start = pathlib.Path(config.invocation_params.dir).resolve()
    for here in (start, *start.parents):
        if (here / "spec" / "capabilities").is_dir():
            return here
    return pathlib.Path(config.rootpath)


def pytest_collection_modifyitems(config, items):
    # imported here, after a tree's conftest has put its own scripts first (b198)
    import spec_unbuilt

    spec_unbuilt.mark(items, spec_root(config))     # an unbuilt requirement's scenario is a strict xfail
