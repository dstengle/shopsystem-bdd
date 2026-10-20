"""The suite fails when a scenario of a script capability bound by pytest-bdd has no test, or two
(design-decision/plugin-scenarios-run-as-pytest-bdd)."""

import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "features"

# The feature files whose scenarios tests/scenarios/ binds. batch-measurement keeps its docstring binding until
# initiative i12; migration-tools joins the list when initiative i8 adds it.
BOUND_BY_PYTEST_BDD = [
    "features/analysis-tools.feature",
    "features/design-model-check.feature",
    "features/feature-file-tools.feature",
]


class BoundTest(unittest.TestCase):
    def test_every_scenario_has_exactly_one_test(self):
        done = subprocess.run([sys.executable, str(SCRIPT), "--dir", "features", "bindings", "--tests", "tests", "--unbound",
                               *BOUND_BY_PYTEST_BDD], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)


if __name__ == "__main__":
    unittest.main()
