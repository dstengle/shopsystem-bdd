## What changed
supervise_glossary.py: `terms_of`, `proposals_of`, `names_one` (whole word or phrase, any case). supervise_answers.py: a question that names one goes to no session and sets `left`. New steps in supervision_delegation_steps.py, a unit test of `names_one`, and the CLAUDE.md row extended.

## Red and green
`python3 -m pytest -q --work-item w223` red: 4 failed (undefined Given steps; r162 also the Then). With the steps only, r163 passed with no code (the plan expected it, a guard) and r162 failed on `"<question>" was given to no session` (a session had been started). After the code all pass: `python3 -m pytest -q tests/scenarios/test_supervision.py tests/scripts/test_supervise_answers.py` gave 6 passed.
Suite at start (the brief's record): 1022 passed, 4 failed, among them these scenarios.

## Tests changed under an allowance
none

## Open questions
A flagged first question with an unflagged second: the second gets a session and its answer is not written (the existing gap rule). Plurals ("ledgers") are not flagged. No scenario covers either.

## Plan code
The plan contained no code, so none was pasted.

## Size
`tools size --limit 300` printed nothing.

## Result
Someone can now run a delegation without it answering glossary questions. Commit 143ecc98. Files: CLAUDE.md, scripts/supervise_answers.py, scripts/supervise_glossary.py, tests/scenarios/supervision_delegation_steps.py, tests/scripts/test_supervise_answers.py. CLAUDE.md is outside the researcher's set but is in the work-item's fileset.

## Budget

- scripts/supervise_glossary.py
- scripts/supervise_answers.py
- tests/scenarios/supervision_delegation_steps.py
- tests/scripts/test_supervise_answers.py
- CLAUDE.md
