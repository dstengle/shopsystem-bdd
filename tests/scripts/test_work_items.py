"""scripts/work_items.py, the plugin's pytest plugin: in a repository with no conftest of its own, loaded as a batch's
default test command loads it (`-p work_items`, the scripts directory on PYTHONPATH)."""
import os
import pathlib
import subprocess
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
FEATURE = """Feature: Thing

  @r1
  Scenario: it answers
    Given nothing

  @r2
  Scenario: it waits
    Given nothing
"""
STEPS = """from pytest_bdd import given, scenarios

scenarios("../features/thing.feature")


@given("nothing")
def nothing():
    pass
"""


def consumer(tmp_path, accepts):
    repo = tmp_path / "consumer"
    for rel, text in {"features/thing.feature": FEATURE, "tests/test_thing.py": STEPS,
                      ".shop/work/i1/w1.md": "---\nkind: work-item\nstatus: claimed\naccepts: [%s]\n---\n" % accepts}.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(text)
    return repo


def pytest(repo, *args):
    env = dict(os.environ, PYTHONPATH=str(SCRIPTS))
    env.pop("PYTEST_PLUGINS", None)
    env.pop("PYTEST_ADDOPTS", None)
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "work_items", *args],
                          cwd=repo, env=env, capture_output=True, text=True)


def test_without_the_option_the_suite_runs_whole(tmp_path):
    done = pytest(consumer(tmp_path, "thing#r1"))
    assert done.returncode == 0 and "2 passed" in done.stdout, done.stdout + done.stderr


TREE_CONFTEST = """import pathlib, sys
SCRIPTS = str(pathlib.Path(__file__).parent / "scripts")
if SCRIPTS in sys.path:
    sys.path.remove(SCRIPTS)
sys.path.insert(0, SCRIPTS)
"""


def _scripts_copy(into):
    import shutil
    into.mkdir(parents=True)
    for source in SCRIPTS.glob("*.py"):
        shutil.copy2(source, into / source.name)


def test_a_tree_whose_conftest_puts_its_scripts_first_is_marked_by_its_own_spec_read(tmp_path):
    """b198: `work batch done` runs a task's suite with the plugin's scripts on PYTHONPATH; the tree's own spec
    modules, which its conftest puts first, are the ones `work_items` marks with."""
    plugin = tmp_path / "plugin"
    _scripts_copy(plugin)
    (plugin / "spec_read.py").write_text("raise ImportError('the plugin\\'s spec_read was imported')\n")
    tree = tmp_path / "tree"
    _scripts_copy(tree / "scripts")
    (tree / "conftest.py").write_text(TREE_CONFTEST)
    (tree / "tests").mkdir()
    (tree / "tests" / "test_one.py").write_text(
        "def test_one():\n    import spec_read\n    assert 'tree' in spec_read.__file__\n")
    env = dict(os.environ, PYTHONPATH=str(plugin))
    env.pop("PYTEST_PLUGINS", None)
    env.pop("PYTEST_ADDOPTS", None)
    done = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "work_items"],
                          cwd=tree, env=env, capture_output=True, text=True)
    assert done.returncode == 0 and "1 passed" in done.stdout, done.stdout + done.stderr
