"""Unit tests of design-model-check lines changed with no scenario row yet: r19's README.md under spec/decisions/
(work-item decisions-readme-not-read); and of the reading design model v5 changes (GF conversion design §7.1: C14,
C21), less the frozen queue's (plan 9)."""

import sys
import unittest

from test_model import CONTEXT, HAVE_CLINGO, ROOT, ModelTest, full

sys.path.insert(0, str(ROOT / "scripts"))
import model_facts


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class NotReadTest(ModelTest):
    def test_r19_a_readme_under_spec_decisions_is_not_a_decision(self):
        self.good()
        self.write("spec/decisions/README.md", "# Decisions\n\nOne file a decision; index.md is generated.\n")
        found, _ = self.check_json()
        self.assertEqual([p for p in found["problems"] if "README.md" in p], [], found)

class V5ReadingTest(ModelTest):
    def problems(self):
        return model_facts.Model(self.tmp).read().problems

    def test_design_and_analysis_are_record_kinds(self):
        for kind, problems in (("design", 0), ("analysis", 0), ("memo", 1)):
            with self.subTest(kind=kind):
                self.write(".shop/records/r.md", f"---\nid: {full('record', 'r')}\nkind: {kind}\nabout: {CONTEXT}\n---\n")
                self.assertEqual(len([p for p in self.problems() if p.startswith(".shop/records/r.md")]), problems)

    def test_a_decision_has_a_status_of_its_lifecycle(self):
        for status, problems in (("proposed", 0), ("accepted", 0), ("rejected", 0), ("superseded", 0), ("ruled", 1)):
            with self.subTest(status=status):
                self.write("spec/decisions/0001-x.md", f"---\nid: {full('design-decision', 'x')}\nsummary: s\n"
                                                       f"status: {status}\n---\n## Decision\nX.\n")
                self.assertEqual(len([p for p in self.problems() if "status 'ruled'" in p]), problems)

    def test_a_requests_lines_outcomes_and_upstream_are_facts(self):
        q = full("request", "q1")
        self.write(".shop/requests/q1.md", f"---\nid: {q}\nkind: request\nasker: internal\nsource: [x]\n"
                   "status: delivered\nturn: asker\ndate: 2026-01-01\n---\n\n## Lines\n1. Do \"a\".\n2. Do b.\n\n"
                   "## Outcomes\n1. accepted\n2. rewritten: Do c.\n\n## Resolution\n1. thing#r1 1.0\n")
        facts = model_facts.Model(self.tmp).read().facts
        for fact in (("line", (q, 1, 'Do "a".')), ("line", (q, 2, "Do b.")), ("outcome", (q, 1, "accepted")),
                     ("outcome", (q, 2, "rewritten")), ("upstream", (q, CONTEXT)), ("resolution_of_line", (q, 1))):
            self.assertIn(fact, facts)
        self.assertTrue([a for n, a in facts if n == "age" and a[0] == q], facts)


if __name__ == "__main__":
    unittest.main()
