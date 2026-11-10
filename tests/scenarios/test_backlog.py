"""features/backlog.feature, generated from spec/capabilities/backlog.md and bound by the step vocabulary: every
scenario, by `scenarios()`. Its handlers are in backlog_handlers.py, over the repository backlog_world.py writes; a step
whose key another capability claims reaches them through work_queue_world's `local` table, so this module binds with
world_four's `bind`, its grammar 4 handlers first. A requirement still in the capability's `unbuilt:` runs as an expected failure."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .world_four import bind

bind(globals(), ROOT, 'backlog')
scenarios("backlog.feature")
