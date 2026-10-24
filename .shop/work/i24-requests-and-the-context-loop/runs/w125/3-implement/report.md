## Budget
- scripts/work_items.py
- tests/scripts/test_work_items.py

## Changed
- `pytest_sessionfinish` decides r65 from `--work-item` and the spec (`accepted`, `guarantees`), on controller and workers; the GUARANTEES stash and its setting are removed. Only exit 5 is changed to 0; not under --whole-suite.
- New test `test_a_guarantees_work_item_left_with_no_test_exits_successfully_under_xdist`.

## Red / green
- Red: `python3 -m pytest -q -n 0 tests/scripts/test_work_items.py -k xdist` -> `assert 5 == 0` (the controller never ran the hook that set the stash).
- Green: tests/scripts/test_work_items.py `12 passed`; `--work-item w125`: `145 passed, 1 skipped`.
- Suite at start: 760 passed, 13 failed at 15a08fa (failures in batch_measurement, design_model_check, work_queue; none in this work-item's files).

## Tests changed under an allowance
none

## Open questions
none. The test needs no xdist guard here (pytest.ini sets -n auto). The merge check end to end under -n auto was not driven; the unit test is the evidence.

Plan contained no code. Size check: `tools size` printed nothing.

Commit: 3cb355a. Files: scripts/work_items.py, tests/scripts/test_work_items.py.
