"""features/supervision.feature, generated from spec/capabilities/supervision.md and bound by the step vocabulary: every
scenario, by `scenarios()`. Its handlers are in supervision_handlers*.py; the repository `work run` runs in is built
by supervision_build.py beside the stand-in claude's directory, so `repo` is a directory of its own under tmp_path.
`bind_all` (work_queue_world.py) binds a step whose noun phrase names its kind with no instance (`a `research` stage
for the work-item w1`), which the vocabulary's own definitions miss by the words of their patterns."""
import pytest
from pytest_bdd import scenarios

from .conftest import ROOT
from .work_queue_world import bind_all


@pytest.fixture
def repo(tmp_path):
    """The repository work run runs in; the stand-in's script and record live beside it, outside it."""
    path = tmp_path / "repo"
    path.mkdir()
    return path


bind_all(globals(), ROOT)
scenarios("supervision.feature")
