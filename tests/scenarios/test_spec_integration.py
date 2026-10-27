"""features/spec-integration.feature, bound to `work run` (scripts/work): the Givens build the repository supervision's
scenarios run in, with an upstream billing kept beside it; the steps are spec_integration_steps.py's."""
from pytest_bdd import scenarios

from .spec_integration_steps import *
from .supervision_world import *     # noqa: F401,F403  (the repo fixture and helpers)

scenarios("spec-integration.feature")
