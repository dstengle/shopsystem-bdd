"""features/scenarios.feature, generated from spec/capabilities/scenarios.md: its steps, read in the step grammar 4 and re-keyed for the CLI adapter by requested.py, go to feature-file-tools' own handlers first (feature_file_tools_world's `bind`, the module its handlers loaded), then to the vocabulary's (vocab.py)."""
import sys
from pathlib import Path

from pytest_bdd import scenarios

sys.modules["shop_feature_file_tools_world"].bind(globals(), Path(__file__).resolve().parents[2])
scenarios("scenarios.feature")
