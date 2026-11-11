"""Unit tests of `model restates` (scripts/model_restates) (the GF conversion's design §8.3, §15). The fixture builders are test_model_spec's."""

import json
import subprocess
import sys
import unittest

from test_model_spec import COMMIT, ROOT, SCRIPT, START, WQ, CodifiedTest, codified

OTHER = "While an initiative is `started`, when the person runs `work abandon` on the initiative, `work` shall set the status of the initiative to `abandoned`."


class RestatesTest(CodifiedTest):
    def setUp(self):
        super().setUp()
        self.write("spec/restated.json", json.dumps({f"wq#r{n}": {"text": f"old {n}", "line": n} for n in range(1, 5)}
                                                    | {"other#r1": {"text": "other one", "line": 9}}))

    def group(self, restates):
        return ["### [g1] Start", f"Restates: {restates}.", f"- [r1] {START}", f"- [r2] {COMMIT}"]

    def test_every_id_restated_or_dropped_exits_0(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.group("r1@0.29, r2@0.29"),
                                                       dropped=["- r3@0.29: restated U3.", "- r4@0.29: no longer done."]))
        r = self.run_model("restates", "wq")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_an_id_neither_restated_nor_dropped_exits_1_naming_it(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.group("r1@0.29"), dropped=["- r3@0.29: gone."]))
        r = self.run_model("restates", "wq")
        self.assertEqual(r.returncode, 1)
        self.assertIn("wq#r2", r.stdout)
        self.assertIn("wq#r4", r.stdout)
        self.assertNotIn("wq#r1:", r.stdout)

    def test_an_uncodified_capability_has_nothing_restated(self):
        self.write("spec/capabilities/wq.md", codified("wq", ["- [r1] **When** asked, `wq` shall answer."], marker=False))
        r = self.run_model("restates", "wq")
        self.assertEqual(r.returncode, 1)
        self.assertIn("wq#r1", r.stdout)

    def test_a_move_into_an_uncodified_capability_is_pending(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.group("r1@0.29, r2@0.29, r3@0.29"),
                                                       dropped=["- r4@0.29: moved to other."]))
        self.write("spec/capabilities/other.md", codified("other", ["- [r1] **When** asked, `o` shall answer."],
                                                          marker=False))
        r = self.run_model("restates", "wq")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("pending", r.stdout)

    def test_a_move_into_a_codified_capability_must_be_restated_there(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.group("r1@0.29, r2@0.29, r3@0.29"),
                                                       dropped=["- r4@0.29: moved to other."]))
        self.write("spec/capabilities/other.md", codified("other", ["### [g1] Abandon", "Restates: other#r1@0.29.",
                                                                     f"- [r1] {OTHER}"]))
        r = self.run_model("restates", "wq")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("wq#r4", r.stdout)
        self.write("spec/capabilities/other.md", codified("other", ["### [g1] Abandon",
                                                                     "Restates: other#r1@0.29, wq#r4@0.29.",
                                                                     f"- [r1] {OTHER}"]))
        self.assertEqual(self.run_model("restates", "wq").returncode, 0)

    def test_a_moved_id_retired_in_its_target_is_dropped(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.group("r1@0.29, r2@0.29, r3@0.29"),
                                                       dropped=["- r4@0.29: moved to other."]))
        why = "retired with other#r3 in 0.31.0 (the-old-workflow-retired)."
        self.write("spec/capabilities/other.md", codified("other", ["### [g1] Abandon", "Restates: other#r1@0.29.",
                                                                     f"- [r1] {OTHER}"], dropped=[f"- wq#r4@0.29: {why}"]))
        r = self.run_model("restates", "--json")
        rows = {row["id"]: row for row in json.loads(r.stdout)["ids"]}
        self.assertEqual((rows["wq#r4"]["state"], rows["wq#r4"]["reason"]), ("dropped", why))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_a_moved_id_restated_by_its_target_is_still_restated(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.group("r1@0.29, r2@0.29, r3@0.29"),
                                                       dropped=["- r4@0.29: moved to other."]))
        self.write("spec/capabilities/other.md", codified("other", ["### [g1] Abandon",
                                                                     "Restates: other#r1@0.29, wq#r4@0.29.",
                                                                     f"- [r1] {OTHER}"]))
        rows = {row["id"]: row for row in json.loads(self.run_model("restates", "--json").stdout)["ids"]}
        self.assertEqual(rows["wq#r4"]["state"], "restated")

    def test_json_and_every_capability(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.group("r1@0.29"), dropped=["- r3@0.29: gone."]))
        r = self.run_model("restates", "--json")
        self.assertEqual(r.returncode, 1)
        found = json.loads(r.stdout)
        missing = sorted(row["id"] for row in found["ids"] if row["state"] == "missing")
        self.assertEqual(missing, ["other#r1", "wq#r2", "wq#r4"])
        self.assertEqual([row["by"] for row in found["ids"] if row["id"] == "wq#r1"], [[f"{WQ}#g1"]])


class LiveRestatesTest(unittest.TestCase):
    def test_the_whole_spec_is_restated_with_nothing_pending(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(ROOT), "restates"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertRegex(r.stdout, r"\b0 pending, 0 missing\b")

if __name__ == "__main__":
    unittest.main()
