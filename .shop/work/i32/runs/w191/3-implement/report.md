## Budget
scripts/supervise_answers.py, tests/scenarios/supervision_delegation_steps.py, tests/scripts/test_supervise_answers.py

# Report
- Changed: `Answers.answers` makes no move for a reviewer's item with no verdict from this run (was KeyError); `re.M` -> `re.MULTILINE` (finding 5); new regression test tests/scripts/test_supervise_answers.py.
- Red: `python3 -m pytest -q tests/scripts/test_supervise_answers.py` with the guard disabled: `KeyError: 'w1'` at supervise_answers.py:86 (expected: D1). Green: 1 passed with the guard.
- Suite at start: 885 passed, 0 failed (10 expected failures listed in the brief). Final: `--work-item w191`: 146 passed, 1 skipped, 56 subtests; r118/r119 scenarios pass.
- Size check: `tools size --limit 300` printed nothing.
- The plan contained no code.

## Tests changed under an allowance
none

## Open questions
- What `work run` ends with and how the person gets out when the left item is the only thing in the way (item stays awaiting-answer with no open question): left unchosen.
- A reviewer's item with several questions, some answered by an earlier run: scenarios silent.

## Outside the file set
none

Commit: 32b5f1fa. Files: the three above.
