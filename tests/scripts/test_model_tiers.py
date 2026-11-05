"""Unit tests of decision-tiers r1, r2, r3 and r6 (workflow simplification plan 6, D2-D4, D12): a decision's `tier`
and `enforced_by` read by `model check`, the rules `w_untiered`, `v_d6`, `v_d7` and `v_d8`, an `enforced_by` written
wrong named, and the index's `tier` column. The scenarios of features/decision-tiers.feature are bound in
tests/scenarios/test_decision_tiers.py; these check what their steps do not (history, chains, the wrong forms)."""

import sys
import unittest

from test_model import HAVE_CLINGO, ROOT, ModelTest, full

sys.path.insert(0, str(ROOT / "scripts"))
import model_report


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class TiersTest(ModelTest):
    def decision(self, name, *fields, status="accepted"):
        """spec/decisions/<name>.md, accepted unless given, with each `key: value` of `fields` in its frontmatter."""
        head = "".join(f"{f}\n" for f in fields)
        status = f"status: {status}\n" if status else ""
        return self.write(f"spec/decisions/{name}.md", f"---\nid: {full('design-decision', name)}\nsummary: s\n"
                                                       f"{status}{head}---\n# {name}\n\n## Decision\nSo.\n")

    def rows(self, code):
        found, _ = self.check_json()
        return sorted(a for name, a in found["violations"] + found["warnings"] if name == code), found

    def test_w_untiered_names_a_decision_with_no_tier(self):
        self.good()
        self.decision("a")
        rows, found = self.rows("w_untiered")
        self.assertEqual(rows, [[full("design-decision", "a")]], found)
        self.decision("a", "tier: judgement")
        self.assertEqual(self.rows("w_untiered")[0], [])

    def test_history_needs_no_tier(self):
        self.good()
        self.decision("a", status="superseded")
        self.decision("b", status="rejected")
        self.decision("c", status=None)
        rows, found = self.rows("w_untiered")
        self.assertEqual(rows, [[full("design-decision", "c")]], found)

    def test_v_d6_a_check_decision_with_no_test(self):
        self.good()
        self.decision("a", "tier: check")
        rows, found = self.rows("v_d6")
        self.assertEqual(rows, [[full("design-decision", "a")]], found)
        self.decision("a", "tier: check", "enforced_by: [tests/test_x.py::test_x]")
        self.write("tests/test_x.py", "def test_x():\n    pass\n")
        rows, found = self.rows("v_d6")
        self.assertEqual(rows, [], found)
        self.assertEqual(found["problems"], [], found)

    def test_v_d7_a_requirement_decision_with_no_requirement(self):
        self.good()
        self.decision("a", "tier: requirement")
        rows, found = self.rows("v_d7")
        self.assertEqual(rows, [[full("design-decision", "a")]], found)
        self.decision("a", "tier: requirement", "enforced_by: [thing#r1]")
        rows, found = self.rows("v_d7")
        self.assertEqual(rows, [], found)
        self.assertEqual((found["unresolved"], found["problems"]), ([], []), found)

    def test_v_d8_fires_only_for_accepted_pairs(self):
        """A -> B -> C (A supersedes B, B supersedes C): each row is (the superseded, its superseder)."""
        a, b, c = (full("design-decision", n) for n in "abc")
        for statuses, wanted in ((("accepted",) * 3, [[b, a], [c, b]]),
                                 (("accepted", "accepted", "superseded"), [[b, a]]),
                                 (("proposed", "accepted", "accepted"), [[c, b]])):
            self.reset()
            self.good()
            self.decision("a", "tier: judgement", "supersedes: [design-decision/b]", status=statuses[0])
            self.decision("b", "tier: judgement", "supersedes: [design-decision/c]", status=statuses[1])
            self.decision("c", "tier: judgement", status=statuses[2])
            rows, found = self.rows("v_d8")
            self.assertEqual(rows, wanted, (statuses, found))

    def test_a_wrong_enforced_by_is_named(self):
        cases = [(["tier: checked"], "checked", "problems"),
                 (["tier: check", "enforced_by: [tests/missing.py]"], "tests/missing.py", "problems"),
                 (["tier: check", "enforced_by: [thing#r1]"], "thing#r1", "problems"),
                 (["tier: requirement", "enforced_by: [tests/test_x.py]"], "tests/test_x.py", "problems"),
                 (["tier: judgement", "enforced_by: [thing#r1]"], "enforced_by", "problems"),
                 (["tier: requirement", "enforced_by: [thing#r9]"], "thing#r9", "unresolved")]
        for fields, words, where in cases:
            self.reset()
            self.good()
            self.write("tests/test_x.py", "def test_x():\n    pass\n")
            self.decision("a", *fields)
            found, r = self.check_json()
            named = [p for p in found[where] if "spec/decisions/a.md" in p and words in p]
            self.assertEqual(len(named), 1, (fields, found[where]))
            self.assertEqual(r.returncode, 1, (fields, r.stdout))

    def test_the_index_gives_the_tier(self):
        self.decision("a", "tier: judgement")
        text = model_report.render_decisions(self.tmp)
        self.assertIn("| decision | summary | status | tier | supersedes | revisit when |", text)
        row = next(line for line in text.splitlines() if "](a.md)" in line)
        self.assertIn("| accepted | judgement |", row)


if __name__ == "__main__":
    unittest.main()
