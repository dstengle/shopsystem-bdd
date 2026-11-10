"""features/batches.feature, generated from spec/capabilities/batches.md and bound by the step vocabulary: every
scenario, by `scenarios()`. Its handlers are in batches_handlers*.py, over the batches, tasks, commits and pull
requests batches_world.py builds and the items backlog_world.py writes; the steps another capability claims reach
them through work_queue_world's `local` table, so this module binds with `bind_all`. A requirement still in the
capability's `unbuilt:` runs as an expected failure."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .world_four import bind

bind(globals(), ROOT, 'batches')
scenarios("batches.feature")
