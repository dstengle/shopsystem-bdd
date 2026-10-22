"""Unit tests of design-model-check lines changed with no scenario row yet: r19's README.md under spec/decisions/,
and r27's work-item that is `withdrawn` (work-items decisions-readme-not-read and withdrawn-accepts-not-reported)."""

import unittest

from test_model import HAVE_CLINGO, ModelTest, cap


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class NotReadTest(ModelTest):
    def test_r19_a_readme_under_spec_decisions_is_not_a_decision(self):
        self.good()
        self.write("spec/decisions/README.md", "# Decisions\n\nOne file a decision; index.md is generated.\n")
        found, _ = self.check_json()
        self.assertEqual([p for p in found["problems"] if "README.md" in p], [], found)

    def test_r27_a_withdrawn_work_item_accepting_a_requirement_no_scenario_names_is_no_file_problem(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."]))
        self.observation()
        self.initiative()
        for status, problems in (("withdrawn", 0), ("drafted", 1)):
            with self.subTest(status=status):
                self.work_item(status=status, accepts="[thing#r2]")
                found, _ = self.check_json()
                self.assertEqual(len([p for p in found["problems"] if p.startswith(".shop/work/i1/w1.md: accepts")]),
                                 problems, found)


if __name__ == "__main__":
    unittest.main()
