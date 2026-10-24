## Budget
- tests/scenarios/test_supervision.py

## Changed
`run_work` in tests/scenarios/test_supervision.py now drops from the inherited PYTHONPATH each entry holding a `work_items.py`, so the fixture repository's `work run` loads this branch's copy (work run adds its own scripts last). Commit 5652908.

## Runs
- Suite record at start: 725 passed, 2 failed (the two guarantees scenarios in test_supervision.py), plus expected failures of other work-items.
- Final: `python3 -m pytest -q -n auto --work-item w121`: 144 passed, 1 skipped. test_supervision.py: 3 passed.
- I could not run with the main checkout's scripts on PYTHONPATH (a command with an env prefix was refused). The change drops such entries, so it should hold under that environment too; `work run`'s check will show.
- size: nothing printed.

## Tests changed under an allowance
tests/scenarios/test_supervision.py::run_work (setup: environment only, no assertion touched).

## Open questions
none

The plan's code question: nothing pasted. Earlier work was already committed (9492062).
