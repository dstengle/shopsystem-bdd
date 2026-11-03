"""migrate run's @holding scenarios: deleted, since `features deprecate` is removed (migration-tools r3@0.29 dropped)."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from migrate_layout import Plan
from migrate_spec import plan_holding

FEATURE = """Feature: Queue

  @holding
  Scenario: Held
    Given a queue
    Then it is held

  Scenario: Kept
    Given a queue
    Then it is kept
"""


class HoldingTest(unittest.TestCase):
    def test_a_holding_scenario_is_deleted_and_the_others_kept(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "features").mkdir()
            (root / "features/queue.feature").write_text(FEATURE)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            plan = Plan(root, "ctx")
            plan_holding(plan)
            self.assertEqual(plan.failures, [])
            text = plan.texts["features/queue.feature"]
            self.assertNotIn("Held", text)
            self.assertNotIn("@holding", text)
            self.assertIn("Scenario: Kept", text)


if __name__ == "__main__":
    unittest.main()
