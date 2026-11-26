"""features/contract-registry.feature, generated from spec/capabilities/contract-registry.md: every scenario, bound by work_queue_world's `bind_all`. Its steps go to contract_registry_handlers' `local`s, which run deposit and retrieve on the shop-folder adapter. An id still in the capability's `unbuilt:` runs as an expected failure."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)

scenarios("contract-registry.feature")
