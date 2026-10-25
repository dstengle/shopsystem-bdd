# Report w175

## Budget
- scripts/workqueue_request.py
- tests/scenarios/requests_write_steps.py

## Changed
`request()` refuses (Refused "the delegation is empty") a given delegation empty after strip, before any write/commit. New Then step "the command is refused because the delegation is empty".

## Red / green
- Red: `python3 -m pytest -q --work-item w175` -> 1 failed (test_request_with_an_empty_delegation_is_refused_and_nothing_changes), step undefined and no refusal in code.
- Green: same command -> 143 passed, 1 skipped. tests/scenarios/test_requests.py: 1 passed.
- Suite at start: 867 passed, 7 failed (r22 scenario among them; the other six are in test_supervision.py, not this work-item's).

## Tests changed under an allowance
none

## Open questions
- Order of refusals when several faults (empty delegation checked first, before origin and line checks; scenarios silent).
- Stored requests with `delegation: ""` or whitespace-only are untouched.
- Exact refusal text beyond "the delegation is empty".

Plan contained no code. Size check: no files over 300.

Someone can now not create a request with an empty/whitespace delegation. Commit: eef9320a.
Files changed: the two above.
