"""features/conversation.feature, generated from spec/capabilities/conversation.md and bound by the step vocabulary:
every scenario, by `scenarios()`. Its handlers are in conversation_handlers.py; a step whose key another capability
claims reaches them through work_queue_world's `local` table, so this module binds with `bind_all`. A requirement
still in the capability's `unbuilt:` runs as an expected failure."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)
scenarios("conversation.feature")
