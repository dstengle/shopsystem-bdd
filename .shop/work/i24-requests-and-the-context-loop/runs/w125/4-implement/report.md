# Report w125

## Budget
No files touched: commit 3cb355a (scripts/work_items.py, tests/scripts/test_work_items.py) already holds the change.

## What I found
The branch starts at 3cb355a "work_items: decide r65's exit from the work-item and spec at session end, on controller and workers". It has the fix and the -n 2 test `test_a_guarantees_work_item_left_with_no_test_exits_successfully_under_xdist`. I made no edit, so I ran no red.

## Runs
Suite record at start: 761 passed, 13 failed at 3cb355a. The 13 failures were scenarios of phases B and C, which other open work-items (w126-w145) accept. The coordinator ruled on this and said they are not this work-item's.
Final: `python3 -m pytest -q --work-item w125 tests/scripts/test_work_items.py` -> 12 passed.
`tools size --limit 300`: no output (no file over the limit).

## Tests changed under an allowance
none

## Open questions
none. (The merge check under `-n auto` end to end is not driven by any test; the new -n 2 unit test is the evidence.)

The plan contained no code.

## Outcome
Someone can now run `--work-item` with `-n` on a guarantees-only work-item and get exit 0. Commits: none by me (3cb355a is the earlier one).
