## Budget
scripts/workqueue_request.py, tests/scenarios/requests_steps.py

## Changed
- workqueue_request.outcome: refused (Refused, nothing written) in the asker's turn (r16).
- workqueue_request.turn: to the upstream sets awaiting-upstream (r18); to the asker sets awaiting-asker unless every line settled (r17); r8/r9 branch kept.
- requests_steps.py: shared Given refactored (write_request, keeps text in context), plural "that have no line outcome", new per-line Given (r17, both Examples rows per the answer, Reading A), new Thens (no line outcome, turn is, refused because asker's turn, as it was).

## Red / green
Red: `python3 -m pytest -q --work-item w127` -> 7 failed (before steps: undefined/mismatched steps). After steps only 4 failed on Then assertions (r16 outcome exit 0 / status assertions for r17 x2, r18). Expected: production did not refuse nor set awaiting-*. r15 and r7 turned green with steps alone (red had been undefined steps/a mismatched Given).
Green: 149 passed, 1 skipped (--work-item w127); test_requests.py + test_work_queue.py: 7 passed.
Suite at start: 752 passed, 7 failed (the 7 were this work-item's scenarios) per Suite record.
The r8 delivered scenario (w128) passes with the code as it is, no change by me.

## Tests changed under an allowance
none (the shared Given in requests_steps.py was extended, not an existing test's assertion)

## Open questions
- exact r16 refusal wording beyond naming the asker's turn; "as it was" checks file bytes only, not no commit
- work outcome with a line number not among the request's lines
- turn to the asker on a delivered request with an unsettled line: sets awaiting-asker (no scenario pins it)

Plan contained no code. size: no file over 300.
Commit: fce7a8c. Files: scripts/workqueue_request.py, tests/scenarios/requests_steps.py.
