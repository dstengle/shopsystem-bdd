## Budget
No edits in this session. Files touched by the existing commits: scripts/workqueue_done.py, tests/scenarios/work_queue_status_steps.py, tests/scripts/test_workqueue_done.py, features/work-queue.feature (retire only).

# Report w240

The work was already committed on work/w240 by an earlier stage: 86ffc4d3 (three proposal Givens, `merged` dropped from closed proposal statuses, unit test and docstring) and 9799e060 (`features retire` of the two deprecated r23 scenarios). This session made no edits. It re-ran the scenarios on that branch.

Red/green: no red run in this session, because the code was already there. The researcher's red (6 undefined-step failures) is in notes.md.

Suite at start: 1088 passed, 0 failed at 9799e060, with 14 expected xfails (w212, w238, w239 items). The person's answer: the earlier whole-suite failure was a flaky git index.lock (i62/q41), and a rerun passed.

Final run: `python3 -m pytest -q --work-item w240`: 187 passed, 1 skipped, 56 subtests passed. `tests/scripts/test_workqueue_done.py`: 6 passed.

Size check: `tools size --limit 300` printed nothing.

## Tests changed under an allowance
none. The `merged` case of test_an_open_proposal_keeps_the_initiative_from_done was rewritten as the plan lists (§4).

## Open questions
none beyond the plan's §5: no scenario pins `merged` holding an initiative open.

The plan contained no code.

Commits: 86ffc4d3, 9799e060.
