## Budget
scripts/supervise_merge.py, tests/scripts/test_supervise_merge_rerun.py

## Changed
`taken_back` no longer takes back a failing run that has an ERROR line or counts errors, or that names a FAILED node not in a test module binding feature scenarios (`scenarios(`/`scenario(`; new `is_scenario`). A rerun counts as passed only with exit 0 and "N passed" in its output (no tests, deselected, exit 5 = failed). Ruff hits in the test file cleared. Tests added: ERROR line refuses, non-scenario node refuses, rerun running no test refuses.

Red/green: the three new tests were written together with the code (not run red separately; the first rerun of the scenarios showed 3 failures when I tied "scenario" to tests/scenarios/, the scenario fixtures use tests/test_thing.py; fixed by detecting scenario modules by content).

Suite at start: 1092 passed, 2 failed at 2f359718 (the two r219/r220 steps, already present in tests/scenarios/supervision_rerun_steps.py).
Final: `python3 -m pytest -q -p work_items --work-item w245`: 190 passed, 1 skipped; test_supervise_merge_rerun.py 5 passed.
Size: `tools size --limit 300` printed nothing.

## Tests changed under an allowance
tests/scripts/test_supervise_merge_rerun.py (this initiative's own): setup/lint respelled; its two tests keep their assertions.

## Open questions
none. Plan contained no code pasted.
