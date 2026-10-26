## Budget

- tests/scenarios/supervision_rounds_steps.py
- tests/scenarios/supervision_delegation_steps.py

## Changed

New helper `apply_did_its_work(plan)` in supervision_rounds_steps.py sets `round:apply` to DONE with a change list naming thing#r1; used by the step "every round ends" (r80, r71) and by "each session given a question under the delegation ..., and every round ends ..." (the delegation scenario). r114 already gave a change list. No feature line or Then touched.

## Runs

Red: the brief's Suite record (3 failed at 78b3e837, the same three scenarios; apply round with no change list stays awaiting-answer per r131).
Green: `python3 -m pytest -q -n auto --work-item w199` -> 207 passed, 1 skipped; `tests/scenarios/test_supervision.py` -> 63 passed.
Size check: nothing printed (no file over 300).

## Tests changed under an allowance

- tests/scenarios/supervision_rounds_steps.py `every_round_ends` (setup): the apply stand-in gives a change list.
- tests/scenarios/supervision_delegation_steps.py `sessions_reply` (setup): same.

## Open questions

none

The plan contained no code that I pasted. Commit: bd7fc9b1.
