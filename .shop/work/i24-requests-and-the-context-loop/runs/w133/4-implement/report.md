# Report of w133

## Budget
scripts/measure_read.py, scripts/workqueue_request.py, scripts/measure_build.py, scripts/measure_show.py, scripts/measure,
tests/scenarios/batch_measurement_world.py, tests/scenarios/batch_measurement_request_steps.py (new),
tests/scenarios/test_batch_measurement.py

Suite at start: 767 passed, 3 failed at 3e80c5c (the 3 are w133's own scenarios; the rest were expected red).

## What changed
- `workqueue_request`: `_path`/`_field` made public as `path_of`/`field` (callers renamed).
- `measure_read.request_of`: reads `fulfils` in the initiative's initiative.md and the request through work's reader. The origin is
  internal (asker `internal` or this context's id), else external. Unreadable links are refused (missing request, no asker, several ids).
- `measure_build.figures_of`: adds `request` {id, origin} only when linked. `measure_show` prints it. `measure` CONTRACT names it.
- Tests: World.request and flush writing initiative.md and the request; new `batch_measurement_request_steps.py`; star import.

## Red and green
- Red: `python3 -m pytest -q --work-item w133 -n 0`: 3 failed, StepDefinitionNotFoundError (Given "i7-cart fulfils no request" etc.).
  After the steps were written, KeyError: 'request' on the r63 Thens (expected: no code gave the figure).
- Green: same command, 145 passed, 1 skipped, 0 failed. Also with `--work-item ""` on test_batch_measurement, test_measure_runs,
  test_work_queue, test_requests: 117 passed, 4 failed. The 4 are in the Suite record's expected-red list.
- r64's own Givens run the stage twice (the log Given writes it), so its Then checks "at least one" stage.

## Tests changed under an allowance
none
## Open questions
Plan section 5 cases left unchosen: request status not accepted or of another context; `fulfils` not a request id; `measure compare` on origins.
The check on `fulfils` is a character-class test only.
## Plan contained code: no.
## Outside the file set: none. Size check: `tools size --limit 300` printed nothing.
Commit: b419ef0. Surprise: the shell has a default work-item filter; `--work-item ""` turns it off.
