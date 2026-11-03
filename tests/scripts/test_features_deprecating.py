"""Unit tests of scripts/features: deprecated and bindings, on one shelf of scenarios."""
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "features"

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

DEPRECATED = SHELF.replace(
    "  @slice-1\n  Scenario: A book is added\n",
    "  @slice-1 @deprecated\n  Scenario: A book is added (deprecated)\n    Deprecated for: A book is added at a place\n").replace(
    "  Scenario: A book is lent\n", "  @deprecated\n  Scenario: A book is lent (deprecated)\n    Deprecated for: removal\n")


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

    def test_deprecated_says_when_a_replacement_is_not_written(self):
        self.shelf.write_text(DEPRECATED.replace("for: A book is added at a place", "for: A book on loan"))
        self.assertIn("A book is added (deprecated) | for: A book on loan | no scenario has that title",
                      self.run_script("deprecated").stdout)

    def test_deprecated_lists_each_with_its_replacements_requirement(self):
        self.shelf.write_text(DEPRECATED)
        done = self.run_script("deprecated")
        self.assertEqual(done.stdout, (
            "features/shelf.feature: A book is added (deprecated) | for: A book is added at a place | features/shelf.feature @r4\n"
            "features/shelf.feature: A book is lent (deprecated) | for: removal | deprecated for removal\n"))
        self.shelf.write_text(SHELF)
        self.assertEqual(self.run_script("deprecated").stdout, "none deprecated\n")

    def test_bindings_names_each_binding_whose_title_is_gone(self):
        self.assertEqual(self.run_script("bindings").stdout, "every binding names a scenario\n")
        self.shelf.write_text(DEPRECATED.replace("A book is lent (deprecated)", "A book is lent"))
        done = self.run_script("bindings")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stdout, 'tests/test_shelf.py:7: no scenario titled "A book is added" in shelf.feature\n')

    def test_unbound_counts_a_scenario_imported_under_another_name(self):
        self.bound.write_text('from pytest_bdd import scenario as s\n\n\n@s("shelf.feature", "A book is added")\ndef test_x():\n    pass\n')
        done = self.run_script("bindings", "--tests", "tests", "--unbound")
        self.assertNotIn("A book is added | bound by no test", done.stdout)

    def test_bindings_checks_the_feature_a_binding_names(self):
        (self.tmp / "features" / "other.feature").write_text("Feature: Other\n\n  Scenario: Elsewhere\n    When x\n")
        self.bound.write_text('from pytest_bdd import scenario\n\n\n@scenario("shelf.feature", "Elsewhere")\ndef test_x():\n    pass\n')
        done = self.run_script("bindings")
        self.assertEqual(done.returncode, 1)
        self.assertIn('no scenario titled "Elsewhere" in shelf.feature', done.stdout)


if __name__ == "__main__":
    unittest.main()
