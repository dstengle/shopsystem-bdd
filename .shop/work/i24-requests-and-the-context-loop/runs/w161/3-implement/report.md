## Budget

- scripts/measure_read.py
- tests/scenarios/batch_measurement_world.py
- tests/scenarios/batch_measurement_request_steps.py
- tests/scenarios/batch_measurement_then_steps.py

## Changed
`request_of` (measure_read.py) reads every `fulfils:` line, refuses more than one request ("more than one request"), a request not in the queue ("the queue does not hold the request"), keeps "has no asker". World holds a list of requests; new Givens/Thens; `no measurement is written`.

## Runs
Red (before any edit; run by the research stage and my first run after the steps): all three scenarios failed at undefined steps. After writing the steps and World, before the code: `2 failed, 143 passed` — r65 failed on "there is no request q3 under ..." (text), r67 on exit code 0 (two-line fulfils measured as q3). r66 passed once its steps existed, since the code already refused (undefined steps were its red; plan noted this).
Green: `python3 -m pytest -q --work-item w161` → 145 passed, 1 skipped. Also test_batch_measurement.py + tests/scripts/test_measure_runs.py: 5 passed.
Suite at start: 831 passed, 3 failed (the three scenarios of this work-item).
size --limit 300: prints nothing.

## Tests changed under an allowance
none (the two existing Givens moved to the list form in the World; asserts unchanged)
## Open questions
Withdrawn request counted as held; same id on two lines is one request; bare id read as request/q3; q3+q4 with one unheld gives the "more than one" reason (plan §5).
## Other
Plan contained no code. Outside the file set: none. Commit 16eaabf.
