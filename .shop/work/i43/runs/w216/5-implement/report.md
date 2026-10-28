## Budget
scripts/supervise_review_read.py, tests/scripts/test_supervise_review_read.py

## Changed
Fix of review finding 1 only: a transition commit names a work-item only if the name is one of the initiative's work-items; else `none`. New test tests/scripts/test_supervise_review_read.py.

## Red / green
Red: `python3 -m pytest -q tests/scripts/test_supervise_review_read.py` failed: `At index 0 diff: 'supervision' != 'none'` (the bug). Green after fix: 1 passed.
Final: `--work-item w216`: 187 passed, 1 skipped. Suite record at start: 1030 passed, 0 failed (w212 expected failures).
`tools size --limit 300`: no output.

## Tests changed under an allowance
none
## Open questions
none
Plan contained no code relevant here. Commit: 449bed14.
