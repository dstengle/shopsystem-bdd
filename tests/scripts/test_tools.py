import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "tools"
HAVE = all(importlib.util.find_spec(name) for name in ("coverage", "pytest_cov", "jedi", "pytest"))

STORE = '''_items = {}


def add(kind, slug):
    item = made(kind, slug)
    _items[item] = kind
    return item


def made(kind, slug):
    return "%s/%s" % (kind, slug)


def forgotten(item):
    if item in _items:
        return _items.pop(item)
    return None


class Shelf:
    def count(self):
        return len(_items)
'''
TESTS = '''from shelf import store
from shelf.store import add as put


def test_an_item_is_added():
    assert store.add("book", "dune") == "book/dune"


def test_an_item_is_put():
    assert put("book", "emma")


def test_the_shelf_counts():
    assert store.Shelf().count() >= 0
'''

class ToolsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.tmp)
        (self.tmp / "shelf").mkdir()
        (self.tmp / "tests").mkdir()
        (self.tmp / "shelf" / "__init__.py").write_text("")
        (self.tmp / "shelf" / "store.py").write_text(STORE)
        (self.tmp / "shelf" / "use.py").write_text("from shelf.store import made\n\n\ndef label(kind, slug):\n    return made(kind, slug).upper()\n")
        (self.tmp / "tests" / "test_store.py").write_text(TESTS)
        (self.tmp / "pytest.ini").write_text("[pytest]\ntestpaths = tests\npythonpath = .\n")

    def run_script(self, *args):
        env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
        return subprocess.run([sys.executable, str(SCRIPT), "--python", sys.executable, *args], cwd=self.tmp,
                              capture_output=True, text=True, env=env)

    def test_probe_gives_a_line_a_tool_and_the_interpreter(self):
        done = self.run_script("probe")
        lines = done.stdout.splitlines()
        self.assertEqual(len(lines), 9)
        for line, name in zip(lines, ("coverage", "pytest-cov", "jedi", "ast-grep", "ruff", "vulture", "import-linter", "hypothesis")):
            self.assertRegex(line, r"^%s (\d[\w.]*|missing: .+)$" % name)
        self.assertEqual(lines[-1], "python: %s (--python)" % sys.executable)
        self.assertEqual(done.returncode, 1 if "missing" in done.stdout else 0)

    @unittest.skipIf(sys.prefix != sys.base_prefix, "this interpreter is a virtualenv")
    def test_install_refuses_an_interpreter_that_is_no_virtualenv(self):
        done = self.run_script("probe")
        if done.returncode == 0:
            self.skipTest("nothing is missing here")
        done = self.run_script("install")
        self.assertEqual(done.returncode, 1)
        self.assertIn("is not a virtualenv", done.stdout)
        self.assertRegex(done.stdout, r"(?m)^\S+ is missing\.\n  It is for: .+\.\n  Without it: .+\.\n  Tried: ")

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_the_map_says_which_tests_execute_a_function(self):
        done = self.run_script("map")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("3 passed", done.stdout)
        done = self.run_script("tests-of", "shelf/store.py:made")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout.splitlines()[:2], ["tests/test_store.py::test_an_item_is_added",
                                                         "tests/test_store.py::test_an_item_is_put"])
        self.assertIn("2 of the 3 tests in the map executed shelf/store.py:made (map made at", done.stdout)
        done = self.run_script("tests-of", "shelf/store.py:11-11", "--by-file")
        self.assertEqual(done.stdout.splitlines()[0], "tests/test_store.py 2")
        done = self.run_script("tests-of", "shelf/store.py:Shelf.count")
        self.assertEqual(done.stdout.splitlines()[0], "tests/test_store.py::test_the_shelf_counts")
        done = self.run_script("tests-of", "shelf/store.py:forgotten")
        self.assertEqual(done.returncode, 0)
        self.assertIn("no test of the map executed shelf/store.py:forgotten (map made at", done.stdout)
        self.assertEqual(self.run_script("tests-of", "shelf/store.py:nothing").returncode, 1)

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_untested_names_each_function_no_test_executed(self):
        self.run_script("map")
        done = self.run_script("untested", "shelf/store.py", "shelf/use.py")
        self.assertEqual(done.stdout.splitlines()[:2], ["shelf/store.py:14 forgotten", "shelf/use.py:4 label"])
        self.assertIn("2 functions no test executed", done.stdout)

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_refs_follow_imports_and_aliases(self):
        done = self.run_script("refs", "shelf.store.add")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout.splitlines()[:3], ["tests/test_store.py:2", "tests/test_store.py:6", "tests/test_store.py:10"])
        self.assertIn("in 0 production and 1 test files; defined at shelf/store.py:4", done.stdout)
        done = self.run_script("refs", "made")
        self.assertIn("shelf/use.py:5", done.stdout)
        self.assertIn("in 2 production and 0 test files", done.stdout)
        done = self.run_script("refs", "nothing_by_this_name")
        self.assertEqual(done.returncode, 1)

    def test_check_heads_each_tool_and_names_a_missing_one(self):
        done = self.run_script("check", "shelf")
        for name in ("ruff", "vulture", "import-linter"):
            self.assertIn("== %s ==" % name, done.stdout)
        self.assertRegex(done.stdout, r"== import-linter ==\n(missing: |the project states no import contracts)")


if __name__ == "__main__":
    unittest.main()
