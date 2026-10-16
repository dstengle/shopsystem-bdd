import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from binding import missing

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

CART = """\"\"\"The cart.\"\"\"


def total(items):
    return sum(items)


class Cart:
    def total(self, items):
        return total(items)


def unused():
    return None
"""
CART_ALL = "def total(items):\n    return sum(items)\n"
OTHER = "def other():\n    return 1\n"
TEST_TOTAL = "from cart import Cart, total\n\n\ndef test_total():\n    assert Cart().total([1, 2]) == 3\n    assert total([1]) == 1\n"
TEST_ONLY_TOTAL = "from cart import total\n\n\ndef test_total():\n    assert total([1]) == 1\n"
TEST_DISCOUNT = "\n\ndef test_discount():\n    assert Cart().total([4]) == 4\n"
TEST_CHECKOUT = "from cart import Cart\n\n\ndef test_checkout():\n    assert Cart().total([5]) == 5\n"
TEST_OTHER = "from other import other\n\n\n" + "".join("def test_other_%d():\n    assert other() == 1\n\n\n" % n for n in range(3))

# stands in for an interpreter (and for lint-imports) beside it: answers as the config beside it says
FAKE = r"""import json, os, runpy, sys
here = os.path.dirname(os.path.abspath(__file__))
config = json.load(open(os.path.join(here, "fake.json")))
tool, args = os.path.basename(sys.argv[0]), sys.argv[1:]
REAL = %r


def note(*words):
    with open(config["log"], "a") as log:
        log.write(json.dumps([tool, *words]) + "\n")


def reply(text, failing=True):
    if text:
        print(text)
    sys.exit(1 if text and failing else 0)


if tool == "lint-imports":
    note(*args)
    reply(config.get("import-linter", ""))
if args[:1] == ["-c"]:
    found = {name: (None if name in config["missing"] else "1.0") for name in args[2:]}
    print(json.dumps(dict(found, virtualenv=config["venv"])))
    sys.exit(0)
if args[:3] == ["-m", "pip", "install"]:
    note(*args[1:])
    if config["pip_fails"]:
        sys.stderr.write(config["pip_error"])
        sys.exit(1)
    sys.exit(0)
if args[:1] == ["-m"] and args[1] in ("ruff", "vulture"):
    note(*args[1:])
    reply(config.get(args[1], ""))
if args[:2] == ["-m", "pytest"]:
    note(*args[1:])
    if config["pytest"] == "noop":
        reply(config["pytest_out"], failing=False)
    os.execv(REAL, [REAL] + args)
for blocked in config["block"]:
    sys.modules[blocked] = None
sys.executable = os.path.abspath(sys.argv[0])
sys.argv = args
runpy.run_path(args[0], run_name="__main__")
""" % sys.executable


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

    def test_probe_log_is_one_line_for_the_plan(self):
        """probe with --log prints the one line to give plan log"""
        done = self.run_script("probe", "--log")
        self.assertRegex(done.stdout, r"^Probe: tools -> coverage \S+, pytest-cov \S+, jedi \S+, .*hypothesis \S+\n$")

    def test_a_project_in_no_known_language_is_told_so(self):
        """a project that is not a Python project has no known analysis tools"""
        for path in list(self.tmp.iterdir()):
            shutil.rmtree(path) if path.is_dir() else path.unlink()
        (self.tmp / "main.go").write_text("package main\n")
        done = self.run_script("probe")
        self.assertEqual(done.returncode, 1)
        self.assertIn("no analysis tools are known for this project's language", done.stderr)
        self.assertEqual(len(done.stderr.strip().splitlines()), 1)

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
        self.assertEqual(done.returncode, 1)
        self.assertIn("0 of the 3 tests in the map executed", done.stdout)
        self.assertEqual(self.run_script("tests-of", "shelf/store.py:nothing").returncode, 1)

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_untested_names_each_function_no_test_executed(self):
        self.run_script("map")
        done = self.run_script("untested", "shelf/store.py", "shelf/use.py")
        self.assertEqual(done.stdout.splitlines()[:2], ["shelf/store.py:14 forgotten", "shelf/use.py:4 label"])
        self.assertIn("2 functions no test executed", done.stdout)

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_tests_of_with_no_map_says_to_make_one(self):
        """tests-of without a map says to make one"""
        done = self.run_script("tests-of", "shelf/store.py:made")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stderr, "tools: no map: make one with tools map\n")

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

    # --- helpers for the scenarios: projects in git, and fake interpreters ---

    def git(self, root, *args):
        done = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=root,
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        return done.stdout.strip()

    def project(self, files):
        """A Python project in git, with these files, committed."""
        root = pathlib.Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, root)
        files = {"pytest.ini": "[pytest]\ntestpaths = tests\npythonpath = src\n", **files}
        for name, text in files.items():
            (root / name).parent.mkdir(parents=True, exist_ok=True)
            (root / name).write_text(text)
        self.git(root, "init", "-q")
        self.commit(root)
        return root

    def commit(self, root, message="m"):
        self.git(root, "add", "-A")
        self.git(root, "commit", "-q", "--allow-empty", "-m", message)
        return self.git(root, "rev-parse", "--short", "HEAD")

    def cli(self, *args, cwd=None, python=None, env=None):
        """Run tools; the interpreter is given with --python only when python is."""
        environ = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
        environ.update(env or {})
        option = ["--python", str(python)] if python else []
        return subprocess.run([sys.executable, str(SCRIPT), *option, *args], cwd=cwd or self.tmp,
                              capture_output=True, text=True, env=environ)

    def fake(self, where, **config):
        """An interpreter at <where>/bin/python that answers as a virtualenv with the tools it is told to
        have, logs what it is asked to run in <where>/calls.log, and runs the rest as the real one."""
        where = pathlib.Path(where)
        (where / "bin").mkdir(parents=True)
        config = {"missing": [], "venv": True, "pip_fails": False, "pip_error": "", "pytest": "run",
                  "pytest_out": "", "block": [], **config, "log": str(where / "calls.log")}
        (where / "bin" / "fake.json").write_text(json.dumps(config))
        for name in ("python", "lint-imports"):
            (where / "bin" / name).write_text("#!%s\n%s" % (sys.executable, FAKE))
            (where / "bin" / name).chmod(0o755)
        return where / "bin" / "python"

    def outside(self):
        path = pathlib.Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, path)
        return path

    def calls(self, python):
        log = pathlib.Path(python).parent.parent / "calls.log"
        return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []

    def under_heading(self, stdout, name):
        return stdout.split("== %s ==\n" % name)[1].split("== ")[0].strip()

    def pip_calls(self, python):
        return [call[3] for call in self.calls(python) if call[:3] == ["python", "pip", "install"]]

    def mapped(self, files):
        """A project in git with its map made."""
        root = self.project(files)
        done = self.cli("map", cwd=root, python=sys.executable)
        self.assertEqual(done.returncode, 0, done.stderr)
        return root

    # --- the scenarios ---

    def test_the_interpreter_is_the_first_of_the_five(self):
        """the interpreter is the first of --python, .venv, venv, $VIRTUAL_ENV and the running one"""
        rows = [("--python", True, True, True, True), ("the project's virtualenv", False, True, True, True),
                ("the project's virtualenv", False, False, True, True), ("the project's virtualenv", False, False, False, True),
                ("neither", False, False, False, False)]
        for source, option, dot, plain, env in rows:
            with self.subTest(source=source, option=option, dot=dot, plain=plain, env=env):
                root = self.project({})
                opt = self.outside()
                chosen = {"--python": self.fake(opt / "py")}
                env_dir = self.outside()
                if env:
                    chosen["env"] = self.fake(env_dir)
                else:
                    (env_dir / "bin").mkdir()
                if dot:
                    chosen[".venv"] = self.fake(root / ".venv")
                if plain:
                    chosen["venv"] = self.fake(root / "venv")
                expected = (chosen["--python"] if option else chosen[".venv"] if dot else chosen["venv"] if plain
                            else chosen["env"] if env else pathlib.Path(sys.executable))
                done = self.cli("probe", cwd=root, python=chosen["--python"] if option else None,
                                env={"VIRTUAL_ENV": str(env_dir)})
                last = done.stdout.splitlines()[-1]
                self.assertTrue(last.startswith("python: %s (" % expected), last)
                self.assertTrue(last.endswith("(%s)" % source) if source != "neither"
                                else "(no virtualenv found" in last, last)

    def test_probe_lists_each_tool_its_version_or_missing_and_the_interpreter(self):
        """probe lists each tool, its version or that it is missing, and the interpreter"""
        python = self.fake(self.outside(), missing=["vulture"])
        done = self.cli("probe", python=python)
        lines = done.stdout.splitlines()
        names = ("coverage", "pytest-cov", "jedi", "ast-grep", "ruff", "vulture", "import-linter", "hypothesis")
        self.assertEqual(len(lines), 9)
        for line, name in zip(lines, names):
            if name == "vulture":
                self.assertRegex(line, r"^vulture missing: \S.+$")
            else:
                self.assertEqual(line, "%s 1.0" % name)
        self.assertEqual(lines[-1], "python: %s (--python)" % python)
        self.assertEqual(done.returncode, 1)

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_install_puts_each_missing_tool_in_with_pip_and_edits_no_dependency_file(self):
        """install puts each missing tool into the interpreter and leaves dependency files alone"""
        root = self.project({"pyproject.toml": "[project]\nname = 'cart'\n", "requirements.txt": "pytest\n"})
        python = self.fake(self.outside(), missing=["jedi", "vulture"])
        done = self.cli("install", cwd=root, python=python)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.pip_calls(python), ["jedi", "vulture"])
        self.assertEqual((root / "pyproject.toml").read_text(), "[project]\nname = 'cart'\n")
        self.assertEqual((root / "requirements.txt").read_text(), "pytest\n")
        self.assertEqual(self.git(root, "status", "--porcelain"), "")

    def test_install_refuses_an_interpreter_that_is_not_a_virtualenv(self):
        """install refuses an interpreter that is not a virtualenv"""
        python = self.fake(self.outside(), missing=["jedi"], venv=False)
        done = self.cli("install", python=python)
        self.assertEqual(done.returncode, 1)
        self.assertIn("is not a virtualenv", done.stdout)
        self.assertEqual(self.pip_calls(python), [])
        self.assertIn("jedi missing", self.cli("probe", "--log", python=python).stdout)

    def test_a_tool_still_missing_after_install_is_reported_with_the_failed_command(self):
        """a tool still missing after install is reported with the failed command"""
        python = self.fake(self.outside(), missing=["jedi"], pip_fails=True,
                           pip_error="e1\ne2\ne3\ne4\ne5\nerror: no matching distribution")
        done = self.cli("install", python=python)
        self.assertEqual(done.returncode, 1)
        self.assertRegex(done.stdout, r"(?m)^jedi is missing\.\n  It is for: .+\.\n  Without it: .+\.\n"
                                      r"  Tried: %s -m pip install jedi\n" % python)
        self.assertIn("error: no matching distribution", done.stdout)
        self.assertNotIn("e1", done.stdout)
        self.assertEqual(self.pip_calls(python), ["jedi"])

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_map_runs_the_suite_once_under_coverage_and_keeps_the_map(self):
        """map runs the suite once under coverage and keeps the map"""
        root = self.project({"src/cart.py": CART, "tests/test_cart.py": TEST_TOTAL + TEST_DISCOUNT})
        python = self.fake(self.outside())
        done = self.cli("map", "--", "-k", "test_total", cwd=root, python=python)
        self.assertEqual(done.returncode, 0, done.stderr)
        runs = [call for call in self.calls(python) if call[:2] == ["python", "pytest"]]
        self.assertEqual(len(runs), 1)
        self.assertIn("--cov-context=test", runs[0])
        self.assertEqual(runs[0][-2:], ["-k", "test_total"])
        self.assertIn("1 passed", done.stdout)
        self.assertTrue((root / ".superpowers" / "tools" / "coverage").is_file())
        listed = self.cli("tests-of", "src/cart.py", cwd=root, python=sys.executable).stdout
        self.assertEqual(listed.splitlines()[0], "tests/test_cart.py::test_total")
        self.assertNotIn("test_discount", listed)

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_tests_of_lists_the_tests_that_executed_a_target_in_the_last_map(self):
        """tests-of lists the tests that executed a target in the last map"""
        root = self.mapped({"src/cart.py": CART, "src/other.py": OTHER, "tests/test_cart.py": TEST_TOTAL,
                            "tests/test_checkout.py": TEST_CHECKOUT, "tests/test_other.py": TEST_OTHER})
        commit = self.git(root, "rev-parse", "--short", "HEAD")
        for target, argument in (("the file", "src/cart.py"), ("the function", "src/cart.py:total"),
                                 ("the method", "src/cart.py:Cart.total"), ("a line range", "src/cart.py:10-20")):
            with self.subTest(target=target):
                done = self.cli("tests-of", argument, cwd=root, python=sys.executable)
                self.assertEqual(done.returncode, 0, done.stderr)
                lines = done.stdout.splitlines()
                self.assertEqual(lines[:-1], ["tests/test_cart.py::test_total", "tests/test_checkout.py::test_checkout"])
                self.assertEqual(lines[-1], "2 of the 5 tests in the map executed %s (map made at %s)" % (argument, commit))

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_tests_of_by_file_counts_tests_per_test_file(self):
        """tests-of with --by-file counts tests per test file"""
        root = self.mapped({"src/cart.py": CART, "tests/test_cart.py": TEST_TOTAL + TEST_DISCOUNT,
                            "tests/test_checkout.py": TEST_CHECKOUT})
        done = self.cli("tests-of", "--by-file", "src/cart.py", cwd=root, python=sys.executable)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout.splitlines()[:2], ["tests/test_cart.py 2", "tests/test_checkout.py 1"])
        self.assertNotIn("::", done.stdout)
        self.assertNotIn("test_total", done.stdout)

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_tests_of_fails_when_nothing_executed_the_target_or_the_function_does_not_exist(self):
        """tests-of fails when nothing executed the target or the function does not exist"""
        root = self.mapped({"src/cart.py": CART, "tests/test_cart.py": TEST_TOTAL})
        for argument in ("src/cart.py:unused", "src/cart.py:missing"):
            with self.subTest(argument=argument):
                done = self.cli("tests-of", argument, cwd=root, python=sys.executable)
                self.assertEqual(done.returncode, 1)
                self.assertNotIn("Traceback", done.stderr)
                if argument.endswith("missing"):
                    self.assertEqual(done.stdout, "")
                    self.assertEqual(done.stderr, "tools: src/cart.py has no function named missing\n")
                else:
                    self.assertIn("0 of the 1 tests in the map executed", done.stdout)
        done = self.cli("tests-of", "src/cart.py:total", cwd=root, python=sys.executable)
        self.assertEqual(done.returncode, 0)

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_untested_lists_the_functions_no_test_executed(self):
        """untested lists the functions no test executed"""
        root = self.mapped({"src/cart.py": "def total(items):\n    return sum(items)\n\n\ndef refund(order):\n    return -order\n",
                            "src/report.py": "def build():\n    return 1\n\n\ndef export():\n    return 2\n",
                            "tests/test_cart.py": "from cart import total\nfrom report import build\n\n\n"
                                                  "def test_total():\n    assert total([1]) == 1\n    assert build() == 1\n"})
        done = self.cli("untested", "src/cart.py", "src/report.py", cwd=root, python=sys.executable)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout.splitlines()[:-1], ["src/cart.py:5 refund", "src/report.py:5 export"])

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_refs_print_path_line_through_imports_and_aliases_then_one_summary_line(self):
        """refs prints each reference as path:line, through imports and aliases, then one summary line"""
        root = self.project({
            "src/cart.py": "def total(items):\n    return sum(items)\n",
            "src/checkout.py": "from cart import total\n\n\ndef pay():\n    return total([1])\n",
            "src/report.py": "from cart import total as cart_total\n\n\ndef show():\n    return cart_total([2])\n",
            "tests/test_cart.py": "from cart import total\n\n\ndef test_total():\n    assert total([1]) == 1\n"})
        done = self.cli("refs", "total", cwd=root, python=sys.executable)
        self.assertEqual(done.returncode, 0, done.stderr)
        lines = done.stdout.splitlines()
        for line in lines[:-1]:
            self.assertRegex(line, r"^\S+:\d+$")
        for call in ("src/checkout.py:5", "src/report.py:5", "tests/test_cart.py:5"):
            self.assertIn(call, lines[:-1])
        self.assertEqual(lines[-1], "%d references to total, in 2 production and 1 test files; defined at src/cart.py:1"
                         % len(lines[:-1]))

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_refs_fails_for_a_name_the_project_does_not_define(self):
        """refs fails for a name the project does not define"""
        root = self.project({"src/cart.py": CART})
        done = self.cli("refs", "nowhere", cwd=root, python=sys.executable)
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stdout, "")
        self.assertNotIn("Traceback", done.stderr)

    def check_project(self, **config):
        root = self.project({"src/cart.py": "def total(items):\n    return sum(items)\n", ".importlinter": "[importlinter]\n"})
        return root, self.fake(self.outside(), **config)

    def test_check_runs_each_tool_under_its_own_heading_and_fails_when_any_reports(self):
        """check runs each tool under its own heading and fails when any reports"""
        for tool in ("ruff", "vulture", "import-linter"):
            with self.subTest(tool=tool):
                root, python = self.check_project(**{tool: "%s found something" % tool})
                done = self.cli("check", "src/cart.py", cwd=root, python=python)
                self.assertEqual(done.returncode, 1)
                for name in ("ruff", "vulture", "import-linter"):
                    self.assertIn("== %s ==\n" % name, done.stdout)
                    self.assertEqual(self.under_heading(done.stdout, name),
                                     "%s found something" % name if name == tool else "clean")
                calls = {call[0] if call[0] != "python" else call[1]: call for call in self.calls(python)
                         if call[:2] != ["python", "pip"]}
                self.assertEqual(calls["ruff"][-1:], ["src/cart.py"])
                self.assertEqual(calls["vulture"][-1:], ["src/cart.py"])
                self.assertEqual(calls["lint-imports"], ["lint-imports"])

    def test_check_names_a_missing_tool_under_its_heading(self):
        """check names a missing tool under its heading"""
        root, python = self.check_project(missing=["vulture"])
        done = self.cli("check", "src/cart.py", cwd=root, python=python)
        self.assertRegex(self.under_heading(done.stdout, "vulture"), r"^missing: \S.+$")
        self.assertNotIn("vulture", [call[1] for call in self.calls(python) if len(call) > 1])

    def test_install_outside_a_virtualenv_explains_each_missing_tool_and_installs_nothing(self):
        """install outside a virtualenv explains each missing tool and installs nothing"""
        python = self.fake(self.outside(), missing=["jedi", "vulture"], venv=False)
        done = self.cli("install", python=python)
        self.assertEqual(done.returncode, 1)
        self.assertEqual(self.pip_calls(python), [])
        for name in ("jedi", "vulture"):
            self.assertRegex(done.stdout, r"(?m)^%s is missing\.\n  It is for: .+\.\n  Without it: .+\.\n"
                                          r"  Tried: %s is not a virtualenv" % (name, python))

    def test_install_with_every_tool_present_says_so_and_succeeds(self):
        """install with every tool present says so and succeeds"""
        for kind, venv in (("is a virtualenv", True), ("is not a virtualenv", False)):
            with self.subTest(kind=kind):
                python = self.fake(self.outside(), venv=venv)
                done = self.cli("install", python=python)
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(done.stdout, "every tool is present\n")
                self.assertEqual(self.pip_calls(python), [])

    def test_install_says_each_tool_it_installed(self):
        """install says each tool it installed"""
        python = self.fake(self.outside(), missing=["jedi"])
        done = self.cli("install", python=python)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout, "jedi installed\n")

    def test_an_interpreter_that_does_not_run_is_refused(self):
        """an interpreter that does not run is refused"""
        broken = self.outside() / "broken"
        broken.write_text("#!/bin/sh\necho 'boom: cannot start' >&2\nexit 3\n")
        broken.chmod(0o755)
        for command in (["probe"], ["install"], ["check", "src/cart.py"]):
            with self.subTest(command=command):
                done = self.cli(*command, python=broken)
                self.assertEqual(done.returncode, 1)
                self.assertEqual(done.stderr, "tools: %s does not run: boom: cannot start\n" % broken)

    def test_the_probe_log_line_names_every_tool_with_its_version_or_missing(self):
        """the probe log line names every tool with its version or missing"""
        python = self.fake(self.outside(), missing=["vulture"])
        done = self.cli("probe", "--log", python=python)
        self.assertEqual(done.stdout, "Probe: tools -> coverage 1.0, pytest-cov 1.0, jedi 1.0, ast-grep 1.0, ruff 1.0, "
                                      "vulture missing, import-linter 1.0, hypothesis 1.0\n")

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_map_replaces_the_earlier_map_and_succeeds_whether_or_not_the_tests_pass(self):
        """map replaces the earlier map and succeeds whether or not the tests pass"""
        for outcome, last in (("passes", "1 passed"), ("has a failure", "1 failed, 1 passed")):
            with self.subTest(outcome=outcome):
                root = self.project({"src/cart.py": CART, "tests/test_cart.py": TEST_TOTAL,
                                     "tests/test_old.py": "from cart import total\n\n\ndef test_old():\n    assert total([1])\n"})
                self.cli("map", cwd=root, python=sys.executable)
                earlier = self.cli("tests-of", "src/cart.py", cwd=root, python=sys.executable).stdout
                self.assertIn("test_old", earlier)
                (root / "tests" / "test_old.py").unlink()
                if outcome != "passes":
                    (root / "tests" / "test_broken.py").write_text("def test_broken():\n    assert False\n")
                commit = self.commit(root)
                done = self.cli("map", cwd=root, python=sys.executable)
                self.assertEqual(done.returncode, 0, done.stderr)
                lines = done.stdout.splitlines()
                self.assertTrue(lines[0].startswith(last), lines)
                self.assertEqual(lines[1], "map: .superpowers/tools/coverage, at %s" % commit)
                later = self.cli("tests-of", "src/cart.py", cwd=root, python=sys.executable).stdout
                self.assertNotIn("test_old", later)
                self.assertIn("(map made at %s)" % commit, later)

    def test_map_that_makes_no_map_is_refused(self):
        """map that makes no map is refused"""
        root = self.project({"src/cart.py": CART})
        python = self.fake(self.outside(), pytest="noop", pytest_out="collected nothing at all")
        done = self.cli("map", cwd=root, python=python)
        self.assertEqual(done.returncode, 1)
        self.assertRegex(done.stderr, r"^tools: no map was made by: %s -m pytest -q .*--cov-context=test --cov-report=\n"
                                      r"collected nothing at all\n$" % python)
        self.assertFalse((root / ".superpowers" / "tools" / "coverage.at").exists())

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_untested_prints_each_function_with_its_place_the_count_and_the_commit(self):
        """untested prints each function with its place, the count and the commit"""
        for count in (0, 2):
            with self.subTest(count=count):
                text = CART_ALL + "".join("\n\ndef lost_%d():\n    return %d\n" % (n, n) for n in range(count))
                root = self.mapped({"src/cart.py": text, "tests/test_cart.py": TEST_ONLY_TOTAL})
                commit = self.git(root, "rev-parse", "--short", "HEAD")
                done = self.cli("untested", "src/cart.py", cwd=root, python=sys.executable)
                self.assertEqual(done.returncode, 0, done.stderr)
                lines = text.splitlines()
                want = ["src/cart.py:%d lost_%d" % (lines.index("def lost_%d():" % n) + 1, n) for n in range(count)]
                self.assertEqual(done.stdout.splitlines(), want + [
                    "%d functions no test executed, in the map made at %s" % (count, commit)])

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_untested_without_a_map_says_to_make_one(self):
        """untested without a map says to make one"""
        root = self.project({"src/cart.py": CART})
        done = self.cli("untested", "src/cart.py", cwd=root, python=sys.executable)
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stderr, "tools: no map: make one with tools map\n")

    def test_without_coverage_tests_of_and_untested_say_to_install_it(self):
        """without coverage tests-of and untested say to install it"""
        root = self.project({"src/cart.py": CART})
        python = self.fake(self.outside(), block=["coverage"])
        for command in ("tests-of", "untested"):
            with self.subTest(command=command):
                done = self.cli(command, "src/cart.py", cwd=root, python=python)
                self.assertEqual(done.returncode, 1)
                self.assertEqual(done.stderr, "tools: coverage is missing from %s: tools install\n" % python)

    def test_without_jedi_refs_says_to_install_it(self):
        """without jedi refs says to install it"""
        root = self.project({"src/cart.py": CART})
        python = self.fake(self.outside(), block=["jedi"])
        done = self.cli("refs", "total", cwd=root, python=python)
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stderr, "tools: jedi is missing from %s: tools install\n" % python)

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_tests_of_on_a_file_that_does_not_exist_is_refused(self):
        """tests-of on a file that does not exist is refused"""
        root = self.mapped({"src/cart.py": CART, "tests/test_cart.py": TEST_TOTAL})
        done = self.cli("tests-of", "src/gone.py", cwd=root, python=sys.executable)
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stderr, "tools: src/gone.py is not a file\n")
        self.assertEqual(done.stdout, "")

    @unittest.skipUnless(HAVE, "coverage, pytest-cov and jedi are needed")
    def test_refs_on_a_defined_name_gives_its_definition_apart_from_its_references(self):
        """refs on a defined name gives its definition apart from its references"""
        for count in (0, 3):
            with self.subTest(count=count):
                uses = "".join("    cart.total([%d])\n" % n for n in range(count))
                root = self.project({"src/cart.py": "def total(items):\n    return sum(items)\n",
                                     "src/checkout.py": "import cart\n\n\ndef pay():\n" + uses + "    return 0\n"})
                done = self.cli("refs", "total", cwd=root, python=sys.executable)
                self.assertEqual(done.returncode, 0, done.stderr)
                lines = done.stdout.splitlines()
                self.assertEqual(len(lines) - 1, count)
                self.assertNotIn("src/cart.py:1", lines[:-1])
                self.assertEqual(lines[-1], "%d reference%s to total, in %d production and 0 test files; defined at src/cart.py:1"
                                 % (count, "" if count == 1 else "s", 1 if count else 0))

    def test_check_with_base_checks_the_changed_python_files_that_remain(self):
        """check with --base checks the changed Python files that remain, in place of the paths given"""
        root = self.project({"src/cart.py": "A = 1\n", "src/old.py": "B = 1\n", "src/report.py": "C = 1\n",
                             "README.md": "one\n"})
        base = self.git(root, "rev-parse", "--short", "HEAD")
        (root / "src" / "cart.py").write_text("A = 2\n")
        (root / "README.md").write_text("two\n")
        (root / "src" / "old.py").unlink()
        self.commit(root)
        python = self.fake(self.outside())
        done = self.cli("check", "--base", base, "src/report.py", cwd=root, python=python)
        self.assertEqual(done.returncode, 0, done.stderr)
        for call in self.calls(python):
            if call[:2] in (["python", "ruff"], ["python", "vulture"]):
                self.assertEqual([a for a in call[2:] if "." in a and not a.startswith("-")], ["src/cart.py"])
        self.assertEqual(len([c for c in self.calls(python) if c[:2] in (["python", "ruff"], ["python", "vulture"])]), 2)

    def test_check_with_a_base_git_cannot_compare_is_refused_with_gits_error(self):
        """check with a base git cannot compare is refused with git's error"""
        root = self.project({"src/cart.py": "A = 1\n"})
        python = self.fake(self.outside())
        done = self.cli("check", "--base", "nosuchref", cwd=root, python=python)
        self.assertEqual(done.returncode, 1)
        wanted = subprocess.run(["git", "diff", "--name-only", "--diff-filter=d", "nosuchref", "--", "*.py"], cwd=root, capture_output=True, text=True).stderr.strip()
        self.assertEqual(done.stderr, "tools: %s\n" % wanted)
        self.assertIn("nosuchref", wanted)
        self.assertEqual(done.stdout, "")

    def test_check_with_no_file_to_check_says_so_under_ruff_and_vulture_and_does_not_fail(self):
        """check with no file to check says so under ruff and vulture and does not fail for them"""
        root = self.project({"src/cart.py": "A = 1\n"})
        base = self.git(root, "rev-parse", "--short", "HEAD")
        python = self.fake(self.outside(), ruff="would fail", vulture="would fail")
        done = self.cli("check", "--base", base, cwd=root, python=python)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.under_heading(done.stdout, "ruff"), "nothing to check")
        self.assertEqual(self.under_heading(done.stdout, "vulture"), "nothing to check")
        self.assertEqual([c for c in self.calls(python) if c[:2] in (["python", "ruff"], ["python", "vulture"])], [])

    def test_check_without_import_contracts_does_not_run_import_linter(self):
        """check without import contracts does not run import-linter"""
        root = self.project({"src/cart.py": "A = 1\n"})
        python = self.fake(self.outside(), **{"import-linter": "would fail"})
        done = self.cli("check", "src/cart.py", cwd=root, python=python)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.under_heading(done.stdout, "import-linter"), "the project states no import contracts")
        self.assertEqual([c for c in self.calls(python) if c[0] == "lint-imports"], [])

    def test_a_tool_that_prints_nothing_is_reported_clean(self):
        """a tool that prints nothing is reported clean"""
        root = self.project({"src/cart.py": "A = 1\n"})
        python = self.fake(self.outside())
        done = self.cli("check", "src/cart.py", cwd=root, python=python)
        self.assertEqual(self.under_heading(done.stdout, "ruff"), "clean")


FEATURE = pathlib.Path(__file__).resolve().parents[2] / "features" / "analysis-tools.feature"


class BindingTest(unittest.TestCase):
    def test_every_scenario_has_its_test(self):
        self.assertEqual(missing(FEATURE, ToolsTest), [])


if __name__ == "__main__":
    unittest.main()
