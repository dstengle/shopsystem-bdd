# Report of w100

## Budget
- tests/scenarios/work_queue_answer_steps.py
- features/batch-measurement.feature (retire only)
- features/work-queue.feature (retire only)
- tests/scenarios/batch_measurement_then_steps.py
- scripts/migrate_upgrade.py
- tests/scripts/test_migrate_upgrade.py
- scripts/measure_read.py

## Changes
- work_queue_answer_steps.py: the r15 When and Then (snapshot imported lazily from test_work_queue, as work_queue_add_steps does).
- `features retire` of the deprecated batch-measurement @r42 scenario and work-queue @r9 outline (both bindings dropped with the blocks, `scenarios()` binds the files).
- gives_totals asserts every token column.
- migrate_upgrade.py: put-back catches `Exception`.
- test_migrate_upgrade.py: `AVersionFileThatHoldsNoVersion` removed, docstring updated.
- measure_read.py: dropped `.replace("Z", "+00:00")` and its noqa (Python 3.11).

## Red and green
- Red: `python3 -m pytest -q "tests/scenarios/test_work_queue.py::test_answer_with_a_newline_in_it_is_refused_and_nothing_changes"` -> 1 failed (undefined When step, as research said). Green after the steps: 1 passed.
- Final: `python3 -m pytest -q --work-item w100` -> 137 passed, 1 skipped. Touched modules (with --whole-suite restricted to them): 130 passed.
- Suite at start: 699 passed, 1 failed (that failing test is the r15 scenario, now green).
- `tools size --limit 300`: prints nothing. `tools check`: nothing to check.

## Tests changed under an allowance
none (the removed class and retired scenarios are listed by the plan/Retires).

## Open questions
- `transcript_inside` is still used by `transcript_inside_with_trips`, so it is not unused. `stages_sessions_took` still defaults turns/round trips; left alone.
- The empty `.shop/plugin-version` case is no longer tested (r30/r31 use only "next").
- D1 (U+2028/form feed in answers) and D2 left as is.

The plan contained no code. Commits: 7de9e66, 22f7453. No files outside the file set.
