## Budget

- scripts/supervise_review_read.py
- tests/scripts/test_supervise_review_read.py

## Changed

TRANSITION in supervise_review_read.py now also takes the name from `work answer|withdraw|retry: <n> a -> b` and `work add: <i>/<n> drafted`; the owner check (name must be an item of the initiative) is kept. Two new unit tests; docstring updated.

## Red / green

- Red: `python3 -m pytest -q tests/scripts/test_supervise_review_read.py` -> 1 failed, 2 passed; `assert ['none'] == ['w1']` for `work answer: w1 awaiting-answer -> ready` (the defect, expected).
- Green: same command, 3 passed. `python3 -m pytest -q --work-item w217`: 189 passed, 1 skipped, 56 subtests passed.
- Suite at start: 1031 passed, 0 failed at ba199fc1 (with w212's parked expected failures).
- `tools size --limit 300`: no output; no file over.

## Tests changed under an allowance
none

## Open questions
- `work add: <other initiative>/w1 drafted` where w1 is also this initiative's item: initiative part not checked.
- Other future `work <verb>:` transition subjects: not taken.

The plan contained no code. Commit: 9d61d97a.

Someone can now see commits made by work answer/withdraw/retry/add attributed to their work-item in a branch review brief. No surprises. Files: the two above.
