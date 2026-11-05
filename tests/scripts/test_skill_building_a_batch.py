"""The batch session's skill, building-a-batch (workflow simplification plan 4, Task 9, D2): `work batch` keeps the
state and the session orchestrates, one subagent for each running task, in parallel, with nothing waiting on the
person before the pull request; checked by reading the skill as test_skill_shaping_items.py reads its skills."""
import re

from test_skill_shaping_items import SKILLS, process

SKILL = SKILLS / "building-a-batch" / "SKILL.md"
ORDER = ("work batch start", "work batch resume", "work batch done", "work batch park", "work batch review")


def test_the_process_runs_the_batch_commands_in_order():
    text = "\n".join(process(SKILL))
    at = [text.find(command) for command in ORDER]
    assert -1 not in at and at == sorted(at), dict(zip(ORDER, at))


def test_tasks_are_dispatched_in_parallel_with_their_trailer():
    text = "\n".join(process(SKILL))
    assert "subagent" in text and "worktree" in text and "Item: b" in text
    assert "in parallel" in text or "at once" in text


def test_nothing_waits_on_the_person():
    steps = process(SKILL)
    review = next(n for n, s in enumerate(steps) if "work batch review" in s)
    for step in steps[:review]:
        assert "ask the person" not in step.lower() and "wait for" not in step.lower(), step


def test_description_starts_use_when():
    head = SKILL.read_text().split("---\n")[1]
    assert re.search(r"(?m)^name: building-a-batch$", head), head
    assert re.search(r"(?m)^description: Use when ", head), head


def step(word):
    return next(s for s in process(SKILL) if word in s)


def test_the_subagent_gets_a_brief_of_its_own():
    """Plan 4 review, S4: no `work run` brief or result file; `work batch done` runs the whole suite."""
    text = step("Dispatch")
    assert "no brief or result file" in text and "`work batch done` runs the whole suite" in text, text
    assert "red first" in text and "never edit" in text and "one scenario at a time" in text, text
    assert "tests/scenarios/test_<cap>.py" in text and "@r<n>" in text, text


def test_a_returning_item_cherry_picks_its_old_branch():
    """Plan 4 rulings, Q1."""
    text = step("Dispatch")
    assert "cherry-pick" in text and "notes" in text, text


def test_each_refusal_of_review_has_its_way_through():
    """Plan 4 review, S3, and the rulings' Q2."""
    text = step("work batch review")
    for said in ("conflict", "merge the earlier item's branch", "park one of the two", "tests fail",
                 "push or gh", "safe to run again"):
        assert said in text, (said, text)
