## Budget
scripts/model.lp, tests/scenarios/design_model_check_given.py, tests/scenarios/design_model_check_then.py, tests/scripts/test_model_output.py, docs/design-model/grammar.md

## Report
Changed: model.lp and grammar.md gate w_unserved_cap on `node(_, "job")`; new Given and Then steps; test_model_output fixture gets an observation.
Red: `pytest -q --work-item w118` -> 1 failed (Then: output had "1 warnings" with w_unserved_cap). Green after: work-item scenarios pass; test_model_output (8) pass.
Suite at start: 722 passed, 1 failed (this scenario).
## Tests changed under an allowance
tests/scripts/test_model_output.py::CheckOutputTest::test_check_ends_with_the_four_counts — fixture only (plan-listed); assertion unchanged, passes.
## Open questions
A context with a job where a capability serves none: unchosen, no scenario.
Plan contained no code. Size check: no output (nothing over). Commit 8a32a57.
