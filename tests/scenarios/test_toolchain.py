"""features/toolchain.feature, generated from spec/capabilities/toolchain.md: every scenario, bound by world_four's `bind` over analysis-tools' handlers alone, not the other capabilities' `local` ones. Its steps are re-keyed for the CLI adapter by requested.py; their handlers are those of the capability its group moved from (vocab.origin). An id still in the capability's `unbuilt:` runs as an expected failure."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .world_four import bind

bind(globals(), ROOT, "analysis-tools", local=False)

scenarios("toolchain.feature")
