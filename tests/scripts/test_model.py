"""Tests of scripts/model. Each test whose docstring is a scenario title of
features/design-model-check.feature is that scenario's step definition."""

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "model"
FEATURE = ROOT / "features" / "design-model-check.feature"

try:
    import clingo  # noqa: F401
    HAVE_CLINGO = True
except ImportError:
    HAVE_CLINGO = False


def cap(name, reqs, group="service", retired="[]", rests_on="[]"):
    lines = "\n".join(reqs)
    return textwrap.dedent(f"""\
        ---
        id: ctx/{name}
        title: {name}
        narrator: a client
        group: {group}
        rests_on: {rests_on}
        formulated_as: features/{name}.feature
        retired: {retired}
        ---

        # {name}

        ## Purpose
        Something.

        ## Behaviour
        """) + lines + "\n\n## Not yet\n- None.\n"


def feature(name, *scenarios):
    out = [f"# formulated from spec/capabilities/{name}.md", f"Feature: {name}", "  Narrator: a client", ""]
    for tag, title in scenarios:
        out += [f"  {tag}", f"  Scenario: {title}", "    Given a thing", "    Then it holds", ""]
    return "\n".join(out)


class ModelTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.write("spec/index.md", "---\nid: ctx\n---\n# ctx\n")

    def write(self, rel, text):
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def run_model(self, *args, python=None):
        cmd = (python or [sys.executable]) + [str(SCRIPT), "--root", str(self.tmp), *args]
        return subprocess.run(cmd, capture_output=True, text=True)

    def good(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, it answers."]))
        self.write("features/thing.feature", feature("thing", ("@r1", "it answers")))

    def initiative(self, ident="i1", source="[obs-1]", status="started"):
        self.write(f"work/{ident}/initiative.md", textwrap.dedent(f"""\
            ---
            id: {ident}
            title: t
            summary: s
            kind: capability-change
            owner-level: ctx
            status: {status}
            priority: 1
            source: {source}
            date: 2026-10-15
            ---
            """))

    def proposal(self, ident="p1", status="drafted", adds="[]", changes="[]", initiative="i1", argues="[thing]"):
        self.write(f"work/{initiative}/{ident}.md", textwrap.dedent(f"""\
            ---
            id: {ident}
            kind: capability-proposal
            part_of: {initiative}
            status: {status}
            argues: {argues}
            adds: {adds}
            changes: {changes}
            date: 2026-10-15
            ---
            """))

    def observation(self, ident="obs-1"):
        self.write("records/observations.md", f"# Observations\n\n## {ident}\nabout: ctx\nby: someone\ndate: 2026-10-15\n\nSeen.\n")


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class CheckTest(ModelTest):
    def test_r1(self):
        """a repository the grammar accepts passes"""
        self.good()
        r = self.run_model("check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("0 violations", r.stdout)
        self.assertIn("0 unresolved references, 0 file problems", r.stdout)

    def test_r2(self):
        """violations are printed by their grammar name and fail the check"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, it answers."]))
        r = self.run_model("check")
        self.assertEqual(r.returncode, 1)
        self.assertRegex(r.stdout, r"v_s3\s+\(1\)\n\s+ctx/thing#r1")

    def test_r3(self):
        """a requirement bullet without an id is refused"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- **When** asked, it answers."], group="guarantees"))
        r = self.run_model("check")
        self.assertIn("v15a", r.stdout)
        self.assertEqual(r.returncode, 1)

    def test_r4(self):
        """two requirements with one id are refused"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r1] Two."], group="guarantees"))
        r = self.run_model("check")
        self.assertIn("v15b", r.stdout)

    def test_r5(self):
        """a retired id used again is refused"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees", retired="[r1]"))
        r = self.run_model("check")
        self.assertIn("v15c", r.stdout)

    def test_r6(self):
        """a proposal changing a requirement no capability has is refused"""
        self.good()
        self.observation()
        self.initiative()
        self.proposal(changes="[thing#r9]")
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v15e\s+\(1\)\n\s+p1, ctx/thing#r9")

    def test_r7(self):
        """a proposal formulated before its requirement has a scenario is refused"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."]))
        self.observation()
        self.initiative()
        self.proposal(status="formulated", adds="[thing#r1]")
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v15f\s+\(1\)\n\s+p1")

    def test_r8(self):
        """a guarantees capability needs no scenarios"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] It is fast."], group="guarantees"))
        r = self.run_model("check")
        self.assertNotIn("v_s3", r.stdout)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_r9(self):
        """references that name nothing are reported"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], rests_on="[decision/nope]"))
        self.write("features/thing.feature", feature("thing", ("@r1", "one"), ("@r7", "seven")))
        r = self.run_model("check")
        self.assertIn("unresolved: features/thing.feature: scenario 'seven' names ctx/thing#r7", r.stdout)
        self.assertIn("unresolved: spec/capabilities/thing.md: decision/nope is not a design-decision", r.stdout)
        self.assertEqual(r.returncode, 1)

    def test_r10(self):
        """a part that reaches no initiative is refused"""
        self.good()
        self.observation()
        self.initiative()
        self.write("work/i1/w1.md", "---\nid: w1\nkind: work-item\npart_of: nowhere\nstatus: drafted\nunder: thing\ncheck: true\n---\n")
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v9c\s+\(1\)\n\s+w1")

    def test_r11(self):
        """warnings are counted and do not fail the check"""
        self.good()
        self.observation()
        r = self.run_model("check")
        self.assertIn("warning w_uncited_obs  (1)", r.stdout)
        self.assertEqual(r.returncode, 0, r.stdout)


class NoSolverTest(ModelTest):
    def test_r12(self):
        """without clingo the check says how to install it"""
        self.good()
        r = self.run_model("check", python=[sys.executable, "-I", "-S"])
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("clingo", r.stdout)
        self.assertIn("-m pip install clingo", r.stdout)

    def test_r13(self):
        """facts are printed in clingo's syntax"""
        self.good()
        r = self.run_model("facts", python=[sys.executable, "-I", "-S"])
        self.assertEqual(r.returncode, 0, r.stderr)
        lines = r.stdout.splitlines()
        self.assertIn('node("ctx/thing", "capability").', lines)
        self.assertIn('req_id("ctx/thing#r1", "ctx/thing", 1).', lines)
        self.assertTrue(all(re.fullmatch(r"\w+\(.*\)\.", l) for l in lines))


class DecisionsTest(ModelTest):
    def decisions(self):
        self.write("decisions/0001-old.md", '---\nid: decision/old\nsummary: "Do it the old way."\ndate: 2026-01-01\nstatus: superseded\n---\n# 1\n')
        self.write("decisions/0002-new.md", '---\nid: decision/new\nsummary: "Do it | the new way."\ndate: 2026-02-01\nstatus: accepted\nsupersedes: decision/old\nrevisit_when: "it hurts"\nrevisit_signal: requests\n---\n# 2\n')

    def test_r14(self):
        """the decisions index lists every decision"""
        self.decisions()
        r = self.run_model("decisions")
        self.assertEqual(r.returncode, 0, r.stderr)
        text = (self.tmp / "spec" / "decisions.md").read_text()
        self.assertIn("| [decision/old](../decisions/0001-old.md) | Do it the old way. | superseded |  |  |", text)
        self.assertIn("| [decision/new](../decisions/0002-new.md) | Do it \\| the new way. | accepted | decision/old | it hurts |", text)

    def test_r15(self):
        """a stale decisions index is reported and left alone"""
        self.decisions()
        target = self.write("spec/decisions.md", "# Decisions\n\nhand-written\n")
        r = self.run_model("decisions", "--check")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not what `model decisions` writes", r.stdout)
        self.assertEqual(target.read_text(), "# Decisions\n\nhand-written\n")


class WhyTest(ModelTest):
    def test_r16(self):
        """why traces a requirement to its initiative's sources"""
        self.good()
        self.observation()
        self.initiative()
        self.proposal(status="merged", adds="[thing#r1]")
        r = self.run_model("why", "thing#r1")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("ctx/thing#r1: **When** asked, it answers.", r.stdout)
        self.assertIn("adds by capability-proposal p1 (merged, 2026-10-15)", r.stdout)
        self.assertIn("part_of initiative i1", r.stdout)
        self.assertIn("source observation obs-1", r.stdout)

    def test_r17(self):
        """why with no proposal says so"""
        self.good()
        r = self.run_model("why", "ctx/thing#r1")
        self.assertEqual(r.returncode, 1)
        self.assertIn("no capability-proposal adds or changes it", r.stdout)


class RangeTest(ModelTest):
    def test_r18(self):
        """a range of ids stands for each id in it"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r2] Two.", "- [r3] Three."]))
        self.observation()
        self.initiative()
        self.proposal(adds="[thing#r1-r3]")
        r = self.run_model("why", "thing#r2")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("adds by capability-proposal p1", r.stdout)


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
        self.write("decisions/0001-x.md", "---\nid: decision/x\nsummary: >-\n  folded\ndate: 2026-01-01\nstatus: accepted\n---\n")
        r = self.run_model("check")
        self.assertIn("summary uses a folded or literal block", r.stdout)
        self.assertEqual(r.returncode, 1)

    def test_a_work_item_under_no_capability_is_unresolved(self):
        self.good()
        self.observation()
        self.initiative(source="[obs-1]")
        self.proposal(adds="[thing#r1]")
        self.write("work/i1/w1.md", "---\nid: thing/1\nkind: work-item\npart_of: p1\nstatus: drafted\nunder: nosuch\ncheck: true\n---\n")
        r = self.run_model("check")
        self.assertIn("ctx/nosuch is not a capability", r.stdout)

    def test_adding_a_retired_id_is_v15c(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."], group="guarantees", retired="[r1]"))
        self.observation()
        self.initiative()
        self.proposal(adds="[thing#r1]")
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v15c\s+\(1\)\n\s+ctx/thing#r1")

    def test_feature_tags_column_zero_lists_and_comments_are_read(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."]).replace(
            "rests_on: []", "rests_on:\n- decision/x").replace("group: service", "group: service   # a comment"))
        self.write("decisions/0001-x.md", '---\nid: decision/x\nsummary: "X."\ndate: 2026-01-01\nstatus: accepted\n---\n')
        self.write("features/thing.feature", "@r1\nFeature: thing\n\n  Example: one\n    Given a\n")
        r = self.run_model("check")
        self.assertEqual(r.returncode, 0, r.stdout)
        facts = self.run_model("facts").stdout
        self.assertIn('rests_on("ctx/thing", "decision/x").', facts)
        self.assertIn('group("ctx/thing", "service").', facts)

    def test_a_held_scenario_is_no_acceptance_scenario(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], retired="[r2]"))
        self.write("features/thing.feature", "\n".join([
            "Feature: thing", "",
            "  @r1", "  Scenario: one", "    Given a", "",
            "  @r1 @holding", "  Scenario: one as it was (held)", "    Given a", "",
            "  @r2 @holding", "  Scenario: two as it was (held)", "    Given a", ""]))
        r = self.run_model("check")
        self.assertEqual(r.returncode, 0, r.stdout)
        facts = self.run_model("facts").stdout
        self.assertNotIn("(held)", facts)

    def test_a_ledger_is_read_where_there_is_no_decisions_directory(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees", rests_on="[decision/x]"))
        self.write("spec/decisions.md", "# Decisions\n\n## decision/x\nX.\ndate: 2026-01-01\n")
        r = self.run_model("check")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn('node("decision/x", "design-decision").', self.run_model("facts").stdout)


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
        self.assertRegex(r.stdout, r"v_k6\s+\(1\)\n\s+p1")

    def test_another_kind_keeps_one_first_part(self):
        self.good()
        self.observation()
        self.initiative()
        p = self.tmp / "work/i1/initiative.md"
        p.write_text(p.read_text().replace("kind: capability-change", "kind: defect"))
        for w in ("w1", "w2"):
            self.write(f"work/i1/{w}.md", f"---\nid: thing/{w}\nkind: work-item\npart_of: i1\nstatus: drafted\nunder: thing\ncheck: true\n---\n")
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v_k5\s+\(1\)\n\s+i1")


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class IriFormTest(ModelTest):
    """Ids in shopsystem-knowledge's IRI form (decision/capability-ids-are-context-scoped); not scenarios of their own."""

    CTX = "missingmass.io/shopsystem/ctx"

    def setUp(self):
        super().setUp()
        self.write("spec/index.md", f"---\nid: {self.CTX}\n---\n# ctx\n")
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r2] Two."], group="guarantees")
                   .replace("id: ctx/thing", f"id: {self.CTX}/thing"))
        self.observation()
        self.initiative()

    def test_every_written_form_names_the_same_requirement(self):
        refs = ["thing#r1", "ctx/thing#r1", f"{self.CTX}/thing#r1", "thing#behaviour/r1", f"{self.CTX}/thing#behaviour/r1"]
        for i, ref in enumerate(refs):
            self.proposal(f"p{i}", adds=f"[{ref}]")
        r = self.run_model("check")
        self.assertIn("0 unresolved references, 0 file problems", r.stdout, r.stdout)
        facts = self.run_model("facts").stdout
        for i in range(len(refs)):
            self.assertIn(f'adds("p{i}", "{self.CTX}/thing#r1").', facts)

    def test_a_range_in_the_context_name_form_expands(self):
        self.proposal(adds="[ctx/thing#r1-r2]")
        facts = self.run_model("facts").stdout
        self.assertIn(f'adds("p1", "{self.CTX}/thing#r2").', facts)

    def test_the_context_name_alone_names_the_context(self):
        self.write("records/observations.md", "# Observations\n\n## obs-1\nabout: ctx\nabout: ctx/thing\nby: someone\ndate: 2026-10-15\n\nSeen.\n")
        facts = self.run_model("facts").stdout
        self.assertIn(f'about("obs-1", "{self.CTX}").', facts)
        self.assertIn(f'about("obs-1", "{self.CTX}/thing").', facts)

    def test_a_capability_id_in_short_form_is_a_file_problem(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees"))
        r = self.run_model("check")
        self.assertIn(f"is not '{self.CTX}/thing'", r.stdout)


class BindingTest(unittest.TestCase):
    def test_every_scenario_has_its_test(self):
        titles = re.findall(r"^\s*Scenario(?: Outline)?:\s*(.+?)\s*$", FEATURE.read_text(), re.M)
        docs = set()
        for cls in (CheckTest, NoSolverTest, DecisionsTest, WhyTest, RangeTest):
            for name in dir(cls):
                if name.startswith("test_"):
                    docs.add((getattr(cls, name).__doc__ or "").strip())
        self.assertEqual([t for t in titles if t not in docs], [])


if __name__ == "__main__":
    unittest.main()
