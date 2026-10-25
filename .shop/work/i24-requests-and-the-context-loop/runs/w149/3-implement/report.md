## Budget
- scripts/workqueue_request.py

## Changed
`turn` (upstream branch) sets accepted/refused from line outcomes only when status is not delivered; turn still passes, r17 branch unchanged.

## Red/green
- Red: `python3 -m pytest -q --work-item w149` -> 1 failed (delivered scenario; status_is got accepted, expected delivered), as planned.
- Green: same command -> 145 passed, 1 skipped. tests/scenarios/test_requests.py: 3 passed.
- Suite at start: 813 passed, 1 failed (this scenario) plus expected failures listed in brief.
- `tools size --limit 300`: no output (nothing over).

## Tests changed under an allowance
none

## Open questions
none beyond the plan's section 5 (upstream turn on delivered with unsettled lines uses r17; outcome on delivered unrefused).

Plan contained no code. Commit: d4be501.
Files changed: scripts/workqueue_request.py. Concerns: none.
