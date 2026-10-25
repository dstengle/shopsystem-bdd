## Budget

scripts/supervise_answers.py, scripts/workqueue_answer.py, tests/scenarios/supervision_delegation_steps.py

## Stop: HAND-BACK

Condition: a scenario the work-item accepts (r119, accept) passes before any production code was written for it.

Suite at start: 883 passed, 2 failed (the two scenarios of this work-item among them).

Red run (before steps): `python3 -m pytest -q -n 0 --work-item w190`: 2 failed (StepDefinitionNotFoundError, expected).
After writing only the three step definitions (Given of a reviewer's question with a done->awaiting-answer log, the
When-clause with a `verdict` result field, the Then reading log.jsonl), same command:
`1 failed, 144 passed`; only `..._asks_for_a_change_makes_the_workitem_ready_again` fails. The log shows
`awaiting-answer -> done` by work run: the existing `asked_from` returns `done` for a reviewer's question, so r119
passes with no production change (the verdict field is ignored).

r118 (change -> ready) is red for the right reason: the log's move is awaiting-answer -> done, not ready (defect D1 in the notes).

Implication: r119 passes by accident of the current code; the work-item is mis-cut, or the person accepts that
r119 needs only its steps while r118 gets the verdict code (then the verdict/accept branch in the plan is not demanded by any scenario).

## Tests changed under an allowance
none
## Open questions
none beyond the plan's section 5.
## Notes
The plan contained no code. Commit c5561011 (steps only; no production code written). Size check not run (only a test file touched; 200 lines or fewer).
Files changed: tests/scenarios/supervision_delegation_steps.py
