## Budget

- scripts/supervise_analysis.py
- tests/scenarios/supervision_analysis_steps.py

## Changes

- `lists_nothing` also requires status DONE (D1, r75).
- `analyse` judges the analysis session with `cut_short` and a readable result.json; a cut-short session or an unreadable result keeps no record and prints a message on stderr (D2, r76).
- Steps added: the two Givens and the two Thens that were missing ("ran no `measure initiative`", "analysis record is not there"; the plan named only the Givens).
- Import: `cut_short` comes via `supervise_worker` because supervise_faults and supervise_worker import each other.

## Red and green

- Red: `python3 -m pytest -q --work-item w153` after the steps, before the code: 2 failed (r75 PARTIAL: measurement was written; r76 turn limit: record kept), 144 passed. They failed on their Then lines, as expected.
- Green: `python3 -m pytest -q --work-item w153`: 146 passed, 1 skipped. `tests/scenarios/test_supervision.py`: 4 passed.
- Suite at start: 818 passed, 2 failed (exactly these two scenarios, plus others expected-red per the brief's record).

## Tests changed under an allowance

none

## Open questions

- An analysis session that ends in success with a readable non-DONE result while writing analysis.md: its record is still copied (no scenario).
- Plan section 5 items (same-day second measure, uncommitted records, no push verification/log for the analysis session) left as is.

## Other

- The plan contained no code.
- Size: `tools size --limit 300` printed nothing.
- Now: a PARTIAL branch review no longer triggers measure/analysis; an analysis cut short leaves no record.
- Commit: f511b7f
- Files changed: the two in the budget.
