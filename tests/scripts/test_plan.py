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


if __name__ == "__main__":
    unittest.main()
