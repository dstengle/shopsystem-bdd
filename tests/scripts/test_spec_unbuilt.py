"""spec_unbuilt: a codified capability's `unbuilt: [r<n>, ...]` read, an id it has no requirement for reported as a
problem, and the strict xfail put on the scenarios of the listed requirements (workflow simplification plan 1)."""
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import spec_unbuilt

HEAD = """---
id: capability/ex.com/prod/ctx/demo
title: Demo
narrator: the person
group: service
language: codified-1
retired: []
%s---

# Demo

## Behaviour

### [g1] one
- [r1] `work` shall print the queue.

### [g2] two
- [r2] `work` shall commit the queue.
"""


def root_with(tmp_path, field="", name="demo"):
    caps = tmp_path / "spec" / "capabilities"
    caps.mkdir(parents=True, exist_ok=True)
    (caps / ("%s.md" % name)).write_text(HEAD % field)
    return tmp_path


class Item:
    def __init__(self, feature, tags):
        scenario = SimpleNamespace(feature=SimpleNamespace(filename="/x/features/%s" % feature), tags=set(tags))
        self.function = SimpleNamespace(__scenario__=scenario)
        self.markers = []

    def add_marker(self, marker):
        self.markers.append(marker)


def test_unbuilt_reads_the_listed_ids(tmp_path):
    assert spec_unbuilt.unbuilt(root_with(tmp_path, "unbuilt: [r2]\n")) == {"demo": {"r2"}}


def test_a_capability_without_unbuilt_marks_nothing(tmp_path):
    root = root_with(tmp_path)
    assert spec_unbuilt.unbuilt(root) == {}
    item = Item("demo.feature", ["g1", "r1"])
    spec_unbuilt.mark([item], root)
    assert item.markers == []


def test_an_unbuilt_id_the_capability_lacks_is_a_problem(tmp_path):
    root = root_with(tmp_path, "unbuilt: [r9]\n")
    assert spec_unbuilt.problems(root) == ["demo: unbuilt r9 is no requirement of the capability"]
    assert spec_unbuilt.unbuilt(root) == {}


def test_an_unbuilt_on_a_capability_that_is_not_codified_is_a_problem(tmp_path):
    root = root_with(tmp_path)
    (root / "spec" / "capabilities" / "old.md").write_text((HEAD % "unbuilt: [r1]\n").replace(
        "language: codified-1\n", ""))
    assert spec_unbuilt.problems(root) == ["old: unbuilt is given on a capability that is not codified"]
    assert spec_unbuilt.unbuilt(root) == {}


def test_the_repository_lists_no_unbuilt_id_it_lacks():
    assert spec_unbuilt.problems(REPO) == []


def test_mark_leaves_the_same_id_of_another_capability_alone(tmp_path):
    root = root_with(root_with(tmp_path, "unbuilt: [r2]\n"), name="other")
    other = Item("other.feature", ["g2", "r2"])
    spec_unbuilt.mark([other], root)
    assert other.markers == []


def test_mark_adds_a_strict_xfail(tmp_path):
    root = root_with(tmp_path, "unbuilt: [r2]\n")
    built, unbuilt = Item("demo.feature", ["g1", "r1"]), Item("demo.feature", ["g2", "r2"])
    spec_unbuilt.mark([built, unbuilt, SimpleNamespace()], root)
    assert built.markers == []
    assert len(unbuilt.markers) == 1
    marker = unbuilt.markers[0].mark
    assert marker.name == "xfail"
    assert marker.kwargs == {"strict": True, "reason": "unbuilt: demo#r2"}


CONFTEST = """import sys
sys.path.insert(0, %r)
import spec_unbuilt


def pytest_collection_modifyitems(config, items):
    spec_unbuilt.mark(items, config.rootpath)
"""

PASSING = """from types import SimpleNamespace


def test_built():
    pass


test_built.__scenario__ = SimpleNamespace(feature=SimpleNamespace(filename="/x/features/demo.feature"), tags={"r2"})
"""


def test_an_unbuilt_scenario_that_passes_fails_the_run(tmp_path):
    root = root_with(tmp_path, "unbuilt: [r2]\n")
    (root / "conftest.py").write_text(CONFTEST % str(REPO / "scripts"))
    (root / "test_demo.py").write_text(PASSING)
    done = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_demo.py"], cwd=root,
                          capture_output=True, text=True)
    assert done.returncode == 1, done.stdout + done.stderr
    assert "XPASS(strict)" in done.stdout


FEATURE = """# generated from spec/capabilities/demo.md by features generate; do not edit
Feature: Demo

  @g1 @r1
  Scenario: one
    When the person runs `work list`
    Then `work` prints the queue

  @g2 @r2
  Scenario: two
    When the person runs `work list`
    Then `work` commits the queue
"""


def test_the_steps_of_an_unbuilt_scenario_are_its_lines(tmp_path):
    root = root_with(tmp_path, "unbuilt: [r2]\n")
    feature = tmp_path / "demo.feature"
    feature.write_text(FEATURE)
    assert spec_unbuilt.unbuilt_lines(feature, root) == {9, 10, 11, 12}
    assert spec_unbuilt.unbuilt_lines(tmp_path / "other.feature", root) == set()


def test_with_unbuilt_appends_and_inserts(tmp_path):
    """plan 4, Task 2: the ids a batch lays appended to `unbuilt:`, once each; the key made after `retired:`."""
    text = HEAD % "unbuilt: [r1]\n"
    assert "unbuilt: [r1, r2]\n" in spec_unbuilt.with_unbuilt(text, ["r2", "r1", "r2"])
    made = spec_unbuilt.with_unbuilt(HEAD % "", ["r2"])
    assert "retired: []\nunbuilt: [r2]\n---" in made
    caps = tmp_path / "spec" / "capabilities"
    caps.mkdir(parents=True)
    (caps / "demo.md").write_text(made)
    assert spec_unbuilt.unbuilt(tmp_path) == {"demo": {"r2"}}
