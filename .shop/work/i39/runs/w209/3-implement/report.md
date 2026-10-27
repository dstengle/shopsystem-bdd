## Budget

- scripts/model.lp
- scripts/model_requests.py
- tests/scenarios/design_model_check_requests.py
- tests/scenarios/design_model_check_then.py
- features/design-model-check.feature (features retire only)

## Changed

- model.lp: v17 also lets off a request with a job-thread part_of (judged from the id, fact `req_thread`) or a raised_for request; v18 skips an id some request is raised for; labels reworded; `#defined` added.
- model_requests.py: reads `raised_for` (kind request, from the id) as `req_raised_for`; `req_thread` for a job-thread part_of; a non-internal asker with only `raised_for` is well formed.
- Steps: new Givens for r120/r121, Then accepts "q2, q3 or q4"; the old r115-only Given reworded to r120's q1 phrase (the r115 scenario is retired).
- `features retire` removed the `@r115 @deprecated` scenario (10 lines).

## Red and green

Start suite record: 968 passed, 8 failed (the design_model_check v17/v18 tests among them; the rest are requests/supervision failures not mine).
Red: `python3 -m pytest -q -n 0 --work-item w209` -> 8 failed (undefined Givens); after the steps, 2 failed on the Then lines (v17 named q3, q4 problem; v18 named other/q3). Expected: no code yet.
Green: same command -> 158 passed, 1 skipped. Also tests/scenarios/test_design_model_check.py + tests/scripts: 157 passed.
`tools size --limit 300`: no file printed.

## Tests changed under an allowance

none (the Given reworded belongs to the retired scenario's replacement, not a test).

## Open questions

- raised_for naming a non-request kind: ignored by the code, no scenario says.
- raised_for naming a request that does not exist: not unresolved.
- A request with both raised_for and part_of/source, or several raised_for.
- An internal asker with only raised_for stays a file problem (plan decision 3).

The plan contained no code.

## Outside the file set

none. Commit c0603921.
