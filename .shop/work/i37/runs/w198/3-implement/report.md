## Budget

- features/supervision.feature
- features/migration-tools.feature
- features/work-queue.feature
- tests/scenarios/supervision_integrate_steps.py
- tests/scenarios/test_work_queue.py

## What changed

`features retire --file <f> <title>` for each of the seven Retires titles (all accepted, none refused). Removed the step `other_initiative` (supervision_integrate_steps.py) and `drafted` (test_work_queue.py), used only by retired scenarios (grep of features/ shows no live use). The plan held no code.

## Runs

- Red: none. The four accepted scenarios (r75, r105, r120, r121) passed before any change, as the research and plan state. The work-item is retire-only; I proceeded as the plan names the retirements as the work. This is the "accepted scenario passes before work" condition, so it is noted here for the person.
- Suite at start: Suite: 926 passed, 0 failed at c3474104 in 27 s.
- Final: `python3 -m pytest -q --work-item w198 tests/scenarios/test_supervision.py ...` -> 10 passed (the environment forces the --work-item filter, so other modules deselect). `tests/scripts/test_bound.py` -> 1 passed. A `-k` run of the integrate scenarios -> 2 passed.
- `tools size --limit 300`: printed nothing.

## Tests changed under an allowance

none. (Generated tests of the retired scenarios went with them, per plan D0.)

## Open questions

none. The plan's defects D1-D3 (unbounded fix loop, one-string questions dropped, cut-short analysis not retried) are not fixed here; they need a follow-up work-item.

## Outside the file set

none.

Commit: ac8ed00f. Files changed: the five above. Concerns: the whole suite was not run by me (work run does).
