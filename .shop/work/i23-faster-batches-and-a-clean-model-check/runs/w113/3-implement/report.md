## Budget

- scripts/workqueue_answer.py
- tests/scenarios/work_queue_answer_steps.py
- features/work-queue.feature (only `features retire`)
- tests/scenarios/test_work_queue.py (outside the file set: setup only, see below)

## Outside the file set

tests/scenarios/test_work_queue.py: the Given "whose work-item w1 is ready" wrote no log.jsonl, so the shared Then "... are as they were" raised FileNotFoundError on the scenario "two lines to a work-item not awaiting-answer". The Given now writes a planned->ready log line for a ready item when the initiative has no log yet.

## Changes

- workqueue_answer.py: LINE_BREAKS (the seven code points of r15); the check runs first in `answer()`; message "the answer has a line break in it; an answer is one line".
- work_queue_answer_steps.py: new When "... with an answer of two lines broken by {line_break}"; the old step removed.
- `features retire` of the deprecated scenario.

## Runs

- Red (after the step, before the code): 7 failed (VT, FF, NEL, LS, PS, the order scenario, and the deprecated scenario whose step I removed); the Then on exit/stderr or "as they were" failed, as expected (answer exited 0 for the new breaks; ready item refused for status first).
- Order scenario still red after code: FileNotFoundError on log.jsonl (setup, fixed above).
- Final: `python3 -m pytest -q --work-item w113`: 144 passed, 1 skipped. test_work_queue.py and test_supervision.py: 8 passed.
- Suite at start (brief): 687 passed, 8 failed (7 of them these scenarios); not rerun.
- size: nothing over 300.

## Tests changed under an allowance

- tests/scenarios/test_work_queue.py, with_items (Given): setup, writes a log for a ready item.

## Open questions

FS/GS/RS in an answer land, and `supervise.held` (splitlines) would split them; old answers with VT/FF/NEL/LS/PS still split under held; an empty answer lands as an empty bullet; a trailing break is refused. No scenario covers them.

The plan contained no code.

## Result
Someone can now give `work answer` no answer with any of the seven line breaks, and the one-line refusal comes before other refusals.
