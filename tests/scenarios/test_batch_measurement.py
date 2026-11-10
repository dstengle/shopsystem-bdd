"""features/batch-measurement.feature, generated from spec/capabilities/batch-measurement.md and bound by pytest-bdd;
its steps are the vocabulary's (vocab.py), run by the handlers of batch_measurement_handlers.py."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)

scenarios("batch-measurement.feature")
