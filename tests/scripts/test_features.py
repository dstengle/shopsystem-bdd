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

    def test_tag_keeps_other_tags(self):
        self.run_script("tag", "Adding several", "r5")
        self.assertEqual(self.cart.read_text(), CART.replace("  @slice-2 @wip\n", "  @slice-2 @wip @r5\n"))

    def test_tag_adds_a_tag_line_where_there_is_none(self):
        self.run_script("tag", "A note that mentions keywords", "r4")
        self.assertEqual(self.cart.read_text(), CART.replace(
            "  Scenario: A note that mentions keywords\n",
            "  @r4\n  Scenario: A note that mentions keywords\n"))

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

    def test_tag_adds_a_requirement_tag_and_keeps_the_others(self):
        self.run_script("tag", "Adding a product", "r4")
        self.run_script("tag", "Adding a product", "r7")
        self.assertEqual(self.cart.read_text(), CART.replace("  @slice-1\n", "  @slice-1 @r4 @r7\n"))

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

  @r4
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


class DeprecatingTest(unittest.TestCase):
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

    def test_deprecate_marks_a_scenario_and_changes_nothing_else_in_it(self):
        done = self.run_script("deprecate", "A book is added", "--for", "A book is added at a place")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.shelf.read_text(), SHELF.replace(
            "  @slice-1\n  Scenario: A book is added\n",
            "  @slice-1 @deprecated\n  Scenario: A book is added (deprecated)\n    Deprecated for: A book is added at a place\n"))

    def test_deprecate_for_removal_on_a_scenario_with_no_tags(self):
        done = self.run_script("deprecate", "A book is lent", "--for-removal")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("  @deprecated\n  Scenario: A book is lent (deprecated)\n    Deprecated for: removal\n    When the reader lends",
                      self.shelf.read_text())

    def test_deprecate_refuses_a_scenario_deprecated_already_and_shows_a_replacement_not_written(self):
        self.run_script("deprecate", "A book is lent", "--for-removal")
        self.assertEqual(self.run_script("deprecate", "A book is lent (deprecated)", "--for-removal").returncode, 1)
        self.assertEqual(self.run_script("deprecate", "A book is added", "--for", "A book is added").returncode, 0)
        self.assertIn("A book is added (deprecated) | for: A book is added | no scenario has that title",
                      self.run_script("deprecated").stdout)

    def test_deprecated_lists_each_with_its_replacements_requirement(self):
        self.run_script("deprecate", "A book is added", "--for", "A book is added at a place")
        self.run_script("deprecate", "A book is lent", "--for-removal")
        done = self.run_script("deprecated")
        self.assertEqual(done.stdout, (
            "features/shelf.feature: A book is added (deprecated) | for: A book is added at a place | features/shelf.feature @r4\n"
            "features/shelf.feature: A book is lent (deprecated) | for: removal | deprecated for removal\n"))
        self.shelf.write_text(SHELF)
        self.assertEqual(self.run_script("deprecated").stdout, "none deprecated\n")

    def test_retire_removes_a_deprecated_scenario_only(self):
        self.run_script("deprecate", "A book is added", "--for", "A book is added at a place")
        done = self.run_script("retire", "A book is added (deprecated)")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.shelf.read_text(), SHELF.replace(
            "  @slice-1\n  Scenario: A book is added\n    One book on the shelf.\n    When the reader adds \"dune\"\n    Then the shelf holds 1 book\n\n", ""))
        before = self.shelf.read_text()
        done = self.run_script("retire", "A book is lent")
        self.assertEqual(done.returncode, 1)
        self.assertIn("not tagged @deprecated", done.stderr)
        self.assertEqual(self.shelf.read_text(), before)

    def test_retire_the_last_scenario_leaves_the_file_ending_in_one_newline(self):
        self.run_script("deprecate", "A book is lent", "--for-removal")
        self.run_script("retire", "A book is lent (deprecated)")
        self.assertTrue(self.shelf.read_text().endswith('Then the shelf holds "dune" at place 2\n'))

    def test_bindings_names_each_binding_whose_title_is_gone(self):
        self.assertEqual(self.run_script("bindings").stdout, "every binding names a scenario\n")
        self.run_script("deprecate", "A book is added", "--for", "A book is added at a place")
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
        self.run_script("deprecate", "A book is added", "--for", "A book is added at a place")
        done = self.run_script("rebind", "A book is added", "A book is added (deprecated)")
        self.assertEqual((done.returncode, done.stdout), (0, "1 binding rebound\n"), done.stderr)
        self.assertEqual(self.bound.read_text(), BOUND.replace(
            '@scenario(FEATURE, "A book is added")', '@scenario(FEATURE, "A book is added (deprecated)")'))
        self.assertEqual(self.run_script("bindings").returncode, 0)

    def test_rebind_refuses_a_title_no_feature_has_and_says_when_nothing_names_the_old_one(self):
        done = self.run_script("rebind", "A book is added", "Nothing by this name")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(self.bound.read_text(), BOUND)
        done = self.run_script("rebind", "A book is added at a place", "A book is lent")
        self.assertEqual((done.returncode, done.stdout), (0, "0 bindings rebound\n"))


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

    def test_deprecating_a_scenario_marks_it_deprecated_and_records_what_for(self):
        """deprecating a scenario marks it deprecated and records what for"""
        plain = scenario("Apply a code", body="    When a code is applied\n    Then the total drops\n")
        voucher = scenario("Apply a voucher")
        for replacement, option, deprecated_for in (
                (True, ("--for", "Apply a voucher"), "Apply a voucher"),
                (False, ("--for", "Apply a voucher"), "Apply a voucher"),
                (False, ("--for-removal",), "removal")):
            with self.subTest(option=option, replacement=replacement):
                path = self.write("features/cart.feature", feature(plain, voucher) if replacement else feature(plain))
                before = path.read_text()
                done = self.run_script("deprecate", "Apply a code", *option)
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(path.read_text(), before.replace(
                    "  Scenario: Apply a code\n",
                    "  @deprecated\n  Scenario: Apply a code (deprecated)\n    Deprecated for: %s\n" % deprecated_for))

    def test_deprecating_a_scenario_already_deprecated_is_refused(self):
        """deprecating a scenario already deprecated is refused"""
        self.write("features/cart.feature", feature(scenario(
            "Apply a code (deprecated)", "@deprecated", "    Deprecated for: removal\n    Given a step\n")))
        reason = self.refused("deprecate", "Apply a code (deprecated)", "--for", "Apply a voucher")
        self.assertIn("already deprecated", reason)

    def test_the_deprecated_list_shows_each_deprecated_scenario_and_what_will_retire_it(self):
        """the deprecated list shows each deprecated scenario and what will retire it"""
        voucher = scenario("Apply a voucher", "@r3")
        for deprecated_for, others, shown in (
                ("Apply a voucher", [voucher], "features/cart.feature @r3"),
                ("Apply a voucher", [], "no scenario has that title"),
                ("removal", [], "deprecated for removal")):
            with self.subTest(deprecated_for):
                self.write("features/cart.feature", feature(
                    scenario("Apply a code (deprecated)", "@deprecated", "    Deprecated for: %s\n    Given a step\n" % deprecated_for), *others))
                done = self.run_script("deprecated")
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(done.stdout, "features/cart.feature: Apply a code (deprecated) | for: %s | %s\n" % (deprecated_for, shown))

    def test_the_deprecated_list_says_when_nothing_is_deprecated(self):
        """the deprecated list says when nothing is deprecated"""
        self.write("features/cart.feature", feature(scenario("Apply a code", "@slice-1")))
        done = self.run_script("deprecated")
        self.assertEqual((done.returncode, done.stdout), (0, "none deprecated\n"))

    def test_retiring_a_deprecated_scenario_removes_its_block(self):
        """retiring a deprecated scenario removes its block"""
        held = scenario("Apply a code (deprecated)", "@deprecated", "    Deprecated for: removal\n    Given a step\n")
        rest = [scenario("Empty cart"), scenario("Checkout")]
        path = self.write("features/cart.feature", feature(rest[0], held, rest[1]))
        done = self.run_script("retire", "Apply a code (deprecated)")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(path.read_text(), feature(*rest))

    def test_retiring_a_scenario_that_is_not_deprecated_is_refused(self):
        """retiring a scenario that is not deprecated is refused"""
        self.write("features/cart.feature", feature(scenario("Apply a code", "@slice-1")))
        self.assertIn("not tagged @deprecated", self.refused("retire", "Apply a code"))

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

    def test_deprecating_a_scenario_prints_its_file_and_new_title(self):
        """deprecating a scenario prints its file and new title"""
        self.write("features/cart.feature", feature(scenario("Apply a code")))
        done = self.run_script("deprecate", "Apply a code", "--for-removal")
        self.assertEqual((done.returncode, done.stdout), (0, "features/cart.feature: Apply a code (deprecated)\n"), done.stderr)

    def test_the_deprecated_list_flags_a_deprecated_scenario_it_cannot_place(self):
        """the deprecated list flags a deprecated scenario it cannot place"""
        for body, others, said in (
                ("    Given a step\n", [], "no Deprecated for: line"),
                ("    Deprecated for: Apply a voucher\n    Given a step\n", [scenario("Apply a voucher")], "the replacement has no @r<n> tag")):
            with self.subTest(said):
                self.write("features/cart.feature", feature(scenario("Apply a code (deprecated)", "@deprecated", body), *others))
                done = self.run_script("deprecated")
                self.assertEqual(done.returncode, 0, done.stderr)
                lines = [x for x in done.stdout.splitlines() if "Apply a code (deprecated)" in x]
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
            done = self.run_script("deprecate", "Apply a code", "--for-removal", "--file", "features/%s.feature" % name)
            self.assertEqual(done.returncode, 0, done.stderr)
        for name in ("cart", "old"):
            done = self.run_script("rebind", "Apply a code", "Apply a code (deprecated)", "--file", "features/%s.feature" % name)
            self.assertEqual((done.returncode, done.stdout), (0, "1 binding rebound\n"), done.stderr)
            moved = [m for m in modules if '"Apply a code (deprecated)")' in (self.tmp / m).read_text()]
            self.assertEqual(moved, ["tests/test_cart.py"] if name == "cart" else list(modules))
        self.assertEqual(self.run_script("bindings").returncode, 0)


if __name__ == "__main__":
    unittest.main()
