"""Unit tests of scripts/features on feature files written for each test: the deprecated list."""
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "features"

def feature(*scenarios, tags="", background=""):
    head = "%sFeature: Cart\n  Narrator: a shopper\n\n" % (tags + "\n" if tags else "")
    return head + background + "\n".join(scenarios)


def block(title, tags="", body="    Given a step\n", kind="Scenario"):
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

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.tmp, capture_output=True, text=True)


class ScenarioTest(Workspace, unittest.TestCase):
    """Unit tests of `features` on feature files. The scenarios are bound in tests/scenarios/test_feature_file_tools.py."""

    def test_the_deprecated_list_shows_each_deprecated_scenario_and_what_will_retire_it(self):
        voucher = block("Apply a voucher", "@r3")
        for deprecated_for, others, shown in (
                ("Apply a voucher", [voucher], "features/cart.feature @r3"),
                ("Apply a voucher", [], "no scenario has that title"),
                ("removal", [], "deprecated for removal")):
            with self.subTest(deprecated_for):
                self.write("features/cart.feature", feature(
                    block("Apply a code (deprecated)", "@deprecated", "    Deprecated for: %s\n    Given a step\n" % deprecated_for), *others))
                done = self.run_script("deprecated")
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(done.stdout, "features/cart.feature: Apply a code (deprecated) | for: %s | %s\n" % (deprecated_for, shown))

    def test_the_deprecated_list_names_each_file_that_has_the_replacements_title(self):
        self.write("features/a.feature", feature(
            block("Apply a code (deprecated)", "@deprecated", "    Deprecated for: Apply a voucher\n    Given a step\n"),
            block("Apply a voucher", "@r5")))
        self.write("features/b.feature", feature(block("Apply a voucher", "@slice-1")))
        done = self.run_script("deprecated")
        self.assertEqual(done.stdout, "features/a.feature: Apply a code (deprecated) | for: Apply a voucher | "
                                      "features/a.feature @r5; features/b.feature has no @r<n> tag\n")

    def test_the_deprecated_list_says_once_that_the_deprecated_for_line_is_empty(self):
        self.write("features/cart.feature", feature(
            block("Apply a code (deprecated)", "@deprecated", "    Deprecated for:\n    Given a step\n")))
        done = self.run_script("deprecated")
        self.assertEqual(done.stdout, "features/cart.feature: Apply a code (deprecated) | the Deprecated for: line is empty\n")

    def test_the_deprecated_list_says_when_nothing_is_deprecated(self):
        self.write("features/cart.feature", feature(block("Apply a code", "@slice-1")))
        done = self.run_script("deprecated")
        self.assertEqual((done.returncode, done.stdout), (0, "none deprecated\n"))

    def test_the_deprecated_list_flags_a_deprecated_scenario_it_cannot_place(self):
        for body, others, said in (
                ("    Given a step\n", [], "no Deprecated for: line"),
                ("    Deprecated for: Apply a voucher\n    Given a step\n", [block("Apply a voucher")], "the replacement has no @r<n> tag")):
            with self.subTest(said):
                self.write("features/cart.feature", feature(block("Apply a code (deprecated)", "@deprecated", body), *others))
                done = self.run_script("deprecated")
                self.assertEqual(done.returncode, 0, done.stderr)
                lines = [x for x in done.stdout.splitlines() if "Apply a code (deprecated)" in x]
                self.assertEqual(len(lines), 1)
                self.assertTrue(lines[0].endswith("| " + said), lines[0])


if __name__ == "__main__":
    unittest.main()
