"""Tests of scripts/model. Each test whose docstring is a scenario title of
features/design-model-check.feature is that scenario's step definition."""

import json
import os
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

# On PYTHONPATH, a clingo.py that hides clingo from an interpreter, as the fixture harness does.
HIDE_CLINGO = 'raise ImportError("clingo is hidden for this test")\n'

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
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."]))
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
    def test_r2(self):
        """violations are printed by their grammar name and fail the check"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."]))
        r = self.run_model("check")
        self.assertEqual(r.returncode, 1)
        self.assertRegex(r.stdout, r"v_s3\s+\(1\)\n\s+" + re.escape(THING + "#r1"))

    def test_r3(self):
        """a requirement bullet without an id is refused"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- **When** asked, `thing` shall answer."], group="guarantees"))
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
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] `thing` shall be fast."], group="guarantees"))
        r = self.run_model("check")
        self.assertNotIn("v_s3", r.stdout)
        self.assertEqual(r.returncode, 0, r.stdout)

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
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] `thing` shall answer."]).replace(
            "rests_on: []", "rests_on:\n- x").replace("group: service", "group: service   # a comment"))
        self.write("decisions/0001-x.md", f'---\nid: {full("design-decision", "x")}\nsummary: "X."\ndate: 2026-01-01\nstatus: accepted\n---\n')
        self.write("features/thing.feature", "@r1\nFeature: thing\n\n  Example: one\n    Given a\n")
        r = self.run_model("check")
        self.assertEqual(r.returncode, 0, r.stdout)
        facts = self.run_model("facts").stdout
        self.assertIn(f'rests_on("{THING}", "{full("design-decision", "x")}").', facts)
        self.assertIn(f'group("{THING}", "service").', facts)

    def test_a_held_scenario_is_no_acceptance_scenario(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] `thing` shall answer."], retired="[r2]"))
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
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] `thing` shall answer."], group="guarantees", rests_on="[x]"))
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


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class OutputTest(ModelTest):
    """What the check prints and how a repository's parts are judged (r31-r36)."""

    def unscenarioed(self, count):
        self.write("spec/capabilities/thing.md", cap("thing", [f"- [r{n}] Req {n}." for n in range(1, count + 1)]))

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


def index(*glossary):
    """spec/index.md with a ## Glossary section holding these bullets."""
    return INDEX + "\n## Glossary\n\n" + "\n".join(glossary) + "\n\n## Where things live\n\n- Here.\n"


def term(name):
    return full("term", name)


class GlossaryFactsTest(ModelTest):
    """r48, r50, r51: the glossary read into facts (no solver needed)."""

    def facts(self):
        r = self.run_model("facts", python=[sys.executable, "-I", "-S"])
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout.splitlines()

    def test_r48(self):
        """a glossary bullet is a term of the bounded context"""
        self.write("spec/index.md", index("- **Suite record**: a whole-suite result, e.g. a green run, logged once. Not: test record, run."))
        lines = self.facts()
        self.assertIn(f'node("{term("suite-record")}", "term").', lines)
        self.assertIn(f'avoid("{term("suite-record")}", "test record").', lines)
        self.assertIn(f'avoid("{term("suite-record")}", "run").', lines)
        self.assertEqual([l for l in lines if l.startswith("avoid(")], [f'avoid("{term("suite-record")}", "test record").', f'avoid("{term("suite-record")}", "run").'])

    def test_a_definition_with_a_period_is_one_definition(self):
        self.write("spec/index.md", index("- **store**: where things are kept, e.g. a shelf."))
        lines = self.facts()
        self.assertIn(f'node("{term("store")}", "term").', lines)
        self.assertEqual([l for l in lines if l.startswith("avoid(")], [])

    def test_r50(self):
        """facts give each term its kind, its context and its avoided words"""
        self.write("spec/index.md", index("- **batch**: the slices one session plans. Not: sprint, lot.",
                                          "- **slice**: a unit of work with an observable done."))
        lines = self.facts()
        for t in ("batch", "slice"):
            self.assertIn(f'node("{term(t)}", "term").', lines)
            self.assertIn(f'term_of("{term(t)}", "{CONTEXT}").', lines)
        self.assertIn(f'avoid("{term("batch")}", "sprint").', lines)
        self.assertIn(f'avoid("{term("batch")}", "lot").', lines)
        self.assertFalse([l for l in lines if l.startswith(f'avoid("{term("slice")}"')])

    def test_r51(self):
        """a mention is a whole word in any case, plural allowed"""
        self.write("spec/index.md", index("- **store**: where things are kept. Not: shelf."))
        self.write("spec/capabilities/thing.md", cap("thing", [
            "- [r1] **When** asked, the Store answers.",
            "- [r2] **When** asked, it lists the stores.",
            "- [r3] **When** asked, it can restore a backup.",
            "- [r4] **When** asked, it reads a shelf and a store-front."]))
        self.write("features/thing.feature", "Feature: thing\n\n  @r1\n  Scenario: one\n    Given SHELVES\n    When a shelf is read\n    Then it answers\n\n"
                                             "  @r2\n  Scenario: the store answers\n    Given a thing\n    Then it holds\n")
        lines = self.facts()
        mentions = sorted(l for l in lines if l.startswith("mentions("))
        self.assertEqual(mentions, sorted([
            f'mentions("{THING}#r1", "store").',
            f'mentions("{THING}#r2", "store").',
            f'mentions("{THING}#r4", "shelf").',
            'mentions("features/thing.feature:one", "shelf").',
            'mentions("features/thing.feature:the store answers", "store").']))


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class GlossaryCheckTest(ModelTest):
    """r49, r52-r54: the glossary checked."""

    def test_r49(self):
        """a glossary bullet not in the entry form is a file problem"""
        rows = ["- batch: the slices one session plans.",
                "- **batch** the slices one session plans.",
                "- **batch**: the slices one session plans",
                "- **batch**: the slices one session plans. Not: sprint",
                "- **batch**: . Not: sprint.",
                "- **batch**: the slices. Not: sprint, , lot."]
        for bullet in rows:
            with self.subTest(bullet=bullet):
                self.reset()
                self.write("spec/index.md", index("- **slice**: a unit of work.", bullet))
                found, r = self.check_json()
                self.assertEqual(len(found["problems"]), 1, found)
                self.assertTrue(found["problems"][0].startswith("spec/index.md"), found)
                self.assertEqual(r.returncode, 1)

    def test_a_good_glossary_passes(self):
        self.write("spec/index.md", index("- **slice**: a unit of work, e.g. a scenario. Not: chunk.",
                                          "- **batch**: the slices one session plans."))
        self.good()
        found, r = self.check_json()
        self.assertEqual((found["violations"], found["problems"], found["unresolved"]), ([], [], []), found)
        self.assertEqual(r.returncode, 0)

    def test_r52(self):
        """a requirement or scenario using an avoided word is v_t1"""
        self.write("spec/index.md", index("- **slice**: a unit of work. Not: chunk."))
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, it plans each chunk.", "- [r2] It plans a slice."]))
        self.write("features/thing.feature", feature("thing", ("@r1", "it plans"), ("@r2", "chunks are planned"),
                                                     ("@r2 @holding", "a chunk as it was")))
        found, r = self.check_json()
        self.assertEqual(sorted(self.violated(found, "v_t1")), sorted([
            [THING + "#r1", "chunk", term("slice")],
            ["features/thing.feature:chunks are planned", "chunk", term("slice")]]), found)
        self.assertFalse([a for a in self.violated(found, "v_t1") if "as it was" in a[0]], found)
        self.assertEqual(r.returncode, 1)
        text = self.run_model("check").stdout
        self.assertIn("v_t1  (2)", text)

    def test_a_restore_is_no_store(self):
        self.write("spec/index.md", index("- **depot**: where things are kept. Not: store."))
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, it can restore a backup."]))
        self.write("features/thing.feature", feature("thing", ("@r1", "a restore")))
        found, _ = self.check_json()
        self.assertEqual(self.violated(found, "v_t1"), [], found)

    def test_r53(self):
        """two entries for one term are v_t2"""
        self.write("spec/index.md", index("- **slice**: a unit of work.", "- **Slice**: a piece of a batch."))
        found, r = self.check_json()
        self.assertEqual(self.violated(found, "v_t2"), [[term("slice")]], found)
        self.assertEqual(r.returncode, 1)

    def test_r54(self):
        """an avoided word that is a term is v_t3"""
        self.write("spec/index.md", index("- **slice**: a unit of work. Not: batch.",
                                          "- **batch**: the slices one session plans.",
                                          "- **hand-back**: an implementer's stop. Not: Hand-back, halt."))
        found, r = self.check_json()
        self.assertEqual(sorted(self.violated(found, "v_t3")), [["batch"], ["hand-back"]], found)
        self.assertEqual(r.returncode, 1)



class InterpreterSearchTest(ModelTest):
    """r12, r55-r57: model check finds clingo behind a virtualenv. clingo is hidden from the first
    interpreter by a clingo.py on PYTHONPATH that raises ImportError; a fake python3 drops PYTHONPATH."""

    def setUp(self):
        super().setUp()
        self.good()
        self.hidden = self.tmp / "hidden"
        self.write("hidden/clingo.py", HIDE_CLINGO)
        self.log = self.tmp / "calls.log"

    def fake(self, dirname, behaviour="find"):
        """A python3 in <dirname> that logs each call. find: runs the real interpreter without the hiding
        PYTHONPATH; probe-only: says yes to the probe but runs the real interpreter with clingo still
        hidden; lack: has no clingo."""
        real = sys.executable
        body = {"find": f'exec /usr/bin/env -u PYTHONPATH "{real}" "$@"',
                "probe-only": f'if [ "$1" = "-c" ]; then exit 0; fi\nexec "{real}" "$@"',
                "lack": "exit 1"}[behaviour]
        p = self.write(f"{dirname}/python3", f'#!/bin/sh\necho "{dirname}: $*" >> "{self.log}"\n{body}\n')
        p.chmod(0o755)
        return p

    def env(self, path_dirs, **extra):
        env = {k: v for k, v in os.environ.items() if k not in ("SHOPSYSTEM_MODEL_PYTHON", "VIRTUAL_ENV", "SHOPSYSTEM_MODEL_REEXEC")}
        env["PYTHONPATH"] = str(self.hidden)
        env["PATH"] = os.pathsep.join(str(d) for d in path_dirs)
        env.update(extra)
        return env

    def run_check(self, env):
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.tmp), "check"],
                              capture_output=True, text=True, env=env, timeout=60)

    def calls(self):
        return self.log.read_text().splitlines() if self.log.exists() else []

    @unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
    def test_r55(self):
        """without clingo the check runs again under the first interpreter that has it"""
        self.fake("venv/bin")
        self.fake("lacks", "lack")
        self.fake("bin")
        self.fake("later")
        self.fake("chosen")
        probe = "-c import clingo"
        cases = [
            ("PATH in order, the virtualenv's bin/ skipped",
             [self.tmp / "venv/bin", self.tmp / "lacks", self.tmp / "bin", self.tmp / "later"],
             {"VIRTUAL_ENV": str(self.tmp / "venv")}, "bin", [f"lacks: {probe}", f"bin: {probe}"]),
            ("$SHOPSYSTEM_MODEL_PYTHON first", [self.tmp / "bin"],
             {"SHOPSYSTEM_MODEL_PYTHON": str(self.tmp / "chosen/python3")}, "chosen", [f"chosen: {probe}"]),
        ]
        for name, path_dirs, extra, used, probes in cases:
            with self.subTest(name):
                self.log.unlink(missing_ok=True)
                r = self.run_check(self.env(path_dirs, **extra))
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                self.assertIn("0 violations", r.stdout)
                self.assertEqual(self.calls(), probes + [f"{used}: {SCRIPT} --root {self.tmp} check"])

    def test_r56(self):
        """the check runs again only once"""
        self.fake("bin", "probe-only")
        r = self.run_check(self.env([self.tmp / "bin"]))
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("clingo", r.stdout)
        self.assertEqual(len([c for c in self.calls() if str(SCRIPT) in c]), 1, self.calls())

    def test_r57(self):
        """with no interpreter that has clingo the check names each one it tried"""
        self.fake("lacks", "lack")
        missing_python = self.tmp / "nowhere/python3"
        for name, path_dirs, extra, tried in [
                ("no interpreter on PATH", [self.tmp / "empty"], {}, []),
                ("interpreters that lack it", [self.tmp / "lacks"], {"SHOPSYSTEM_MODEL_PYTHON": str(missing_python)},
                 [str(missing_python), str(self.tmp / "lacks/python3")])]:
            with self.subTest(name):
                r = self.run_check(self.env(path_dirs, **extra))
                self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
                self.assertIn("clingo", r.stdout)
                self.assertIn("pip install clingo", r.stdout)
                named = r.stdout.split("it tried has it:", 1)[1].split("\n", 1)[0]
                self.assertEqual([p.strip() for p in named.rstrip(".").split(",")],
                                 tried + ["/usr/local/bin/python3", "/usr/bin/python3"])
                self.assertEqual([c for c in self.calls() if str(SCRIPT) in c], [])


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class WithdrawnTest(ModelTest):
    """r58-r59: a withdrawn part is closed; an abandoned initiative has no open part."""

    def breakdown(self, initiative, proposal, item):
        self.good()
        self.observation()
        self.initiative(status=initiative)
        self.proposal(status=proposal, adds="[thing#r1]")
        self.work_item(status=item, part_of="capability-proposal/p1")

    def about_initiative(self, found):
        return [v for v in found["violations"] if I1 in v[1]]

    def test_r58(self):
        """a withdrawn part is closed"""
        self.breakdown("done", "withdrawn", "withdrawn")
        found, _ = self.check_json()
        self.assertEqual(found["problems"], [], found)
        self.assertEqual(self.about_initiative(found), [], found)

    def test_r59(self):
        """an abandoned initiative with an open part is v_d2"""
        self.breakdown("abandoned", "withdrawn", "drafted")
        found, r = self.check_json()
        self.assertEqual(self.violated(found, "v_d2"), [[I1]], found)
        self.assertEqual(r.returncode, 1)
        self.reset()
        self.breakdown("abandoned", "withdrawn", "withdrawn")
        found, _ = self.check_json()
        self.assertEqual(self.about_initiative(found), [], found)


# The scenarios bound as pytest-bdd tests, by title, in BOUND of tests/scenarios/test_design_model_check.py.
SCENARIO_MODULE = pathlib.Path(__file__).resolve().parents[1] / "scenarios" / "test_design_model_check.py"


def moved_titles():
    """The titles of the scenarios that the pytest-bdd module binds."""
    import ast
    for node in ast.parse(SCENARIO_MODULE.read_text()).body:
        if isinstance(node, ast.Assign) and [t.id for t in node.targets if isinstance(t, ast.Name)] == ["BOUND"]:
            return list(ast.literal_eval(node.value))
    raise AssertionError("no BOUND in %s" % SCENARIO_MODULE)


class BindingTest(unittest.TestCase):
    def test_every_scenario_has_its_test(self):
        gone = set(moved_titles())
        self.assertEqual([t for t in missing(FEATURE, CheckTest, DecisionsTest,
                                             ReadingTest, GrammarFixTest, TypeFirstTest, FilesReadTest, OutputTest,
                                             WhyScenarioTest, IdFormTest, HeldAndLedgerTest, GlossaryFactsTest,
                                             GlossaryCheckTest, InterpreterSearchTest, WithdrawnTest) if t not in gone], [])


if __name__ == "__main__":
    unittest.main()
