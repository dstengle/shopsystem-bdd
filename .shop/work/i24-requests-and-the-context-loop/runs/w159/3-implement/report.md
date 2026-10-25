# w159 report

## Budget
- scripts/model_work.py
- tests/scenarios/design_model_check_problems.py
- tests/scenarios/design_model_check_records.py (new)
- tests/scenarios/test_design_model_check.py

## Changed
- model_work.py STATUSES: awaiting-answer added to capability-proposal, withdrawn to request.
- `malformed_record` Given moved to the new design_model_check_records.py (existing branches unchanged), with a branch for each new row (proposal via world.proposal(status="awaiting-answer"), request via request_text(status="withdrawn")). Import line added to test_design_model_check.py. No CLAUDE.md row needed (tests/scenarios/ row covers it).

## Red / green
- Red: `python3 -m pytest -q -p no:warnings --work-item w159` after the step move, before code: 2 failed. Then assertion: `problems: [".shop/work/requests/q1.md: status 'withdrawn' is not one of accepted, ...", ...]` (and the like for p1.md). Expected: the lifecycles lacked the statuses.
- Green: same command after code; plus `--whole-suite` on test_design_model_check.py and test_work_queue.py: 263 passed, 1 xfailed, 4 xpassed. test_model_reading, test_model_withdrawn, test_model: pass.
- Suite at start: 833 passed, 2 failed (the two r27 rows), plus six expected failures other work-items own.

## Tests changed under an allowance
none (malformed_record moved unchanged for existing rows: a respelling/move).

## Open questions
none beyond the plan's section 5 (nothing writes a withdrawn request; done-rule v_d1 for withdrawn requests unchanged, per D3/D4).

The plan contained no code.

## Size
`tools size --limit 300` printed nothing.

## Result
Someone can now run `model check` on a repo with an awaiting-answer capability-proposal or a withdrawn request without a file problem. Commit 11d8024.
