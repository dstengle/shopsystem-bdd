"""Tests of scripts/model. Each test whose docstring is a scenario title of
features/design-model-check.feature is that scenario's step definition."""

import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

from binding import missing

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "model"
FEATURE = ROOT / "features" / "design-model-check.feature"

try:
    import clingo  # noqa: F401
    HAVE_CLINGO = True
except ImportError:
    HAVE_CLINGO = False

PATH = "ex.com/prod/ctx"
CONTEXT = f"bounded-context/{PATH}"
INDEX = f"---\nid: {CONTEXT}\n---\n# ctx\n"


def full(kind, name):
    """A node's id in full: <kind>/<context path>/<name>."""
    return f"{kind}/{PATH}/{name}"


THING = full("capability", "thing")
P1 = full("capability-proposal", "p1")
I1 = full("initiative", "i1")
W1 = full("work-item", "w1")
OBS1 = full("observation", "obs-1")


def cap(name, reqs, group="service", retired="[]", rests_on="[]"):
    lines = "\n".join(reqs)
    return textwrap.dedent(f"""\
        ---
        id: capability/{PATH}/{name}
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
        self.write("spec/index.md", INDEX)

    def write(self, rel, text):
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def run_model(self, *args, python=None):
        cmd = (python or [sys.executable]) + [str(SCRIPT), "--root", str(self.tmp), *args]
        return subprocess.run(cmd, capture_output=True, text=True)

    def reset(self):
        """A fresh repository directory, for a test that runs one scenario under several examples."""
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.write("spec/index.md", INDEX)

    def check_json(self, *args):
        r = self.run_model("check", "--json", *args)
        return json.loads(r.stdout), r

    def violated(self, found, relation):
        return [a for name, a in found["violations"] if name == relation]

    def work_item(self, ident="w1", **fields):
        fm = {"id": full("work-item", ident), "kind": "work-item", "part_of": "initiative/i1", "status": "drafted", "under": "thing", "check": "true"}
        fm.update(fields)
        body = "".join(f"{k}: {v}\n" for k, v in fm.items() if v is not None)
        self.write(f"work/i1/{ident}.md", f"---\n{body}---\n")

    def good(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, it answers."]))
        self.write("features/thing.feature", feature("thing", ("@r1", "it answers")))

    def initiative(self, ident="i1", source="[observation/obs-1]", status="started", kind="capability-change"):
        self.write(f"work/{ident}/initiative.md", textwrap.dedent(f"""\
            ---
            id: {full("initiative", ident)}
            title: t
            summary: s
            kind: {kind}
            owner-level: ctx
            status: {status}
            priority: 1
            source: {source}
            date: 2026-10-15
            ---
            """))

    def proposal(self, ident="p1", status="drafted", adds="[]", changes="[]", initiative="i1", argues="[thing]",
                 removes="[]", date="2026-10-15"):
        self.write(f"work/{initiative}/{ident}.md", textwrap.dedent(f"""\
            ---
            id: {full("capability-proposal", ident)}
            kind: capability-proposal
            part_of: initiative/{initiative}
            status: {status}
            argues: {argues}
            adds: {adds}
            changes: {changes}
            removes: {removes}
            date: {date}
            ---
            """))

    def observation(self, ident="obs-1"):
        self.write("records/observations.md", f"# Observations\n\n## {full('observation', ident)}\nabout: {CONTEXT}\nby: someone\ndate: 2026-10-15\n\nSeen.\n")


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
        self.assertRegex(r.stdout, r"v_s3\s+\(1\)\n\s+" + re.escape(THING + "#r1"))

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
        self.assertRegex(r.stdout, r"v15e\s+\(1\)\n\s+" + re.escape(f"{P1}, {THING}#r9"))

    def test_r7(self):
        """a proposal formulated before its requirement has a scenario is refused"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."]))
        self.observation()
        self.initiative()
        self.proposal(status="formulated", adds="[thing#r1]")
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v15f\s+\(1\)\n\s+" + re.escape(P1))

    def test_r8(self):
        """a guarantees capability needs no scenarios"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] It is fast."], group="guarantees"))
        r = self.run_model("check")
        self.assertNotIn("v_s3", r.stdout)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_r9(self):
        """references that name nothing are reported"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], rests_on="[nope]"))
        self.write("features/thing.feature", feature("thing", ("@r1", "one"), ("@r7", "seven")))
        r = self.run_model("check")
        self.assertIn(f"unresolved: features/thing.feature: scenario 'seven' names {THING}#r7", r.stdout)
        self.assertIn(f"unresolved: spec/capabilities/thing.md: {full('design-decision', 'nope')} is not a design-decision", r.stdout)
        self.assertEqual(r.returncode, 1)

    def test_r10(self):
        """a part that reaches no initiative is refused"""
        self.good()
        self.observation()
        self.initiative()
        self.work_item(part_of="initiative/nowhere")
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v9c\s+\(1\)\n\s+" + re.escape(W1))

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
        self.assertIn(f'node("{THING}", "capability").', lines)
        self.assertIn(f'req_id("{THING}#r1", "{THING}", 1).', lines)
        self.assertTrue(all(re.fullmatch(r"\w+\(.*\)\.", l) for l in lines))


class DecisionsTest(ModelTest):
    def decisions(self):
        self.write("decisions/0001-old.md", f'---\nid: {full("design-decision", "old")}\nsummary: "Do it the old way."\ndate: 2026-01-01\nstatus: superseded\n---\n# 1\n')
        self.write("decisions/0002-new.md", f'---\nid: {full("design-decision", "new")}\nsummary: "Do it | the new way."\ndate: 2026-02-01\nstatus: accepted\nsupersedes: design-decision/old\nrevisit_when: "it hurts"\nrevisit_signal: requests\n---\n# 2\n')

    def test_r14(self):
        """the decisions index lists every decision"""
        self.decisions()
        r = self.run_model("decisions")
        self.assertEqual(r.returncode, 0, r.stderr)
        text = (self.tmp / "spec" / "decisions.md").read_text()
        old, new = full("design-decision", "old"), full("design-decision", "new")
        self.assertIn(f"| [{old}](../decisions/0001-old.md) | Do it the old way. | superseded |  |  |", text)
        self.assertIn(f"| [{new}](../decisions/0002-new.md) | Do it \\| the new way. | accepted | {old} | it hurts |", text)

    def test_r15(self):
        """a stale decisions index is reported and left alone"""
        self.decisions()
        target = self.write("spec/decisions.md", "# Decisions\n\nhand-written\n")
        r = self.run_model("decisions", "--check")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not what `model decisions` writes", r.stdout)
        self.assertEqual(target.read_text(), "# Decisions\n\nhand-written\n")

    def test_r37(self):
        """a current decisions index passes the check"""
        self.decisions()
        self.assertEqual(self.run_model("decisions").returncode, 0)
        r = self.run_model("decisions", "--check")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("spec/decisions.md is current", r.stdout)

    def test_r38(self):
        """writing the decisions index names the file and leaves out decisions with no id"""
        self.decisions()
        self.write("decisions/0003-anon.md", "---\nsummary: Nameless.\nstatus: accepted\n---\n")
        r = subprocess.run([sys.executable, str(SCRIPT), "--root", ".", "decisions"], capture_output=True, text=True, cwd=self.tmp)
        self.assertEqual(r.stdout.strip(), "wrote spec/decisions.md", r.stderr)
        text = (self.tmp / "spec" / "decisions.md").read_text()
        self.assertIn(f"[{full('design-decision', 'new')}]", text)
        self.assertNotIn("Nameless.", text)


class WhyTest(ModelTest):
    def test_r16(self):
        """why traces a requirement to its initiative's sources"""
        self.good()
        self.observation()
        self.initiative()
        self.proposal(status="merged", adds="[thing#r1]")
        r = self.run_model("why", "thing#r1")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f"{THING}#r1: **When** asked, it answers.", r.stdout)
        self.assertIn(f"adds by capability-proposal {P1} (merged, 2026-10-15)", r.stdout)
        self.assertIn(f"part_of initiative {I1}", r.stdout)
        self.assertIn(f"source observation {OBS1}", r.stdout)

    def test_r17(self):
        """why with no proposal says so"""
        self.good()
        r = self.run_model("why", "capability/thing#r1")
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
        self.assertIn(f"adds by capability-proposal {P1}", r.stdout)


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
        self.write("decisions/0001-x.md", f"---\nid: {full('design-decision', 'x')}\nsummary: >-\n  folded\ndate: 2026-01-01\nstatus: accepted\n---\n")
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
        self.assertRegex(r.stdout, r"v15c\s+\(1\)\n\s+" + re.escape(THING + "#r1"))

    def test_feature_tags_column_zero_lists_and_comments_are_read(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."]).replace(
            "rests_on: []", "rests_on:\n- x").replace("group: service", "group: service   # a comment"))
        self.write("decisions/0001-x.md", f'---\nid: {full("design-decision", "x")}\nsummary: "X."\ndate: 2026-01-01\nstatus: accepted\n---\n')
        self.write("features/thing.feature", "@r1\nFeature: thing\n\n  Example: one\n    Given a\n")
        r = self.run_model("check")
        self.assertEqual(r.returncode, 0, r.stdout)
        facts = self.run_model("facts").stdout
        self.assertIn(f'rests_on("{THING}", "{full("design-decision", "x")}").', facts)
        self.assertIn(f'group("{THING}", "service").', facts)

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
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees", rests_on="[x]"))
        self.write("spec/decisions.md", "# Decisions\n\n## design-decision/x\nX.\ndate: 2026-01-01\n")
        r = self.run_model("check")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn(f'node("{full("design-decision", "x")}", "design-decision").', self.run_model("facts").stdout)


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
        self.assertRegex(r.stdout, r"v_k6\s+\(1\)\n\s+" + re.escape(P1))

    def test_another_kind_keeps_one_first_part(self):
        self.good()
        self.observation()
        self.initiative()
        p = self.tmp / "work/i1/initiative.md"
        p.write_text(p.read_text().replace("kind: capability-change", "kind: defect"))
        for w in ("thing-w1", "thing-w2"):
            self.work_item(w)
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v_k5\s+\(1\)\n\s+" + re.escape(I1))


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class TypeFirstTest(ModelTest):
    """Ids are type-first (decision/capability-ids-are-context-scoped); not scenarios of their own."""

    def setUp(self):
        super().setUp()
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r2] Two."], group="guarantees"))
        self.observation()
        self.initiative()

    def test_every_accepted_form_names_the_same_requirement(self):
        refs = ["thing#r1", "capability/thing#r1", f"{THING}#r1",
                "thing#behaviour/r1", "capability/thing#behaviour/r1", f"{THING}#behaviour/r1"]
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
        self.write("records/observations.md", f"# Observations\n\n## {OBS1}\nabout: {CONTEXT}\nabout: capability/thing\nabout: thing\n")
        found, _ = self.check_json()
        self.assertEqual([d for d in found["unresolved"] if "thing" in d], ["records/observations.md: thing names nothing in this repository"], found)
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
        self.write("decisions/0001-x.md", decision.format(full("design-decision", "x"), "measurement/m1"))
        self.write("decisions/0002-y.md", decision.format(full("design-decision", "y"), "requests"))
        self.write("records/m1.md", f"---\nid: {full('measurement', 'm1')}\nkind: measurement\nabout: {CONTEXT}\n---\n")
        found, _ = self.check_json()
        self.assertEqual(self.violated(found, "v13"), [], found)
        facts = self.run_model("facts").stdout
        self.assertIn(f'revisit_signal("{full("design-decision", "x")}", "{full("measurement", "m1")}").', facts)
        self.assertIn(f'revisit_signal("{full("design-decision", "y")}", "requests").', facts)

    def test_a_ledger_heading_is_type_first(self):
        shutil.rmtree(self.tmp / "work")
        for heading, problems in [("design-decision/x", 0), (full("design-decision", "x"), 0), ("decision/x", 1)]:
            with self.subTest(heading=heading):
                self.write("spec/decisions.md", f"# Decisions\n\n## {heading}\nX.\n")
                found, _ = self.check_json()
                self.assertEqual(len([p for p in found["problems"] if p.startswith("spec/decisions.md")]), problems, found)
                facts = self.run_model("facts").stdout
                self.assertEqual(f'node("{full("design-decision", "x")}", "design-decision").' in facts, not problems, facts)


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class FilesReadTest(ModelTest):
    """Which files are read, and how references and file shapes are judged (r19-r30)."""

    def test_r19(self):
        """model reads the repository's files under its root"""
        feat = feature("thing", ("@r1", "it answers"))
        rows = [
            ("spec/index.md", "---\nid: bounded-context/row.com/prod/rowctx\n---\n",
             'node("bounded-context/row.com/prod/rowctx", "bounded-context").', True, True),
            ("spec/capabilities/thing.md", cap("thing", ["- [r1] One."]), f'node("{THING}", "capability").', True, True),
            ("features/sub/thing.feature", feat, 'features/sub/thing.feature:it answers', True, True),
            ("decisions/0001-one.md", f"---\nid: {full('design-decision', 'one')}\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n",
             f'node("{full("design-decision", "one")}", "design-decision").', True, True),
            ("work/i1/initiative.md", f"---\nid: {I1}\nstatus: started\n---\n", f'node("{I1}", "initiative").', True, True),
            ("records/observations.md", f"# Observations\n\n## {OBS1}\nabout: {CONTEXT}\n", f'node("{OBS1}", "observation").', True, True),
            ("records/review/f1.md", f"---\nid: {full('review-finding', 'f1')}\nkind: review-finding\n---\n",
             f'node("{full("review-finding", "f1")}", "review-finding").', True, True),
            ("records/review/f2.md", "---\nkind: review-finding\nabout: capability/zzmark\n---\n", "zzmark", False, True),
            ("spec/capabilities/thing.md", cap("thing", ["- [r1] One."]), f'node("{THING}", "capability").', True, False),
        ]
        for rel, text, marker, included, with_root in rows:
            with self.subTest(file=rel, with_root=with_root, included=included):
                self.reset()
                self.write(rel, text)
                if with_root:
                    facts = self.run_model("facts").stdout
                else:
                    facts = subprocess.run([sys.executable, str(SCRIPT), "facts"], capture_output=True, text=True, cwd=self.tmp).stdout
                self.assertEqual(marker in facts, included, facts)

    def test_r20(self):
        """a scenario names a requirement by its tag in its capability's feature file"""
        scenario_tag = "Feature: thing\n\n  @r2\n  Scenario: two\n    Given a\n"
        feature_tag = "@r2\nFeature: thing\n\n  Scenario: two\n    Given a\n"
        own = "formulated_as: features/thing.feature\n"
        sub = "formulated_as: features/sub/thing-flow.feature\n"
        rows = [
            (own, "features/thing.feature", scenario_tag, False),
            (own, "features/thing.feature", feature_tag, False),
            ("", "features/thing.feature", scenario_tag, False),
            (sub, "features/sub/thing-flow.feature", scenario_tag, False),
            (sub, "features/other.feature", scenario_tag, True),
        ]
        for formulated, path, text, reported in rows:
            with self.subTest(formulated=formulated, path=path, reported=reported):
                self.reset()
                self.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."]).replace(own, formulated))
                self.write(path, text)
                found, _ = self.check_json()
                self.assertEqual([THING + "#r2"] in self.violated(found, "v_s3"), reported, found)

    def test_r21(self):
        """a reference written name#r<n> is that capability's requirement"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r2] Two."]))
        self.observation()
        self.initiative()
        self.proposal(adds="[thing#r2]")
        r = self.run_model("why", "capability/thing#r2")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn(f"{THING}#r2: Two.", r.stdout)
        self.assertIn(f"adds by capability-proposal {P1}", r.stdout)

    def test_r22(self):
        """a reference in neither requirement form, or a reversed range, is unresolved"""
        for ref in ["thing", "thing#2", "thing#line2", "thing#r3-r1", "design-decision/thing#r1"]:
            with self.subTest(reference=ref):
                self.reset()
                self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r2] Two.", "- [r3] Three."], group="guarantees"))
                self.observation()
                self.initiative()
                self.proposal(adds=f"[{ref}]")
                found, _ = self.check_json()
                self.assertEqual(len([d for d in found["unresolved"] if f"'{ref}' is not a requirement reference" in d]), 1, found)

    def test_r23(self):
        """a proposal adding or removing a requirement no capability has is unresolved, unless it adds a retired id"""
        rows = [("adds", "r9", "unresolved"), ("removes", "r9", "unresolved"),
                ("adds", "r4", "v15c"), ("removes", "r4", "unresolved")]
        for change, rid, reported in rows:
            with self.subTest(change=change, id=rid):
                self.reset()
                self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees", retired="[r4]"))
                self.observation()
                self.initiative()
                self.proposal(**{change: f"[thing#{rid}]"})
                found, _ = self.check_json()
                unresolved = [d for d in found["unresolved"] if f"{THING}#{rid}" in d]
                v15c = [a for a in self.violated(found, "v15c") if a == [f"{THING}#{rid}"]]
                if reported == "unresolved":
                    self.assertEqual((len(unresolved), v15c), (1, []), found)
                else:
                    self.assertEqual((unresolved, len(v15c)), ([], 1), found)

    def test_r24(self):
        """a frontmatter reference to nothing, or to the wrong kind, is unresolved"""
        def supersedes():
            self.write("decisions/0001-x.md", f"---\nid: {full('design-decision', 'x')}\nsummary: S\ndate: 2026-01-01\nstatus: accepted\nsupersedes: ghost\n---\n")
        rows = [
            ("supersedes", supersedes),
            ("source", lambda: self.initiative(source="[observation/ghost]")),
            ("part_of", lambda: self.work_item(part_of="initiative/ghost")),
            ("argues", lambda: self.proposal(argues="[ghost]")),
            ("under", lambda: self.work_item(under="ghost")),
            ("for", lambda: self.work_item(**{"for": "work-item/ghost"})),
            ("blocked_by", lambda: self.work_item(blocked_by="work-item/ghost")),
            ("depends_on", lambda: self.work_item(depends_on="ghost")),
            ("under", lambda: (self.write("decisions/0001-x.md", f"---\nid: {full('design-decision', 'ghost')}\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n"),
                               self.work_item(under="design-decision/ghost"))),
        ]
        for field, make in rows:
            with self.subTest(field=field):
                self.reset()
                self.good()
                self.observation()
                self.initiative()
                make()
                found, _ = self.check_json()
                self.assertEqual(len([d for d in found["unresolved"] if "ghost" in d]), 1, found)

    def test_r25(self):
        """a malformed index or capability file is a file problem"""
        def capfile(ident="capability/acme.com/shop/cart/thing", behaviour=True, retired="[]"):
            text = cap("thing", ["- [r1] One."], group="guarantees", retired=retired).replace(f"id: {THING}", f"id: {ident}")
            return text if behaviour else text.replace("## Behaviour", "## Requirements")
        rows = [
            ("spec/index.md is missing", None, "spec/index.md"),
            ("spec/index.md has no id", "---\ntitle: x\n---\n", "spec/index.md"),
            ("id other", capfile("capability/acme.com/shop/cart/other"), "spec/capabilities/thing.md"),
            ("no Behaviour", capfile(behaviour=False), "spec/capabilities/thing.md"),
            ("retired three", capfile(retired="[three]"), "spec/capabilities/thing.md"),
        ]
        for case, text, named in rows:
            with self.subTest(case=case):
                self.reset()
                if case.startswith("spec/index.md"):
                    (self.tmp / "spec/index.md").unlink()
                    if text:
                        self.write("spec/index.md", text)
                else:
                    self.write("spec/index.md", "---\nid: bounded-context/acme.com/shop/cart\n---\n")
                    self.write("spec/capabilities/thing.md", text)
                found, _ = self.check_json()
                self.assertEqual(len([p for p in found["problems"] if p.startswith(named)]), 1, found)

    def test_r26(self):
        """a feature file no capability is formulated as, or with a title twice, is a file problem"""
        own = "formulated_as: features/thing.feature\n"
        sub = "formulated_as: features/sub/thing-flow.feature\n"
        one = feature("thing", ("@r1", "one"))
        rows = [
            (own, "features/stray.feature", one, True),
            ("", "features/thing.feature", one, False),
            (sub, "features/thing.feature", one, True),
            (own, "features/thing.feature", feature("thing", ("@r1", "Apply a code"), ("@r1", "Apply a code")), True),
            (own, "features/thing.feature", feature("thing", ("@r1", "Apply a code"), ("@r1 @holding", "Apply a code")), False),
        ]
        for formulated, path, text, reports in rows:
            with self.subTest(formulated=formulated, path=path, reports=reports):
                self.reset()
                self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees").replace(own, formulated))
                self.write(path, text)
                found, _ = self.check_json()
                self.assertEqual(any(p.startswith(path) for p in found["problems"]), reports, found)

    def test_r27(self):
        """a malformed work directory or work file is a file problem"""
        def part(**changes):
            fm = {"id": full("work-item", "p1"), "kind": "work-item", "part_of": "initiative/i1", "status": "drafted", "under": "thing", "check": "true"}
            fm.update(changes)
            self.write("work/i1/p1.md", "---\n" + "".join(f"{k}: {v}\n" for k, v in fm.items() if v is not None) + "---\n")

        def initiative_with(old, new):
            p = self.tmp / "work/i1/initiative.md"
            p.write_text(p.read_text().replace(old, new))
        rows = [
            ("no initiative.md", lambda: part(), "work/i1:"),
            ("initiative.md no id", lambda: (self.initiative(), initiative_with(f"id: {I1}\n", "")), "work/i1/initiative.md:"),
            ("part no id", lambda: (self.initiative(), part(id=None)), "work/i1/p1.md:"),
            ("part kind banana", lambda: (self.initiative(), part(kind="banana")), "work/i1/p1.md:"),
            ("part no status", lambda: (self.initiative(), part(status=None)), "work/i1/p1.md:"),
            ("part status outside lifecycle", lambda: (self.initiative(), part(status="loved")), "work/i1/p1.md:"),
            ("initiative priority high", lambda: (self.initiative(), initiative_with("priority: 1", "priority: high")), "work/i1/initiative.md:"),
            ("initiative date 16/10/2026", lambda: (self.initiative(), initiative_with("date: 2026-10-15", "date: 16/10/2026")), "work/i1/initiative.md:"),
        ]
        for case, make, named in rows:
            with self.subTest(case=case):
                self.reset()
                self.good()
                make()
                found, _ = self.check_json()
                self.assertEqual(len([p for p in found["problems"] if p.startswith(named)]), 1, found)
                if case == "no initiative.md":
                    self.assertFalse(any("work/i1/initiative.md" in p for p in found["problems"]), found)

    def test_r28(self):
        """a work-item accepting a requirement no scenario names is a file problem"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."]))
        self.observation()
        self.initiative()
        self.work_item(accepts="[thing#r2]")
        found, _ = self.check_json()
        self.assertEqual(len([p for p in found["problems"] if p.startswith("work/i1/w1.md") and f"{THING}#r2" in p]), 1, found)

    def test_r29(self):
        """a malformed decision, record or frontmatter is a file problem"""
        decision = "---\nid: {}\nsummary: {}\ndate: 2026-01-01\nstatus: accepted\n---\n"
        x = full("design-decision", "x")
        rows = [
            ("decision no id", lambda: self.write("decisions/0001-x.md", "---\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n")),
            ("record kind banana", lambda: self.write("records/note.md", f"---\nid: {full('review-finding', 'n1')}\nkind: banana\n---\n")),
            ("folded block", lambda: self.write("decisions/0001-x.md", decision.format(x, ">-\n  folded"))),
            ("literal block", lambda: self.write("decisions/0001-x.md", decision.format(x, "|\n  literal"))),
            ("same id twice", lambda: (self.write("decisions/0001-x.md", decision.format(x, "S")),
                                       self.write("records/observations.md", f"# Observations\n\n## {x}\nabout: {CONTEXT}\n"))),
        ]
        for case, make in rows:
            with self.subTest(case=case):
                self.reset()
                self.good()
                make()
                found, r = self.check_json()
                if case == "same id twice":
                    # a type-first id names its kind, so the observation's heading is also not an observation id (r46)
                    self.assertEqual(len([p for p in found["problems"] if f"{x} is both" in p]), 1, found)
                else:
                    self.assertEqual(len(found["problems"]), 1, found)

    def test_r30(self):
        """file problems are each printed and fail the check"""
        for name in ("thing", "other"):
            self.write(f"spec/capabilities/{name}.md", cap(name, ["- [r1] One."], group="guarantees").replace("## Behaviour", "## Requirements"))
        r = self.run_model("check")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertEqual(len(re.findall(r"^file: spec/capabilities/(thing|other)\.md: no '## Behaviour' section$", r.stdout, re.M)), 2, r.stdout)


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class OutputTest(ModelTest):
    """What the check prints and how a repository's parts are judged (r31-r36)."""

    def unscenarioed(self, count):
        self.write("spec/capabilities/thing.md", cap("thing", [f"- [r{n}] Req {n}." for n in range(1, count + 1)]))

    def test_r31(self):
        """the check ends with the four counts"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], rests_on="[nope]"))
        self.write("features/stray.feature", "Feature: stray\n")
        r = self.run_model("check")
        self.assertIn("1 violations, 1 warnings, 1 unresolved references, 1 file problems", r.stdout.splitlines()[-1], r.stdout)

    def test_r32(self):
        """rows of a violated relation are limited, saying how many more there are"""
        for rows, limit, shown, more in [(5, ["--limit", "2"], 2, 3), (12, [], 10, 2)]:
            with self.subTest(rows=rows, limit=limit):
                self.reset()
                self.unscenarioed(rows)
                r = self.run_model("check", *limit)
                m = re.search(rf"^v_s3  \({rows}\)\n((?:    .*\n)+)", r.stdout, re.M)
                lines = m.group(1).splitlines()
                self.assertEqual(len([l for l in lines if THING + "#r" in l]), shown, r.stdout)
                self.assertIn(f"    ... and {more} more", lines)

    def test_r33(self):
        """with --json the check's findings are one JSON object"""
        for state, status in [("accepts", 0), ("unnamed", 1)]:
            with self.subTest(state=state):
                self.reset()
                if state == "accepts":
                    self.good()
                else:
                    self.unscenarioed(1)
                found, r = self.check_json()
                self.assertEqual(sorted(found), ["problems", "unresolved", "violations", "warnings"])
                self.assertEqual(r.returncode, status)
                self.assertEqual(bool(found["violations"]), status == 1)

    def test_r34(self):
        """only a capability-change initiative may hold several parts directly"""
        self.write("spec/capabilities/other.md", cap("other", ["- [r1] One."], group="guarantees"))
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees"))
        self.observation()
        self.initiative(kind="defect")
        for w in ("w1", "w2"):
            self.work_item(w)
        found, _ = self.check_json()
        self.assertEqual(self.violated(found, "v_k5"), [[I1]], found)
        self.reset()
        self.write("spec/capabilities/other.md", cap("other", ["- [r1] One."], group="guarantees"))
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees"))
        self.observation()
        self.initiative()
        self.proposal("p1", adds="[thing#r1]")
        self.proposal("p2", adds="[other#r1]", argues="[other]")
        found, _ = self.check_json()
        self.assertEqual(self.violated(found, "v_k5"), [], found)

    def test_r35(self):
        """a proposal arguing two capabilities is refused"""
        self.write("spec/capabilities/other.md", cap("other", ["- [r1] One."], group="guarantees"))
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees"))
        self.observation()
        self.initiative()
        self.proposal(adds="[thing#r1, other#r1]", argues="[thing, other]")
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v_k6\s+\(1\)\n\s+" + re.escape(P1))

    def test_r36(self):
        """an initiative may be done when its proposal is formulated"""
        self.good()
        self.observation()
        self.initiative(status="done")
        self.proposal(status="formulated", adds="[thing#r1]")
        found, _ = self.check_json()
        self.assertEqual([v for v in found["violations"] if I1 in v[1]], [], found)


class WhyScenarioTest(ModelTest):
    """model why and the forms of a reference (r39-r43)."""

    def thing(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."]))
        self.observation()
        self.initiative()

    def test_r39(self):
        """why refuses an argument that is not a requirement reference"""
        self.good()
        r = self.run_model("why", "thing")
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("'thing' is not a requirement reference", r.stdout)

    def test_r40(self):
        """why on a requirement no capability has still lists its proposals"""
        self.good()
        self.observation()
        self.initiative()
        self.proposal(changes="[thing#r9]")
        r = self.run_model("why", "thing#r9")
        lines = r.stdout.splitlines()
        self.assertEqual(lines[0], f"{THING}#r9: no capability has this requirement now")
        self.assertIn(f"  changes by capability-proposal {P1} (drafted, 2026-10-15)", lines)

    def test_r41(self):
        """why lists every proposal naming the requirement by date, and fails when none adds or changes it"""
        p1 = dict(ident="p1", removes="[thing#r2]", date="2026-10-01")
        rows = [
            ([p1, dict(ident="p2", adds="[thing#r2]", date="2026-09-01")], ["p2", "p1"], 0),
            ([p1, dict(ident="p2", changes="[thing#r2]", date="2026-09-01")], ["p2", "p1"], 0),
            ([p1, dict(ident="p2", removes="[thing#r2]", date="2026-09-01")], ["p2", "p1"], 1),
            ([p1], ["p1"], 1),
        ]
        for proposals, listed, status in rows:
            with self.subTest(listed=listed, status=status, n=len(proposals)):
                self.reset()
                self.thing()
                for p in proposals:
                    self.proposal(**p)
                r = self.run_model("why", "thing#r2")
                self.assertEqual(r.returncode, status, r.stdout)
                seen = re.findall(r"^  [\w/]+ by capability-proposal " + re.escape(full("capability-proposal", "")) +
                                  r"(p\d) \((\w+), (\d{4}-\d\d-\d\d)\)$", r.stdout, re.M)
                self.assertEqual([p for p, _, _ in seen], listed, r.stdout)
                self.assertTrue(all(s == "drafted" for _, s, _ in seen))
                self.assertEqual([d for _, _, d in seen], sorted(d for _, _, d in seen))

    def test_r42(self):
        """the behaviour/ form of a reference names the same requirement"""
        self.thing()
        self.proposal(adds=f"[{THING}#behaviour/r2]")
        r = self.run_model("why", f"{THING}#r2")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn(f"adds by capability-proposal {P1}", r.stdout)


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class IdFormTest(ModelTest):
    """The forms an id and a reference take (r43, r46, r47)."""

    def setUp(self):
        super().setUp()
        self.files()

    def files(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees"))
        self.observation()
        self.initiative()

    def test_r43(self):
        """a node may be written in short where its field allows it"""
        rows = [("argues", "thing", THING), ("argues", "capability/thing", THING), ("argues", THING, THING),
                ("part_of", "initiative/i1", I1), ("part_of", "i1", None)]
        for field, written, read in rows:
            with self.subTest(field=field, written=written):
                self.proposal(argues=f"[{written}]" if field == "argues" else "[thing]")
                if field == "part_of":
                    p = self.tmp / "work/i1/p1.md"
                    p.write_text(p.read_text().replace("part_of: initiative/i1", f"part_of: {written}"))
                found, _ = self.check_json()
                facts = self.run_model("facts").stdout
                if read:
                    self.assertEqual(found["unresolved"], [], found)
                    self.assertIn(f'{field}("{P1}", "{read}").', facts)
                else:
                    self.assertEqual([d for d in found["unresolved"] if f" {written} " in d], [f"work/i1/p1.md: {written} names nothing in this repository"], found)

    def test_r46(self):
        """a node whose id is not in type-first form is a file problem"""
        def capability(ident):
            self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees").replace(f"id: {THING}", f"id: {ident}"))

        def initiative(ident):
            p = self.tmp / "work/i1/initiative.md"
            p.write_text(p.read_text().replace(f"id: {I1}", f"id: {ident}"))
        rows = [
            ("spec/index.md", lambda: self.write("spec/index.md", "---\nid: ctx\n---\n")),
            ("spec/index.md", lambda: self.write("spec/index.md", "---\nid: bounded-context/ctx\n---\n")),
            ("spec/capabilities/thing.md", lambda: capability("thing")),
            ("spec/capabilities/thing.md", lambda: capability("ctx/thing")),
            ("spec/capabilities/thing.md", lambda: capability(full("design-decision", "thing"))),
            ("decisions/0001-x.md", lambda: self.write("decisions/0001-x.md", "---\nid: decision/x\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n")),
            ("work/i1/initiative.md", lambda: initiative("i1")),
            ("work/i1/p1.md", lambda: self.work_item("p1", id=full("capability-proposal", "p1"))),
            ("records/observations.md", lambda: self.write("records/observations.md", f"# Observations\n\n## obs-1\nabout: {CONTEXT}\n")),
            ("records/f1.md", lambda: self.write("records/f1.md", "---\nid: f1\nkind: review-finding\n---\n")),
        ]
        for named, make in rows:
            with self.subTest(file=named):
                self.reset()
                self.files()
                make()
                found, _ = self.check_json()
                self.assertEqual(len([p for p in found["problems"] if p.startswith(named)]), 1, found)

    def test_r47(self):
        """a reference in a refused form is unresolved"""
        def refs():
            self.write("decisions/0001-x.md", f"---\nid: {full('design-decision', 'x')}\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n")
            self.write("records/observations.md", f"# Observations\n\n## {OBS1}\nabout: {CONTEXT}\n\n## {full('observation', 'x')}\nabout: {CONTEXT}\n")
        rows = [
            ("ctx/thing#r1", lambda: self.proposal(adds="[ctx/thing#r1]")),
            ("ctx/thing", lambda: self.proposal(argues="[ctx/thing]")),
            ("decision/x", lambda: self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees", rests_on="[decision/x]"))),
            ("obs/x", lambda: self.initiative(source="[obs/x]")),
        ]
        for written, make in rows:
            with self.subTest(reference=written):
                self.reset()
                self.files()
                refs()
                make()
                found, _ = self.check_json()
                self.assertEqual(len([d for d in found["unresolved"] if written in d]), 1, found)
                self.assertEqual(found["problems"], [], found)


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class HeldAndLedgerTest(ModelTest):
    """r44-r45."""

    def test_r44(self):
        """a held scenario names no requirement"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."]))
        self.write("features/thing.feature", "Feature: thing\n\n  @r2 @holding\n  Scenario: two as it was\n    Given a\n")
        found, _ = self.check_json()
        self.assertEqual(self.violated(found, "v_s3"), [[THING + "#r2"]], found)

    def test_r45(self):
        """without a decisions directory the ledger's design-decision headings are the decisions"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees", rests_on="[design-decision/one]"))
        self.write("spec/decisions.md", "# Decisions\n\n## design-decision/one\nOne way\nto do it.\n\ndate: 2026-01-01\n")
        found, _ = self.check_json()
        self.assertEqual(found["unresolved"], [], found)
        self.assertEqual(self.violated(found, "v12a"), [], found)
        self.assertIn(f'summary("{full("design-decision", "one")}", "One way to do it.").', self.run_model("facts").stdout)


class BindingTest(unittest.TestCase):
    def test_every_scenario_has_its_test(self):
        self.assertEqual(missing(FEATURE, CheckTest, NoSolverTest, DecisionsTest, WhyTest, RangeTest,
                                 ReadingTest, GrammarFixTest, TypeFirstTest, FilesReadTest, OutputTest,
                                 WhyScenarioTest, IdFormTest, HeldAndLedgerTest), [])


if __name__ == "__main__":
    unittest.main()
