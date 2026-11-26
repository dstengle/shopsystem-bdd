"""The shared refusal steps (b686): world_refusal's `refuses` (ThenDoes refuse, which requested.py's ThenRefuses
reaches) and world_cli's `refuses` fail on a usage error, argparse's `usage:` on stderr with exit 2, so a scenario
does not pass on a mistyped command; a refusal, exit 1 or exit 2 with no usage text, still passes them."""
import pathlib
import subprocess
import sys
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import world_cli
import world_refusal

STEPS = [world_refusal.refuses, world_cli.refuses]
USAGE = subprocess.CompletedProcess(
    ["work", "decison"], 2, "", "usage: work [-h] {decision,...}\nwork: error: argument command: invalid choice\n")
REFUSALS = [subprocess.CompletedProcess(["work", "decision"], 1, "", "refused: no --tier\n"),
            subprocess.CompletedProcess(["features", "generate", "g"], 2, "", "refused: a guarantees capability\n")]


def step(done):
    return SimpleNamespace(context={"result": done}, text="`work` refuses `work decision`")


@pytest.mark.parametrize("refuses", STEPS)
def test_a_usage_error_fails_the_step(refuses):
    with pytest.raises(AssertionError, match="usage error"):
        refuses(step(USAGE))


@pytest.mark.parametrize("done", REFUSALS)
@pytest.mark.parametrize("refuses", STEPS)
def test_a_refusal_passes_the_step(refuses, done):
    refuses(step(done))
