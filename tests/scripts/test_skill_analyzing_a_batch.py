"""analyzing-a-batch measures a batch (workflow simplification plan 7, Task 5, D14, D16), checked by reading the skill:
its process runs `measure batch`, `show` and `compare` by batch name, judges the defects, and makes a candidate that
changes a knob a decision; an initiative of the old queue is still measured until plan 9."""
from test_skill_shaping_items import SKILLS, process

SKILL = SKILLS / "analyzing-a-batch" / "SKILL.md"


def test_it_measures_a_batch():
    steps = "\n".join(process(SKILL))
    for words in ("measure batch <batch>", "measure show", "measure compare <earlier batch> <batch>", "cost by role",
                  "defect"):
        assert words in steps, words


def test_a_candidate_that_changes_a_knob_is_a_decision():
    assert "a-knob-is-changed-by-a-decision" in SKILL.read_text()


def test_an_initiative_is_still_measured_until_plan_9():
    assert "measure initiative" in SKILL.read_text()


def test_it_reads_the_measurement_building_a_batch_wrote():
    """Plan 7 review M8: building-a-batch measures the batch; this skill measures it only when nothing did."""
    step = process(SKILL)[0]
    assert "the measurement building-a-batch wrote" in step and "only when there is none" in step, step
