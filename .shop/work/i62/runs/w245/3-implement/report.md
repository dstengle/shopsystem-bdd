## Budget

- scripts/supervise_merge.py
- tests/scenarios/supervision_tests_steps.py

## Changed

- `Merge.taken_back` (supervise_merge.py): reads `FAILED <node id>` lines of the failing scenario/suite runs, runs each distinct node id once more alone (the work-item command without `-n auto`, plus the node id), logs each under event `rerun`. The merge goes ahead when all pass; a failing run naming no scenario is refused as before.
- New Given in supervision_tests_steps.py with its own fixture ("it closes" fails unless pytest was invoked with a node id).

## Runs

Red: I did not re-run red myself; the research notes record it (StepDefinitionNotFoundError at the Given, line 2086). Honest note: I wrote step and code before a red run of my own.
Suite at start: 1087 passed, 3 failed (the brief's record; many expected).
Final: `python3 -m pytest -q --work-item w245` -> 182 passed, 1 skipped. tests/scenarios/test_supervision.py also passes.
`tools size --limit 300`: prints nothing.

## Tests changed under an allowance
none

## Open questions
- Failing run that also has ERROR lines or non-scenario tests: any `FAILED` node id with `::` is rerun; ERROR lines are not covered.
- `[tests]` override with a work-item command that does not take a node id.
- Parametrized ids containing " - " would be cut.

The plan contained no code. Commit: 397c0f2d.
Files changed: scripts/supervise_merge.py, tests/scenarios/supervision_tests_steps.py.
