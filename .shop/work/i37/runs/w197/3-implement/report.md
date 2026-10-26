## Budget

- scripts/workqueue_request.py
- tests/scenarios/requests_steps.py
- features/requests.feature (features retire only)

## Changes

- `turn` returns without passing the turn when the upstream's end sets `accepted` (r23); `resolve` writes `turn: asker` with `delivered` (r24).
- `status_is` Then: "not accepted" means any status but `accepted`.
- `features retire` removed the deprecated r7 scenario (both Examples).

## Red / green

Suite at start: 924 passed, 4 failed at b6815a57 (the 4 failing are this work-item's scenarios).
Red: `python3 -m pytest -q --work-item w197` -> 4 failed, 146 passed (r7 x2: status literal "not accepted"; r23: turn asker not upstream; r24: turn upstream not asker).
Green: same command -> 148 passed, 1 skipped. `tests/scenarios/test_requests.py`: 4 passed.
`tools size --limit 300`: printed nothing.

## Tests changed under an allowance

none. (Retired deprecated r7 tests removed with their scenario, as the plan lists; `status_is` rewritten as the plan lists.)

## Open questions

- Accepted request now stays in upstream's turn: what an outcome/ask on it does is unspecified; left unchosen.
- supervise_intake's waiting set does not rerun an accepted request left in the upstream's turn.
- A second upstream `turn` on an accepted request sets accepted again and keeps the turn (falls out of r8/r23, no special case).
- D1: `work request` accepts a request with no lines.

The plan contained no code.

## Commits

9237a0f9
