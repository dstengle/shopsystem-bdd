"""Unit tests of scripts/model. The scenarios of features/design-model-check.feature are bound in
tests/scenarios/test_design_model_check.py. A test here that shares a scenario's subject usually checks what its steps do
not; test_r5 and test_r20 repeat their scenarios and stay until a later cleanup removes them. ModelTest and the file
builders here serve test_model_reading.py and test_model_glossary.py too."""

import json
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
LP = ROOT / "scripts" / "model.lp"

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
    def test_r3(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- **When** asked, `thing` shall answer."], group="guarantees"))
        r = self.run_model("check")
        self.assertIn("v15a", r.stdout)
        self.assertEqual(r.returncode, 1)

    def test_r5(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees", retired="[r1]"))
        r = self.run_model("check")
        self.assertIn("v15c", r.stdout)

    def test_r8(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] `thing` shall be fast."], group="guarantees"))
        r = self.run_model("check")
        self.assertNotIn("v_s3", r.stdout)
        self.assertEqual(r.returncode, 0, r.stdout)


class RulesTest(ModelTest):
    def test_every_relation_model_lp_shows_has_one_label(self):
        """r2, r65: a relation model.lp shows has exactly one label, and no label names a relation not shown"""
        text = LP.read_text()
        shown = {m for line in text.splitlines() for m in re.findall(r"#show\s+(\w+)/\d+\.", line.split("%")[0])}
        shown -= {"label"}
        labels = re.findall(r'^label\("([^"]+)",\s*"((?:[^"\\]|\\.)+)"\)\.', text, re.MULTILINE)
        names = [c for c, _ in labels]
        self.assertEqual(sorted(set(names)), sorted(shown))
        self.assertEqual(len(names), len(set(names)), "a code has two labels")


class DecisionsTest(ModelTest):
    def test_the_index_is_written_with_no_decision_yet(self):
        r = self.run_model("decisions")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("spec/decisions/index.md", r.stdout)
        text = (self.tmp / "spec/decisions/index.md").read_text()
        self.assertTrue(text.startswith("# "), text)
        self.assertNotIn("](", text)


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
        self.breakdown("abandoned", "withdrawn", "drafted")
        found, r = self.check_json()
        self.assertEqual(self.violated(found, "v_d2"), [[I1]], found)
        self.assertEqual(r.returncode, 1)
        self.reset()
        self.breakdown("abandoned", "withdrawn", "withdrawn")
        found, _ = self.check_json()
        self.assertEqual(self.about_initiative(found), [], found)


if __name__ == "__main__":
    unittest.main()
