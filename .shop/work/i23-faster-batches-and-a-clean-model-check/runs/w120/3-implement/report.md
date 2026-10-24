## Budget
- tests/scenarios/work_queue_answer_steps.py

## Changed
Removed the one surplus blank line after the imports in tests/scenarios/work_queue_answer_steps.py.

## Red / green
- Red (expected: the work-item's check, not a scenario): `tools check tests/scenarios/work_queue_answer_steps.py` -> `tests/scenarios/work_queue_answer_steps.py:2:1: I001 [*] Import block is un-sorted or un-formatted`, exit 1.
- Green: same command -> `All checks passed!`, vulture clean, exit 0.
- `python3 -m pytest -q --work-item w120`: 146 passed, 1 skipped (r15's scenarios were green before and after).
- Note: `scripts/tools` of the repo was refused as a command; I ran the plugin's `tools check` on the file by the brief's Scripts path. The project-wide check was not run.
- Suite at start: Suite: 724 passed, 0 failed at 811e799 in 14 s.
- `tools size --limit 300`: printed nothing.

## Tests changed under an allowance
none

## Open questions
- An empty answer ("") to an awaiting-answer item is accepted and written as an empty bullet.
- U+001C/U+001D/U+001E are accepted as one line, though `splitlines` in the `has_answer` step would see two.

The plan contained no code.

## Outcome
`tools check` on the step module now exits 0. Commit: edad3b6. Files changed: 1.
