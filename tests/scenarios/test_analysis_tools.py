"""features/analysis-tools.feature, generated from spec/capabilities/analysis-tools.md and bound by pytest-bdd; its
steps are the vocabulary's (vocab.py), run by the handlers of analysis_tools_handlers.py."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .world_four import bind

bind(globals(), ROOT, "analysis-tools", local=False)

scenarios("analysis-tools.feature")
