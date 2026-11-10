"""The batch session's skill, building-a-batch (workflow simplification plan 4, Task 9, D2): `work batch` keeps the
state and the session orchestrates, one subagent for each running task, in parallel, with nothing waiting on the
person before the pull request, then the pull request's one review by `pr-reviewer` and its fixes (plan 5, Task 6,
pr-review r1, r2); checked by reading the skill as test_skill_shaping_items.py reads its skills."""
import re

import pytest
from test_skill_shaping_items import SKILLS, process

SKILL = SKILLS / "building-a-batch" / "SKILL.md"
ORDER = ("work batch start", "work batch resume", "work batch done", "work batch park", "work batch review",
         "work batch brief", "work batch reviewed")


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


def test_the_subagent_reads_the_judgement_decisions():
    """Plan 6, D15: the batch's tasks are its plan, and the judgement decisions go to it as context."""
    text = step("Dispatch")
    assert "tier: judgement" in text, text


def review_step():
    """The first step naming `pr-reviewer`."""
    return next(n for n, s in enumerate(process(SKILL)) if "pr-reviewer" in s)


@pytest.mark.requirement("pr-review#r1")
def test_r1_the_published_pull_request_is_reviewed():
    steps = process(SKILL)
    publish = next(n for n, s in enumerate(steps) if "work batch review" in s)
    at = review_step()
    assert at > publish, (at, publish)
    text = steps[at]
    found = [text.find(said) for said in ("work batch brief", "pr-reviewer", "work batch reviewed")]
    assert -1 not in found and found == sorted(found), found


@pytest.mark.requirement("pr-review#r10")
def test_r10_no_review_after_a_task():
    for one in process(SKILL):
        if "work batch done" in one:
            assert "pr-reviewer" not in one and "work batch brief" not in one, one


def test_the_fix_loop_cites_item_and_finding():
    text = process(SKILL)[review_step()]
    for said in ("Item: b", "Finding: f", "work batch resume"):
        assert said in text, (said, text)
    assert "at once" in text or "in parallel" in text, text


def test_the_review_loop_asks_nothing():
    text = process(SKILL)[review_step()].lower()
    assert "ask the person" not in text and "wait for" not in text, text


def test_each_refusal_of_the_review_loop_has_its_way_through():
    """Plan 5 review, S3, M3, and the rulings' Q1 and Q3."""
    text = process(SKILL)[review_step()]
    for said in ("A refused `reviewed`", "run `work batch brief` again", "a fresh `pr-reviewer`",
                 "never edit the findings file",                          # S3: a malformed findings file
                 "byte for byte at the brief's `Findings file:` path",    # plan 7 B1: the reply saved
                 "Saving is not editing",
                 "no item is left in-batch", "work batch abandon",        # S3: every item parked
                 ".shop/batches/<n>/review-<k>.md",                       # S3: where a finding's text is
                 '--trailer "Item: b<j>" --trailer "Finding: f<m>"',      # M3
                 "another item's open finding",                           # Q1: a merged-in fix
                 "work idea"):                                            # Q3: an observation
        assert said in text, (said, text)


def test_each_subagent_is_described_for_its_role():
    """Plan 7, D14: the descriptions `measure batch` reads a subagent's role from."""
    text = SKILL.read_text()
    for words in ("batch-<n> t<k> b<j>", "batch-<n> review <k>", "batch-<n> fix f<m>"):
        assert words in text, words


def test_a_merged_batch_is_measured():
    text = SKILL.read_text()
    merged = text.index("work batch merged <batch>")
    assert "measure batch <batch>" in text[merged:], text[merged:]


def test_an_abandoned_batch_is_measured_too():
    """Plan 7 review M8: this skill runs `measure batch`, after `merged` and after `abandon`."""
    text = SKILL.read_text()
    abandon = text.index("work batch abandon <batch>")
    assert "measure batch <batch>" in text[abandon:abandon + 300], text[abandon:abandon + 300]
