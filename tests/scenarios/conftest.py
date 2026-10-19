"""Fixtures every scenario step module shares."""
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"


@pytest.fixture
def repo(tmp_path):
    """A fresh temporary directory, the root of the repository a scenario builds."""
    return tmp_path


@pytest.fixture
def context():
    """What a When step leaves for the Then steps."""
    return {}


@pytest.fixture
def run(repo):
    """Run one of the scripts (model, features, tools) with this Python; return the completed process.

    `run("model", "check", "--root", ...)`: the arguments go to the script as given; `cwd` defaults to the repository root.
    """
    def _run(script, *args, cwd=None, **kwargs):
        cmd = [sys.executable, str(SCRIPTS / script), *map(str, args)]
        return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or repo, **kwargs)
    return _run


def pytest_configure(config):
    """The feature files' requirement tags (@r1 ...) are marks; register them."""
    for number in range(1, 200):
        config.addinivalue_line("markers", "r%d: scenario of requirement r%d" % (number, number))
