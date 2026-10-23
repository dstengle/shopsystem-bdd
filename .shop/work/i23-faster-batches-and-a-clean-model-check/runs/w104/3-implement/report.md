## Budget
scripts/model_work.py, scripts/model.lp, tests/scenarios/design_model_check_given.py, design_model_check_then.py, design_model_check_problems.py, design_model_check_one_each.py, tests/scripts/test_model_output.py (7 files)

## Changed
- model_work.py: `accepts` fact for every accepted requirement (requirement id when no scenario names it); file problem only if not withdrawn, not a guarantees capability, not a retired id accepted by a green work-item. Unknown capability tolerated (stays a file problem).
- model.lp: `w_unserved_cap` needs a job node.
- Steps added (given: no-job context, guarantees r2, retired r2, green work-item; then: "prints no file problem naming", "does not give w_unserved_cap"); `malformed_work` branch; FIELDS key.
- test_model_output setup: added an uncited observation (plan decision 5).

## Red / green
Start: `python3 -m pytest -q --work-item w104` → 5 failed, 149 passed (missing steps; code defects D1-D4). The "built" row went green with the test-side branch alone (code was already right, per plan; the part needed a capability-proposal id).
Final: `--work-item w104` → 154 passed, 1 skipped. Also test_model_output, test_model_withdrawn, test_model, test_design_model_check: 34 passed (+scenario module green).
Suite at start (brief): 683 passed, 8 failed at cecfda2 (listed in brief); not re-run.

## Tests changed under an allowance
tests/scripts/test_model_output.py::CheckOutputTest::test_check_ends_with_the_four_counts — plan-listed; setup only (observation added), assertion unchanged.

## Open questions
Plan section 5: `pytest --work-item` refuses a work-item whose only accepts are unnamed; brief shows no scenarios for an unnamed accept; guarantees ranges partly named; two capabilities no job — none chosen.

Plan contained no code. Size: `tools size --limit 300` printed nothing.
Commit: d3d0fe2.
Files: the 7 above.
