"""`features generate` (design-r3 §5): one scenario a group read off its requirements' facts, no solver, the example data of its `given` block
(any other given line left out with a line on stderr), and the exit codes of a codified, an uncodified and a broken
capability."""
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

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
    Given an initiative i1
    And the initiative i1 is not `proposed`
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
    And a work-item w1
    And the work-item w1 is not `green`
    And the work-item w1 is not `withdrawn`
    And a work-item w2 that is `green`
    When the person runs `work list`
    Then `work` prints the work-item w1
    And `work` does not print the work-item w2
'''

G1 = [
    "  @g1 @r1 @r2",
    "  Scenario: `work run` with no initiative takes the open initiatives side by side",
    "    Given an initiative i1",
    "    And the initiative i1 is not `done`",
    "    And the initiative i1 is not `abandoned`",
    "    And an initiative i2 that is `done`",
    "    When the person runs `work run`",
    "    Then `work run` takes the initiative i1",
    "    And `work run` does not take the initiative i2",
]


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
    assert changed == ["    Then `work` exits with an error naming the reason r1"]


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


def test_an_every_response_gives_one_contrast_by_rule(repo):
    """`take every initiative whose status is not done or abandoned`: one more initiative with the first value the
    restriction excludes, and its absent response a `does not` Then (design-r3 §5 rule 5)."""
    assert features(repo, "generate", "supervision").returncode == 0
    lines = generated(repo, "supervision").split("\n\n")[1].splitlines()
    assert lines[:len(G1)] == G1
    assert all(line.startswith("    And ") for line in lines[len(G1):])
    assert not any("i3" in line for line in lines)


def test_an_if_group_states_the_restriction_it_excludes(repo):
    assert features(repo, "generate", "work-queue").returncode == 0
    block = generated(repo, "work-queue").split("  @g2 @r3")[1].split("  @g3")[0]
    assert "    Given an initiative i1\n    And the initiative i1 is not `proposed`\n" in block


def test_a_given_line_that_is_not_example_data_is_left_out_with_one_line_on_stderr(repo):
    done = features(repo, "generate", "work-queue")
    assert done.returncode == 0, done.stderr
    assert done.stderr.count("\n") == 1
    assert "work-queue#g1" in done.stderr and "an initiative i1 that is `proposed`" in done.stderr
    block = generated(repo, "work-queue").split("  @g1 @r1 @r2")[1].split("  @g2")[0]
    assert block.count("an initiative i1 that is `proposed`") == 1


def test_a_logic_only_group_has_no_scenario(repo):
    assert features(repo, "generate", "supervision").returncode == 0
    text = generated(repo, "supervision")
    assert "@g2" not in text
    assert "    When `work run` starts the stage s1\n" in text


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


def test_a_service_capability_with_no_group_has_no_feature(repo):
    """Plan 9, D4: a codified service capability whose every line is retired has no feature file."""
    (repo / "spec" / "capabilities" / "legacy.md").unlink()
    (repo / "spec" / "capabilities" / "x.md").write_text(
        "---\nid: capability/example.org/fixture/x\ntitle: X\nnarrator: the person\ngroup: service\n"
        "language: codified-1\nrests_on: []\nretired: [r1]\n---\n\n# X\n\n## Purpose\nRetired.\n\n## Behaviour\n\n"
        "## Not yet\n- None.\n")
    (repo / "features").mkdir(exist_ok=True)
    (repo / "features" / "x.feature").write_text("# generated from spec/capabilities/x.md by features generate; do not edit\n"
                                                 "Feature: X\n  Narrator: the person\n")
    check = features(repo, "generate", "--check", "x")
    assert check.returncode == 1, check.stdout + check.stderr
    assert "differs: features/x.feature" in check.stdout
    done = features(repo, "generate", "x")
    assert done.returncode == 0, done.stderr
    assert "removed features/x.feature" in done.stdout
    assert not (repo / "features" / "x.feature").exists()
    assert features(repo, "generate", "--check", "x").returncode == 0


def test_a_requirement_that_does_not_parse_is_refused_naming_it(tmp_path):
    toolchain.require()
    shutil.copytree(FIXTURES / "broken", tmp_path / "broken")
    done = features(tmp_path / "broken", "generate", "thing")
    assert done.returncode == 1
    assert "thing#r2" in done.stderr
    assert not (tmp_path / "broken" / "features").exists()


def test_byte_stable_under_two_hash_seeds(repo):
    texts = []
    for seed in ("1", "2"):
        done = subprocess.run([sys.executable, str(FEATURES), "generate", "--preview",
                               str(repo / "spec" / "capabilities" / "supervision.md")], cwd=repo, capture_output=True,
                              text=True, env=dict(os.environ, PYTHONHASHSEED=seed))
        assert done.returncode == 0, done.stderr
        texts.append(done.stdout)
    assert texts[0] == texts[1]


def test_generation_imports_no_solver():
    text = (REPO / "scripts" / "features_generate.py").read_text() + (REPO / "scripts" / "spec_steps.py").read_text()
    assert not re.search(r"spec_solve|spec_trace\b|spec_engine|telingo|clingo\.Control", text)


def test_check_on_the_live_repo_is_fast_and_clean():
    """Every live service capability is read off its requirements' facts without a crash, in under 5 s with the parse
    cache warm (a run over 5 s is taken again, once, since it may have warmed the cache); the checked-in features
    may differ until layer 4 regenerates them."""
    toolchain.require()
    for _ in range(2):
        start = time.monotonic()
        done = features(REPO, "generate", "--check")
        took = time.monotonic() - start
        if took < 5:
            break
    assert done.returncode in (0, 1), done.stdout + done.stderr
    assert "Traceback" not in done.stderr
    assert took < 5, "features generate --check took %.1f s" % took


def test_byte_stable(tmp_path):
    """design-r3 §5: every live service capability's feature is the same bytes under two hash seeds."""
    toolchain.require()
    procs = {}
    for seed in ("1", "2"):
        shutil.copytree(REPO / "spec", tmp_path / seed / "spec")
        procs[seed] = subprocess.Popen([sys.executable, str(FEATURES), "generate"], cwd=tmp_path / seed,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                       env=dict(os.environ, PYTHONHASHSEED=seed))
    for proc in procs.values():
        _, err = proc.communicate(timeout=120)
        assert proc.returncode == 0, err
    texts = [{p.name: p.read_bytes() for p in (tmp_path / seed / "features").glob("*.feature")} for seed in procs]
    assert texts[0] and texts[0] == texts[1]


def test_a_glossary_in_plugin_2_categories_is_refused_naming_each_term_and_its_label(repo):
    index = repo / "spec" / "index.md"
    index.write_text(index.read_text().replace("(proper noun)", "(actor)").replace("(noun)", "(kind)"))
    done = features(repo, "generate", "work-queue")
    assert done.returncode == 1, done.stderr
    assert "Traceback" not in done.stderr
    assert "initiative (kind) is written (noun)" in done.stderr
    assert "the person (actor) is written (proper noun)" in done.stderr
    assert not (repo / "features").exists()
