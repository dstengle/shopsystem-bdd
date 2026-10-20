"""Unit tests of scripts/features on feature files written for each test: deprecate, deprecated, retire and rebind."""
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
    """Unit tests of `features` on feature files. The scenarios are bound in tests/scenarios/test_feature_file_tools.py."""

    def test_deprecating_a_scenario_marks_it_deprecated_and_records_what_for(self):
        plain = block("Apply a code", body="    When a code is applied\n    Then the total drops\n")
        voucher = block("Apply a voucher")
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
        self.write("features/cart.feature", feature(block(
            "Apply a code (deprecated)", "@deprecated", "    Deprecated for: removal\n    Given a step\n")))
        reason = self.refused("deprecate", "Apply a code (deprecated)", "--for", "Apply a voucher")
        self.assertIn("already deprecated", reason)

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

    def test_retiring_a_deprecated_scenario_removes_its_block(self):
        deprecated = block("Apply a code (deprecated)", "@deprecated", "    Deprecated for: removal\n    Given a step\n")
        rest = [block("Empty cart"), block("Checkout")]
        path = self.write("features/cart.feature", feature(rest[0], deprecated, rest[1]))
        done = self.run_script("retire", "Apply a code (deprecated)")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(path.read_text(), feature(*rest))

    def test_retiring_a_scenario_that_is_not_deprecated_is_refused(self):
        self.write("features/cart.feature", feature(block("Apply a code", "@slice-1")))
        self.assertIn("not tagged @deprecated", self.refused("retire", "Apply a code"))

    def test_deprecating_a_scenario_prints_its_file_and_new_title(self):
        self.write("features/cart.feature", feature(block("Apply a code")))
        done = self.run_script("deprecate", "Apply a code", "--for-removal")
        self.assertEqual((done.returncode, done.stdout), (0, "features/cart.feature: Apply a code (deprecated)\n"), done.stderr)

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


def binding(title, feature_name="cart.feature", line=12):
    pad = "".join("# filler\n" for _ in range(line - 2))
    return 'from pytest_bdd import scenario\n%s@scenario("%s", "%s")\ndef test_x():\n    pass\n' % (pad, feature_name, title)


class BindingsScenarioTest(Workspace, unittest.TestCase):
    """Unit tests of `features` on test-module bindings."""

    def test_rebind_with_file_takes_a_new_title_that_several_feature_files_have(self):
        # rebind --file follows only its own file when both files have the new title
        self.write("features/cart.feature", feature(block("Apply a code")))
        self.write("features/old.feature", feature(block("Apply a code")))
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
