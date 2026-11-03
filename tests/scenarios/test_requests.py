"""features/requests.feature, generated from spec/capabilities/requests.md and bound by the step vocabulary: every
scenario, by `scenarios()`. Its handlers are in requests_handlers.py (and work_queue_handlers.py for `work`'s
output, its errors and the files it writes and commits)."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)
scenarios("requests.feature")
