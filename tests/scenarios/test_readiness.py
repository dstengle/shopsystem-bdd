"""features/readiness.feature, generated from spec/capabilities/readiness.md and bound by the step vocabulary: every
scenario, by `scenarios()`. Its handlers are in readiness_handlers.py, over the codified spec readiness_world.py
writes and the items backlog_world.py writes; the item steps another capability claims reach them through
work_queue_world's `local` table, so this module binds with `bind_all`."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)
scenarios("readiness.feature")
