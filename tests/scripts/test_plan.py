import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "plan"

PLAN = '''# Cart slices

## Slice 1: Add a product
- Kind: capability
- Scenarios: cart / Adding a product
- Observable: a shopper sees one item in the cart
- Unknown: none
- Needs: none
- Status: green

## Slice 2: Several products
- Kind: capability
- Scenarios: cart / Adding several
- Observable: a shopper sees the count
- Unknown: none
- Needs: none
- Status: planned

## Satisfied by existing behaviour

## Log
- 2026-10-01 Suite: 3 passed, 1 failed at abc1234 in 12 s
- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built
'''


class PlanTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        plans = self.tmp / "docs" / "superpowers" / "plans"
        plans.mkdir(parents=True)
        self.plan = plans / "cart-slices.md"
        self.plan.write_text(PLAN)

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.tmp,
                              capture_output=True, text=True)

    def git(self, *args):
        return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
                              cwd=self.tmp, check=True, capture_output=True, text=True).stdout.strip()

    def test_check_accepts_a_valid_plan(self):
        done = self.run_script("check")
        self.assertEqual((done.returncode, done.stdout), (0, "ok\n"))

    def test_check_refuses_sections_out_of_order(self):
        self.plan.write_text(PLAN.replace("## Satisfied by existing behaviour\n\n", "") +
                             "\n## Satisfied by existing behaviour\n")
        done = self.run_script("check")
        self.assertEqual(done.returncode, 1)
        self.assertIn("out of order", done.stderr)

    def test_log_appends_a_dated_line(self):
        self.run_script("log", "slice 2 green", "--date", "2026-10-03")
        self.assertEqual(self.plan.read_text(), PLAN + "- 2026-10-03 slice 2 green\n")

    def test_backlog_is_created_before_the_log(self):
        self.run_script("backlog", "slow lookup on 10k items", "--date", "2026-10-03")
        self.assertIn("## Satisfied by existing behaviour\n\n## Backlog\n"
                      "- 2026-10-03 slow lookup on 10k items\n\n## Log\n", self.plan.read_text())

    def test_status_sets_one_slice(self):
        self.run_script("status", "2", "in progress")
        text = self.plan.read_text()
        self.assertEqual(text, PLAN.replace("- Status: planned\n", "- Status: in progress\n"))

    def test_status_refuses_an_unknown_status(self):
        done = self.run_script("status", "2", "done")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(self.plan.read_text(), PLAN)

    def test_status_may_carry_a_note(self):
        done = self.run_script("status", "2", "in progress: waits on slice 1")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.run_script("show", "--open").stdout,
                         "2 Several products: in progress: waits on slice 1\n")

    def test_status_refuses_a_missing_slice(self):
        self.assertEqual(self.run_script("status", "7", "green").returncode, 1)

    def test_add_slice_goes_in_number_order(self):
        done = self.run_script("add-slice", "1.1", "Remove a product", "--kind", "capability",
                               "--scenarios", "cart / Removing a product",
                               "--observable", "a shopper removes a pen")
        self.assertEqual(done.returncode, 0, done.stderr)
        text = self.plan.read_text()
        self.assertLess(text.index("## Slice 1:"), text.index("## Slice 1.1: Remove a product"))
        self.assertLess(text.index("## Slice 1.1:"), text.index("## Slice 2:"))
        self.assertIn("- Needs: none\n- Status: planned\n\n## Slice 2:", text)

    def test_add_slice_refuses_an_enabling_slice_without_a_check(self):
        done = self.run_script("add-slice", "3", "Fast suite", "--kind", "enabling",
                               "--scenarios", "x", "--observable", "y")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(self.plan.read_text(), PLAN)

    def test_add_slice_refuses_an_existing_number(self):
        done = self.run_script("add-slice", "2", "Again", "--kind", "capability",
                               "--scenarios", "x", "--observable", "y")
        self.assertEqual(done.returncode, 1)

    def test_an_unknown_section_survives_every_edit(self):
        notes = "## Notes\nfree text the script does not own\n\n"
        self.plan.write_text(PLAN.replace("## Log\n", notes + "## Log\n"))
        self.run_script("status", "2", "green")
        self.run_script("log", "x", "--date", "2026-10-03")
        self.assertIn(notes + "## Log\n", self.plan.read_text())

    def test_show_open(self):
        self.assertEqual(self.run_script("show", "--open").stdout, "2 Several products: planned\n")

    def test_show_requests(self):
        self.assertEqual(self.run_script("show", "--requests").stdout,
                         "- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built\n")

    def test_show_last_suite(self):
        self.assertEqual(self.run_script("show", "--last-suite").stdout,
                         "- 2026-10-01 Suite: 3 passed, 1 failed at abc1234 in 12 s\n")

    def test_archive_moves_green_slices_and_log_keeping_requests(self):
        done = self.run_script("archive", "14", "--date", "2026-10-06")
        self.assertEqual(done.returncode, 0, done.stderr)
        archived = (self.plan.parent / "archive" / "cart-slices-14.md").read_text()
        self.assertIn("## Slice 1: Add a product", archived)
        self.assertIn("- 2026-10-01 Suite: 3 passed", archived)
        text = self.plan.read_text()
        self.assertNotIn("## Slice 1:", text)
        self.assertTrue(text.endswith(
            "## Log\n- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built\n"
            "- 2026-10-06 Batch 14 archived to archive/cart-slices-14.md; "
            "last 2026-10-01 Suite: 3 passed, 1 failed at abc1234 in 12 s\n"
            "- 2026-10-01 Suite: 3 passed, 1 failed at abc1234 in 12 s\n"))

    def test_archive_keeps_continuation_lines_with_their_entries(self):
        self.plan.write_text(PLAN.replace(
            "kb serve is not built\n",
            "kb serve is not built\n  needed by slice 53\n- 2026-10-03 HAND-BACK slice 2\n  evidence: red\n"))
        done = self.run_script("archive", "14", "--date", "2026-10-06")
        self.assertEqual(done.returncode, 0, done.stderr)
        archived = (self.plan.parent / "archive" / "cart-slices-14.md").read_text()
        self.assertIn("kb serve is not built\n  needed by slice 53\n"
                      "- 2026-10-03 HAND-BACK slice 2\n  evidence: red\n", archived)
        self.assertIn("## Log\n- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built\n"
                      "  needed by slice 53\n- 2026-10-06 Batch 14", self.plan.read_text())

    def test_archive_keeps_open_questions_in_the_log(self):
        self.plan.write_text(PLAN.replace(
            "kb serve is not built\n",
            "kb serve is not built\n- 2026-10-03 RE-FORMULATE cart / Adding several\n  evidence: red\n"
            "- 2026-10-03 QUESTION FOR THE SPEC: clamp or raise?\n- 2026-10-04 slice 1 green\n"))
        done = self.run_script("archive", "14", "--date", "2026-10-06")
        self.assertEqual(done.returncode, 0, done.stderr)
        text = self.plan.read_text()
        self.assertIn("- 2026-10-03 RE-FORMULATE cart / Adding several\n  evidence: red\n"
                      "- 2026-10-03 QUESTION FOR THE SPEC: clamp or raise?\n- 2026-10-06 Batch 14", text)
        self.assertNotIn("slice 1 green", text)

    def test_last_suite_holds_after_archive(self):
        self.git("init", "-q")
        (self.tmp / "code.txt").write_text("one\n")
        self.git("add", "code.txt")
        self.git("commit", "-qm", "code")
        tested = self.git("rev-parse", "--short", "HEAD")
        self.plan.write_text(PLAN.replace("abc1234", tested))
        self.git("add", "-A")
        self.git("commit", "-qm", "checkpoint")
        self.assertEqual(self.run_script("archive", "14", "--date", "2026-10-06").returncode, 0)
        self.git("add", "-A")
        self.git("commit", "-qm", "archive")
        done = self.run_script("show", "--last-suite", "--current")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertEqual(done.stdout, "- 2026-10-01 Suite: 3 passed, 1 failed at %s in 12 s\ncurrent\n" % tested)

    def test_current_without_last_suite_is_a_usage_error(self):
        self.assertEqual(self.run_script("show", "--open", "--current").returncode, 2)

    def test_last_suite_holds_until_code_changes(self):
        self.git("init", "-q")
        (self.tmp / "code.txt").write_text("one\n")
        self.git("add", "code.txt")
        self.git("commit", "-qm", "code")
        tested = self.git("rev-parse", "--short", "HEAD")
        self.plan.write_text(PLAN.replace("abc1234", tested))
        self.git("add", "-A")
        self.git("commit", "-qm", "checkpoint")
        done = self.run_script("show", "--last-suite", "--current")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertTrue(done.stdout.endswith("current\n"))
        (self.tmp / "code.txt").write_text("two\n")
        done = self.run_script("show", "--last-suite", "--current")
        self.assertEqual(done.returncode, 1)
        self.assertIn("stale: 1 files changed since", done.stdout)

    def test_last_suite_on_a_commit_not_in_the_repository_is_stale(self):
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("commit", "-qm", "plan")
        self.plan.write_text(PLAN.replace("abc1234", "deadbee"))
        done = self.run_script("show", "--last-suite", "--current")
        self.assertEqual(done.returncode, 1)
        self.assertIn("stale: commit deadbee is not in this repository", done.stdout)

    def lands(self, text):
        self.plan.write_text(PLAN.replace("- Status: planned", "- Lands: %s\n- Status: planned" % text))
        return self.run_script("check")

    def test_a_slice_without_lands_stays_valid(self):
        self.assertEqual(self.run_script("check").returncode, 0)
        self.assertEqual(self.run_script("status", "2", "green").returncode, 0)

    def test_lands_at_the_budget_is_accepted(self):
        self.assertEqual(self.lands("8 production, 4 test").returncode, 0)

    def test_lands_over_the_budget_is_refused_naming_slice_and_budget(self):
        for text in ("9 production, 4 test", "8 production, 5 test"):
            done = self.lands(text)
            self.assertEqual(done.returncode, 1)
            self.assertIn("slice 2: Lands %s is over the budget of 8 production, 4 test" % text, done.stderr)

    def test_a_malformed_lands_is_refused(self):
        done = self.lands("about twenty files")
        self.assertEqual(done.returncode, 1)
        self.assertIn("slice 2: Lands must be '<p> production, <t> test'", done.stderr)

    def test_an_edit_is_refused_while_a_slice_is_over_budget(self):
        self.lands("30 production, 20 test")
        done = self.run_script("status", "2", "in progress")
        self.assertEqual(done.returncode, 1)
        self.assertIn("over the budget", done.stderr)

    def test_add_slice_writes_lands_before_status(self):
        done = self.run_script("add-slice", "3", "Remove", "--kind", "capability", "--scenarios", "cart / Removing",
                               "--observable", "gone", "--lands", "2 production, 1 test")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("- Needs: none\n- Lands: 2 production, 1 test\n- Status: planned\n", self.plan.read_text())

    def test_add_slice_refuses_lands_over_the_budget(self):
        done = self.run_script("add-slice", "3", "Remove", "--kind", "capability", "--scenarios", "cart / Removing",
                               "--observable", "gone", "--lands", "12 production, 1 test")
        self.assertEqual(done.returncode, 1)
        self.assertNotIn("Slice 3", self.plan.read_text())

    def test_archive_keeps_a_green_slices_lands(self):
        self.plan.write_text(PLAN.replace("- Status: green", "- Lands: 3 production, 2 test\n- Status: green"))
        self.assertEqual(self.run_script("archive", "b1").returncode, 0)
        archived = (self.plan.parent / "archive" / "cart-slices-b1.md").read_text()
        self.assertIn("- Lands: 3 production, 2 test", archived)

    def test_lands_sets_the_line_on_a_slice_without_one(self):
        done = self.run_script("lands", "2", "3 production, 1 test")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("- Needs: none\n- Lands: 3 production, 1 test\n- Status: planned\n", self.plan.read_text())

    def test_lands_replaces_the_line(self):
        self.run_script("lands", "2", "3 production, 1 test")
        self.assertEqual(self.run_script("lands", "2", "5 production, 2 test").returncode, 0)
        text = self.plan.read_text()
        self.assertIn("- Lands: 5 production, 2 test\n", text)
        self.assertNotIn("3 production", text)

    def test_lands_over_the_budget_is_refused_and_the_file_unchanged(self):
        before = self.plan.read_text()
        done = self.run_script("lands", "2", "9 production, 1 test")
        self.assertEqual(done.returncode, 1)
        self.assertIn("over the budget", done.stderr)
        self.assertEqual(self.plan.read_text(), before)

    def test_a_second_lands_line_is_refused(self):
        done = self.lands("2 production, 1 test\n- Lands: 30 production, 1 test")
        self.assertEqual(done.returncode, 1)
        self.assertIn("slice 2: more than one Lands line", done.stderr)

    def test_a_lands_line_with_extra_text_is_refused(self):
        self.assertEqual(self.lands("2 production, 1 test (a floor)").returncode, 1)

    def test_a_misspelt_lands_line_is_refused(self):
        for line in ("- lands: 30 production, 1 test", "  - Lands: 30 production, 1 test", "-  Lands: 2 production, 1 test"):
            self.plan.write_text(PLAN.replace("- Status: planned", line + "\n- Status: planned"))
            done = self.run_script("check")
            self.assertEqual(done.returncode, 1, line)
            self.assertIn("slice 2: write the line as '- Lands: <p> production, <t> test'", done.stderr)

    def test_lands_spacing_is_exact(self):
        self.assertEqual(self.lands("2 production,  1 test").returncode, 1)
        self.assertEqual(self.lands("2 production,1 test").returncode, 1)
        self.assertEqual(self.lands("2 production, 1 tests").returncode, 1)

    def test_show_is_refused_while_a_slice_is_over_budget(self):
        self.lands("30 production, 20 test")
        done = self.run_script("show", "--open")
        self.assertEqual(done.returncode, 1)
        self.assertIn("slice 2: Lands 30 production, 20 test is over the budget", done.stderr)

    def test_add_slice_without_lands_says_so_and_succeeds(self):
        done = self.run_script("add-slice", "3", "Remove", "--kind", "capability", "--scenarios", "cart / Removing",
                               "--observable", "gone")
        self.assertEqual(done.returncode, 0)
        self.assertIn("plan: note: slice 3 has no Lands line; set it with: plan lands 3", done.stderr)

    def test_add_slice_with_lands_is_silent(self):
        done = self.run_script("add-slice", "3", "Remove", "--kind", "capability", "--scenarios", "cart / Removing",
                               "--observable", "gone", "--lands", "1 production, 1 test")
        self.assertEqual((done.returncode, done.stderr), (0, ""))


if __name__ == "__main__":
    unittest.main()
