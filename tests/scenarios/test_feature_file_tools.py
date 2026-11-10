"""features/feature-file-tools.feature, generated from spec/capabilities/feature-file-tools.md (codified-2) and bound
by pytest-bdd; its steps, read in the step grammar 4, go to feature-file-tools' own handlers first
(feature_file_tools_world's `bind`, the module its handlers loaded), then to the vocabulary's (vocab.py)."""
import sys
from pathlib import Path

from pytest_bdd import scenarios

sys.modules["shop_feature_file_tools_world"].bind(globals(), Path(__file__).resolve().parents[2])
scenarios("feature-file-tools.feature")
