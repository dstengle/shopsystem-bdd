"""`--work-item <name>`: run only the scenarios tagged with a requirement the work-item accepts. The option is the
plugin's own pytest plugin, scripts/work_items.py, the one `work run` loads in a repository it delivers.

The ceiling (design-r3 §7): each test whose setup, call and teardown together take longer than
`$SHOPSYSTEM_TEST_CEILING` seconds (10 by default) is listed at the end of the run, slowest first. Under xdist the
reports reach the controller, which sums them. It reports and does not fail."""
import os
import pathlib
import sys

SCRIPTS = str(pathlib.Path(__file__).parent / "scripts")
if SCRIPTS not in sys.path:
    sys.path.append(SCRIPTS)

pytest_plugins = ["work_items"]
_durations = {}


def _ceiling():
    return float(os.environ.get("SHOPSYSTEM_TEST_CEILING", "10"))


def pytest_runtest_logreport(report):
    _durations[report.nodeid] = _durations.get(report.nodeid, 0.0) + report.duration


def pytest_terminal_summary(terminalreporter):
    ceiling = _ceiling()
    over = sorted(((s, n) for n, s in _durations.items() if s > ceiling), key=lambda sn: (-sn[0], sn[1]))
    if over:
        terminalreporter.write_line("tests over the %g s ceiling:" % ceiling)
        for seconds, nodeid in over:
            terminalreporter.write_line("%.2f %s" % (seconds, nodeid))
