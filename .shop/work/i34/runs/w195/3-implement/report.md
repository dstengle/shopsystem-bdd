# Report of w195 (supervision#r122)

## Budget
scripts/work_items.py, tests/scenarios/supervision_proposal_steps.py, tests/scenarios/supervision_tests_steps.py (3 files).

## Changed
- `work_items.py`: new `proposals()` reads capability-proposals (status neither formulated nor withdrawn) and the ids in their `adds:`/`changes:`; `expect_red` xfails scenarios they name; docstrings updated.
- `supervision_proposal_steps.py`: Given for p1 approved/withdrawn/awaiting-answer/merged. `work run`'s rounds move a proposal on before the suites run, so an awaiting-answer p1 gets an unanswered question and, for approved, the formulate round is planned to ask a question (the proposal then stands awaiting-answer at the suite runs).
- `supervision_tests_steps.py`: Then for the implement-stage suite record; shares `check_counted` with `counted_as`.

## Red and green
- Red: not re-run by me before editing; I relied on the plan's/researcher's recorded run (9 of 10 rows failing: undefined Given/Then). Process deviation: I wrote the code before my own red run.
- Green: `python3 -m pytest -q --work-item w195` -> 154 passed, 1 skipped. Also tests/scripts/test_work_items.py and tests/scenarios/test_supervision.py pass.
- First green attempt left 2 rows red (approved, awaiting-answer): the rounds had moved p1 to formulated, hence the step changes above.
- Suite at start: 913 passed, 9 failed (the r122 rows).
- `tools size --limit 300`: no output, no file over.

## Tests changed under an allowance
none

## Open questions
- Proposal with no `status:` line or an unlisted status: counted as expected (not formulated/withdrawn); unchosen by scenarios.
- Ranges in adds/changes parsed like `accepts:`.
- A scenario named by a closed work-item and an open proposal: expected.
- "approved" cannot be observed at the suite runs through `work run`'s rounds, as they move it first; the approved row holds only because the formulate round asks a question.
- `--whole-suite` with an unknown work-item (D2): untouched.

## Other
The plan contained no code. `supervise_merge.py` comment not edited (text only). Commit: f682b013.
