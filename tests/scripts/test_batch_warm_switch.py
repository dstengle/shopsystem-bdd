"""b592: the tests switch off the warming that `work batch merged` starts (b588). `batch_warm.start` does nothing while
`$SHOPSYSTEM_NO_WARM` is set, which tests/scripts/conftest.py and tests/scenarios/conftest.py set for every test, so a
test that runs `work batch merged` leaves no warming compiling and prefetching into the cache; test_batch_opening
unsets it."""
import os
from pathlib import Path

import batch_warm
from backlog_testing import work
from test_batch_close import merge, reviewed  # noqa: F401  (the fixture)
from test_batch_review import both_done  # noqa: F401  (the fixture)
from test_batch_tasks import started  # noqa: F401  (the fixture)


def _warmings(root):
    """The running processes of batch_warm.py warming `root`."""
    found = []
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit():
            continue
        try:
            argv = (proc / "cmdline").read_bytes().split(b"\0")
        except OSError:
            continue
        words = [a.decode(errors="replace") for a in argv]
        if any(w.endswith("batch_warm.py") for w in words) and str(root) in words:
            found.append(int(proc.name))
    return found


def test_the_conftest_switches_the_warming_off():
    assert os.environ.get("SHOPSYSTEM_NO_WARM")


def test_start_does_nothing_while_switched_off(tmp_path):
    assert batch_warm.start(tmp_path) is None
    assert _warmings(tmp_path) == []


def test_start_warms_once_switched_on(tmp_path, monkeypatch):
    monkeypatch.delenv("SHOPSYSTEM_NO_WARM")
    missing = tmp_path / "missing"          # a warming of nothing, which fails at once
    process = batch_warm.start(missing)
    assert process is not None
    process.wait(timeout=60)


def test_merged_leaves_no_warming(reviewed, batch_outside):  # noqa: F811
    merge(reviewed, batch_outside)
    done = work(reviewed, "batch", "merged", "batch-1")
    assert done.returncode == 0, done.stderr
    assert _warmings(reviewed) == []
