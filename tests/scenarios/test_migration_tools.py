"""features/migration-tools.feature, generated from spec/capabilities/migration-tools.md and bound by pytest-bdd; its
steps are the vocabulary's (vocab.py), run by the handlers of migration_tools_handlers.py and world_run.py."""
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all

bind_all(globals(), ROOT)

scenarios("migration-tools.feature")
