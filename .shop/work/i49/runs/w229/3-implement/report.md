## Budget
scripts/supervise_rounds.py (comments only; not edited, stopped before).

# Report: HAND-BACK

Stop condition: a scenario the work-item accepts passes before any step definition or code was written.
Evidence: `python3 -m pytest -q --work-item w229` -> `182 passed, 1 skipped, 34 warnings, 56 subtests passed` (the r180 scenario among them).
Suite record at start: 1061 passed, 0 failed at 2357b043 (plus listed expected failures).
Scenarios green: r180 (already). Red: none.
The code already implements r180 (`Rounds.due`); only comments cite the retired r93. The work-item is mis-cut: nothing to turn green.

## Tests changed under an allowance
none

## Open questions
- Started initiative with a not-approved glossary-proposal and no capability-proposal/work-item: unchosen.
- Started initiative fulfilling no request: unchosen.

The plan contained no code. Files changed: none. Commits: none.
