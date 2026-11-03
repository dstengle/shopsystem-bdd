"""features/design-model-check.feature, generated from spec/capabilities/design-model-check.md and bound by the step
vocabulary: every scenario, by `scenarios()`. Its handlers are in design_model_check_handlers*.py."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)
scenarios("design-model-check.feature")
