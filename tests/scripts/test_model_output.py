"""Unit tests of what design-model-check's Implementation section says and its scenarios leave to it (decision
0055): the exit codes, the counts `model check` ends with, its row limit, and the file `model decisions` names."""

import contextlib
import io
import os
import subprocess
import sys
import types
import unittest
from unittest import mock

from test_model import HAVE_CLINGO, SCRIPT, ModelTest, cap, feature
from test_model_spec import DRAFTED, START, CodifiedTest, codified


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class CheckOutputTest(ModelTest):
    def test_check_ends_with_the_four_counts(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."], rests_on="[nope]"))
        self.write("features/stray.feature", "Feature: stray\n")
        self.observation()
        r = self.run_model("check")
        self.assertEqual(r.stdout.splitlines()[-1], "1 violations, 1 warnings, 1 unresolved references, 1 file problems", r.stdout)

    def test_rows_of_a_violated_relation_are_limited(self):
        for rows, args, shown, more in ((5, ["--limit", "2"], 2, 3), (12, [], 10, 2)):
            with self.subTest(rows=rows, args=args):
                self.reset()
                self.write("spec/capabilities/thing.md", cap("thing", [f"- [r{n}] Req {n}." for n in range(1, rows + 1)]))
                lines = self.run_model("check", *args).stdout.splitlines()
                at = lines.index(f"v_s3  a group has no scenario  ({rows})")
                block = [line for line in lines[at + 1:at + 1 + shown + 1]]
                self.assertEqual(len([line for line in block if "thing#g" in line]), shown, lines)
                self.assertEqual(block[-1], f"    ... and {more} more", lines)

    def test_exit_codes_of_check(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."]))
        self.write("features/thing.feature", feature("thing", ("@r1", "it answers")))
        self.assertEqual(self.run_model("check").returncode, 0)
        self.assertEqual(self.run_model("check", "--json").returncode, 0)
        self.observation()
        self.assertEqual(self.run_model("check").returncode, 0, "a warning alone exits 0")
        for case, path, text in (("violation", "spec/capabilities/other.md", cap("other", ["- [r1] One."])),
                                 ("unresolved", "features/thing.feature", feature("thing", ("@r1", "a"), ("@r7", "b"))),
                                 ("file problem", "features/stray.feature", "Feature: stray\n")):
            with self.subTest(case=case):
                self.write(path, text)
                self.assertEqual(self.run_model("check").returncode, 1)
                self.assertEqual(self.run_model("check", "--json").returncode, 1)

    def test_check_without_clingo_exits_2(self):
        self.write("hidden/clingo.py", 'raise ImportError("hidden")\n')
        env = {k: v for k, v in os.environ.items() if k not in ("SHOPSYSTEM_MODEL_PYTHON", "SHOPSYSTEM_MODEL_REEXEC")}
        env.update(PYTHONPATH=str(self.tmp / "hidden"), PATH=str(self.tmp / "empty"))
        cmd = [sys.executable, str(SCRIPT), "--root", str(self.tmp), "check"]
        r = subprocess.run(cmd, capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)


class OtherCommandsTest(ModelTest):
    def test_decisions_prints_the_file_it_wrote(self):
        r = self.run_model("decisions")
        self.assertEqual((r.returncode, r.stdout.strip()), (0, "wrote %s" % (self.tmp / "spec/decisions/index.md")), r.stderr)

    def test_a_stale_index_exits_1(self):
        self.write("spec/decisions/index.md", "# hand written\n")
        self.assertEqual(self.run_model("decisions", "--check").returncode, 1)

    def test_bad_usage_exits_2(self):
        self.assertEqual(self.run_model("banana").returncode, 2)


class LanguageCommandsTest(CodifiedTest):
    """`model parse`, `lexicon` and `logic` (the GF conversion's design §15)."""

    def test_parse_prints_one_tree(self):
        r = self.run_model("parse", START)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(len(r.stdout.strip().splitlines()), 1, r.stdout)
        self.assertTrue(r.stdout.startswith("When NoPre (k_agent_Event"), r.stdout)

    def test_a_refusal_exits_1_with_the_hint(self):
        r = self.run_model("parse", DRAFTED)
        self.assertEqual(r.returncode, 1)
        self.assertIn("`drafted`", r.stdout)
        self.assertIn("parsed up to: When the person runs `work start` on an initiative, `work` shall set the status of "
                      "the initiative to", r.stdout)
        self.assertIn("nearest words:", r.stdout)

    def test_parse_a_file_numbers_its_lines(self):
        path = self.write("lines.txt", START + "\n\n" + DRAFTED + "\n")
        r = self.run_model("parse", "--file", str(path))
        self.assertEqual(r.returncode, 1)
        out = r.stdout.splitlines()
        self.assertTrue(out[0].startswith("1: When NoPre (k_agent_Event"), out)
        self.assertTrue([line for line in out if line.startswith("3: ") and "`drafted`" in line], out)

    def test_parse_a_file_skips_its_comment_lines(self):
        path = self.write("corpus.txt", "# a corpus: sentences that parse\n" + START + "\n")
        r = self.run_model("parse", "--file", str(path))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertTrue(r.stdout.startswith("2: When NoPre (k_agent_Event"), r.stdout)

    def test_parse_a_codified_file_parses_its_statements_only(self):
        path = self.write("spec/capabilities/wq.md", codified("wq", self.start_group()))
        r = self.run_model("parse", "--file", str(path))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        lines = path.read_text().splitlines()
        out = r.stdout.splitlines()
        self.assertEqual(len(out), 2, out)
        for row in out:
            n, tree = row.split(": ", 1)
            self.assertTrue(lines[int(n) - 1].startswith("- [r"), (row, lines[int(n) - 1]))
            self.assertTrue(tree.startswith("When NoPre (k_agent_Event"), row)

    def test_parse_a_codified_file_names_the_line_of_a_refused_statement(self):
        path = self.write("spec/capabilities/wq.md", codified("wq", self.start_group(f"- [r3] {DRAFTED}")))
        r = self.run_model("parse", "--file", str(path))
        self.assertEqual(r.returncode, 1)
        n = next(i for i, line in enumerate(path.read_text().splitlines(), 1) if line.startswith("- [r3]"))
        self.assertTrue([line for line in r.stdout.splitlines() if line.startswith(f"{n}: ") and "`drafted`" in line],
                        r.stdout)

    def test_parse_the_universal_file_parses_its_conditions(self):
        text = "---\nlanguage: codified-2\n---\n\n# Universal\n\n## Behaviour\n\n- [U1] " + START + "\n"
        path = self.write("spec/universal.md", text)
        r = self.run_model("parse", "--file", str(path))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(r.stdout.startswith("9: When NoPre (k_agent_Event"), r.stdout)

    def test_parse_in_a_grammar_that_is_not_there_exits_2(self):
        r = self.run_model("parse", "--grammar", "Nope", START)
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)

    def test_lexicon_lists_terms_by_category(self):
        r = self.run_model("lexicon")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertRegex(r.stdout, r"(?m)^kind \(\d+\)$")
        self.assertRegex(r.stdout, r"(?m)^  initiative$")
        self.assertRegex(r.stdout, r"(?m)^  status \(of work-item\): `drafted`, ")
        self.assertEqual(self.run_model("lexicon", "--check").returncode, 0)

    def test_lexicon_check_gives_the_term_rules(self):
        text = (self.tmp / "spec/index.md").read_text().replace(
            "## Glossary\n", "## Glossary\n\n- **level** (attribute of initiative): how deep it goes.\n", 1)
        self.write("spec/index.md", text)
        r = self.run_model("lexicon", "--check")
        self.assertEqual(r.returncode, 1)
        self.assertRegex(r.stdout, r"(?m)^v_t4  level  ")

    def test_logic_passes_spec_solve_its_report(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import model_report
        calls = []
        fake = types.SimpleNamespace(run=lambda root, capability=None, extra=None: calls.append((root, capability)) or ["F"],
                                     report=lambda findings, _as_json: ("L1 r1 r2\n" if findings == ["F"] else "", 1))
        args = types.SimpleNamespace(root=str(self.tmp), capability="wq", json=False)
        out = io.StringIO()
        with mock.patch.dict(sys.modules, {"spec_solve": fake}), contextlib.redirect_stdout(out):
            self.assertEqual(model_report.cmd_logic(args), 1)
        self.assertEqual(calls, [(str(self.tmp), "wq")])
        self.assertIn("L1 r1 r2", out.getvalue())

    def test_logic_without_spec_solve_exits_2(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import model_report
        args = types.SimpleNamespace(root=str(self.tmp), capability=None, json=False)
        out = io.StringIO()
        with mock.patch.dict(sys.modules, {"spec_solve": None}), contextlib.redirect_stdout(out):
            self.assertEqual(model_report.cmd_logic(args), 2)
        self.assertIn("spec_solve", out.getvalue())


if __name__ == "__main__":
    unittest.main()
