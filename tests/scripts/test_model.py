"""Unit tests of scripts/model. The scenarios of features/design-model-check.feature are bound in
tests/scenarios/test_design_model_check.py. A test here that shares a scenario's subject usually checks what its steps do
not; test_r5 and test_r20 repeat their scenarios and stay until a later cleanup removes them. ModelTest and the file
builders here serve test_model_reading.py and test_model_glossary.py too. Every fixture is codified (design model v5):
the index carries the typed glossary of tests/scripts/fixtures/glossary/, and `cap()` writes one group a requirement."""

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
sys.path.insert(0, str(ROOT / "tests"))
import toolchain
from model_fixture import (  # noqa: F401 -- the builders, imported from here by the other model tests
    CONTEXT,
    HEAD,
    I1,
    INDEX,
    OBS1,
    P1,
    PATH,
    STATEMENT,
    THING,
    W1,
    cap,
    feature,
    full,
)

SCRIPT = ROOT / "scripts" / "model"
LP = ROOT / "scripts" / "model.lp"

try:
    import clingo  # noqa: F401
    HAVE_CLINGO = True
except ImportError:
    HAVE_CLINGO = False

class ModelTest(unittest.TestCase):
    def setUp(self):
        toolchain.require()
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
        """A statement with no id: v15a, and the reader reports its line."""
        self.write("spec/capabilities/thing.md", cap("thing", ["- **When** asked, `thing` shall answer."], group="guarantees"))
        r = self.run_model("check")
        self.assertIn("v15a", r.stdout)
        self.assertIn("a requirement is not '- [r<n>] <statement>'", r.stdout)
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
        self.assertEqual(self.violated(found, "v_d5"), [[I1]], found)
        self.assertEqual(r.returncode, 1)
        self.reset()
        self.breakdown("abandoned", "withdrawn", "withdrawn")
        found, _ = self.check_json()
        self.assertEqual(self.about_initiative(found), [], found)


class Facts:
    """Facts written by hand, standing in for a Model: the v5 rules over facts `model facts` does not emit yet (P5)."""

    def __init__(self, text):
        self.text = text

    def asp(self):
        return self.text


def solve(text):
    sys.path.insert(0, str(ROOT / "scripts"))
    import model_check
    return [(name, args) for name, args in model_check.solve(Facts(text))[0]]


CAP = 'node("c","capability"). narrator("c","n"). in("c","x"). node("x","bounded-context"). '
GROUP = CAP + 'node("g","requirement-group"). in("g","c"). group_id("g","c",1). node("q","requirement"). req_id("q","c",1). member_of("q","g"). '
TESTED = GROUP + 'node("s","scenario"). generates("g","s"). '
WI = 'node("i","initiative"). status("i","started"). node("p","capability-proposal"). part_of("p","i"). status("p","drafted"). '
REQ = 'node("r","request"). asker("r","internal"). upstream("r","x"). req_source("r","o"). node("o","observation"). '
V5 = [   # (facts, code, the rows it gives)
    (TESTED, None, []),
    (GROUP, "v_s3", [["g"]]), (GROUP + 'logic_only("g").', "v_s3", []), (GROUP + 'group("c","guarantees").', "v_s3", []),
    (TESTED + 'node("s2","scenario").', "v_s1", [["s2"]]),
    (TESTED + 'node("g2","requirement-group"). in("g2","c"). generates("g2","s").', "v_s2", [["s"]]),
    (TESTED + 'node("g2","requirement-group"). in("g2","c"). member_of("q","g2").', "v_s4", [["q"]]),
    (TESTED + 'codified("c"). node("q2","requirement"). req_id("q2","c",2).', "v_s4", [["q2"]]),
    (TESTED + 'node("g2","requirement-group"). in("g2","c").', "v15g", [["g2"]]),
    (TESTED + 'node("g2","requirement-group"). in("g2","c"). group_id("g2","c",1).', "v15g", [["g"], ["g2"]]),
    (TESTED + 'node("u","universal-condition"). node("u2","universal-condition"). u_id("u2",1).', "v15h", [["u"]]),
    (TESTED + 'retired_group("c",1).', "v15i", [["g"]]),
    (TESTED + 'restates("g","c#r9@0.29"). restates("g","c#r1@0.29"). restated_id("c#r1@0.29").', "v15j", [["g", "c#r9@0.29"]]),
    (TESTED + 'node("q2","requirement"). member_of("q2","g"). pre("q","a"). pre("q2","b").', "v15k", [["g"]]),
    (TESTED + 'node("t","term"). term_of("t","x"). typed("x").', "v_t4", [["t"]]),
    (TESTED + 'node("t","term"). term_of("t","x").', "v_t4", []),
    (TESTED + 'value_of("v","k","a"). value_of("v","k","b").', "v_t5", [["v"]]),
    (TESTED + 'node("v","term"). category("v","value").', "v_t5", [["v"]]),
    (TESTED + 'linearises("t1","x y"). linearises("t2","x y").', "v_t6", [["t1", "t2"]]),
    (GROUP + WI + 'status("p","formulated"). adds("p","q").', "v15f", [["p"]]),
    (TESTED + WI + 'changes("p","q").', "v15e", [["p", "q"]]), (TESTED + WI + 'changes("p","g").', "v15e", []),
    (TESTED + 'resolution("r","s"). node("r","request"). status("r","accepted").', "v3", [["r", "s"]]),
    (WI + 'status("i","abandoned").', "v_d5", [["i"]]),
    (REQ + 'node("t","job-thread"). status("t","built"). req_part_of("r","t"). status("r","accepted").', "v_d2", [["t"]]),
    (REQ + 'status("r","delivered"). outcome("r",1,"accepted"). line("r",1,"x"). outcome("r",2,"accepted"). '
           'line("r",2,"y"). resolution_of_line("r",2).', "v_d4", [["r", 1]]),
    (REQ + 'asker("r2","bounded-context/a"). upstream("r2","x"). node("r2","request").', "v7", []),
    (REQ + 'asker("r2","bounded-context/a"). upstream("r2","x"). node("r2","request"). node("m","context-seam").', "v7", [["r2"]]),
    (REQ + 'node("t","job-thread"). node("p","capability-proposal"). part_of("p","t").', "v_b3", [["t"]]),
    (REQ + 'node("t","job-thread"). node("p","map-escalation"). part_of("p","t").', "v9c", []),
    (REQ + 'node("p","work-item"). part_of("p","r").', "v18b", [["p", "r"]]),
    ('foreign("request/a/b/c/q1").', "v18d", [["request/a/b/c/q1"]]),
    (WI + 'status("i","proposed"). age("i",91).', "w_stale_proposed", [["i"]]),
    (REQ + 'status("r","accepted"). age("r",91).', "w_stale_intake", [["r"]]),
    (" ".join(f'node("r{n}","request"). upstream("r{n}","x"). status("r{n}","open").' for n in range(6)), "w_many_requests", [["x"]]),
    (WI + 'date("i","2026-10-24").', "v16a", [["i"]]), (WI + 'date("i","2026-10-23").', "v16a", []),
]


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class V5RulesTest(unittest.TestCase):
    def test_each_v5_rule_over_the_facts_it_reads(self):
        for facts, code, rows in V5:
            with self.subTest(code=code, facts=facts):
                found = solve(facts)
                if code is None:
                    self.assertEqual([f for f in found if f[0].startswith("v")], [], found)
                else:
                    self.assertEqual(sorted(a for name, a in found if name == code), rows, found)

    def test_the_rules_v5_retires_are_gone_and_its_renamed_codes_are_listed(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "rules"], capture_output=True, text=True)
        codes = {line.split()[0] for line in r.stdout.splitlines()}
        self.assertFalse(codes & {"v1", "v7b", "v_k1", "v_k2", "v_b2", "v18"}, r.stdout)
        self.assertTrue({"v_d5", "w_stale_proposed", "v18d", "v15g", "v15h", "v15i", "v15j", "v15k", "v_t4", "v_t5",
                         "v_t6", "v_s4", "v_d4"} <= codes, r.stdout)
        self.assertNotIn("cross-context-request", LP.read_text())


if __name__ == "__main__":
    unittest.main()
