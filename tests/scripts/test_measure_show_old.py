"""An initiative's measurement of plugin 0.30 is still shown and compared after `measure initiative` is retired
(workflow simplification plan 9, Task 7; batch-measurement r18-r22 kept, so history stays readable)."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MEASURE = REPO / "scripts" / "measure"


def newest():
    """The newest real 0.30 initiative record of this repository."""
    found = sorted(p for p in (REPO / ".shop/records/measurements").glob("*.md") if re.search(r"-i\d+(-|\.md$)", p.name))
    return found[-1]


def measure(cwd, *args):
    return subprocess.run([sys.executable, str(MEASURE), *args], cwd=cwd, capture_output=True, text=True)


def test_an_initiative_measurement_is_still_shown_and_compared(tmp_path):
    record = tmp_path / ".shop/records/measurements" / newest().name
    record.parent.mkdir(parents=True)
    shutil.copyfile(newest(), record)
    shown = measure(tmp_path, "show", str(record))
    assert shown.returncode == 0, shown.stderr
    assert "stages" in shown.stdout and "totals" in shown.stdout, shown.stdout
    compared = measure(tmp_path, "compare", str(record), str(record))
    assert compared.returncode == 0, compared.stderr
    assert "ratio" in compared.stdout, compared.stdout
    gone = measure(tmp_path, "initiative", "i1")
    assert gone.returncode == 2 and "invalid choice: 'initiative'" in gone.stderr, gone.stderr
