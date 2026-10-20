"""Unit tests of scripts/model's reading: the files it reads and how, the forms of an id, and the grammar's fixes.
ModelTest and the file builders are in test_model.py."""

import re
import unittest

from test_model import CONTEXT, HAVE_CLINGO, I1, OBS1, P1, THING, ModelTest, cap, feature, full


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class ReadingTest(ModelTest):
    """How files are read; not scenarios of their own."""

    def test_a_reversed_range_is_unresolved(self):
        self.good()
        self.observation()
        self.initiative()
        self.proposal(adds="[thing#r3-r1]")
        r = self.run_model("check")
        self.assertIn("'thing#r3-r1' is not a requirement reference", r.stdout)

    def test_a_folded_block_is_a_file_problem(self):
        self.good()
        self.write("spec/decisions/0001-x.md", f"---\nid: {full('design-decision', 'x')}\nsummary: >-\n  folded\ndate: 2026-01-01\nstatus: accepted\n---\n")
        r = self.run_model("check")
        self.assertIn("summary uses a folded or literal block", r.stdout)
        self.assertEqual(r.returncode, 1)

    def test_a_work_item_under_no_capability_is_unresolved(self):
        self.good()
        self.observation()
        self.initiative()
        self.proposal(adds="[thing#r1]")
        self.work_item("thing-1", part_of="capability-proposal/p1", under="nosuch")
        r = self.run_model("check")
        self.assertIn(f"{full('capability', 'nosuch')} is not a capability", r.stdout)

    def test_adding_a_retired_id_is_v15c(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."], group="guarantees", retired="[r1]"))
        self.observation()
        self.initiative()
        self.proposal(adds="[thing#r1]")
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v15c  .+  \(1\)\n\s+" + re.escape(THING + "#r1"))

    def test_feature_tags_column_zero_lists_and_comments_are_read(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] `thing` shall answer."]).replace(
            "rests_on: []", "rests_on:\n- x").replace("group: service", "group: service   # a comment"))
        self.write("spec/decisions/0001-x.md", f'---\nid: {full("design-decision", "x")}\nsummary: "X."\ndate: 2026-01-01\nstatus: accepted\n---\n\n## Decision\nWe do it.\n')
        self.write("features/thing.feature", "@r1\nFeature: thing\n\n  Example: one\n    Given a\n")
        r = self.run_model("check")
        self.assertEqual(r.returncode, 0, r.stdout)
        facts = self.run_model("facts").stdout
        self.assertIn(f'rests_on("{THING}", "{full("design-decision", "x")}").', facts)
        self.assertIn(f'group("{THING}", "service").', facts)

    def test_a_deprecated_scenario_is_no_acceptance_scenario(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] `thing` shall answer."], retired="[r2]"))
        self.write("features/thing.feature", "\n".join([
            "Feature: thing", "",
            "  @r1", "  Scenario: one", "    Given a", "",
            "  @r1 @deprecated", "  Scenario: one as it was (deprecated)", "    Given a", "",
            "  @r2 @deprecated", "  Scenario: two as it was (deprecated)", "    Given a", ""]))
        r = self.run_model("check")
        self.assertEqual(r.returncode, 0, r.stdout)
        facts = self.run_model("facts").stdout
        self.assertNotIn("(deprecated)", facts)


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class GrammarFixTest(ModelTest):
    """FIX notes of model.lp that change what grammar.md v3 accepts; not scenarios of their own."""

    def test_a_capability_change_holds_one_proposal_per_capability(self):
        self.write("spec/capabilities/other.md", cap("other", ["- [r1] One."], group="guarantees"))
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees"))
        self.observation()
        self.initiative()
        self.proposal("p1", adds="[thing#r1]")
        self.proposal("p2", adds="[other#r1]", argues="[other]")
        r = self.run_model("check")
        self.assertNotIn("v_k5", r.stdout)
        self.assertNotIn("v_k6", r.stdout)

    def test_a_capability_proposal_arguing_two_capabilities_is_v_k6(self):
        self.write("spec/capabilities/other.md", cap("other", ["- [r1] One."], group="guarantees"))
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees"))
        self.observation()
        self.initiative()
        self.proposal(adds="[thing#r1, other#r1]", argues="[thing, other]")
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v_k6  .+  \(1\)\n\s+" + re.escape(P1))

    def test_another_kind_keeps_one_first_part(self):
        self.good()
        self.observation()
        self.initiative()
        p = self.tmp / ".shop/work/i1/initiative.md"
        p.write_text(p.read_text().replace("kind: capability-change", "kind: defect"))
        for w in ("thing-w1", "thing-w2"):
            self.work_item(w)
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v_k5  .+  \(1\)\n\s+" + re.escape(I1))


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class TypeFirstTest(ModelTest):
    """Ids are type-first (decision/capability-ids-are-context-scoped); not scenarios of their own."""

    def setUp(self):
        super().setUp()
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r2] Two."], group="guarantees"))
        self.observation()
        self.initiative()

    def test_every_accepted_form_names_the_same_requirement(self):
        refs = ["thing#r1", "capability/thing#r1", f"{THING}#r1"]
        for i, ref in enumerate(refs):
            self.proposal(f"p{i}", adds=f"[{ref}]")
        r = self.run_model("check")
        self.assertIn("0 unresolved references, 0 file problems", r.stdout, r.stdout)
        facts = self.run_model("facts").stdout
        for i in range(len(refs)):
            self.assertIn(f'adds("{full("capability-proposal", f"p{i}")}", "{THING}#r1").', facts)

    def test_a_range_in_a_short_form_expands(self):
        self.proposal(adds="[capability/thing#r1-r2]")
        facts = self.run_model("facts").stdout
        self.assertIn(f'adds("{P1}", "{THING}#r2").', facts)

    def test_about_needs_a_kind(self):
        self.write(".shop/records/observations.md", f"# Observations\n\n## {OBS1}\nabout: {CONTEXT}\nabout: capability/thing\nabout: thing\n")
        found, _ = self.check_json()
        self.assertEqual([d for d in found["unresolved"] if "thing" in d], [".shop/records/observations.md: thing names nothing in this repository"], found)
        facts = self.run_model("facts").stdout
        self.assertIn(f'about("{OBS1}", "{CONTEXT}").', facts)
        self.assertIn(f'about("{OBS1}", "{THING}").', facts)

    def test_a_capability_may_be_named_as_a_kind(self):
        self.write("spec/capabilities/job.md", cap("job", ["- [r1] One."], group="guarantees"))
        self.proposal(adds="[job#r1]", argues="[job]")
        found, _ = self.check_json()
        self.assertEqual((found["unresolved"], found["problems"]), ([], []), found)
        facts = self.run_model("facts").stdout
        self.assertIn(f'argues("{P1}", "{full("capability", "job")}").', facts)
        self.assertIn(f'adds("{P1}", "{full("capability", "job")}#r1").', facts)

    def test_a_capability_file_name_must_be_a_name(self):
        self.write("spec/capabilities/My.Thing.md", cap("My.Thing", ["- [r1] One."], group="guarantees"))
        found, _ = self.check_json()
        self.assertEqual(len([p for p in found["problems"] if p.startswith("spec/capabilities/My.Thing.md")]), 1, found)

    def test_forms_outside_the_convention_are_unresolved(self):
        other = "capability/other.com/x/y/thing"
        rows = [
            (other, lambda: self.proposal(argues=f"[{other}]")),
            (f"{other}#r1", lambda: self.proposal(adds=f"[{other}#r1]")),
            ("Thing", lambda: self.proposal(argues="[Thing]")),
            ("Thing#r1", lambda: self.proposal(adds="[Thing#r1]")),
            ("capability/Thing", lambda: self.proposal(argues="[capability/Thing]")),
            ("thing.v2", lambda: self.proposal(argues="[thing.v2]")),
            ("thing.v2#r1", lambda: self.proposal(adds="[thing.v2#r1]")),
            ("for: w1", lambda: (self.work_item("w1"), self.work_item("w2", **{"for": "w1"}))),
            ("blocked_by: w1", lambda: (self.work_item("w1"), self.work_item("w2", blocked_by="[w1]"))),
            ("source: obs-1", lambda: self.initiative(source="[obs-1]")),
        ]
        for written, make in rows:
            with self.subTest(reference=written):
                self.setUp()
                make()
                ref = written.split(": ")[-1]
                found, _ = self.check_json()
                self.assertEqual(len([d for d in found["unresolved"] if f"{ref!r}" in d or f" {ref} " in d]), 1, found)

    def test_a_revisit_signal_is_a_reference(self):
        decision = "---\nid: {}\nsummary: S\ndate: 2026-01-01\nstatus: accepted\nrevisit_signal: {}\n---\n"
        self.write("spec/decisions/0001-x.md", decision.format(full("design-decision", "x"), "measurement/m1"))
        self.write("spec/decisions/0002-y.md", decision.format(full("design-decision", "y"), "requests"))
        self.write(".shop/records/m1.md", f"---\nid: {full('measurement', 'm1')}\nkind: measurement\nabout: {CONTEXT}\n---\n")
        found, _ = self.check_json()
        self.assertEqual(self.violated(found, "v13"), [], found)
        facts = self.run_model("facts").stdout
        self.assertIn(f'revisit_signal("{full("design-decision", "x")}", "{full("measurement", "m1")}").', facts)
        self.assertIn(f'revisit_signal("{full("design-decision", "y")}", "requests").', facts)


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class FilesReadTest(ModelTest):
    """Which files are read, and how references and file shapes are judged (r19-r30)."""

    def test_r20(self):
        scenario_tag = "Feature: thing\n\n  @r2\n  Scenario: two\n    Given a\n"
        feature_tag = "@r2\nFeature: thing\n\n  Scenario: two\n    Given a\n"
        rows = [
            ("features/thing.feature", scenario_tag, False),
            ("features/thing.feature", feature_tag, False),
            ("features/sub/thing.feature", scenario_tag, True),
            ("features/other.feature", scenario_tag, True),
        ]
        for path, text, reported in rows:
            with self.subTest(path=path, reported=reported):
                self.reset()
                self.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."]))
                self.write(path, text)
                found, _ = self.check_json()
                self.assertEqual([THING + "#r2"] in self.violated(found, "v_s3"), reported, found)

    def test_r26(self):
        one = feature("thing", ("@r1", "one"))
        rows = [
            ("features/stray.feature", one, True),
            ("features/thing.feature", one, False),
            ("features/sub/thing.feature", one, True),
            ("features/thing.feature", feature("thing", ("@r1", "Apply a code"), ("@r1", "Apply a code")), True),
            ("features/thing.feature", feature("thing", ("@r1", "Apply a code"), ("@r1 @deprecated", "Apply a code")), False),
        ]
        for path, text, reports in rows:
            with self.subTest(path=path, reports=reports):
                self.reset()
                self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees"))
                self.write(path, text)
                found, _ = self.check_json()
                self.assertEqual(any(p.startswith(path) for p in found["problems"]), reports, found)


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class DeprecatedAndLedgerTest(ModelTest):
    """r44."""

    def test_r44(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."]))
        self.write("features/thing.feature", "Feature: thing\n\n  @r2 @deprecated\n  Scenario: two as it was\n    Given a\n")
        found, _ = self.check_json()
        self.assertEqual(self.violated(found, "v_s3"), [[THING + "#r2"]], found)


if __name__ == "__main__":
    unittest.main()
