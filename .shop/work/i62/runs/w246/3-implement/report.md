## Budget
- scripts/supervise_merge.py
- tests/scripts/test_supervise_merge_rerun.py
- tests/scenarios/supervision_rerun_steps.py

## Changed
- Finding 1: the refused merge's question gives every failed pre-merge run that names a scenario whose second run failed (each once, with command and output), then the second runs.
- Finding 2: the `rerun` log write is removed, and the two assertions on it.

## Red / green
- Red: `python3 -m pytest -q -n 0 tests/scripts/test_supervise_merge_rerun.py` failed on the new test (question lacked "bang", the suite run's output); expected, as the question held only failed[0].
- Green: same file 9 passed; `--work-item w246` 195 passed, 1 skipped.
- Suite at start: 1101 passed, 0 failed.
- `tools size`: nothing printed.

## Tests changed under an allowance
- tests/scripts/test_supervise_merge_rerun.py::test_a_scenario_failing_in_both_runs_gets_one_run_alone_and_a_pass_there_merges: interim (rerun log assertion removed per plan part 4).
- tests/scenarios/supervision_rerun_steps.py::closes_run_alone: rerun log assertion removed, as the plan lists.

## Open questions
Plan part 5 cases: a shared run appears once; output kept whole; both first runs given when both name the scenario; scenarios that passed alone not listed. No scenario asserts these.

Plan contained no code. Commit 0b306638.
