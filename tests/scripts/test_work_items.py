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


def test_a_move_to_a_status_outside_the_lifecycle_is_refused(tmp_path):
    sys.path.insert(0, str(SCRIPTS))
    import workqueue
    item = tmp_path / ".shop/work/i1/w1.md"
    item.parent.mkdir(parents=True)
    item.write_text("---\nkind: work-item\nstatus: drafted\n---\n")
    try:
        workqueue.move(tmp_path, "i1", "w1", "finished", by="someone")
    except workqueue.Refused as refused:
        assert "finished is no status" in str(refused)
    else:
        raise AssertionError("moved to finished")
    assert "status: drafted" in item.read_text() and not (item.parent / "log.jsonl").exists()
