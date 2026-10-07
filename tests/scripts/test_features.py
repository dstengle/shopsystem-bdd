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


if __name__ == "__main__":
    unittest.main()
