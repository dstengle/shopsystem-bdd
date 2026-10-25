# report of w178

## Budget

scripts/workqueue_request.py, scripts/supervise.py, scripts/supervise_all.py, scripts/supervise_intake.py,
tests/scenarios/supervision_request_steps.py (new), tests/scenarios/supervision_intake_steps.py,
tests/scenarios/test_supervision.py, features/supervision.feature (retire only). 8 files.

## What changed

- `workqueue_request.asked_here`: requests whose asker is this context (`internal` or `bounded-context/<path>`) and
  status awaiting-asker (reading B), with their open questions (D1, D4).
- `supervise.asked`: prints them after the statuses, turns exit 0 into 3 (D2, D3); used by `Run.run` and `run_all`.
- `Intake`: brief asks for a line outcome or a question `<line>. <question>` in the result's `questions` (D6, D7);
  `take` writes each with `workqueue_request.ask` under the lock before merging, resetting and faulting on failure (D8).
- Steps: new supervision_request_steps.py; intake steps replaced (old all-lines Given/Thens removed).
- Retired the three @deprecated scenarios (r9, r67 outline, r82) with `features retire`.

## Red / green

Start (suite record): 864 passed, 6 failed at da0bfcde; the 6 failing are this work-item's scenarios.
Red: `python3 -m pytest -q -n 0 --work-item w178` -> 6 failed (r9, r101, r67[open], r67[awaiting-upstream], r100, r82),
each StepDefinitionNotFoundError on the new Given/Then (expected: the steps were undefined). Deviation: I wrote the
production code before running the red again with my steps, the red run above was against the untouched base.
Green: same command -> 148 passed, 1 skipped. Touched modules (test_supervision, test_requests, test_work_queue with
`--whole-suite`): 271 passed, 5 xfailed, 9 xpassed.

`tools size --limit 300`: no output. `tools check`: nothing to check.

## Tests changed under an allowance

none (the retired scenarios' tests removed per Retires).

## Outside the file set

none.

## Open questions

- A result question not starting with `<n>. ` or naming a line the request lacks: today it is a fault of the round
  (the request stays as it was); the number is not validated against lines.
- A round that gives a question on a line and also a line outcome on it.
- Whether a run refused before it starts prints the requests found.
- Order of several requests/questions: request name order, question order.
- An awaiting-asker request with all questions answered: printed with no questions.
- workqueue_done.py:35 vs measure_read.py:71 "this context" forms; I accept both `internal` and the prefixed id.
- The check's exit is 3 (D3); an unreadable spec/index.md leaves only `internal` as this context.
- An intake round leaving an internal request awaiting-asker makes that same run exit 3 (D9).

The plan contained no code.

## Now possible

`work run` ends with an error naming each own request waiting on its asker with open questions; an intake round's
questions land in the request.

Commit: dfc78964.
