## Budget

- scripts/supervise_answers.py
- scripts/supervise_glossary.py
- tests/scripts/test_supervise_answers.py
- tests/scenarios/supervision_delegation_steps.py
- features/supervision.feature (features retire only)

## What changed
- supervise_answers.py: every open question is asked; names_one test and import removed; docstring cites r209/r210.
- supervise_glossary.py: names_one, proposals_of, terms_of deleted; docstring reworded.
- test_supervise_answers.py: deleted the names_one test (plan part 4, listed).
- supervision_delegation_steps.py: g1 Given takes optional question; w2 Given widened to any wN; g1 Then widened; two r210 After Thens added.
- features/supervision.feature: r162 outline retired via `features retire` (plan D2).

## Red and green
- Red: `python3 -m pytest -q --work-item w230`: 4 failed (undefined steps); after the steps r209 passed (code already held it, as the plan said), r210 2 failed on the Then (w2 questions not asked).
- Green: same command: 184 passed, 1 skipped. tests/scripts/test_supervise_answers.py and test_supervision.py: passed.
- Suite at start: 1065 passed, 4 failed (the r209/r210 examples) plus expected failures in test_requests.py.

## Tests changed under an allowance
none

## Open questions
Plan part 5: glossary-proposal question that names files; one already answered; exit status when only glossary-proposal questions remain. Left unchosen.

## Other
Plan contained no code. `tools size`: printed nothing (no file over 300). Commit 051b2b9d.
