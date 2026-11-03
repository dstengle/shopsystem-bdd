"""`features generate` (design §14.2, §13.4): one scenario a group, witnesses by rule, the `given` block, and the exit
codes of a codified, an uncodified and a broken capability."""
import pathlib
import shutil
import subprocess
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FEATURES = REPO / "scripts" / "features"
FIXTURES = REPO / "tests" / "scripts" / "fixtures" / "generate"

WORK_QUEUE = '''\
# generated from spec/capabilities/work-queue.md by features generate; do not edit
Feature: Work queue
  Narrator: the person

  @g1 @r1 @r2
  Scenario: `work start` starts a proposed initiative
    Given an initiative i1 that is `proposed`
    When the person runs `work start` on the initiative i1
    Then the initiative i1 is `started`
    And `work` exits successfully

  @g2 @r3
  Scenario: `work start` refuses an initiative that is not proposed
    Given an initiative i1 that is `started`
    When the person runs `work start` on the initiative i1
    Then `work` exits with an error naming the status of the initiative i1

  @g3 @r4
  Scenario: `work list` prints the open work-items
    Given the file `spec/index.md` holds:
      | term | category |
      | initiative | kind |
    And the file `notes.md` holds:
      """
      The first line.
      The second line.
      """
    And a work-item w1 that is `drafted`
    And a work-item w2 that is `green`
    And a work-item w3 that is `withdrawn`
    When the person runs `work list`
    Then `work` prints the work-item w1
    And `work` does not print the work-item w2
    And `work` does not print the work-item w3
'''

G1 = '''\
  @g1 @r1 @r2
  Scenario: `work run` with no initiative takes the open initiatives side by side
    Given an initiative i1 that is `proposed`
    And an initiative i2 that is `proposed`
    And an initiative i3 that is `done`
    And an initiative i4 that is `abandoned`
    When the person runs `work run`
    Then `work run` takes the initiative i1
    And `work run` takes the initiative i2
    And `work run` does not take the initiative i3
    And `work run` does not take the initiative i4
    And `work run` interleaves the initiative i1
    And `work run` interleaves the initiative i2
'''


@pytest.fixture
def repo(tmp_path):
    toolchain.require()
    shutil.copytree(FIXTURES / "repo", tmp_path / "repo")
    return tmp_path / "repo"


def features(root, *args):
    return subprocess.run([sys.executable, str(FEATURES), *args], cwd=root, capture_output=True, text=True)


def generated(root, name):
    return (root / "features" / ("%s.feature" % name)).read_text()


def test_a_codified_capability_generates_the_same_bytes_twice(repo):
    first = features(repo, "generate", "work-queue")
    assert first.returncode == 0, first.stderr
    text = generated(repo, "work-queue")
    assert text == WORK_QUEUE
    again = features(repo, "generate", "work-queue")
    assert again.returncode == 0, again.stderr
    assert generated(repo, "work-queue") == text


def test_editing_one_group_changes_only_that_scenarios_lines(repo):
    assert features(repo, "generate", "work-queue").returncode == 0
    before = generated(repo, "work-queue").splitlines()
    cap = repo / "spec" / "capabilities" / "work-queue.md"
    cap.write_text(cap.read_text().replace("naming the status of the initiative.", "naming the reason."))
    assert features(repo, "generate", "work-queue").returncode == 0
    after = generated(repo, "work-queue").splitlines()
    start, end = before.index("  @g2 @r3"), before.index("  @g3 @r4")
    assert before[:start] == after[:start]
    assert before[end:] == after[after.index("  @g3 @r4"):]
    changed = [line for line in after[start:after.index("  @g3 @r4")] if line not in before]
    assert changed == ["    Then `work` exits with an error naming the reason"]


def test_check_exits_1_after_a_hand_edit_and_0_when_every_file_matches(repo):
    (repo / "spec" / "capabilities" / "legacy.md").unlink()
    assert features(repo, "generate", "work-queue", "supervision").returncode == 0
    clean = features(repo, "generate", "--check")
    assert clean.returncode == 0, clean.stdout + clean.stderr
    path = repo / "features" / "work-queue.feature"
    path.write_text(path.read_text().replace("exits successfully", "exits happily"))
    edited = features(repo, "generate", "--check")
    assert edited.returncode == 1
    assert "features/work-queue.feature" in edited.stdout


def test_naming_an_uncodified_capability_exits_2_and_writes_nothing(repo):
    done = features(repo, "generate", "work-queue", "legacy")
    assert done.returncode == 2
    assert "spec/capabilities/legacy.md is not codified: run `migrate upgrade`" in done.stderr
    assert not (repo / "features").exists() or not list((repo / "features").iterdir())
    assert features(repo, "generate", "--check", "legacy").returncode == 2


def test_check_with_no_names_refuses_an_uncodified_service_capability(repo):
    assert features(repo, "generate", "work-queue", "supervision").returncode == 0
    done = features(repo, "generate", "--check")
    assert done.returncode == 2, done.stdout + done.stderr
    assert "spec/capabilities/legacy.md is not codified: run `migrate upgrade`" in done.stderr


def test_the_spikes_g1_gives_the_four_initiative_witness(repo):
    assert features(repo, "generate", "supervision").returncode == 0
    assert G1 in generated(repo, "supervision")


def test_an_if_group_gives_the_invalid_input(repo):
    assert features(repo, "generate", "work-queue").returncode == 0
    block = generated(repo, "work-queue").split("  @g2 @r3")[1].split("  @g3")[0]
    assert "    Given an initiative i1 that is `started`\n" in block


def test_a_logic_only_group_has_no_scenario_and_a_response_np_is_kept(repo):
    assert features(repo, "generate", "supervision").returncode == 0
    text = generated(repo, "supervision")
    assert "@g2" not in text
    assert ("    Given a stage s1\n    When `work run` starts the stage s1\n"
            "    Then `work run` gives the stage s1 only a brief\n") in text


def test_preview_prints_a_draft_and_writes_nothing(repo, tmp_path):
    draft = tmp_path / "draft.md"
    draft.write_text((repo / "spec" / "capabilities" / "work-queue.md").read_text())
    done = features(repo, "generate", "--preview", str(draft))
    assert done.returncode == 0, done.stderr
    assert done.stdout == WORK_QUEUE.replace("work-queue.md", "draft.md")
    assert not (repo / "features").exists()


def test_a_guarantees_capability_has_no_feature(repo):
    done = features(repo, "generate", "review")
    assert done.returncode == 2
    assert "guarantees" in done.stderr


def test_a_requirement_that_does_not_parse_is_refused_naming_it(tmp_path):
    toolchain.require()
    shutil.copytree(FIXTURES / "broken", tmp_path / "broken")
    done = features(tmp_path / "broken", "generate", "thing")
    assert done.returncode == 1
    assert "thing#r2" in done.stderr
    assert not (tmp_path / "broken" / "features").exists()


def test_check_on_the_live_repo_matches_every_capability():
    toolchain.require()
    done = features(REPO, "generate", "--check")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "skipped" not in done.stdout
