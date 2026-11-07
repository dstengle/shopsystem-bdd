"""Unit tests of scripts/model_spec: `model` reading the codified spec (the GF conversion's design §7, §8, §13.4).

A fixture repository here has the typed glossary of tests/scripts/fixtures/glossary/ and capability files written by
`codified()`. The helpers serve test_model_restates.py too."""

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))
import toolchain

SCRIPT = ROOT / "scripts" / "model"
GLOSSARY = ROOT / "tests" / "scripts" / "fixtures" / "glossary" / "spec" / "index.md"
PATH = "example.org/fixture/glossary"
CTX = f"bounded-context/{PATH}"
WQ = f"capability/{PATH}/wq"

START = "When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to `started`."
COMMIT = "When the person runs `work start` on an initiative that is `proposed`, `work` shall commit the transition."
ABANDON = "When the person runs `work abandon` on an initiative that is `started`, `work` shall set its status to `abandoned`."
DRAFTED = "When the person runs `work start` on an initiative that is `drafted`, `work` shall set its status to `started`."
AMBIGUOUS = "When the person runs `work list`, `work` shall print every request line in a request that is `accepted`."
LOCK = "`work run` shall hold the spec lock."


def codified(name, behaviour, dropped=(), retired="[]", marker=True, terms=()):
    """A capability file in the codified format; `behaviour` is its Behaviour section's lines."""
    head = textwrap.dedent(f"""\
        ---
        id: capability/{PATH}/{name}
        title: {name}
        narrator: the person
        group: service
        {"language: codified-1" if marker else ""}
        rests_on: []
        retired: {retired}
        ---

        # {name}

        ## Purpose
        Something.

        """)
    out = head + ("## Terms\n\n" + "\n".join(terms) + "\n\n" if terms else "")
    out += "## Behaviour\n\n" + "\n".join(behaviour) + "\n\n## Not yet\n- None.\n"
    if dropped:
        out += "\n## Dropped\n" + "\n".join(dropped) + "\n"
    return out


def generated(name, *groups):
    """A feature file of generated scenarios, one per (g<n>, [r<n>...]) group."""
    out = [f"Feature: {name}", ""]
    for g, reqs in groups:
        out += ["  @" + " @".join([g] + list(reqs)), f"  Scenario: {g} holds", "    Given a thing", "    Then it holds", ""]
    return "\n".join(out)


class CodifiedTest(unittest.TestCase):
    def setUp(self):
        toolchain.require()
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.write("spec/index.md", GLOSSARY.read_text())
        self.write("spec/restated.json", json.dumps({"wq#r3": {"text": "old three", "line": 3},
                                                     "wq#r4": {"text": "old four", "line": 4},
                                                     "other#r1": {"text": "other one", "line": 9}}))

    def write(self, rel, text):
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def run_model(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.tmp), *args], capture_output=True,
                              text=True)

    def facts(self):
        r = self.run_model("facts")
        self.assertEqual(r.returncode, 0, r.stderr)
        return set(r.stdout.splitlines())

    def check(self):
        r = self.run_model("check", "--json")
        return json.loads(r.stdout), r

    def rows(self, found, code):
        return [a for name, a in found["violations"] if name == code]

    def start_group(self, *extra):
        return ["### [g1] `work start` starts a proposed initiative", "Restates: r3@0.29, other#r1@0.29.",
                f"- [r1] {START}", f"- [r2] {COMMIT}", *extra]


class FactsTest(CodifiedTest):
    def test_a_group_and_its_requirements_are_read(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.start_group()))
        f = self.facts()
        g, q1 = f"{WQ}#g1", f"{WQ}#r1"
        for fact in (f'node("{g}", "requirement-group").', f'group_id("{g}", "{WQ}", 1).', f'in("{g}", "{WQ}").',
                     f'node("{q1}", "requirement").', f'req_id("{q1}", "{WQ}", 1).', f'member_of("{q1}", "{g}").',
                     f'member_of("{WQ}#r2", "{g}").', f'codified("{WQ}").', f'parsed("{q1}").',
                     f'restates("{g}", "wq#r3@0.29").', f'restates("{g}", "other#r1@0.29").',
                     'restated_id("wq#r3@0.29").'):
            self.assertIn(fact, f)
        self.assertFalse([x for x in f if x.startswith("has_req(")], "has_req is derived from member_of")
        pre = sorted(x.split(", ", 1)[1] for x in f if x.startswith("pre("))
        self.assertEqual(len(pre), 2)
        self.assertEqual(pre[0], pre[1], "both statements share the trigger")

    def test_an_uncodified_capability_is_v_p0_and_its_lines_are_not_read(self):
        self.write("spec/capabilities/old.md", codified("old", ["- [r1] **When** asked, `old` shall answer."],
                                                        marker=False))
        self.write("features/old.feature", "Feature: old\n\n  @r1\n  Scenario: asked\n    Then it answers\n")
        f = self.facts()
        self.assertIn('uncodified("spec/capabilities/old.md").', f)
        self.assertFalse([x for x in f if "old#r1" in x or x.startswith(("has_req(", "has_sc(", "ears_"))])
        found, _ = self.check()
        self.assertEqual(self.rows(found, "v_p0"), [["spec/capabilities/old.md"]])
        self.assertIn("migrate upgrade", found["labels"]["v_p0"])

    def test_an_index_that_is_not_codified_is_v_p0(self):
        index = GLOSSARY.read_text().replace("language: codified-1\n", "")
        self.write("spec/index.md", index)
        found, _ = self.check()
        self.assertEqual(self.rows(found, "v_p0"), [["spec/index.md"]])
        self.assertFalse([d for d in found["problems"] if "glossary bullet" in d], found["problems"])

    def test_a_universal_condition_is_a_node_that_parses(self):
        self.write("spec/universal.md", "---\nid: capability/%s/universal\nlanguage: codified-1\n---\n\n"
                                        "## Behaviour\n\n- [U1] %s\n- [U2] Things shall be fine.\n" % (PATH, LOCK))
        f = self.facts()
        u1, u2 = f"universal-condition/{PATH}/u1", f"universal-condition/{PATH}/u2"
        self.assertIn(f'node("{u1}", "universal-condition").', f)
        self.assertIn(f'u_id("{u1}", 1).', f)
        self.assertIn(f'parsed("{u1}").', f)
        self.assertTrue([x for x in f if x.startswith(f'unparsed("{u2}"')], f)

    def test_the_typed_glossary_gives_categories_and_values(self):
        f = self.facts()
        t = lambda name: f"term/{PATH}/{name}"
        self.assertIn(f'typed("{CTX}").', f)
        self.assertIn(f'category("{t("initiative")}", "kind").', f)
        self.assertIn(f'category("{t("status-of-work-item")}", "attribute").', f)
        self.assertIn(f'value_of("{t("drafted-of-work-item")}", "{t("work-item")}", "{t("status-of-work-item")}").', f)
        self.assertIn(f'category("{t("drafted-of-work-item")}", "value").', f)
        self.assertIn(f'avoid("{t("initiative")}", "epic").', f)

    def test_a_word_in_two_categories_is_two_terms(self):
        """The legacy reader keyed a word once; the lexicon gives a kind and a resource of one spelling two terms."""
        text = GLOSSARY.read_text().replace("## Glossary\n", "## Glossary\n\n- **pool** (noun): a set of workers.\n"
                                            "- **pool** (noun, exclusive): held by a round.\n", 1)
        self.write("spec/index.md", text)
        f = self.facts()
        self.assertIn(f'category("term/{PATH}/pool", "kind").', f)
        self.assertIn(f'category("term/{PATH}/pool-resource", "resource").', f)

    def test_a_requirement_of_a_codified_file_gives_no_mentions(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.start_group()))
        self.assertFalse([x for x in self.facts() if x.startswith("mentions(")])

    def test_a_generated_scenario_is_generated_from_its_group(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.start_group()))
        self.write("features/wq.feature", generated("wq", ("g1", ["r1", "r2"])))
        f = self.facts()
        self.assertIn(f'generates("{WQ}#g1", "features/wq.feature:g1 holds").', f)
        self.assertIn('node("features/wq.feature:g1 holds", "scenario").', f)
        self.assertFalse([x for x in f if x.startswith("has_sc(")])

    def test_a_logic_only_group_is_marked(self):
        self.write("spec/capabilities/wq.md", codified("wq", ["### [g1] Rounds hold the lock", f"- [r1] {LOCK}"]))
        self.assertIn(f'logic_only("{WQ}#g1").', self.facts())

    def test_a_retired_group_id(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.start_group(), retired="[r9, g4]"))
        f = self.facts()
        self.assertIn(f'retired_group("{WQ}", 4).', f)
        self.assertIn(f'retired_id("{WQ}", 9).', f)

    def test_a_given_line_is_read_by_the_typed_steps_grammar(self):
        given = ["", "```given", "an initiative i1 that is `proposed`", "the initiative i1 frobs widgets", "```"]
        self.write("spec/capabilities/wq.md", codified("wq", self.start_group(*given)))
        unparsed = [x for x in self.facts() if x.startswith("given_unparsed(")]
        self.assertEqual(unparsed, [f'given_unparsed("{WQ}#g1", "the initiative i1 frobs widgets").'])


class CheckTest(CodifiedTest):
    def test_a_statement_with_no_id_is_v15a_and_a_repeated_id_v15b(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.start_group() + [
            "### [g2] Again", f"- {START}", f"- [r1] {COMMIT}"]))
        found, _ = self.check()
        self.assertEqual(self.rows(found, "v15a"), [[f"{WQ}#line23"]])
        self.assertEqual(len(self.rows(found, "v15b")), 1, found)

    def test_an_unparsed_statement_is_read_for_avoided_words(self):
        self.write("spec/capabilities/wq.md", codified("wq", ["### [g1] Start",
                                                              "- [r1] When the person runs `work start`, the user is told."]))
        found, _ = self.check()
        self.assertTrue(self.rows(found, "v_p1"), found)
        self.assertIn("user", [row[1] for row in self.rows(found, "v_t1")], found)

    def test_a_line_that_does_not_parse_is_v_p1(self):
        self.write("spec/capabilities/wq.md", codified("wq", ["### [g1] Start", f"- [r1] {DRAFTED}"]))
        found, r = self.check()
        rows = self.rows(found, "v_p1")
        self.assertEqual(len(rows), 1, found)
        self.assertEqual(rows[0][0], f"{WQ}#r1")
        self.assertIn("`drafted`", rows[0][1])
        self.assertEqual(r.returncode, 1)
        text = self.run_model("check").stdout
        self.assertRegex(text, r"(?m)^v_p1  ")

    def test_an_ambiguous_line_is_v_p2(self):
        self.write("spec/capabilities/wq.md", codified("wq", ["### [g1] List", f"- [r1] {AMBIGUOUS}"]))
        found, _ = self.check()
        self.assertEqual(self.rows(found, "v_p2"), [[f"{WQ}#r1"]], found)

    def test_statements_of_a_group_with_two_triggers_are_v15k(self):
        self.write("spec/capabilities/wq.md", codified("wq", ["### [g1] Mixed", f"- [r1] {START}", f"- [r2] {ABANDON}"]))
        found, _ = self.check()
        self.assertEqual(self.rows(found, "v15k"), [[f"{WQ}#g1"]], found)

    def test_a_group_of_more_than_one_statement_is_v15l(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.start_group() + ["### [g2] One", f"- [r3] {LOCK}"]))
        self.assertEqual(self.rows(self.check()[0], "v15l"), [[f"{WQ}#g1"]])

    def test_a_given_line_that_is_not_example_data_is_v15m(self):
        given = ["```given", "an initiative i1 that is `proposed`", "the file `a.md` holds:", "  # a",
                 'the file `b.md` holds "x"', "```"]
        self.write("spec/capabilities/wq.md", codified("wq", ["### [g1] Start", f"- [r1] {START}", *given]))
        self.assertEqual(self.rows(self.check()[0], "v15m"), [[f"{WQ}#g1", "an initiative i1 that is `proposed`"]])

    def test_two_groups_sharing_features_condition_and_trigger_are_v15n(self):
        self.write("spec/capabilities/wq.md", codified("wq", ["### [g1] A", f"- [r1] {START}", "### [g2] B",
                                                              f"- [r2] {COMMIT}", "### [g3] C", f"- [r3] {ABANDON}"]))
        self.assertEqual(self.rows(self.check()[0], "v15n"), [[f"{WQ}#g1", f"{WQ}#g2"]])

    def test_a_group_with_a_scenario_or_logic_only_is_no_v_s3(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.start_group() + [
            "", "### [g2] Abandon", f"- [r3] {ABANDON}", "", "### [g3] Lock", f"- [r4] {LOCK}"]))
        self.write("features/wq.feature", generated("wq", ("g1", ["r1", "r2"])))
        found, _ = self.check()
        self.assertEqual(self.rows(found, "v_s3"), [[f"{WQ}#g2"]], found)
        self.assertEqual(self.rows(found, "v_s1"), [])
        self.assertEqual(self.rows(found, "v_s2"), [])

    def test_a_restated_id_0_29_did_not_have_is_v15j(self):
        self.write("spec/capabilities/wq.md", codified("wq", ["### [g1] Start", "Restates: r77@0.29.", f"- [r1] {START}"]))
        found, _ = self.check()
        self.assertEqual(self.rows(found, "v15j"), [[f"{WQ}#g1", "wq#r77@0.29"]], found)

    def test_a_retired_group_used_again_is_v15i(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.start_group(), retired="[g1]"))
        found, _ = self.check()
        self.assertIn([f"{WQ}#g1"], self.rows(found, "v15i"), found)

    def test_a_malformed_codified_file_is_a_file_problem(self):
        self.write("spec/capabilities/wq.md", codified("wq", ["- [r1] " + START]))
        found, _ = self.check()
        self.assertTrue([p for p in found["problems"] if p.startswith("spec/capabilities/wq.md:")
                         and "outside a group" in p], found)

    def test_a_scenario_naming_a_group_that_is_not_there_is_unresolved(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.start_group()))
        self.write("features/wq.feature", generated("wq", ("g1", ["r1"]), ("g7", [])))
        found, _ = self.check()
        self.assertTrue([d for d in found["unresolved"] if f"{WQ}#g7" in d], found)

    def test_a_reference_to_a_0_29_id_resolves_through_restated_json(self):
        self.write("spec/capabilities/wq.md", codified("wq", self.start_group()))
        self.write("features/wq.feature", generated("wq", ("g1", ["r1", "r2"])))
        self.write(".shop/work/i1/initiative.md", f"---\nid: initiative/{PATH}/i1\ntitle: t\nsummary: s\n"
                   "kind: capability-change\nstatus: done\nsource: [x]\n---\n")
        self.write(".shop/work/i1/wq.md", f"---\nid: capability-proposal/{PATH}/p1\nkind: capability-proposal\n"
                   "part_of: initiative/i1\nargues: wq\nstatus: formulated\nadds: [wq#r3@0.29, wq#r9@0.29]\n---\n")
        found, _ = self.check()
        self.assertFalse([d for d in found["unresolved"] if "@0.29" in d], found)
        self.assertFalse(self.rows(found, "v3"))


class LiveTest(unittest.TestCase):
    def test_every_file_of_the_live_spec_is_codified(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import spec_read
        files = [ROOT / "spec" / "index.md", ROOT / "spec" / "universal.md",
                 *sorted((ROOT / "spec" / "capabilities").glob("*.md"))]
        self.assertEqual([p.name for p in files if not spec_read.codified(p)], [])

if __name__ == "__main__":
    unittest.main()
