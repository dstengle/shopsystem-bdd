import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "features"

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

    def test_move_carrying_feature_tags_verifies(self):
        checkout = self._before_and_checkout(header="Feature: Checkout\n  Narrator: a shopper\n")
        done = self.run_script("move", "Adding a product", "--to", "features/checkout.feature",
                               "--inline-background", "--carry-feature-tags")
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

    def test_a_test_module_that_does_not_parse_is_refused_by_name(self):
        self.bound.write_text("def broken(:\n")
        done = self.run_script("bindings")
        self.assertEqual(done.returncode, 1)
        self.assertIn("tests/test_shelf.py does not parse", done.stderr)


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


if __name__ == "__main__":
    unittest.main()
