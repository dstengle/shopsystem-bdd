"""features/laying.feature, generated from spec/capabilities/laying.md: every scenario, bound by work_queue_world's `bind_all`. Its steps go to laying_handlers' `local`s, which lay, lift and check an item through the laying port with the in-process adapter. An id still in the capability's `unbuilt:` runs as an expected failure."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)

scenarios("laying.feature")
