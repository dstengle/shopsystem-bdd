"""features/request-watch.feature, generated from spec/capabilities/request-watch.md: every scenario, bound by work_queue_world's `bind_all`. Its steps are re-keyed for the CLI adapter by requested.py; their handlers are those of the capability its group moved from (vocab.origin). An id still in the capability's `unbuilt:` runs as an expected failure."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)

scenarios("request-watch.feature")
