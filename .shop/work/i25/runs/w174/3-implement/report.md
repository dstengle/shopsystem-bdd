## Budget

- scripts/work
- scripts/workqueue_answer.py
- tests/scenarios/work_queue_answer_steps.py
- features/work-queue.feature (retire only, via `features retire`)
- tests/scenarios/test_work_queue.py (only if the retired scenario's binding needs removing)

## Changes
`work answer` got `--change`/`--accept` (mutually exclusive); `workqueue_answer.reviewed` sends a reviewer's question to ready or done and refuses with neither flag; the deprecated @r14 outline was retired via `features retire`; one new When step in work_queue_answer_steps.py. test_work_queue.py was not touched.

## Red and green
Red: `python3 -m pytest -q --work-item w174` gave 2 failed (r26, r27: StepDefinitionNotFoundError for the "saying that..." When steps), as expected: no step definition and no flag.
Green: `--work-item w174` and tests/scenarios/test_work_queue.py: 5 passed.
Suite record at start: 870 passed, 8 failed (including the three reviewer-answer tests in work_queue).
The plan contained no code.

## Tests changed under an allowance
none

## Open questions
- Either flag on a proposal's answer or on a non-reviewer question is ignored (plan decision 4); both flags together give argparse's usage error.
- The r28 scenario's step is not written (r28 is not accepted here).

## Outside the file set
none

## Size
`tools size --limit 300` printed nothing.

Commit: f06024a7
