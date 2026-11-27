"""features/applying.feature, generated from spec/capabilities/applying.md: every scenario, bound by work_queue_world's `bind_all`. Its steps go to applying_handlers' `local`s, which apply an item to a specification through the specification service's apply (spec_apply). An id still in the capability's `unbuilt:` runs as an expected failure."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)

scenarios("applying.feature")
