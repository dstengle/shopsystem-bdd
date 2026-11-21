"""scripts/work_items.py under `work batch start`'s run of the laid lines' scenarios (batch_laid, b488):
`$SHOPSYSTEM_LAID` keeps only the unbuilt scenarios of the ids it names, and each that passes, non-strict, is written
to `$SHOPSYSTEM_LAID_REPORT` with its ids and title, once, with xdist and without."""
import os
import pathlib
import subprocess
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
CAPABILITY = """---
id: capability/ex.com/prod/ctx/thing
title: Thing
narrator: the person
group: service
language: codified-1
retired: []
unbuilt: [r1, r2]
---

# Thing

## Behaviour

### [g1] one
- [r1] `work` shall print the queue.

### [g2] two
- [r2] `work` shall commit the queue.
"""
FEATURE = """Feature: Thing

  @r1
  Scenario: it answers
    Given nothing

  @r2
  Scenario: it waits
    Given nothing

  @r3
  Scenario: it is built
    Given nothing
"""
STEPS = """from pytest_bdd import given, scenarios

scenarios("../features/thing.feature")


@given("nothing")
def nothing():
    pass
"""


def consumer(tmp_path):
    repo = tmp_path / "consumer"
    for rel, text in {"spec/capabilities/thing.md": CAPABILITY, "features/thing.feature": FEATURE,
                      "tests/test_thing.py": STEPS}.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(text)
    return repo


@pytest.mark.parametrize("workers", [[], ["-n", "2"]])
def test_only_the_laid_scenarios_run_and_each_that_passes_is_reported(tmp_path, workers):
    repo = consumer(tmp_path)
    report = tmp_path / "passed"
    env = dict(os.environ, PYTHONPATH=str(SCRIPTS), SHOPSYSTEM_LAID="thing#r2",
               SHOPSYSTEM_LAID_REPORT=str(report), SHOPSYSTEM_UNBUILT_NONSTRICT=str(repo))
    for name in ("PYTEST_PLUGINS", "PYTEST_ADDOPTS", "PYTEST_XDIST_WORKER"):
        env.pop(name, None)
    done = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "work_items",
                           *workers], cwd=repo, env=env, capture_output=True, text=True)
    summary = done.stdout.strip().splitlines()[-1]       # xdist's controller counts no deselected
    assert done.returncode == 0 and "1 xpassed" in summary and " passed" not in summary, (
        done.stdout + done.stderr)
    assert report.read_text().splitlines() == ["thing#r2\tit waits"]


def test_without_the_variable_nothing_is_deselected_or_reported(tmp_path):
    repo = consumer(tmp_path)
    env = dict(os.environ, PYTHONPATH=str(SCRIPTS), SHOPSYSTEM_UNBUILT_NONSTRICT=str(repo))
    for name in ("PYTEST_PLUGINS", "PYTEST_ADDOPTS", "SHOPSYSTEM_LAID", "SHOPSYSTEM_LAID_REPORT"):
        env.pop(name, None)
    done = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "work_items"],
                          cwd=repo, env=env, capture_output=True, text=True)
    assert done.returncode == 0 and "1 passed, 2 xpassed" in done.stdout, done.stdout + done.stderr
