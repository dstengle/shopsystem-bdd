# w221 report

## Budget

scripts/model_work.py, scripts/model.lp, tests/scenarios/conftest.py, tests/scenarios/design_model_check_given.py, tests/scenarios/design_model_check_trace.py, tests/scenarios/design_model_check_problems.py, tests/scenarios/design_model_check_work.py (new), tests/scenarios/test_design_model_check.py, features/design-model-check.feature (retire only). 9 files.

## What changed

- glossary-proposal is a part kind with lifecycle drafted/awaiting-answer/approved/withdrawn (`model_work.py`).
- A glossary-proposal's `term/` refs in adds/changes/removes are collected and judged after all of `.shop/work/` is read; excused only by an approved glossary-proposal's `removes` (any initiative).
- `model.lp`: `approved` closes a glossary-proposal only (r123).
- `model.lp` v_k3: a glossary-proposal no longer counts as a non-capability-proposal part of a capability-change initiative. Not in the plan; r123's scenario failed on v_k3 once glossary-proposal became a part ("v_k3 ... initiative/ex.com/prod/ctx/i1"). Small, needed for the Then line.
- Tests: glossary-proposal writer in conftest; r122/r123 Givens; `malformed_work` moved to new `design_model_check_work.py` with the r124 rows; two Givens used only by the retired scenarios removed. Five deprecated r124 scenarios retired with `features retire`.

## Red and green

- Red: `python3 -m pytest -q --work-item w221 -n auto` after writing steps: 8 failed (glossary-proposal refused as a kind: "needs an id and a kind among capability-proposal, ..."; r122 rows therefore not unresolved). Expected: production code absent.
- After model_work.py + closed(): 1 failed, r123: `v_k3` named the initiative; fixed as above.
- Final: `python3 -m pytest -q --work-item w221 -n auto`: 211 passed, 1 skipped. `tests/scenarios/test_design_model_check.py`: 31 passed.
- Suite at start (brief): 1044 passed, 37 failed at 79f94713 (includes w221's scenarios and parked w212 ones). Whole suite not run.

## Tests changed under an allowance

none (the removed Givens served only retired scenarios; `malformed_work` was moved, its dead "status not in lifecycle" branch dropped with its deprecated row).

## Open questions

- A glossary-proposal listing something other than `term/<x>`: ignored by the code, unchosen.
- A glossary-proposal with `argues`: read as for other parts (argues check), unchosen otherwise.
- Whether an approved glossary-proposal's removes excuses a capability-proposal's term ref: left unchanged.

## Size check

`tools size --limit 300` printed nothing.

The plan contained no code.

## Result

Someone can now run `model check` on a repository with glossary-proposals: terms are checked, approved ones close, and done initiatives may hold them. Commit: 6a7131c0.

Files changed: the nine above. Concerns: none.
