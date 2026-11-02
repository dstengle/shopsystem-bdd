## Budget

- scripts/work_items.py
- scripts/supervise_merge.py
- tests/scripts/test_supervise_merge_rerun.py
- tests/scripts/test_work_items.py

Suite record at start: Suite: 1097 passed, 0 failed at 2c8925d6 in 36 s (expected reds as the brief lists).

## Changed

Fixes findings 1-3 (and 4, ruff) of review 10, as the person ruled:
1. Scenario or not is decided by pytest-bdd's `__scenario__`, not module text or path. `work_items` marks each scenario's reports (user property, reaching the xdist controller) and, under `--work-item`, prints `SCENARIO <node id>` for each failed scenario in the terminal summary. `taken_back` refuses when a FAILED node has no such line. `is_scenario` is gone.
2. `-n 0` is added to the rerun only when the suite command had `-n`.
3. Errors are looked for only in `ERROR ` lines after "short test summary info" and in the last output line.
4. ruff clean (unused `Path` import dropped, PLC0206 and RUF059 removed).

## Red and green

Red: `python3 -m pytest -q -n 0 tests/scripts/test_work_items.py` — the new test failed: "Right contains 2 more items, first extra item: 'SCENARIO tests/test_thing.py::test_it_answers'" (the plugin printed no such lines). Merge tests, after changing the stub to the SCENARIO form: 5 failed, 3 passed (the no-`-n` test, the captured-output errors test and the old module-text path failing). Green: both modules 21 passed; `--work-item w245`: 194 passed, 1 skipped.

## Tests changed under an allowance

- tests/scripts/test_supervise_merge_rerun.py (first committed after base; setup/interim): the stubbed output now carries `SCENARIO <node>` lines and the fixture writes no module files; `test_a_failing_node_that_is_not_a_scenario_is_not_taken_back` now names a node in tests/scripts (no SCENARIO line); `test_a_failing_run_with_an_error_line_is_not_taken_back` puts the ERROR line under the short summary header. Three tests added (no -n, captured-output "errors", final-line error).

## Open questions

none

The plan contained no code that I pasted. Size: `tools size --limit 300` printed nothing. `tools check`: ruff clean, vulture clean.

## Commit

fa1b6eea

Files changed: the four in Budget. Concerns: a delivery's own `tests` commands without the work_items plugin print no SCENARIO lines, so their failures are never taken back (refusal side).
