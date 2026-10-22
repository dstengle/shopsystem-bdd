"""scripts/work_items.py, the plugin's `--work-item`: in a repository with no conftest of its own, loaded as work run's
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
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "work_items", *args],
                          cwd=repo, env=env, capture_output=True, text=True)


def test_runs_only_the_accepted_scenarios(tmp_path):
    done = pytest(consumer(tmp_path, "thing#r1"), "--work-item", "w1")
    assert done.returncode == 0 and "1 passed, 1 deselected" in done.stdout, done.stdout + done.stderr


def test_a_range_accepts_each_requirement_in_it(tmp_path):
    done = pytest(consumer(tmp_path, "thing#r1-r2"), "--work-item", "w1")
    assert done.returncode == 0 and "2 passed" in done.stdout, done.stdout + done.stderr


def test_without_the_option_the_suite_runs_whole(tmp_path):
    done = pytest(consumer(tmp_path, "thing#r1"))
    assert done.returncode == 0 and "2 passed" in done.stdout, done.stdout + done.stderr


def test_a_work_item_that_is_not_there_is_refused(tmp_path):
    done = pytest(consumer(tmp_path, "thing#r1"), "--work-item", "w9")
    assert done.returncode != 0 and "no such work-item" in done.stdout + done.stderr, done.stdout + done.stderr


def test_a_work_item_none_of_whose_scenarios_are_collected_is_refused(tmp_path):
    done = pytest(consumer(tmp_path, "other#r1"), "--work-item", "w1")
    assert done.returncode != 0 and "w1 accepts none of the scenarios it collected" in done.stdout + done.stderr, done.stdout + done.stderr


def test_a_test_that_is_not_a_scenario_is_kept(tmp_path):
    repo = consumer(tmp_path, "other#r1")
    (repo / "test_probe.py").write_text("def test_probe():\n    pass\n")
    done = pytest(repo, "--work-item", "w1", "test_probe.py")
    assert done.returncode == 0 and "1 passed" in done.stdout, done.stdout + done.stderr


def test_a_non_scenario_does_not_save_a_run_whose_scenarios_are_all_unaccepted(tmp_path):
    repo = consumer(tmp_path, "other#r1")
    (repo / "test_probe.py").write_text("def test_probe():\n    pass\n")
    done = pytest(repo, "--work-item", "w1")
    assert done.returncode != 0 and "accepts none of the scenarios" in done.stdout + done.stderr, done.stdout + done.stderr


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
