"""features/shop.feature, generated from spec/capabilities/shop.md: every scenario, bound by world_four's `bind` (the chains of the capability each scenario's group moved from first). Its steps are re-keyed for the CLI adapter by requested.py; their handlers are those of the capability its group moved from (vocab.origin). An id still in the capability's `unbuilt:` runs as an expected failure."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .world_four import bind

bind(globals(), ROOT)

scenarios("shop.feature")
