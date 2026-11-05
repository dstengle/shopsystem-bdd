"""The suite fails when a scenario of a script capability bound by pytest-bdd has no test, or two
(design-decision/plugin-scenarios-run-as-pytest-bdd)."""

import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "features"

# The feature files whose scenarios tests/scenarios/ binds.
BOUND_BY_PYTEST_BDD = [
    "features/analysis-tools.feature",
    "features/backlog.feature",
    "features/batch-measurement.feature",
    "features/batches.feature",
    "features/conversation.feature",
    "features/decision-tiers.feature",
    "features/design-model-check.feature",
    "features/feature-file-tools.feature",
    "features/intake.feature",
    "features/migration-tools.feature",
    "features/readiness.feature",
    "features/telemetry.feature",
]


class BoundTest(unittest.TestCase):
    def test_every_step_of_a_generated_feature_has_one_handler(self):
        """A generated feature's steps are bound by the vocabulary (design §14.3): `features vocab --check` replaces
        the file list below as each capability is converted."""
        sys.path.insert(0, str(ROOT / "tests"))
        import toolchain
        toolchain.require()
        done = subprocess.run([sys.executable, str(SCRIPT), "vocab", "--check", "--tests", "tests/scenarios"], cwd=ROOT,
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    def test_every_scenario_has_exactly_one_test(self):
        done = subprocess.run([sys.executable, str(SCRIPT), "--dir", "features", "bindings", "--tests", "tests", "--unbound",
                               *BOUND_BY_PYTEST_BDD], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)


if __name__ == "__main__":
    unittest.main()
