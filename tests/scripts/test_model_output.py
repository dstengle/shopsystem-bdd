"""Unit tests of what design-model-check's Implementation section says and its scenarios leave to it (decision
0055): the exit codes, the counts `model check` ends with, its row limit, and the file `model decisions` names."""

import os
import subprocess
import sys
import unittest

from test_model import HAVE_CLINGO, SCRIPT, ModelTest, cap, feature


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
                at = lines.index(f"v_s3  a requirement has no scenario  ({rows})")
                block = [line for line in lines[at + 1:at + 1 + shown + 1]]
                self.assertEqual(len([line for line in block if "thing#r" in line]), shown, lines)
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

    def test_exit_codes_of_why(self):
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."]))
        self.assertEqual(self.run_model("why", "thing#r1").returncode, 0, "no proposal adds or changes it is an answer")
        self.assertEqual(self.run_model("why", "thing").returncode, 2, "not a requirement reference")

    def test_bad_usage_exits_2(self):
        self.assertEqual(self.run_model("banana").returncode, 2)


if __name__ == "__main__":
    unittest.main()
