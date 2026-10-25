## Budget

- scripts/supervise_brief.py
- tests/scenarios/supervision_integrate_steps.py

## Changed

- `Briefs.integrate_lines` now writes `Ids drafted elsewhere (number added lines above each on the same capability): <ids or none>`. Also fixed ruff I001 (import order) and ISC004 (the string-concat line) in this file.
- `integrate_given_ids` also asserts the brief has a line starting "Ids drafted elsewhere" and that the given ids are on it. FURB167 fixed (`re.M` to `re.MULTILINE`, 2 lines).

## Red / green

- Red: `python3 -m pytest -q --work-item w172` gave `2 failed, 144 passed, 1 skipped`. Both r102 scenarios failed, on the new label assertion, because the brief still carried the old wording.
- Green: `python3 -m pytest -q --work-item w172` gave `146 passed, 1 skipped, 56 subtests passed`. `tests/scenarios/test_supervision.py` gave 4 passed.
- Suite at start: 867 passed, 0 failed at 015fea21. I did not run the whole suite.
- `tools size --limit 300`: printed nothing.

## Tests changed under an allowance

`integrate_given_ids` (tests/scenarios/supervision_integrate_steps.py) is a step first committed after Base. The plan's D2 has it rewritten to also assert the label, and that is the only change to what it asserts.

## Open questions

- The layout of the line when there are no ids: I wrote the label followed by "none".
- The order and separator of the listed ids: I used `", "`, in the order `added_by_others` returns them.

## Plan code

The plan contained no code, so none was pasted.

## Now possible

The integrate round finds the "Ids drafted elsewhere" line its instructions name, and is told to number above each listed id.

## Commits

a1ff989a

## Concerns

None.
