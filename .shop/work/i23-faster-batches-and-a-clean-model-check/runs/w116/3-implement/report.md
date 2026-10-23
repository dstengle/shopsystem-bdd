# report w116

## Budget
scripts/model_work.py, scripts/model.lp, tests/scenarios/design_model_check_given.py, tests/scenarios/design_model_check_problems.py

## Changed
- model_work.py: a work-item's accepted requirement with no named scenario is no file problem when its capability is in the guarantees group, or when the work-item is `green` and the id is retired.
- model.lp: removed the capability-proposal `closed` rule naming built/delivered/ruled/green/refused.
- Steps: guarantees Given, retired Given, status-bearing work-item Given, `it prints no file problem naming` Then, `built` proposal branch in malformed_work.

## Red / green
- Red: `python3 -m pytest -q --work-item w116` → 3 failed: the built row (no branch in malformed_work), and the two scenarios (undefined steps; then, with steps, the assertion failed with "accepts ...thing#r2, which no scenario names yet" in problems).
- Green: same command → 150 passed, 1 skipped. Also tests/scenarios/test_design_model_check.py, tests/scripts/test_model.py, test_model_withdrawn.py, test_model_reading.py: 40 passed.
- Suite at start: 714 passed, 3 failed (the three w116 scenarios). Plan contained no code.

## Tests changed under an allowance
none

## Open questions
- Work-item accepting a requirement its capability lacks (D3): left as "no scenario names yet".
- `work run --work-item` refuses a guarantees-only work-item (not touched).
- v_w4 for guarantees/green-retired work-item with no check (r106, other work-item).
- A guarantees requirement a scenario does name: exemption not covered.

## Size
`tools size --limit 300` printed nothing (problems.py is exactly 300).

Commit: 495a420. Files: the four above.
