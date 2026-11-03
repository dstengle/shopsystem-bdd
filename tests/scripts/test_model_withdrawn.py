"""Unit tests of design-model-check lines changed with no scenario row yet: r19's README.md under spec/decisions/,
and r27's work-item that is `withdrawn` (work-items decisions-readme-not-read and withdrawn-accepts-not-reported);
and of the reading design model v5 changes (GF conversion design §7.1: C10, C11, C13, C14, C17, C21-C23)."""

import sys
import unittest

from test_model import CONTEXT, HAVE_CLINGO, ROOT, THING, ModelTest, cap, full

sys.path.insert(0, str(ROOT / "scripts"))
import model_facts  # noqa: E402


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


class Grouped(model_facts.Model):
    """A Model that also has thing#g1 holding thing#r1, as model_spec (P5) will read it; generated or not."""

    def __init__(self, root, generated):
        super().__init__(root)
        self.generated = generated

    def read_capabilities(self):
        super().read_capabilities()
        g = THING + "#g1"
        self.node(g, "requirement-group")
        self.fact("in", g, THING)
        self.fact("member_of", THING + "#r1", g)
        if self.generated:
            self.fact("generates", g, full("scenario", "thing-g1"))


class V5ReadingTest(ModelTest):
    def problems(self):
        return model_facts.Model(self.tmp).read().problems

    def test_design_and_analysis_are_record_kinds(self):
        for kind, problems in (("design", 0), ("analysis", 0), ("memo", 1)):
            with self.subTest(kind=kind):
                self.write(".shop/records/r.md", f"---\nid: {full('record', 'r')}\nkind: {kind}\nabout: {CONTEXT}\n---\n")
                self.assertEqual(len([p for p in self.problems() if p.startswith(".shop/records/r.md")]), problems)

    def test_job_thread_and_cross_context_request_are_no_parts(self):
        self.initiative()
        for kind in ("job-thread", "cross-context-request"):
            with self.subTest(kind=kind):
                self.write(".shop/work/i1/x1.md", f"---\nid: {full(kind, 'x1')}\nkind: {kind}\nstatus: proposed\n---\n")
                found = [p for p in self.problems() if p.startswith(".shop/work/i1/x1.md: needs an id and a kind")]
                self.assertEqual(len(found), 1, self.problems())

    def test_merged_is_a_legacy_status_only_under_a_closed_initiative(self):
        self.good()
        for status, problems in (("done", 0), ("abandoned", 0), ("started", 1)):
            with self.subTest(initiative=status):
                self.initiative(status=status)
                self.proposal(status="merged", adds="[thing#r1]")
                self.assertEqual(len([p for p in self.problems() if "status 'merged'" in p]), problems, self.problems())

    def test_a_decision_has_a_status_of_its_lifecycle(self):
        for status, problems in (("proposed", 0), ("accepted", 0), ("rejected", 0), ("superseded", 0), ("ruled", 1)):
            with self.subTest(status=status):
                self.write("spec/decisions/0001-x.md", f"---\nid: {full('design-decision', 'x')}\nsummary: s\n"
                                                       f"status: {status}\n---\n## Decision\nX.\n")
                self.assertEqual(len([p for p in self.problems() if "status 'ruled'" in p]), problems)

    def test_a_work_item_accepts_a_group(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."]))
        self.initiative()
        for generated, accepts, problems in ((True, "thing#g1", []), (False, "thing#g1", ["no scenario names yet"]),
                                             (True, "thing#r1", []), (False, "thing#g2", ["which no capability has"])):
            with self.subTest(generated=generated, accepts=accepts):
                self.work_item(accepts=f"[{accepts}]")
                model = Grouped(self.tmp, generated).read()
                said = [p for p in model.problems + model.dangling if "w1.md: accepts" in p]
                self.assertEqual(len(said), len(problems), said)
                self.assertTrue(all(w in p for w, p in zip(problems, said)), said)
                if accepts != "thing#g2":
                    self.assertIn(("accepts", (full("work-item", "w1"), f"{THING}#{accepts[6:]}")), model.facts)

    def test_a_requests_lines_outcomes_and_upstream_are_facts(self):
        q = full("request", "q1")
        self.write(".shop/work/requests/q1.md", f"---\nid: {q}\nkind: request\nasker: internal\nsource: [x]\n"
                   "status: delivered\nturn: asker\ndate: 2026-01-01\n---\n\n## Lines\n1. Do \"a\".\n2. Do b.\n\n"
                   "## Outcomes\n1. accepted\n2. rewritten: Do c.\n\n## Resolution\n1. thing#r1 1.0\n")
        facts = model_facts.Model(self.tmp).read().facts
        for fact in (("line", (q, 1, 'Do "a".')), ("line", (q, 2, "Do b.")), ("outcome", (q, 1, "accepted")),
                     ("outcome", (q, 2, "rewritten")), ("upstream", (q, CONTEXT)), ("resolution_of_line", (q, 1))):
            self.assertIn(fact, facts)
        self.assertTrue([a for n, a in facts if n == "age" and a[0] == q], facts)


if __name__ == "__main__":
    unittest.main()
