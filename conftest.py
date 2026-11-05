"""`--work-item <name>`: run only the scenarios tagged with a requirement the work-item accepts. The option is the
plugin's own pytest plugin, scripts/work_items.py, the one `work run` loads in a repository it delivers.

The ceiling (design-r3 §7): each test whose setup, call and teardown together take longer than
`$SHOPSYSTEM_TEST_CEILING` seconds (10 by default) is listed at the end of the run, slowest first. Under xdist the
reports reach the controller, which sums them. It reports and does not fail.

The `live_logic` tests are one xdist group (`--dist loadgroup` in pytest.ini), so one worker solves the live spec."""
import os
import pathlib
import sys

import pytest

SCRIPTS = str(pathlib.Path(__file__).parent / "scripts")
if SCRIPTS not in sys.path:
    sys.path.append(SCRIPTS)

pytest_plugins = ["work_items"]
_durations = {}


def _quiet_git():
    """No background maintenance in the suite's repositories (plan 5 review, S6): every git a test runs, `work`'s
    included, inherits `maintenance.auto=false` and `gc.auto=0`, added after any `GIT_CONFIG_*` already set."""
    count = int(os.environ.get("GIT_CONFIG_COUNT", "0") or 0)
    for key, value in (("maintenance.auto", "false"), ("gc.auto", "0")):
        os.environ["GIT_CONFIG_KEY_%d" % count], os.environ["GIT_CONFIG_VALUE_%d" % count] = key, value
        count += 1
    os.environ["GIT_CONFIG_COUNT"] = str(count)


if "maintenance.auto" not in {v for k, v in os.environ.items() if k.startswith("GIT_CONFIG_KEY_")}:
    _quiet_git()


def _ceiling():
    return float(os.environ.get("SHOPSYSTEM_TEST_CEILING", "10"))


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items):
    """Every `live_logic` test is one xdist group: the live spec is solved once a run, on one worker (plan-r3 S12).
    First, so that xdist's own hook reads the group."""
    for item in items:
        if item.get_closest_marker("live_logic"):
            item.add_marker(pytest.mark.xdist_group("live_logic"))


def pytest_runtest_logreport(report):
    _durations[report.nodeid] = _durations.get(report.nodeid, 0.0) + report.duration


def pytest_terminal_summary(terminalreporter):
    ceiling = _ceiling()
    over = sorted(((s, n) for n, s in _durations.items() if s > ceiling), key=lambda sn: (-sn[0], sn[1]))
    if over:
        terminalreporter.write_line("tests over the %g s ceiling:" % ceiling)
        for seconds, nodeid in over:
            terminalreporter.write_line("%.2f %s" % (seconds, nodeid))
