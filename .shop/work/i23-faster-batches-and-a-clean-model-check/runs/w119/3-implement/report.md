## Budget
- scripts/supervise_pool.py
- tests/scenarios/supervision_parallel_steps.py

## Changed
- Pool.choose builds its status map from every initiative (workqueue.items), this initiative's winning on a shared name (D1); file status read, no `agrees` (D2).
- Three new steps in supervision_parallel_steps.py (D3).

## Red / green
- Red: `python3 -m pytest -q --work-item w119` -> 1 failed (the cross-initiative scenario), `AssertionError: ([], '')` on the Then: no worker started. Expected: the blocker in i2 was not seen.
- Green: same command -> 140 passed, 1 skipped. test_supervision.py: passes.
- Suite at start: 715 passed, 1 failed (this scenario).
- `tools size --limit 300`: prints nothing.

## Tests changed under an allowance
none

## Open questions
Plan §5: checkout-visibility of i2's green; id-form blocker; absent blocker silent; file/log disagreement counted by file.

## Other
Plan contained no code. No files outside the set. Commit fd035f0.
