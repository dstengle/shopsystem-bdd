## Budget
- scripts/work
- scripts/workqueue_answer.py
- tests/scenarios/work_queue_answer_steps.py
- features/work-queue.feature (features retire only)

## What changed
`work answer` takes `--change`/`--accept`; `workqueue_answer.answer` refuses a reviewer's question (log `before`=done) without a verdict (r28), moves to ready (r26) or done (r27); both flags together are refused (D1). Four step definitions added. Deprecated r14 outline retired with `features retire`.

## Red and green
Red: `python3 -m pytest -q --work-item w176` -> 3 failed (StepDefinitionNotFoundError for the new When steps), expected. Green: same command after the change, with tests/scenarios/test_work_queue.py: 6 passed.
Suite at start: 868 passed, 3 failed at 9c79765c (the three were these scenarios).

## Tests changed under an allowance
none
## Open questions
Flags on non-reviewer askers/proposals; delegated reviewer answer path (supervise_answers) still lands done; --accept item gets reviewed again by work run (plan part 5).
## Notes
The plan contained no code. `tools size`: no lines (nothing over 300). w176.md has no Retires entry; retired per plan D3.
Commit: 35f79e86. Files: scripts/work, scripts/workqueue_answer.py, tests/scenarios/work_queue_answer_steps.py, features/work-queue.feature.
