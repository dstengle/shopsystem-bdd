"""features/batch-measurement.feature, bound to scripts/measure.

The Given steps describe the initiative's log, its stages' sessions, transcripts and commits on a World; the When
runs `measure initiative` once, in-process, in the repository; the Then steps read the measurement or the refusal.
The World is batch_measurement_world.py, the steps batch_measurement_*_steps.py.
"""
from pytest_bdd import scenarios

from .batch_measurement_given_steps import *
from .batch_measurement_reading_steps import *
from .batch_measurement_request_steps import *
from .batch_measurement_show_steps import *
from .batch_measurement_then_steps import *
from .batch_measurement_world import measure_run, world  # noqa: F401  fixtures

scenarios("batch-measurement.feature")
