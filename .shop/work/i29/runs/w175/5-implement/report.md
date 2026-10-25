## Budget
scripts/workqueue_request.py, tests/scenarios/requests_write_steps.py (no further edits this session)

## Report
An earlier implement stage already committed 72bd6f14 "work request refuses an empty delegation (requests r22)": `request()` raises Refused("the delegation is empty") when a given delegation is empty after stripping (reading B); new Then "the command is refused because the delegation is empty". This session found nothing left to change and made no edit.
- Red (earlier stage, not rerun): Then step undefined (StepDefinitionNotFoundError); request wrote delegation "" and committed.
- Suite at start: 868 passed, 6 failed at 72bd6f14 (failures are i29 supervision r105-r109, accepted by w181, not this item's); w175 scenarios themselves pass.
- Final run: `python3 -m pytest -q --work-item w175` -> 143 passed, 1 skipped, 56 subtests passed.
- Size check: `tools size --limit 300` printed nothing.
- Tests changed under an allowance: none. Plan contained no code.

## Open questions
Order of refusals when several faults; pre-existing stored empty delegations; exact refusal text beyond "delegation is empty"; non-space whitespace (stripped).

Files changed: the two above. Concerns: none.
