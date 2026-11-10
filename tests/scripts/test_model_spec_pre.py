"""Unit tests of v15k and v15n over grammar 4's lines: `pre(Q, Key)`, a line's preconditions and trigger, which
model_spec reads only off the old language's trees. Each is an expected failure until a grammar 4 line's `pre` is read
(design-model-check r179 is in `unbuilt:` for it): reading it now finds three pairs of migration-tools' groups that
share their condition and trigger (g29 and g30, g40 and g41, g46 and g57)."""
import unittest

from test_model_spec import ABANDON, COMMIT, START, WQ, CodifiedTest, codified


class PreTest(CodifiedTest):
    @unittest.expectedFailure
    def test_two_statements_of_one_trigger_have_one_pre(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.start_group()))
        pre = sorted(x.split(", ", 1)[1] for x in self.facts() if x.startswith("pre("))
        self.assertEqual(len(pre), 2)
        self.assertEqual(pre[0], pre[1], "both statements share the trigger")

    @unittest.expectedFailure
    def test_statements_of_a_group_with_two_triggers_are_v15k(self):
        self.write("spec/capabilities/wq.md", codified("wq", ["### [g1] Mixed", f"- [r1] {START}", f"- [r2] {ABANDON}"]))
        found, _ = self.check()
        self.assertEqual(self.rows(found, "v15k"), [[f"{WQ}#g1"]], found)

    @unittest.expectedFailure
    def test_two_groups_sharing_features_condition_and_trigger_are_v15n(self):
        self.write("spec/capabilities/wq.md", codified("wq", ["### [g1] A", f"- [r1] {START}", "### [g2] B",
                                                              f"- [r2] {COMMIT}", "### [g3] C", f"- [r3] {ABANDON}"]))
        self.assertEqual(self.rows(self.check()[0], "v15n"), [[f"{WQ}#g1", f"{WQ}#g2"]])


if __name__ == "__main__":
    unittest.main()
