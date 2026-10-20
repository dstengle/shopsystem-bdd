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
LP = ROOT / "scripts" / "model.lp"
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
        self.write(f".shop/work/i1/{ident}.md", f"---\n{body}---\n")

    def good(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."]))
        self.write("features/thing.feature", feature("thing", ("@r1", "it answers")))

    def initiative(self, ident="i1", source="[observation/obs-1]", status="started", kind="capability-change"):
        self.write(f".shop/work/{ident}/initiative.md", textwrap.dedent(f"""\
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
        self.write(f".shop/work/{initiative}/{ident}.md", textwrap.dedent(f"""\
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
        self.write(".shop/records/observations.md", f"# Observations\n\n## {full('observation', ident)}\nabout: {CONTEXT}\nby: someone\ndate: 2026-10-15\n\nSeen.\n")


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class CheckTest(ModelTest):
    def test_r2(self):
        """violations are printed by their grammar name and fail the check"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."]))
        r = self.run_model("check")
        self.assertEqual(r.returncode, 1)
        self.assertRegex(r.stdout, r"v_s3  a requirement has no scenario  \(1\)\n\s+" + re.escape(THING + "#r1"))

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
        self.assertRegex(r.stdout, r"v15e  a proposal changes a requirement no capability has  \(1\)\n\s+" + re.escape(f"{P1}, {THING}#r9"))

    def test_r7(self):
        """a proposal formulated before its requirement has a scenario is refused"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."]))
        self.observation()
        self.initiative()
        self.proposal(status="formulated", adds="[thing#r1]")
        r = self.run_model("check")
        self.assertRegex(r.stdout, r"v15f  a formulated proposal leaves a requirement without a scenario  \(1\)\n\s+" + re.escape(P1))

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
        self.assertRegex(r.stdout, r"v9c  a part reaches no initiative  \(1\)\n\s+" + re.escape(W1))

    def test_r11(self):
        """warnings are counted and do not fail the check"""
        self.good()
        self.observation()
        r = self.run_model("check")
        self.assertIn("warning w_uncited_obs  an observation no initiative cites  (1)", r.stdout)
        self.assertEqual(r.returncode, 0, r.stdout)


class RulesTest(ModelTest):
    def test_model_rules_prints_every_rule_with_its_plain_label(self):
        """model rules prints every rule with its plain label"""
        r = self.run_model("rules")
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = [line.split("  ", 1) for line in r.stdout.splitlines()]
        self.assertTrue(all(len(row) == 2 and row[1] for row in rows), r.stdout)
        codes = [c for c, _ in rows]
        self.assertEqual(codes, lp_labels(), r.stdout)
        self.assertIn(["v_s3", "a requirement has no scenario"], rows)
        firstw = min(i for i, c in enumerate(codes) if c.startswith("w_"))
        self.assertTrue(all(c.startswith("w_") for c in codes[firstw:]), codes)
        self.assertTrue(all(c.startswith("v") for c in codes[:firstw]), codes)

    def test_every_relation_model_lp_shows_has_one_label(self):
        """r2, r65: a relation model.lp shows has exactly one label, and no label names a relation not shown"""
        text = LP.read_text()
        shown = {m for line in text.splitlines() for m in re.findall(r"#show\s+(\w+)/\d+\.", line.split("%")[0])}
        shown -= {"label"}
        labels = re.findall(r'^label\("([^"]+)",\s*"((?:[^"\\]|\\.)+)"\)\.', text, re.M)
        names = [c for c, _ in labels]
        self.assertEqual(sorted(set(names)), sorted(shown))
        self.assertEqual(len(names), len(set(names)), "a code has two labels")


def lp_labels():
    return re.findall(r'^label\("([^"]+)",', LP.read_text(), re.M)


class DecisionsTest(ModelTest):
    def decisions(self):
        self.write("spec/decisions/0001-old.md", f'---\nid: {full("design-decision", "old")}\nsummary: "Do it the old way."\ndate: 2026-01-01\nstatus: superseded\n---\n# 1\n')
        self.write("spec/decisions/0002-new.md", f'---\nid: {full("design-decision", "new")}\nsummary: "Do it | the new way."\ndate: 2026-02-01\nstatus: accepted\nsupersedes: design-decision/old\nrevisit_when: "it hurts"\nrevisit_signal: requests\n---\n# 2\n')

    def test_the_index_is_written_with_no_decision_yet(self):
        """the decisions index is written when there is no decision yet"""
        r = self.run_model("decisions")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("spec/decisions/index.md", r.stdout)
        text = (self.tmp / "spec/decisions/index.md").read_text()
        self.assertTrue(text.startswith("# "), text)
        self.assertNotIn("](", text)

    def test_r15(self):
        """a stale decisions index is reported and left alone"""
        self.decisions()
        target = self.write("spec/decisions/index.md", "# Decisions\n\nhand-written\n")
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
        self.assertIn("spec/decisions/index.md is current", r.stdout)


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

    def test_a_held_scenario_is_no_acceptance_scenario(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] `thing` shall answer."], retired="[r2]"))
        self.write("features/thing.feature", "\n".join([
            "Feature: thing", "",
            "  @r1", "  Scenario: one", "    Given a", "",
            "  @r1 @deprecated", "  Scenario: one as it was (held)", "    Given a", "",
            "  @r2 @deprecated", "  Scenario: two as it was (held)", "    Given a", ""]))
        r = self.run_model("check")
        self.assertEqual(r.returncode, 0, r.stdout)
        facts = self.run_model("facts").stdout
        self.assertNotIn("(held)", facts)


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

    def test_r19(self):
        """model reads the repository's files under its root"""
        feat = feature("thing", ("@r1", "it answers"))
        decision = f"---\nid: {full('design-decision', 'one')}\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n"
        one = f'node("{full("design-decision", "one")}", "design-decision").'
        initiative, i1 = f"---\nid: {I1}\nstatus: started\n---\n", f'node("{I1}", "initiative").'
        observations, obs = f"# Observations\n\n## {OBS1}\nabout: {CONTEXT}\n", f'node("{OBS1}", "observation").'
        rows = [
            ("spec/index.md", "---\nid: bounded-context/row.com/prod/rowctx\n---\n",
             'node("bounded-context/row.com/prod/rowctx", "bounded-context").', True, True),
            ("spec/capabilities/thing.md", cap("thing", ["- [r1] One."]), f'node("{THING}", "capability").', True, True),
            ("features/sub/thing.feature", feat, 'features/sub/thing.feature:it answers', True, True),
            ("spec/decisions/0001-one.md", decision, one, True, True),
            ("spec/decisions/index.md", decision, one, False, True),
            (".shop/work/i1/initiative.md", initiative, i1, True, True),
            (".shop/records/observations.md", observations, obs, True, True),
            (".shop/records/review/f1.md", f"---\nid: {full('review-finding', 'f1')}\nkind: review-finding\n---\n",
             f'node("{full("review-finding", "f1")}", "review-finding").', True, True),
            (".shop/records/review/f2.md", "---\nkind: review-finding\nabout: capability/zzmark\n---\n", "zzmark", False, True),
            ("decisions/0001-one.md", decision, one, False, True),
            ("work/i1/initiative.md", initiative, i1, False, True),
            ("records/observations.md", observations, obs, False, True),
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
        """a feature file no capability is formulated as, or with a title twice, is a file problem"""
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
                self.assertEqual(sorted(found), ["labels", "problems", "unresolved", "violations", "warnings"])
                codes = {name for name, _ in found["violations"] + found["warnings"]}
                self.assertEqual(set(found["labels"]), codes, found)
                self.assertTrue(all(isinstance(v, str) and v for v in found["labels"].values()), found)
                self.assertEqual(r.returncode, status)
                self.assertEqual(bool(found["violations"]), status == 1)

    def test_r34(self):
        """only a capability-change initiative may have several parts directly"""
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
        self.assertRegex(r.stdout, r"v_k6  .+  \(1\)\n\s+" + re.escape(P1))




@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class HeldAndLedgerTest(ModelTest):
    """r44."""

    def test_r44(self):
        """a deprecated scenario names no requirement"""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."]))
        self.write("features/thing.feature", "Feature: thing\n\n  @r2 @deprecated\n  Scenario: two as it was\n    Given a\n")
        found, _ = self.check_json()
        self.assertEqual(self.violated(found, "v_s3"), [[THING + "#r2"]], found)


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

    def test_a_definition_with_a_period_is_one_definition(self):
        self.write("spec/index.md", index("- **store**: where things are kept, e.g. a shelf."))
        lines = self.facts()
        self.assertIn(f'node("{term("store")}", "term").', lines)
        self.assertEqual([l for l in lines if l.startswith("avoid(")], [])

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
                                                     ("@r2 @deprecated", "a chunk as it was")))
        found, r = self.check_json()
        self.assertEqual(sorted(self.violated(found, "v_t1")), sorted([
            [THING + "#r1", "chunk", term("slice")],
            ["features/thing.feature:chunks are planned", "chunk", term("slice")]]), found)
        self.assertFalse([a for a in self.violated(found, "v_t1") if "as it was" in a[0]], found)
        self.assertEqual(r.returncode, 1)
        text = self.run_model("check").stdout
        self.assertIn("v_t1  a word the glossary avoids  (2)", text)

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
        self.assertEqual([t for t in missing(FEATURE, CheckTest, RulesTest, DecisionsTest,
                                             ReadingTest, GrammarFixTest, TypeFirstTest, FilesReadTest, OutputTest,
                                             HeldAndLedgerTest, GlossaryFactsTest,
                                             GlossaryCheckTest, WithdrawnTest) if t not in gone], [])


if __name__ == "__main__":
    unittest.main()
