"""Unit tests of `model restates` (scripts/model_restates) and of `model why` following `restates` (the GF
conversion's design §8.3, §15). The fixture builders are test_model_spec's."""

import json
import subprocess
import sys
import unittest

from test_model_spec import COMMIT, ROOT, SCRIPT, START, WQ, CodifiedTest, codified

OTHER = "When the person runs `work abandon` on an initiative that is `started`, `work` shall set its status to `abandoned`."


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

    def test_json_and_every_capability(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.group("r1@0.29"), dropped=["- r3@0.29: gone."]))
        r = self.run_model("restates", "--json")
        self.assertEqual(r.returncode, 1)
        found = json.loads(r.stdout)
        missing = sorted(row["id"] for row in found["ids"] if row["state"] == "missing")
        self.assertEqual(missing, ["other#r1", "wq#r2", "wq#r4"])
        self.assertEqual([row["by"] for row in found["ids"] if row["id"] == "wq#r1"], [[f"{WQ}#g1"]])

    def test_why_follows_restates_to_the_0_29_text(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.group("r3@0.29")))
        r = self.run_model("why", "wq#r1")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn(START, r.stdout)
        self.assertIn(f"{WQ}#g1", r.stdout)
        self.assertIn("wq#r3@0.29: old 3", r.stdout)
        old = self.run_model("why", "wq#r3@0.29")
        self.assertEqual(old.returncode, 0, old.stderr)
        self.assertIn("old 3", old.stdout)
        self.assertIn(f"restated by {WQ}#g1", old.stdout)
        data = json.loads(self.run_model("why", "--json", "wq#r1").stdout)
        self.assertEqual(data["restates"], [{"id": "wq#r3@0.29", "text": "old 3"}])


class LiveRestatesTest(unittest.TestCase):
    def test_spec_migration_is_not_restated_yet(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(ROOT), "restates", "spec-migration"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertRegex(r.stdout, r"(?m)^spec-migration#r1\b")


if __name__ == "__main__":
    unittest.main()
