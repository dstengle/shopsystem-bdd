"""features/work-queue.feature, generated from spec/capabilities/work-queue.md and bound by the step vocabulary: every
scenario, by `scenarios()`. Its handlers are in work_queue_handlers.py."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)
scenarios("work-queue.feature")
