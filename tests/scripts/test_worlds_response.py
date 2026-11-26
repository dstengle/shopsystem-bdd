"""consistency r46/r47's Thens tell the two worlds apart (b783): design_model_check_worlds_response's `framed` builds
lodge's frames of two prepositions (g46) or of one preposition its two frames share (g47) by the scenario's group,
and the consequence c1 the Then expects is set by the scenario's own Givens. Each scenario run in the other's world
(the group pick swapped by a plugin that monkeypatches `shared`) fails on that Then; in its own world it passes."""
import os
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = "shop_design_model_check_worlds_response"
PLUGIN = '''import sys


def pytest_runtest_setup(item):
    """`framed`'s group pick swapped, so a scenario is built in the other world."""
    module = sys.modules["%s"]
    picked = module.shared
    module.shared = lambda step: not picked(step)
''' % MODULE
SCENARIOS = {"g46": "frame_its_line_uses", "g47": "frames_share"}


def scenario(tmp_path, group, swapped):
    """Consistency's scenario of the group, run with the pick swapped or not."""
    args = [sys.executable, "-m", "pytest", "-q", "-n", "0", "-p", "no:cacheprovider",
            "tests/scenarios/test_consistency.py", "-k", SCENARIOS[group]]
    env = dict(os.environ)
    if swapped:
        (tmp_path / "swap_world.py").write_text(PLUGIN)
        env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(tmp_path), env.get("PYTHONPATH")]))
        args[3:3] = ["-p", "swap_world"]
    return subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True, timeout=600)


@pytest.mark.parametrize("group", sorted(SCENARIOS))
def test_scenario_in_the_other_world_fails_on_its_consequence(tmp_path, group):
    done = scenario(tmp_path, group, swapped=True)
    assert done.returncode == 1 and "1 failed" in done.stdout, done.stdout + done.stderr
    assert "printed_consequence" in done.stdout, done.stdout


@pytest.mark.parametrize("group", sorted(SCENARIOS))
def test_scenario_in_its_own_world_not_the_other_world_passes(tmp_path, group):
    done = scenario(tmp_path, group, swapped=False)
    assert done.returncode == 0 and "1 passed" in done.stdout, done.stdout + done.stderr
