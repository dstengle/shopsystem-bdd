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
    env.pop("PYTEST_ADDOPTS", None)
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


def capabilities(repo, **groups):
    for cap, guarantees in groups.items():
        path = repo / "spec" / "capabilities" / ("%s.md" % cap)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\nkind: capability\n%s---\n" % ("group: guarantees\n" if guarantees else ""))


def test_a_guarantees_work_item_has_its_scenarios_deselected_and_exits_successfully(tmp_path):
    repo = consumer(tmp_path, "other#r1")
    capabilities(repo, other=True)
    done = pytest(repo, "--work-item", "w1")
    assert done.returncode == 0 and "2 deselected" in done.stdout, done.stdout + done.stderr


def test_a_guarantees_work_item_left_with_no_test_exits_successfully_under_xdist(tmp_path):
    repo = consumer(tmp_path, "other#r1")
    capabilities(repo, other=True)
    done = pytest(repo, "-n", "2", "--work-item", "w1")
    assert done.returncode == 0, done.stdout + done.stderr


def test_a_guarantees_work_item_keeps_a_test_that_is_not_a_scenario(tmp_path):
    repo = consumer(tmp_path, "other#r1")
    capabilities(repo, other=True)
    (repo / "test_probe.py").write_text("def test_probe():\n    pass\n")
    done = pytest(repo, "--work-item", "w1")
    assert done.returncode == 0 and "1 passed, 2 deselected" in done.stdout, done.stdout + done.stderr


def test_one_requirement_outside_a_guarantees_capability_refuses_the_run(tmp_path):
    repo = consumer(tmp_path, "other#r1, mixed#r1")
    capabilities(repo, other=True, mixed=False)
    done = pytest(repo, "--work-item", "w1")
    assert done.returncode != 0 and "w1 accepts none of the scenarios it collected" in done.stdout + done.stderr


def test_a_failed_scenario_is_named_in_the_summary_and_a_failed_test_that_is_not_one_is_not(tmp_path):
    repo = consumer(tmp_path, "thing#r1-r2")
    (repo / "tests/test_thing.py").write_text(STEPS.replace("    pass", "    assert False"))
    (repo / "test_probe.py").write_text("def test_probe():\n    assert False\n")
    done = pytest(repo, "--work-item", "w1")
    lines = (done.stdout + done.stderr).splitlines()
    named = [l for l in lines if l.startswith("SCENARIO ")]
    assert sorted(named) == ["SCENARIO tests/test_thing.py::test_it_answers",
                             "SCENARIO tests/test_thing.py::test_it_waits"], done.stdout
    assert not [l for l in named if "probe" in l]


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


GENERATED = """# generated from spec/capabilities/thing.md by features generate; do not edit
Feature: Thing

  @g1 @r1
  Scenario: it answers
    Given nothing

  @g2
  Scenario: it waits
    Given nothing
"""
CODIFIED = """---
id: capability/example.org/fixture/thing
group: service
language: codified-1
---

# Thing

## Behaviour

### [g1] it answers
- [r1] `thing` shall answer.

### [g2] it waits
- [r2] `thing` shall wait.
- [r3] `thing` shall wait again.

### [g3] it holds
- [r4] `thing` shall hold at most `workers` worker slots at a time.
"""


def codified(tmp_path, accepts, retires=False):
    repo = consumer(tmp_path, accepts)
    (repo / "features" / "thing.feature").write_text(GENERATED)
    (repo / "spec" / "capabilities").mkdir(parents=True)
    (repo / "spec" / "capabilities" / "thing.md").write_text(CODIFIED)
    if retires:
        item = repo / ".shop/work/i1/w1.md"
        item.write_text(item.read_text() + "\n# thing: retire thing\n\n## Retires\n\n- \"the code\" (thing @r9)\n")
    return repo


def test_a_group_accepted_runs_its_scenario(tmp_path):
    done = pytest(codified(tmp_path, "thing#g2"), "--work-item", "w1")
    assert done.returncode == 0 and "1 passed, 1 deselected" in done.stdout, done.stdout + done.stderr


def test_a_range_of_groups_runs_each_scenario(tmp_path):
    done = pytest(codified(tmp_path, "thing#g1-g2"), "--work-item", "w1")
    assert done.returncode == 0 and "2 passed" in done.stdout, done.stdout + done.stderr


def test_a_requirement_runs_the_scenario_of_its_group_in_the_spec(tmp_path):
    done = pytest(codified(tmp_path, "thing#r3"), "--work-item", "w1")
    assert done.returncode == 0 and "1 passed, 1 deselected" in done.stdout, done.stdout + done.stderr


def test_a_requirement_of_a_group_with_no_scenario_is_like_a_guarantee(tmp_path):
    done = pytest(codified(tmp_path, "thing#r4"), "--work-item", "w1")
    assert done.returncode == 0 and "2 deselected" in done.stdout, done.stdout + done.stderr


def test_a_work_item_that_only_retires_runs_the_whole_suite(tmp_path):
    repo = codified(tmp_path, "", retires=True)
    (repo / "test_probe.py").write_text("def test_probe():\n    pass\n")
    done = pytest(repo, "--work-item", "w1")
    assert done.returncode == 0 and "3 passed" in done.stdout, done.stdout + done.stderr
