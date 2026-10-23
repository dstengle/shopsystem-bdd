## Budget

- scripts/model_work.py
- scripts/model.lp
- tests/scenarios/design_model_check_one_each.py

## Changed
- model_work.py `read_part`: one `accepts(W, <requirement>)` fact per accepted requirement, from the field; the scenario lookup stays only for the r27 file problem and exemptions.
- model.lp: FIX note that accepts' second argument is a requirement.
- one_each steps: FIELDS entry "accepts thing#r2 and no check".

## Red / green
- Red: `python3 -m pytest -q -n 0 --work-item w117` -> 1 failed (the r106 scenario, at the Then: `v_w4` printed for w1), 142 passed. Expected: no accepts fact for an unnamed requirement.
- Green: `python3 -m pytest -q --work-item w117` -> 143 passed, 1 skipped. Also tests/scripts/test_model_withdrawn.py and tests/scenarios/test_design_model_check.py: 7 passed.
- Suite at start: 721 passed, 1 failed (this scenario, expected).

## Tests changed under an allowance
none

## Open questions
- Wording of the r27 file problem for a requirement no capability has.
- Whether accepting a requirement its capability lacks is an unresolved reference.
- An accepted reference `resolve_req` refuses gives no fact (v_w4 if no check).
- Duplicate entries naming one requirement: clingo sees one fact.

## Other
Plan contained no code. `tools size --limit 300`: printed nothing. `model facts` now shows requirement-valued accepts lines (no test asserts them).
Commit: aaeea80 model check: v_w4 reads a work-item's accepts from its field (r106)
Files: scripts/model_work.py, scripts/model.lp, tests/scenarios/design_model_check_one_each.py. No concerns.
