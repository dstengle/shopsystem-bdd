## Budget
scripts/supervise_outputs.py, scripts/supervise_rounds.py, tests/scenarios/supervision_session_faults_steps.py, tests/scenarios/supervision_rounds_steps.py, features/supervision.feature (only `features retire`).

## Outside the file set
tests/scenarios/supervision_rounds_steps.py: `answered_proposal` now reads the row's clause "and the apply round for p1 ends with a change list that adds X on thing" and sets the apply stand-in (before, the clause was ignored and the apply round gave no list).

# Report of w200 implement: DONE

Changed: `supervise_outputs.unformulated` (a formulate round's output: a non-deprecated scenario tagged @r<n> in features/<capability>.feature for each id of the proposal's adds and changes); `run_round`'s formulate branch asks r131's question (naming the missing scenarios) and the proposal goes to awaiting-answer when the round gave no question and something is missing. Steps: `stage_gives` commits a scenario (stand-in `commit`) for the formulate row that gives one, and for an apply round the formulate round after it. Deprecated r131 outline retired.

Red: `python3 -m pytest -q -n0 --work-item w200 -x`: the r131 formulate row failed on the Then, `AssertionError: ("the formulate round's scenario for thing#r4", '\n- Is a title given twice one book or two?\n')` (no question asked, p1 formulated), after the apply clause was wired (before that it failed on another question). Expected: the check did not exist.
Green: same command, 212 passed, 1 skipped; after the retire 208 passed, 1 skipped. Also tests/scenarios/test_supervision.py and tests/scripts: 211 passed, 1 skipped (before the retire).
Suite at start: 949 passed, 1 failed (the r131 formulate row); it now passes.

## Tests changed under an allowance
- tests/scenarios/supervision_session_faults_steps.py `stage_gives`, setup: formulate round and apply round stand-ins commit the scenario (r132 formulate and apply rows).
- tests/scenarios/supervision_rounds_steps.py `answered_proposal`, setup: the apply clause.

## Open questions
Plan part 5: a requirement in `changes` that the list removes; a capability's `formulated_as:` feature path (code reads features/<capability>.feature); where it is read when the merge fails (read after the merge); a @deprecated scenario does not count. r83 stayed green with no change.

Plan contained no code. Size check: no file over 300.
Someone can now see a formulate round that commits no scenario for what its proposal adds or changes asked about instead of formulated.
Commit: c42d0188.
