import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "features"

CART = '''# formulated from spec/capabilities/cart.md
@cart
Feature: Cart
  Narrator: a shopper

  Background:
    Given an empty cart

  @slice-1
  Scenario: Adding a product
    When the shopper adds a "pen"
    Then the cart holds 1 item

  @slice-2 @wip
  Scenario Outline: Adding several
    When the shopper adds <n> pens
    Then the cart holds <n> items

    Examples:
      | n |
      | 2 |
      | 3 |

    @slow
    Examples:
      | n  |
      | 10 |

  Scenario: A note that mentions keywords
    Given a note
      """
      Scenario: not a scenario
      @slice-9
      """
    Then nothing happens
'''


class FeaturesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        (self.tmp / "features").mkdir()
        self.cart = self.tmp / "features" / "cart.feature"
        self.cart.write_text(CART)

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.tmp,
                              capture_output=True, text=True)

    def test_count_by_tag_counts_outline_rows_and_inherits_tags(self):
        done = self.run_script("count", "--by-tag")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout, "cart 5\nslice-1 1\nslice-2 3\nslow 1\nwip 3\ntotal 5\n")

    def test_docstring_text_is_not_a_scenario_or_tag(self):
        done = self.run_script("list", "--tag", "slice-9")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stdout, "")

    def test_list_by_tag(self):
        done = self.run_script("list", "--tag", "@slice-2")
        self.assertEqual(done.stdout, "features/cart.feature: Adding several\n")

    def test_list_by_title(self):
        done = self.run_script("list", "--title", "note")
        self.assertEqual(done.stdout, "features/cart.feature: A note that mentions keywords\n")

    def test_tag_replaces_slice_tag_and_nothing_else(self):
        done = self.run_script("tag", "Adding a product", "slice-3")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.cart.read_text(), CART.replace("  @slice-1\n", "  @slice-3\n"))

    def test_tag_keeps_other_tags(self):
        self.run_script("tag", "Adding several", "slice-5.1")
        self.assertEqual(self.cart.read_text(), CART.replace("  @slice-2 @wip\n", "  @slice-5.1 @wip\n"))

    def test_tag_adds_a_tag_line_where_there_is_none(self):
        self.run_script("tag", "A note that mentions keywords", "slice-4")
        self.assertEqual(self.cart.read_text(), CART.replace(
            "  Scenario: A note that mentions keywords\n",
            "  @slice-4\n  Scenario: A note that mentions keywords\n"))

    def test_tag_refuses_an_unknown_title(self):
        done = self.run_script("tag", "Removing a product", "slice-3")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(self.cart.read_text(), CART)

    def test_tag_refuses_a_title_in_two_files(self):
        other = self.tmp / "features" / "other.feature"
        other.write_text("Feature: Other\n\n  Scenario: Adding a product\n    Given x\n")
        done = self.run_script("tag", "Adding a product", "slice-3")
        self.assertEqual(done.returncode, 1)
        self.assertIn("cart.feature", done.stderr)
        self.assertIn("other.feature", done.stderr)
        self.assertEqual(self.cart.read_text(), CART)

    def test_tag_rejects_a_malformed_slice(self):
        self.assertEqual(self.run_script("tag", "Adding a product", "3").returncode, 2)

    def test_tag_sets_a_requirement_tag_and_keeps_slice_tags(self):
        done = self.run_script("tag", "Adding a product", "r4")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.cart.read_text(), CART.replace("  @slice-1\n", "  @slice-1 @r4\n"))

    def test_tag_replaces_a_requirement_tag(self):
        self.run_script("tag", "Adding a product", "r4")
        self.run_script("tag", "Adding a product", "r7")
        self.assertEqual(self.cart.read_text(), CART.replace("  @slice-1\n", "  @slice-1 @r7\n"))

    def test_tag_rejects_a_three_part_slice(self):
        self.assertEqual(self.run_script("tag", "Adding a product", "slice-1.2.3").returncode, 2)
        self.assertEqual(self.cart.read_text(), CART)

    def _before_and_checkout(self, header="@cart\nFeature: Checkout\n  Narrator: a shopper\n"):
        shutil.copytree(self.tmp / "features", self.tmp / "before")
        checkout = self.tmp / "features" / "checkout.feature"
        checkout.write_text(header)
        return checkout

    def test_move_with_background_inlined_verifies(self):
        checkout = self._before_and_checkout()
        done = self.run_script("move", "Adding a product", "--to", "features/checkout.feature",
                               "--inline-background")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn('    Given an empty cart\n    When the shopper adds a "pen"\n', checkout.read_text())
        self.assertNotIn("Adding a product", self.cart.read_text())
        done = self.run_script("verify-moved", "--from", "before")
        self.assertEqual((done.returncode, done.stdout), (0, "3 scenarios match\n"))

    def test_verify_catches_a_lost_background(self):
        self._before_and_checkout()
        self.run_script("move", "Adding a product", "--to", "features/checkout.feature")
        done = self.run_script("verify-moved", "--from", "before")
        self.assertEqual(done.returncode, 1)
        self.assertIn("changed: Adding a product (steps)", done.stdout)

    def test_verify_catches_a_lost_feature_tag(self):
        self._before_and_checkout(header="Feature: Checkout\n  Narrator: a shopper\n")
        self.run_script("move", "Adding a product", "--to", "features/checkout.feature",
                        "--inline-background")
        done = self.run_script("verify-moved", "--from", "before")
        self.assertEqual(done.returncode, 1)
        self.assertIn("changed: Adding a product (tags)", done.stdout)

    def test_move_keeping_feature_tags_verifies(self):
        checkout = self._before_and_checkout(header="Feature: Checkout\n  Narrator: a shopper\n")
        done = self.run_script("move", "Adding a product", "--to", "features/checkout.feature",
                               "--inline-background", "--keep-feature-tags")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("  @slice-1\n  @cart\n  Scenario: Adding a product\n", checkout.read_text())
        done = self.run_script("verify-moved", "--from", "before")
        self.assertEqual((done.returncode, done.stdout), (0, "3 scenarios match\n"))

    def test_verify_catches_a_changed_step(self):
        shutil.copytree(self.tmp / "features", self.tmp / "before")
        self.cart.write_text(CART.replace("holds 1 item", "holds one item"))
        done = self.run_script("verify-moved", "--from", "before")
        self.assertEqual(done.returncode, 1)
        self.assertIn("changed: Adding a product (steps)", done.stdout)

    def test_verify_catches_a_duplicate_title(self):
        shutil.copytree(self.tmp / "features", self.tmp / "before")
        (self.tmp / "features" / "other.feature").write_text(
            "Feature: Other\n\n  Scenario: Adding a product\n    Given x\n")
        done = self.run_script("verify-moved", "--from", "before")
        self.assertEqual(done.returncode, 1)
        self.assertIn("duplicate title after: Adding a product", done.stdout)


SHELF = """# formulated from spec/capabilities/shelf.md
Feature: Shelf
  Narrator: a reader

  @slice-1
  Scenario: A book is added
    One book on the shelf.
    When the reader adds "dune"
    Then the shelf holds 1 book

  @slice-4
  Scenario: A book is added at a place
    When the reader adds "dune" at place 2
    Then the shelf holds "dune" at place 2

  Scenario: A book is lent
    When the reader lends "dune"
    Then the shelf holds 0 books
"""

BOUND = """from pytest_bdd import scenario, scenarios
import pytest_bdd

FEATURE = "shelf.feature"


@scenario(FEATURE, "A book is added")
def test_added():
    pass


@pytest_bdd.scenario("shelf.feature", 'A book is lent')
def test_lent():
    pass


def test_plain():
    assert "A book is added" == "A book is added"
"""


class HoldingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        (self.tmp / "features").mkdir()
        (self.tmp / "tests").mkdir()
        self.shelf = self.tmp / "features" / "shelf.feature"
        self.shelf.write_text(SHELF)
        self.bound = self.tmp / "tests" / "test_shelf.py"
        self.bound.write_text(BOUND)

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.tmp, capture_output=True, text=True)

    def test_hold_marks_a_scenario_and_changes_nothing_else_in_it(self):
        done = self.run_script("hold", "A book is added", "--for", "A book is added at a place")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.shelf.read_text(), SHELF.replace(
            "  @slice-1\n  Scenario: A book is added\n",
            "  @slice-1 @holding\n  Scenario: A book is added (held)\n    Held for: A book is added at a place\n"))

    def test_hold_for_removal_on_a_scenario_with_no_tags(self):
        done = self.run_script("hold", "A book is lent", "--for-removal")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("  @holding\n  Scenario: A book is lent (held)\n    Held for: removal\n    When the reader lends",
                      self.shelf.read_text())

    def test_hold_refuses_a_scenario_held_already_and_shows_a_replacement_not_written(self):
        self.run_script("hold", "A book is lent", "--for-removal")
        self.assertEqual(self.run_script("hold", "A book is lent (held)", "--for-removal").returncode, 1)
        self.assertEqual(self.run_script("hold", "A book is added", "--for", "A book is added").returncode, 0)
        self.assertIn("A book is added (held) | for: A book is added | no scenario has that title",
                      self.run_script("holding").stdout)

    def test_holding_lists_each_with_its_replacements_slice(self):
        self.run_script("hold", "A book is added", "--for", "A book is added at a place")
        self.run_script("hold", "A book is lent", "--for-removal")
        done = self.run_script("holding")
        self.assertEqual(done.stdout, (
            "features/shelf.feature: A book is added (held) | for: A book is added at a place | slice-4\n"
            "features/shelf.feature: A book is lent (held) | for: removal | the slice that removes the behaviour\n"))
        self.shelf.write_text(SHELF)
        self.assertEqual(self.run_script("holding").stdout, "none held\n")

    def test_retire_removes_a_held_scenario_only(self):
        self.run_script("hold", "A book is added", "--for", "A book is added at a place")
        done = self.run_script("retire", "A book is added (held)")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.shelf.read_text(), SHELF.replace(
            "  @slice-1\n  Scenario: A book is added\n    One book on the shelf.\n    When the reader adds \"dune\"\n    Then the shelf holds 1 book\n\n", ""))
        before = self.shelf.read_text()
        done = self.run_script("retire", "A book is lent")
        self.assertEqual(done.returncode, 1)
        self.assertIn("not tagged @holding", done.stderr)
        self.assertEqual(self.shelf.read_text(), before)

    def test_retire_the_last_scenario_leaves_the_file_ending_in_one_newline(self):
        self.run_script("hold", "A book is lent", "--for-removal")
        self.run_script("retire", "A book is lent (held)")
        self.assertTrue(self.shelf.read_text().endswith('Then the shelf holds "dune" at place 2\n'))

    def test_bindings_names_each_binding_whose_title_is_gone(self):
        self.assertEqual(self.run_script("bindings").stdout, "every binding names a scenario\n")
        self.run_script("hold", "A book is added", "--for", "A book is added at a place")
        done = self.run_script("bindings")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stdout, 'tests/test_shelf.py:7: no scenario titled "A book is added" in shelf.feature\n')

    def test_bindings_checks_the_feature_a_binding_names(self):
        (self.tmp / "features" / "other.feature").write_text("Feature: Other\n\n  Scenario: Elsewhere\n    When x\n")
        self.bound.write_text('from pytest_bdd import scenario\n\n\n@scenario("shelf.feature", "Elsewhere")\ndef test_x():\n    pass\n')
        done = self.run_script("bindings")
        self.assertEqual(done.returncode, 1)
        self.assertIn('no scenario titled "Elsewhere" in shelf.feature', done.stdout)

    def test_rebind_rewrites_the_title_in_the_call_and_nothing_else(self):
        self.run_script("hold", "A book is added", "--for", "A book is added at a place")
        done = self.run_script("rebind", "A book is added", "A book is added (held)")
        self.assertEqual((done.returncode, done.stdout), (0, "1 binding rebound\n"), done.stderr)
        self.assertEqual(self.bound.read_text(), BOUND.replace(
            '@scenario(FEATURE, "A book is added")', '@scenario(FEATURE, "A book is added (held)")'))
        self.assertEqual(self.run_script("bindings").returncode, 0)

    def test_rebind_refuses_a_title_no_feature_has_and_says_when_nothing_names_the_old_one(self):
        done = self.run_script("rebind", "A book is added", "Nothing by this name")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(self.bound.read_text(), BOUND)
        done = self.run_script("rebind", "A book is added at a place", "A book is lent")
        self.assertEqual((done.returncode, done.stdout), (0, "0 bindings rebound\n"))


PLAN = """# shelf slices

## Slice 1: Added
- Kind: capability
- Scenarios: shelf / A book is added
- Status: green

## Slice 4: Placed
- Kind: capability
- Scenarios: shelf / A book is added at a place
- Status: planned

## Slice 4.1: Lent
- Kind: capability
- Scenarios: shelf / A book is lent
- Status: blocked: awaiting the spec

## Slice 5: Counted
- Kind: capability
- Scenarios: shelf / Counted
- Status: in progress

## Log
"""

TESTS = """import pytest


def marked(name):
    return getattr(pytest.mark, name)


@marked("slice-1")
def test_built():
    assert True


@marked("slice-4")
def test_waiting():
    assert False


@marked("slice-4.1")
def test_blocked_and_early():
    assert True


@marked("slice-5")
def test_in_progress():
    assert False


@marked("slice-3")
def test_archived():
    assert True


def test_untagged():
    assert True
"""


class SliceExpectationsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        plans = self.tmp / "docs" / "superpowers" / "plans"
        plans.mkdir(parents=True)
        (plans / "shelf-slices.md").write_text(PLAN)
        (self.tmp / "test_shelf.py").write_text(TESTS)
        (self.tmp / "pytest.ini").write_text("[pytest]\nmarkers =\n" + "".join(
            "    slice-%s\n" % n for n in ("1", "3", "4", "4.1", "5")))
        done = subprocess.run([sys.executable, str(SCRIPT), "plugin", "."], cwd=self.tmp, capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("  from slice_expectations import *", done.stdout)
        (self.tmp / "conftest.py").write_text("from slice_expectations import *  # noqa: F401,F403\n")

    def pytest(self, *args):
        return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args],
                              cwd=self.tmp, capture_output=True, text=True).stdout

    def test_a_planned_slice_is_expected_and_an_early_pass_fails(self):
        out = self.pytest("-rxf")
        self.assertIn("XFAIL test_shelf.py::test_waiting - slice 4 is planned", out)
        self.assertIn("FAILED test_shelf.py::test_blocked_and_early", out)
        self.assertIn("[XPASS(strict)] slice 4.1 is blocked", out)
        self.assertIn("FAILED test_shelf.py::test_in_progress", out)
        self.assertIn("slices: 2 expected to fail, of slice 4, 4.1", out)
        self.assertIn("2 failed, 3 passed, 1 xfailed", out)

    def test_the_slice_being_built_is_run_as_it_is(self):
        out = self.pytest("--slice", "4", "--slice", "slice-4.1", "-rxf")
        self.assertIn("FAILED test_shelf.py::test_waiting", out)
        self.assertIn("2 failed, 4 passed", out)
        self.assertNotIn("expected to fail", out)

    def test_no_plan_expects_nothing(self):
        (self.tmp / "docs" / "superpowers" / "plans" / "shelf-slices.md").unlink()
        out = self.pytest()
        self.assertIn("slices: no one living plan found", out)
        self.assertIn("2 failed, 4 passed", out)


def feature(*scenarios, tags="", background=""):
    head = "%sFeature: Cart\n  Narrator: a shopper\n\n" % (tags + "\n" if tags else "")
    return head + background + "\n".join(scenarios)


def scenario(title, tags="", body="    Given a step\n", kind="Scenario"):
    return "%s  %s: %s\n%s" % ("  %s\n" % tags if tags else "", kind, title, body)


NOTE_WITH = '    Given a note\n      """\n      %s\n      """\n'


class Workspace:
    """A scratch directory `features` runs in, shared by the scenario tests that run it on files."""

    def setUp(self):
        self.fresh()

    def fresh(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def write(self, name, text):
        path = self.tmp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def everything(self):
        return {str(p.relative_to(self.tmp)): p.read_text() for p in sorted(self.tmp.rglob("*")) if p.is_file()}

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.tmp, capture_output=True, text=True)

    def refused(self, *args):
        """Run an edit that must be refused: exit 1, a reason on stderr, every file as it was."""
        before = self.everything()
        done = self.run_script(*args)
        self.assertEqual(done.returncode, 1, done.stdout + done.stderr)
        self.assertEqual(done.stdout, "")
        self.assertEqual(self.everything(), before)
        return done.stderr


class ScenarioTest(Workspace, unittest.TestCase):
    """The feature-file-tools scenarios that run `features` on feature files."""

    def test_retagging_replaces_the_first_slice_tag_and_drops_the_others(self):
        """retagging replaces the first slice tag and drops the others"""
        text = feature(scenario("Apply a code", "@wip @slice-1 @slice-2 @r3"))
        path = self.write("features/cart.feature", text)
        done = self.run_script("tag", "Apply a code", "slice-4")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(path.read_text(), text.replace("@wip @slice-1 @slice-2 @r3", "@wip @slice-4 @r3"))

    def test_a_scenario_without_a_slice_tag_gets_one(self):
        """a scenario without a slice tag gets one"""
        for before, after in (("  @wip\n", "  @wip @slice-2\n"),
                              ("  @wip\n  @r1\n", "  @wip\n  @r1 @slice-2\n"),
                              ("", "  @slice-2\n")):
            with self.subTest(before=before):
                template = feature("%s  Scenario: Apply a code\n    Given a step\n")
                path = self.write("features/cart.feature", template % before)
                done = self.run_script("tag", "Apply a code", "slice-2")
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(path.read_text(), template % after)

    def test_holding_a_scenario_marks_it_held_and_records_what_for(self):
        """holding a scenario marks it held and records what for"""
        plain = scenario("Apply a code", body="    When a code is applied\n    Then the total drops\n")
        voucher = scenario("Apply a voucher")
        for replacement, option, held_for in (
                (True, ("--for", "Apply a voucher"), "Apply a voucher"),
                (False, ("--for", "Apply a voucher"), "Apply a voucher"),
                (False, ("--for-removal",), "removal")):
            with self.subTest(option=option, replacement=replacement):
                path = self.write("features/cart.feature", feature(plain, voucher) if replacement else feature(plain))
                before = path.read_text()
                done = self.run_script("hold", "Apply a code", *option)
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(path.read_text(), before.replace(
                    "  Scenario: Apply a code\n",
                    "  @holding\n  Scenario: Apply a code (held)\n    Held for: %s\n" % held_for))

    def test_holding_a_scenario_already_held_is_refused(self):
        """holding a scenario already held is refused"""
        self.write("features/cart.feature", feature(scenario(
            "Apply a code (held)", "@holding", "    Held for: removal\n    Given a step\n")))
        reason = self.refused("hold", "Apply a code (held)", "--for", "Apply a voucher")
        self.assertIn("held already", reason)

    def test_the_holding_list_shows_each_held_scenario_and_what_will_retire_it(self):
        """the holding list shows each held scenario and what will retire it"""
        voucher = scenario("Apply a voucher", "@slice-3")
        for held_for, others, shown in (
                ("Apply a voucher", [voucher], "slice-3"),
                ("Apply a voucher", [], "no scenario has that title"),
                ("removal", [], "the slice that removes the behaviour")):
            with self.subTest(held_for):
                self.write("features/cart.feature", feature(
                    scenario("Apply a code (held)", "@holding", "    Held for: %s\n    Given a step\n" % held_for), *others))
                done = self.run_script("holding")
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(done.stdout, "features/cart.feature: Apply a code (held) | for: %s | %s\n" % (held_for, shown))

    def test_the_holding_list_says_when_nothing_is_held(self):
        """the holding list says when nothing is held"""
        self.write("features/cart.feature", feature(scenario("Apply a code", "@slice-1")))
        done = self.run_script("holding")
        self.assertEqual((done.returncode, done.stdout), (0, "none held\n"))

    def test_retiring_a_held_scenario_removes_its_block(self):
        """retiring a held scenario removes its block"""
        held = scenario("Apply a code (held)", "@holding", "    Held for: removal\n    Given a step\n")
        rest = [scenario("Empty cart"), scenario("Checkout")]
        path = self.write("features/cart.feature", feature(rest[0], held, rest[1]))
        done = self.run_script("retire", "Apply a code (held)")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(path.read_text(), feature(*rest))

    def test_retiring_a_scenario_that_is_not_held_is_refused(self):
        """retiring a scenario that is not held is refused"""
        self.write("features/cart.feature", feature(scenario("Apply a code", "@slice-1")))
        self.assertIn("not tagged @holding", self.refused("retire", "Apply a code"))

    def test_moving_a_title_that_no_file_or_several_files_hold_is_refused(self):
        """moving a title that no file or several files hold is refused"""
        for holders, says, named in (([], "no scenario titled 'Apply a code'", []),
                                     (["cart", "old"], "several", ["features/cart.feature", "features/old.feature"])):
            with self.subTest(holders):
                self.fresh()
                self.write("features/codes.feature", feature(scenario("Empty cart")))
                for name in holders:
                    self.write("features/%s.feature" % name, feature(scenario("Apply a code")))
                reason = self.refused("move", "Apply a code", "--to", "features/codes.feature")
                self.assertIn(says, reason)
                self.assertEqual(re.findall(r"features/\w+\.feature", reason), named)
                if named:
                    self.assertIn(", ".join(named), reason)

    def test_holding_a_scenario_prints_its_file_and_new_title(self):
        """holding a scenario prints its file and new title"""
        self.write("features/cart.feature", feature(scenario("Apply a code")))
        done = self.run_script("hold", "Apply a code", "--for-removal")
        self.assertEqual((done.returncode, done.stdout), (0, "features/cart.feature: Apply a code (held)\n"), done.stderr)

    def test_the_holding_list_flags_a_held_scenario_it_cannot_place(self):
        """the holding list flags a held scenario it cannot place"""
        for body, others, said in (
                ("    Given a step\n", [], "no 'Held for:' line"),
                ("    Held for: Apply a voucher\n    Given a step\n", [scenario("Apply a voucher")], "no slice yet")):
            with self.subTest(said):
                self.write("features/cart.feature", feature(scenario("Apply a code (held)", "@holding", body), *others))
                done = self.run_script("holding")
                self.assertEqual(done.returncode, 0, done.stderr)
                lines = [x for x in done.stdout.splitlines() if "Apply a code (held)" in x]
                self.assertEqual(len(lines), 1)
                self.assertTrue(lines[0].endswith("| " + said), lines[0])


def binding(title, feature_name="cart.feature", line=12):
    pad = "".join("# filler\n" for _ in range(line - 2))
    return 'from pytest_bdd import scenario\n%s@scenario("%s", "%s")\ndef test_x():\n    pass\n' % (pad, feature_name, title)


class BindingsScenarioTest(Workspace, unittest.TestCase):
    """The feature-file-tools scenarios about test-module bindings."""

    def test_rebind_with_file_takes_a_new_title_that_several_feature_files_hold(self):
        """rebind --file follows only its own file when both files hold the new title"""
        self.write("features/cart.feature", feature(scenario("Apply a code")))
        self.write("features/old.feature", feature(scenario("Apply a code")))
        modules = {"tests/test_cart.py": binding("Apply a code", "cart.feature"),
                   "tests/test_old.py": binding("Apply a code", "old.feature")}
        for name, text in modules.items():
            self.write(name, text)
        for name in ("cart", "old"):
            done = self.run_script("hold", "Apply a code", "--for-removal", "--file", "features/%s.feature" % name)
            self.assertEqual(done.returncode, 0, done.stderr)
        for name in ("cart", "old"):
            done = self.run_script("rebind", "Apply a code", "Apply a code (held)", "--file", "features/%s.feature" % name)
            self.assertEqual((done.returncode, done.stdout), (0, "1 binding rebound\n"), done.stderr)
            moved = [m for m in modules if '"Apply a code (held)")' in (self.tmp / m).read_text()]
            self.assertEqual(moved, ["tests/test_cart.py"] if name == "cart" else list(modules))
        self.assertEqual(self.run_script("bindings").returncode, 0)


class PluginCommandTest(Workspace, unittest.TestCase):
    """The feature-file-tools scenarios about `features plugin`."""

    def test_the_plugin_is_written_into_the_directory_with_its_registration_line(self):
        """the plugin is written into the directory with its registration line"""
        (self.tmp / "tests").mkdir()
        done = self.run_script("plugin", "tests")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual((self.tmp / "tests" / "slice_expectations.py").read_text(),
                         (ROOT / "scripts" / "slice_expectations.py").read_text())
        self.assertIn("conftest.py", done.stdout)
        self.assertIn("\n  from slice_expectations import *", done.stdout)

    def test_writing_the_plugin_to_a_path_that_is_not_a_directory_is_refused(self):
        """writing the plugin to a path that is not a directory is refused"""
        self.write("tests/notes.txt", "notes\n")
        self.assertIn("tests/notes.txt is not a directory", self.refused("plugin", "tests/notes.txt"))

    def test_writing_the_plugin_replaces_an_existing_one_and_reads_no_feature_file(self):
        """writing the plugin replaces an existing one and reads no feature file"""
        self.write("tests/slice_expectations.py", "# an older plugin\n")
        self.write("features/rules.feature", "Feature: Rules\n\n  Rule: a rule\n\n    Scenario: Inside\n      Given a step\n")
        done = self.run_script("plugin", "tests")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual((self.tmp / "tests" / "slice_expectations.py").read_text(),
                         (ROOT / "scripts" / "slice_expectations.py").read_text())

    def test_the_registration_line_for_a_package_imports_relatively(self):
        """the registration line for a package imports relatively"""
        self.write("tests/__init__.py", "")
        done = self.run_script("plugin", "tests")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("\n  from .slice_expectations import *", done.stdout)
        self.assertNotIn("from slice_expectations", done.stdout)


def plan_text(**statuses):
    return "# slices\n\n" + "".join(
        "## Slice %s: S\n- Kind: capability\n- Scenarios: cart / S\n- Status: %s\n\n" % (n, s)
        for n, s in statuses.items()) + "## Log\n"


class PluginRunScenarioTest(unittest.TestCase):
    """The feature-file-tools scenarios that run pytest with slice_expectations.py registered."""

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.ini = ""
        self.set_ini()
        done = subprocess.run([sys.executable, str(SCRIPT), "plugin", "."], cwd=self.tmp, capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        (self.tmp / "conftest.py").write_text("from slice_expectations import *  # noqa: F401,F403\n")
        (self.tmp / "docs" / "superpowers" / "plans").mkdir(parents=True)

    def set_ini(self, slice_plan=None):
        (self.tmp / "pytest.ini").write_text("[pytest]\nmarkers =\n    slice-2\n    slice-3\n"
                                             + ("slice_plan = %s\n" % slice_plan if slice_plan else ""))

    def write(self, name, text):
        path = self.tmp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def plan(self, name="2026-10-01-slices.md", **statuses):
        self.write("docs/superpowers/plans/" + name, plan_text(**statuses))

    def tests(self, **results):
        """One test per slice, named test_slice_<n>, tagged @slice-<n>, passing or failing."""
        body = "import pytest\n\n\n"
        for n, passes in results.items():
            body += '@getattr(pytest.mark, "slice-%s")\ndef test_%s():\n    assert %s\n\n\n' % (n[1:], n, passes)
        self.write("test_slices.py", body)

    def pytest(self, *args):
        return subprocess.run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-rxf", *args],
                              cwd=self.tmp, capture_output=True, text=True)

    def test_a_test_of_a_planned_or_blocked_slice_is_expected_to_fail(self):
        """a test of a planned or blocked slice is expected to fail"""
        for status in ("planned", "blocked"):
            for passes in (False, True):
                with self.subTest(status=status, passes=passes):
                    self.plan(**{"2": status})
                    self.tests(s2=passes)
                    done = self.pytest()
                    if passes:
                        self.assertIn("FAILED test_slices.py::test_s2 - [XPASS(strict)] slice 2 is %s" % status, done.stdout)
                        self.assertEqual(done.returncode, 1)
                    else:
                        self.assertIn("XFAIL test_slices.py::test_s2 - slice 2 is %s" % status, done.stdout)
                        self.assertEqual(done.returncode, 0, done.stdout)
                    self.assertIn("slices: 1 expected to fail, of slice 2", done.stdout)

    def test_a_test_of_a_slice_under_way_done_or_gone_from_the_plan_runs_as_it_is(self):
        """a test of a slice under way, done or gone from the plan runs as it is"""
        for standing in ("in progress", "green", None):
            with self.subTest(standing):
                self.plan(**({"2": standing} if standing else {"3": "planned"}))
                self.tests(s2=True)
                done = self.pytest()
                self.assertEqual(done.returncode, 0, done.stdout)
                self.assertIn("1 passed", done.stdout)
                self.assertNotIn("expected to fail", done.stdout)

    def test_naming_a_slice_runs_its_tests_as_they_are(self):
        """naming a slice runs its tests as they are"""
        self.plan(**{"2": "planned"})
        self.tests(s2=True)
        done = self.pytest("--slice", "2")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("1 passed", done.stdout)

    def test_with_no_one_living_plan_no_test_is_expected_to_fail(self):
        """with no one living plan no test is expected to fail"""
        for plans in (0, 2):
            with self.subTest(plans=plans):
                for name in ("2026-10-01-slices.md", "2026-10-02-slices.md")[:plans]:
                    self.plan(name, **{"2": "planned"})
                self.tests(s2=True)
                done = self.pytest()
                self.assertEqual(done.returncode, 0, done.stdout)
                self.assertIn("1 passed", done.stdout)
                self.assertIn("slices: no one living plan found; nothing is expected to fail", done.stdout)
                for name in (self.tmp / "docs" / "superpowers" / "plans").iterdir():
                    name.unlink()

    def test_the_living_plan_is_the_one_slice_plan_names_or_else_the_one_plan_file(self):
        """the living plan is the one slice_plan names, or else the one plan file"""
        rows = (("plans/current.md", True, "plans/current.md"),
                (None, True, "docs/superpowers/plans/2026-10-01-slices.md"),
                (None, False, None),
                (None, 2, None))
        for named, files, read in rows:
            with self.subTest(named=named, files=files):
                shutil.rmtree(self.tmp / "docs")
                (self.tmp / "docs" / "superpowers" / "plans").mkdir(parents=True)
                self.set_ini(named)
                if named:
                    self.write(named, plan_text(**{"2": "planned"}))
                if files:
                    self.plan(**({"2": "planned"} if named is None else {"2": "green"}))
                if files == 2:
                    self.plan("2026-10-02-slices.md", **{"2": "planned"})
                self.tests(s2=False)
                done = self.pytest()
                header = "slices: %s" % read if read else "slices: no one living plan found"
                self.assertIn(header, done.stdout)
                # A failing test of slice 2 is expected to fail only under the plan that was read.
                self.assertIn("1 xfailed" if read else "1 failed", done.stdout)

    def test_naming_several_slices_runs_each_ones_tests_as_they_are(self):
        """naming several slices runs each one's tests as they are"""
        self.plan(**{"2": "planned", "3": "planned"})
        self.tests(s2=True, s3=True)
        done = self.pytest("--slice", "2", "--slice", "slice-3")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("2 passed", done.stdout)

    def test_the_runs_header_names_the_living_plan_or_says_there_is_none(self):
        """the run's header names the living plan or says there is none"""
        self.plan(**{"2": "green"})
        self.assertRegex(self.pytest().stdout, r"(?m)^slices: docs/superpowers/plans/2026-10-01-slices\.md$")
        (self.tmp / "docs" / "superpowers" / "plans" / "2026-10-01-slices.md").unlink()
        self.assertRegex(self.pytest().stdout, r"(?m)^slices: no one living plan found")

    def test_a_slice_plan_naming_a_missing_file_expects_nothing_to_fail(self):
        """a slice_plan naming a missing file expects nothing to fail"""
        self.set_ini("plans/missing.md")
        self.tests(s2=True)
        done = self.pytest()
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("1 passed", done.stdout)
        self.assertRegex(done.stdout, r"(?m)^slices: plans/missing\.md$")


if __name__ == "__main__":
    unittest.main()
