"""features/telemetry.feature, generated from spec/capabilities/telemetry.md and bound by the step vocabulary: every
scenario, by `scenarios()`. Its handlers are in telemetry_handlers.py, over the batches' world; a step whose key
another capability holds reaches them through work_queue_world's `local` table, so this module binds with
`bind_all`. An id still in the capability's `unbuilt:` runs as an expected failure."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)
scenarios("telemetry.feature")
