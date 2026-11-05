"""The plugin's pytest plugin: on every run, a scenario of a requirement its codified capability lists in `unbuilt:`
is a strict xfail (spec_unbuilt). Standard library and pytest only.

It keeps the name of plugin 1.x's `--work-item` plugin, whose options went with `work run` in 2.0.0 (workflow
simplification plan 9, D14), because `batch_tasks`' default test command and consumers' `[batch] tests` load it as
`-p work_items`, the scripts directory on PYTHONPATH; this repository's conftest.py loads it the same way.
"""
import pathlib

import spec_unbuilt


def spec_root(config):
    """The nearest directory at or above where pytest was started that has spec/capabilities/, else pytest's root."""
    start = pathlib.Path(config.invocation_params.dir).resolve()
    for here in (start, *start.parents):
        if (here / "spec" / "capabilities").is_dir():
            return here
    return pathlib.Path(config.rootpath)


def pytest_collection_modifyitems(config, items):
    spec_unbuilt.mark(items, spec_root(config))     # an unbuilt requirement's scenario is a strict xfail
