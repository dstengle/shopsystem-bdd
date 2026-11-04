"""spec_unbuilt: a codified capability's `unbuilt: [r<n>, ...]` read, an id it has no requirement for reported as a
problem, and the non-strict xfail put on the scenarios of the listed requirements (workflow simplification plan 1)."""
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

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


def root_with(tmp_path, field=""):
    caps = tmp_path / "spec" / "capabilities"
    caps.mkdir(parents=True)
    (caps / "demo.md").write_text(HEAD % field)
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


def test_mark_adds_a_non_strict_xfail(tmp_path):
    root = root_with(tmp_path, "unbuilt: [r2]\n")
    built, unbuilt = Item("demo.feature", ["g1", "r1"]), Item("demo.feature", ["g2", "r2"])
    spec_unbuilt.mark([built, unbuilt, SimpleNamespace()], root)
    assert built.markers == []
    assert len(unbuilt.markers) == 1
    marker = unbuilt.markers[0].mark
    assert marker.name == "xfail"
    assert marker.kwargs == {"strict": False, "reason": "unbuilt: demo#r2"}


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
