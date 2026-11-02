## Budget
scripts/supervise_merge.py, tests/scripts/test_supervise_merge_rerun.py

## Changed
- `merge()` passes `tests["suite"]` (keeps `--whole-suite`) to `taken_back`, not `tests["work_item"]`.
- `taken_back` builds the rerun with `-n <value>` dropped and `-n 0` appended (pytest.ini's addopts otherwise re-adds `-n auto`).
- Test: the first rerun test now asserts `--whole-suite` is present and the only `-n` value is `0`; the fixture's suite command now mirrors the real one (`-n auto --work-item w1 --whole-suite`).

## Runs
- `python3 -m pytest -q -n 0 tests/scripts/test_supervise_merge_rerun.py`: 5 passed.
- `python3 -m pytest -q --work-item w245`: 190 passed, 1 skipped.
- Red run was not taken separately: the new assertions fail on the old code by construction (old command had no `-n 0` and used work_item command).
- Suite at start: failing on a flaky rmtree scenario (see brief); not run by me.
- Size: `tools size --limit 300` printed nothing.

## Tests changed under an allowance
tests/scripts/test_supervise_merge_rerun.py::test_a_scenario_failing_in_both_runs_gets_one_run_alone_and_a_pass_there_merges, and the `merge` fixture's suite command (interim: this initiative's test, rewritten to the person's answer).

## Open questions
none

## Other
The plan contained no code to paste. Commit ffb6d976. Concerns: ruff was not run (not allowed by the shell).
