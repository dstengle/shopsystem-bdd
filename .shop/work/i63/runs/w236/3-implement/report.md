## Budget

- scripts/supervise_faults.py
- tests/scenarios/supervision_faults_steps.py

## Changed
- `Faults.checkout_changes` leaves out every path under another group run's initiative directory (not put back, not listed).
- New Given (two sessions change i1's and i2's initiative.md) and Then "nothing recorded of {name} names {path}" in supervision_faults_steps.py.

## Runs
- Suite record at start: 1080 passed, 4 failed (the brief's list, including this scenario's test among them).
- Red: `python3 -m pytest -q --work-item w236` -> 1 failed, 180 passed (first StepDefinitionNotFoundError; after the Given and Then were written, AssertionError on the last Then, since i2's path was put back and named).
- Green: same command -> 181 passed, 1 skipped, 56 subtests passed. tests/scenarios/test_supervision.py also passes.
- `tools size --limit 300`: no output, no file over.

## Tests changed under an allowance
none

## Open questions
- i2's own check: when an i2 session ends with .shop/work/i2/initiative.md changed, i2's run treats it as its own path (r215/r216, not accepted here).
- Order of i1's and i2's checks; later broad commits taking in i2's change; rename porcelain lines (`old -> new`) under another initiative's directory.

The plan contained no code.

## Outcome
A change under another side-by-side initiative's directory is no longer put back or named in a fault. Commit c27c3c7e.
