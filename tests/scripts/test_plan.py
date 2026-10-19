import datetime
import pathlib
import re
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
        """checking a valid plan says ok"""
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
        """setting a slice's status changes only that status"""
        self.run_script("status", "2", "in progress")
        text = self.plan.read_text()
        self.assertEqual(text, PLAN.replace("- Status: planned\n", "- Status: in progress\n"))

    def test_status_refuses_an_unknown_status(self):
        """a status plan does not know is refused"""
        before = self.plan.read_bytes()
        for status in ("done", "done: merged", "blocked"):
            with self.subTest(status=status):
                done = self.run_script("status", "2", status)
                self.assertEqual(done.returncode, 1)
                self.assertIn("slice 2: Status must be", done.stderr)
                self.assertEqual(self.plan.read_bytes(), before)

    def test_status_may_carry_a_note(self):
        done = self.run_script("status", "2", "in progress: waits on slice 1")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.run_script("show", "--open").stdout,
                         "2 Several products: in progress: waits on slice 1\n")

    def test_status_refuses_a_missing_slice(self):
        """setting the status of a slice the plan does not have is refused"""
        done = self.run_script("status", "7", "green")
        self.assertEqual(done.returncode, 1)
        self.assertIn("no slice 7", done.stderr)

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
        """the current flag without last-suite is bad usage"""
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
        """a suite record naming an unknown commit is stale"""
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
        """a slice without a Lands line is valid"""
        done = self.run_script("check")
        self.assertEqual((done.returncode, done.stdout), (0, "ok\n"))
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

    # The scenarios' Background says today is 2026-10-16; this runs the script on that day.
    TODAY = "2026-10-16"
    ON_THE_DAY = (
        "import datetime, runpy, sys\n"
        "class Day(datetime.date):\n"
        "    @classmethod\n"
        "    def today(cls):\n"
        "        return cls(2026, 10, 16)\n"
        "datetime.date = Day\n"
        "sys.argv = sys.argv[1:]\n"
        "runpy.run_path(sys.argv[0], run_name='__main__')\n")

    def plan_cli(self, *args):
        return subprocess.run([sys.executable, "-c", self.ON_THE_DAY, str(SCRIPT), *args], cwd=self.tmp,
                              capture_output=True, text=True)

    def use(self, relative, text):
        """Make the one plan of the directory a file of this name and text."""
        self.plan.unlink()
        self.plan = self.tmp / relative
        self.plan.parent.mkdir(parents=True, exist_ok=True)
        self.plan.write_text(text)

    def stamped(self, files):
        """A repository whose plan's Suite record names a commit that holds `files`; returns the commit."""
        self.git("init", "-q")
        for name, text in files.items():
            (self.tmp / name).parent.mkdir(parents=True, exist_ok=True)
            (self.tmp / name).write_text(text)
            self.git("add", name)
        self.git("commit", "-qm", "code")
        tested = self.git("rev-parse", "--short", "HEAD")
        self.plan.write_text(PLAN.replace("abc1234", tested))
        self.git("add", "-A")
        self.git("commit", "-qm", "checkpoint")
        return tested

    @staticmethod
    def slice_lines(text, n):
        block = re.search(r"^## Slice %s:.*?(?=^## |\Z)" % re.escape(n), text, re.M | re.S)
        return block.group(0).splitlines() if block else []

    @staticmethod
    def section_lines(text, name):
        block = re.search(r"^## %s\n(.*?)(?=^## |\Z)" % re.escape(name), text, re.M | re.S)
        return block.group(1).splitlines() if block else []

    @staticmethod
    def slice_blocks(*numbers):
        return "".join("## Slice %s: Cart %s\n- Kind: capability\n- Scenarios: cart / x\n- Observable: o\n"
                       "- Unknown: none\n- Needs: none\n- Status: planned\n\n" % (n, n) for n in numbers)

    def test_an_invalid_plan_refuses_every_command_and_names_every_problem(self):
        """an invalid plan refuses every command and names every problem"""
        self.plan.write_text(PLAN.replace("## Satisfied by existing behaviour\n\n", "")
                             .replace("- Status: planned\n", "") + "\n## Satisfied by existing behaviour\n")
        before = self.plan.read_bytes()
        done = self.plan_cli("log", "started batch")
        self.assertEqual(done.returncode, 1)
        self.assertIn("section Satisfied by existing behaviour is out of order after Log", done.stderr)
        self.assertIn("slice 2: Status must be", done.stderr)
        self.assertEqual(self.plan.read_bytes(), before)

    def test_an_edit_that_would_break_the_plan_is_refused_with_every_problem_named(self):
        """an edit that would break the plan is refused with every problem named"""
        self.plan.write_text(PLAN.replace("## Satisfied", self.slice_blocks("3") + "## Satisfied"))
        before = self.plan.read_bytes()
        done = self.plan_cli("add-slice", "4", "Checkout", "--kind", "capability", "--check", "a check",
                             "--observable", "o")
        self.assertEqual(done.returncode, 1)
        problems = [line for line in done.stderr.splitlines() if "slice 4:" in line]
        self.assertEqual(len(problems), 2, done.stderr)
        self.assertTrue(any("needs Scenarios" in line for line in problems), problems)
        self.assertTrue(any("has Check, not Scenarios" in line for line in problems), problems)
        self.assertEqual(self.plan.read_bytes(), before)

    def test_a_section_plan_does_not_know_survives_an_edit_untouched(self):
        """a section plan does not know survives an edit untouched"""
        notes = "## Notes\nfree text the script does not own\n  - kept as written\n\n"
        self.plan.write_text(PLAN.replace("## Log\n", notes + "## Log\n"))
        done = self.plan_cli("log", "started batch")
        self.assertEqual(done.returncode, 0, done.stderr)
        text = self.plan.read_text()
        self.assertIn("- 2026-10-16 started batch\n", text)
        self.assertEqual(text.count(notes), 1)
        self.assertEqual(text.split("## Notes\n")[1].split("## Log\n")[0] + "", notes.split("## Notes\n")[1])

    def test_log_and_backlog_entries_are_appended_with_a_date(self):
        """log and backlog entries are appended with a date"""
        base = PLAN.replace("## Log\n- 2026-10-01 Suite: 3 passed, 1 failed at abc1234 in 12 s\n"
                            "- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built\n",
                            "## Backlog\n- 2026-09-01 earlier backlog entry\n\n"
                            "## Log\n- 2026-09-02 earlier log entry\n")
        rows = (("log", "Log", [], "2026-10-16"), ("log", "Log", ["--date", "2026-10-01"], "2026-10-01"),
                ("backlog", "Backlog", [], "2026-10-16"),
                ("backlog", "Backlog", ["--date", "2026-10-01"], "2026-10-01"))
        for command, section, option, date in rows:
            with self.subTest(command=command, option=option):
                self.plan.write_text(base)
                done = self.plan_cli(command, "check the totals", *option)
                self.assertEqual(done.returncode, 0, done.stderr)
                entries = [l for l in self.section_lines(self.plan.read_text(), section) if l.startswith("- ")]
                self.assertEqual(len(entries), 2)
                self.assertEqual(entries[-1], "- %s check the totals" % date)

    def test_a_missing_log_or_backlog_section_is_created_where_it_belongs(self):
        """a missing Log or Backlog section is created where it belongs"""
        rows = (("backlog", ["Satisfied by existing behaviour", "Log"]),
                ("log", ["Satisfied by existing behaviour", "Backlog"]))
        for command, present in rows:
            with self.subTest(command=command):
                text = PLAN.split("## Satisfied")[0]
                text += "".join("## %s\n- 2026-09-01 earlier\n\n" % name for name in present)
                self.plan.write_text(text)
                done = self.plan_cli(command, "check the totals")
                self.assertEqual(done.returncode, 0, done.stderr)
                after = re.findall(r"^## (?!Slice )(.+)$", self.plan.read_text(), re.M)
                self.assertEqual(after, ["Satisfied by existing behaviour", "Backlog", "Log"])

    def test_an_added_slice_goes_in_number_order_with_status_planned(self):
        """an added slice goes in number order with Status planned"""
        rows = ((["1", "2.9", "3"], "2.10", ["1", "2.9", "2.10", "3"]),
                (["1.1", "2"], "1", ["1", "1.1", "2"]), (["1", "3"], "2", ["1", "2", "3"]))
        for before, number, after in rows:
            with self.subTest(number=number):
                self.plan.write_text("# Cart slices\n\n" + self.slice_blocks(*before))
                done = self.plan_cli("add-slice", number, "Checkout", "--kind", "capability",
                                     "--scenarios", "cart / x", "--observable", "o")
                self.assertEqual(done.returncode, 0, done.stderr)
                text = self.plan.read_text()
                self.assertEqual(re.findall(r"^## Slice (\S+):", text, re.M), after)
                self.assertIn("- Status: planned", self.slice_lines(text, number))

    def test_adding_a_slice_that_does_not_fit_is_refused(self):
        """adding a slice that does not fit is refused"""
        before = self.plan.read_bytes()
        rows = (("3", ["--check", "a check"], "slice 3: a capability slice needs Scenarios"),
                ("2", ["--scenarios", "cart / x"], "slice 2 exists"))
        for number, given, reason in rows:
            with self.subTest(number=number):
                done = self.plan_cli("add-slice", number, "Checkout", "--kind", "capability", *given,
                                     "--observable", "o")
                self.assertEqual(done.returncode, 1)
                self.assertIn(reason, done.stderr)
                self.assertEqual(self.plan.read_bytes(), before)

    def test_adding_a_slice_with_or_without_a_lands_line(self):
        """adding a slice with or without a Lands line"""
        rows = (([], None), (["--lands", "3 production, 1 test"], "- Lands: 3 production, 1 test"))
        for option, line in rows:
            with self.subTest(option=option):
                self.plan.write_text(PLAN)
                done = self.plan_cli("add-slice", "3", "Checkout", "--kind", "capability",
                                     "--scenarios", "cart / x", "--observable", "o", *option)
                self.assertEqual(done.returncode, 0, done.stderr)
                lands = [l for l in self.slice_lines(self.plan.read_text(), "3") if l.startswith("- Lands")]
                if line is None:
                    self.assertEqual(lands, [])
                    self.assertIn("slice 3 has no Lands line", done.stderr)
                    self.assertIn("plan lands 3", done.stderr)
                else:
                    self.assertEqual(lands, [line])
                    self.assertEqual(done.stderr, "")

    def test_a_slice_over_the_module_budget_is_refused_whatever_the_command(self):
        """a slice over the module budget is refused whatever the command"""
        for production, test in ((9, 1), (3, 5)):
            with self.subTest(production=production, test=test):
                self.lands("%d production, %d test" % (production, test))
                before = self.plan.read_bytes()
                done = self.plan_cli("log", "started batch")
                self.assertEqual(done.returncode, 1)
                self.assertIn("slice 2: Lands %d production, %d test is over the budget of 8 production, 4 test"
                              % (production, test), done.stderr)
                self.assertEqual(self.plan.read_bytes(), before)

    def test_a_slice_with_a_badly_written_or_repeated_lands_line_is_refused(self):
        """a slice with a badly written or repeated Lands line is refused"""
        rows = (("- Lands: 2 production, 1 test\n- Lands: 3 production, 1 test", "slice 2: more than one Lands line"),
                ("- Lands: 2 prod, 1 tests", "slice 2: Lands must be"))
        for lines, problem in rows:
            with self.subTest(lines=lines):
                self.plan.write_text(PLAN.replace("- Status: planned", lines + "\n- Status: planned"))
                done = self.plan_cli("check")
                self.assertEqual(done.returncode, 1)
                self.assertIn(problem, done.stderr)

    def test_setting_a_slices_lands_line_replaces_any_it_had(self):
        """setting a slice's Lands line replaces any it had"""
        for had in (None, "1 production, 1 test"):
            with self.subTest(had=had):
                self.plan.write_text(PLAN if had is None else
                                     PLAN.replace("- Status: planned", "- Lands: %s\n- Status: planned" % had))
                done = self.plan_cli("lands", "2", "3 production, 2 test")
                self.assertEqual(done.returncode, 0, done.stderr)
                lands = [l for l in self.slice_lines(self.plan.read_text(), "2") if l.startswith("- Lands")]
                self.assertEqual(lands, ["- Lands: 3 production, 2 test"])

    def test_showing_open_slices_lists_every_slice_that_is_not_green(self):
        """showing open slices lists every slice that is not green"""
        self.plan.write_text("# Cart slices\n\n" + self.slice_blocks("1", "2", "3")
                             .replace("Cart 1", "Cart").replace("Cart 2", "Checkout").replace("Cart 3", "Refunds")
                             .replace("Status: planned", "Status: green", 1)
                             .replace("Status: planned", "Status: in progress", 1))
        done = self.plan_cli("show", "--open")
        self.assertEqual(done.returncode, 0, done.stderr)
        lines = done.stdout.splitlines()
        self.assertEqual(len(lines), 2, done.stdout)
        self.assertTrue("Checkout" in lines[0] and lines[0].endswith("in progress"), lines)
        self.assertTrue("Refunds" in lines[1] and lines[1].endswith("planned"), lines)
        self.assertNotIn("Cart", done.stdout)

    def test_showing_requests_lists_the_logs_request_entries(self):
        """showing requests lists the Log's REQUEST entries"""
        two = ("- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built\n"
               "- 2026-10-03 REQUEST shopsystem-cart: expose totals\n")
        other = "- 2026-10-04 slice 2 started\n"
        self.plan.write_text(PLAN.replace("- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built\n",
                                          two + other))
        done = self.plan_cli("show", "--requests")
        self.assertEqual((done.returncode, done.stdout), (0, two))

    def test_showing_the_last_suite_record_gives_the_logs_last_suite_entry(self):
        """showing the last suite record gives the Log's last Suite entry"""
        later = "- 2026-10-05 Suite: 9 passed, 0 failed at def5678 in 14 s\n"
        self.plan.write_text(PLAN + later)
        done = self.plan_cli("show", "--last-suite")
        self.assertEqual((done.returncode, done.stdout), (0, later))

    def test_the_current_flag_says_whether_the_last_suite_record_still_holds(self):
        """the current flag says whether the last suite record still holds"""
        tested = self.stamped({"code.txt": "one\n"})
        record = "- 2026-10-01 Suite: 3 passed, 1 failed at %s in 12 s" % tested
        rows = ((self.plan, "a change under docs/superpowers/plans/", "current", 0),
                (self.tmp / "code.txt", "a change outside it", "stale: ", 1))
        for path, label, verdict, status in rows:
            with self.subTest(change=label):
                path.write_text(path.read_text() + "changed\n")
                done = self.plan_cli("show", "--last-suite", "--current")
                lines = done.stdout.splitlines()
                self.assertEqual(lines[0], record)
                self.assertEqual(len(lines), 2, done.stdout)
                if status == 0:
                    self.assertEqual(lines[1], verdict)
                else:
                    self.assertTrue(lines[1].startswith(verdict) and len(lines[1]) > len(verdict), lines)
                self.assertEqual(done.returncode, status)

    def test_archiving_writes_the_green_slices_and_the_log_beside_the_plan_and_removes_those_slices(self):
        """archiving writes the green slices and the Log beside the plan and removes those slices"""
        text = ("# Foo slices\n\n" + self.slice_blocks("1", "2", "3").replace("Status: planned", "Status: green")
                .replace("Cart 2", "Cart two").replace("- Status: green\n\n## Slice 3", "- Status: planned\n\n## Slice 3")
                + "## Log\n- 2026-10-01 first\n- 2026-10-02 second\n- 2026-10-03 third\n")
        self.use("docs/superpowers/plans/foo-slices.md", text)
        done = self.plan_cli("archive", "batch-1")
        self.assertEqual(done.returncode, 0, done.stderr)
        archive = (self.plan.parent / "archive" / "foo-slices-batch-1.md").read_text()
        for n in ("1", "3"):
            self.assertIn("## Slice %s:" % n, archive)
        self.assertNotIn("## Slice 2:", archive)
        self.assertEqual([l for l in self.section_lines(archive, "Log") if l],
                         ["- 2026-10-01 first", "- 2026-10-02 second", "- 2026-10-03 third"])
        left = self.plan.read_text()
        self.assertIn("## Slice 2:", left)
        self.assertNotIn("## Slice 1:", left)
        self.assertNotIn("## Slice 3:", left)

    def test_archiving_leaves_the_log_holding_what_is_still_owed_and_the_suite_record(self):
        """archiving leaves the Log holding what is still owed and the suite record"""
        request = "- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built\n  needed by slice 53\n"
        reform = "- 2026-10-03 RE-FORMULATE cart / Adding several\n  evidence: red\n"
        question = "- 2026-10-03 QUESTION FOR THE SPEC: clamp or raise?\n  see r4\n"
        earlier = "- 2026-10-01 Suite: 3 passed, 1 failed at abc1234 in 12 s\n"
        later = "- 2026-10-05 Suite: 4 passed, 0 failed in 9 s\n"
        log = request + "- 2026-10-02 slice 1 green\n" + earlier + reform + "- 2026-10-04 noted\n" + question + later
        self.plan.write_text(PLAN.split("## Log\n")[0] + "## Log\n" + log)
        done = self.plan_cli("archive", "batch-1")
        self.assertEqual(done.returncode, 0, done.stderr)
        note = ("- 2026-10-16 Batch batch-1 archived to archive/cart-slices-batch-1.md; last "
                + later[2:])
        self.assertEqual("\n".join(self.section_lines(self.plan.read_text(), "Log")).strip() + "\n",
                         request + reform + question + note + later)
        shown = self.plan_cli("show", "--last-suite", "--current")
        self.assertEqual(shown.stdout.splitlines()[0], later.rstrip("\n"))

    def test_archiving_is_refused_when_the_archive_exists_or_nothing_is_green(self):
        """archiving is refused when the archive exists or nothing is green"""
        rows = (("a green slice, whose archive for batch-1 already exists", True, "exists"),
                ("no green slice", False, "no green slice"))
        for state, green, reason in rows:
            with self.subTest(state=state):
                self.plan.write_text(PLAN if green else PLAN.replace("- Status: green", "- Status: planned"))
                archive = self.plan.parent / "archive"
                if green:
                    archive.mkdir(exist_ok=True)
                    (archive / "cart-slices-batch-1.md").write_text("already here\n")
                done = self.plan_cli("archive", "batch-1")
                self.assertEqual(done.returncode, 1)
                self.assertIn(reason, done.stderr)

    def test_plan_works_on_the_named_file_or_the_one_plan_in_the_current_directory(self):
        """plan works on the named file or the one plan in the current directory"""
        mine, other = "docs/superpowers/plans/2026-10-01-cart-slices.md", "other/2026-10-02-refunds-slices.md"
        for file_option, target, untouched in (([], mine, other), (["--file", other], other, mine)):
            with self.subTest(target=target):
                self.use(mine, PLAN)
                (self.tmp / other).parent.mkdir(exist_ok=True)
                (self.tmp / other).write_text(PLAN)
                done = self.plan_cli(*file_option, "log", "started batch")
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertTrue((self.tmp / target).read_text().endswith("- 2026-10-16 started batch\n"))
                self.assertEqual((self.tmp / untouched).read_text(), PLAN)

    def test_without_file_no_plan_or_several_plans_is_refused(self):
        """without --file, no plan or several plans is refused"""
        for count in (0, 2):
            with self.subTest(count=count):
                for old in self.plan.parent.glob("*.md"):
                    old.unlink()
                for i in range(count):
                    (self.plan.parent / ("p%d-slices.md" % i)).write_text(PLAN)
                done = self.plan_cli("check")
                self.assertEqual(done.returncode, 1)
                self.assertIn("found %d" % count, done.stderr)
                self.assertIn("--file", done.stderr)

    def test_a_plan_file_that_cannot_be_read_is_refused(self):
        """a plan file that cannot be read is refused"""
        done = self.plan_cli("--file", "missing/none-slices.md", "check")
        self.assertEqual(done.returncode, 1)
        self.assertIn("cannot read missing/none-slices.md", done.stderr)

    def test_showing_the_backlog_prints_each_entry_with_its_continuation_lines(self):
        """showing the backlog prints each entry with its continuation lines"""
        entries = "- 2026-09-01 slow lookup\n  on ten thousand items\n  seen twice\n- 2026-09-02 odd total\n"
        rows = (("with two entries", PLAN.replace("## Log", "## Backlog\n" + entries + "\n## Log"), entries),
                ("empty", PLAN.replace("## Log", "## Backlog\n\n## Log"), ""), ("missing", PLAN, ""))
        for label, text, output in rows:
            with self.subTest(backlog=label):
                self.plan.write_text(text)
                done = self.plan_cli("show", "--backlog")
                self.assertEqual((done.returncode, done.stdout), (0, output))

    def test_showing_requests_or_the_last_suite_record_keeps_continuation_lines(self):
        """showing requests or the last suite record keeps continuation lines"""
        request = "- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built\n  needed by slice 53\n  and 54\n"
        suite = "- 2026-10-01 Suite: 3 passed, 1 failed at abc1234 in 12 s\n  slow: cart 4 s\n  flaky: none\n"
        self.plan.write_text(PLAN.split("## Log\n")[0] + "## Log\n" + suite + request)
        for option, entry in (("--requests", request), ("--last-suite", suite)):
            with self.subTest(option=option):
                done = self.plan_cli("show", option)
                self.assertEqual((done.returncode, done.stdout), (0, entry))

    def test_a_log_with_no_suite_record(self):
        """a Log with no suite record"""
        self.plan.write_text(PLAN.replace("- 2026-10-01 Suite: 3 passed, 1 failed at abc1234 in 12 s\n", ""))
        plain = self.plan_cli("show", "--last-suite")
        self.assertEqual((plain.returncode, plain.stdout), (0, ""))
        current = self.plan_cli("show", "--last-suite", "--current")
        self.assertEqual(current.returncode, 1)
        self.assertIn("no suite record", current.stderr)

    def test_a_suite_record_naming_no_commit_is_stale(self):
        """a suite record naming no commit is stale"""
        self.plan.write_text(PLAN.replace(" at abc1234", ""))
        done = self.plan_cli("show", "--last-suite", "--current")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stdout.splitlines()[-1], "stale: the record names no commit")

    def test_the_stale_reason_counts_and_names_every_changed_file(self):
        """the stale reason counts and names every changed file"""
        tested = self.stamped({"src/cart.py": "one\n", "src/checkout.py": "one\n"})
        (self.tmp / "src/cart.py").write_text("two\n")
        self.git("commit", "-qam", "change cart")
        (self.tmp / "src/checkout.py").write_text("two\n")
        done = self.plan_cli("show", "--last-suite", "--current")
        self.assertEqual(done.stdout.splitlines()[-1],
                         "stale: 2 files changed since %s: src/cart.py, src/checkout.py" % tested)

    def test_setting_the_lands_line_of_a_slice_the_plan_does_not_have_is_refused(self):
        """setting the Lands line of a slice the plan does not have is refused"""
        before = self.plan.read_bytes()
        done = self.plan_cli("lands", "7", "2 production, 1 test")
        self.assertEqual(done.returncode, 1)
        self.assertIn("no slice 7", done.stderr)
        self.assertEqual(self.plan.read_bytes(), before)

    def test_a_green_status_with_a_note_counts_as_green(self):
        """a green status with a note counts as green"""
        text = PLAN.replace("Add a product", "Cart").replace("Several products", "Checkout") \
                   .replace("- Status: green", "- Status: green: merged early")
        for command in (["show", "--open"], ["archive", "batch-1"]):
            with self.subTest(command=command[0]):
                self.plan.write_text(text)
                done = self.plan_cli(*command)
                self.assertEqual(done.returncode, 0, done.stderr)
                if command[0] == "show":
                    self.assertEqual(done.stdout, "2 Checkout: planned\n")
                else:
                    archive = (self.plan.parent / "archive" / "cart-slices-batch-1.md").read_text()
                    self.assertIn("## Slice 1: Cart", archive)
                    self.assertNotIn("## Slice 1:", self.plan.read_text())
                    self.assertIn("## Slice 2:", self.plan.read_text())

    def test_archiving_creates_the_archive_directory_and_starts_the_file_with_the_plans_title(self):
        """archiving creates the archive directory and starts the file with the plan's title"""
        self.assertFalse((self.plan.parent / "archive").exists())
        done = self.plan_cli("archive", "batch-1")
        self.assertEqual(done.returncode, 0, done.stderr)
        archive = self.plan.parent / "archive"
        self.assertTrue(archive.is_dir())
        self.assertTrue((archive / "cart-slices-batch-1.md").read_text().startswith("# Cart slices\n"))

    def test_the_logs_archive_line_carries_the_given_date_or_todays(self):
        """the Log's archive line carries the given date or today's"""
        for option, date in (([], "2026-10-16"), (["--date", "2026-10-01"], "2026-10-01")):
            with self.subTest(option=option):
                self.plan.write_text(PLAN)
                done = self.plan_cli("archive", "batch-1", *option)
                self.assertEqual(done.returncode, 0, done.stderr)
                line = [l for l in self.section_lines(self.plan.read_text(), "Log")
                        if "archive/cart-slices-batch-1.md" in l]
                self.assertEqual(len(line), 1)
                self.assertTrue(line[0].startswith("- %s " % date), line)
                shutil.rmtree(self.plan.parent / "archive")

    def test_a_refused_command_says_why_on_stderr_and_exits_1(self):
        """a refused command says why on stderr and exits 1"""
        done = self.plan_cli("status", "7", "green")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stderr, "plan: no slice 7\n")


if __name__ == "__main__":
    unittest.main()
