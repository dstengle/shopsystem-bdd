# Report of w132

## Budget
- scripts/model.lp
- scripts/model_requests.py
- scripts/model_work.py
- scripts/model_facts.py
- tests/scenarios/design_model_check_requests.py
- tests/scenarios/design_model_check_then.py

## What changed
model.lp: v16a, v_d3, v17, v18 added; v3 replaced (v3/2 over request, requirement); v_d1 gained the request clause under one label. model_requests.py emits asker, req_part_of, req_source, resolution. model_work.py emits date and fulfils. model_facts.py emits `foreign` (in qualify and check_id). Steps: Givens in design_model_check_requests.py, generic names/does-not-name Thens in design_model_check_then.py.

## Red and green
Red: `python3 -m pytest -q -n 0 --work-item w132` gave 15 failed (undefined steps, no rules), as the plan said.
Green: the same command after the change gave 157 passed, 1 skipped. tests/scripts and tests/scenarios/test_design_model_check.py: 156 passed, 1 skipped.
Suite at start (brief's record): 752 passed, 15 failed; the whole suite is not rerun by me.
`tools size --limit 300`: nothing printed, no file over.

## Tests changed under an allowance
none

## Open questions
Plan section 5 cases, left unchosen: this repo's own i24 is v16a until it fulfils a request; a bare-path or product-level asker under v_d1; fulfils naming a missing request; part_of naming a missing job-thread; w_uncited_obs ignoring request citations; v18 for ids qualify never sees; malformed Resolution entries.

## Notes
The plan contained no code, so nothing was pasted. request_text gained optional arguments; its old callers are unchanged.
Commit: 437dc1c. Files: the six in Budget.
