"""features/decision-tiers.feature, generated from spec/capabilities/decision-tiers.md and bound by the step vocabulary:
every scenario, by `scenarios()`. Its handlers are in decision_tiers_handlers.py, with `model` run through
design-model-check's; a design-decision's condition, whose key design-model-check holds, reaches them through
work_queue_world's `local` table, so this module binds with `bind_all`. An id still in the capability's `unbuilt:`
runs as an expected failure."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)
scenarios("decision-tiers.feature")
