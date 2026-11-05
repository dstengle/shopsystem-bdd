"""features/intake.feature, generated from spec/capabilities/intake.md and bound by the step vocabulary: every
scenario, by `scenarios()`. Its handlers are in intake_handlers.py, over the requests readiness_world.py and
world_nodes.py write and the items backlog_world.py writes; the steps another capability claims reach them through
work_queue_world's `local` table, so this module binds with `bind_all`. A requirement still in the capability's
`unbuilt:` runs as an expected failure."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)
scenarios("intake.feature")
