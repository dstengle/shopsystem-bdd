# Report w155

## Budget
- tests/scenarios/supervision_delegation_steps.py
- scripts/supervise_answers.py

## Changed
- supervise_answers.ask: on a fault (or changed .shop/work files) it calls the existing `keep_round(name, "answer", label)` before refusing, so the stage directory and log lines are committed and pushed with no transition. Exit stays an error.
- Steps added for r89 (Given turn limit, Then "has no answer") and r90 (Given error with notes.md, two Thens).

## Red/green
- Start suite record: 828 passed, 2 failed (the two w155 scenarios, plus expected others).
- Red: `pytest -q --work-item w155`: r89 StepDefinitionNotFoundError; after steps, r90 failed: `AssertionError: ([], "work: the session answering w1's question faulted: ...")` (nothing committed). r89 passes with the step alone, as the plan said (production code already left the question unanswered).
- Green: `python3 -m pytest -q --work-item w155` -> 144 passed, 1 skipped.

## Tests changed under an allowance
none

## Open questions
- Commit message of the faulted answer's record ("work: w1 answer round 1-answer faulted", reuses keep_round's form).
- Two open questions where the first session faults: the run stops, second never asked.
- Non-DONE outcome without a fault (QUESTION/PARTIAL): not probed; left as is.

## Size
`tools size --limit 300` printed nothing.

The plan contained no code. Commit: b1442b4.

Files changed: scripts/supervise_answers.py, tests/scenarios/supervision_delegation_steps.py
