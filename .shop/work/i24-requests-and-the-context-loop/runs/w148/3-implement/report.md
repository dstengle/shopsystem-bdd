# Report of w148

## Budget
- tests/scenarios/work_queue_request_steps.py (new)
- tests/scenarios/test_work_queue.py
- scripts/workqueue_request.py

## Changed
- `request` refuses a `--lines` path that is not a regular file: `the file <path> does not exist`, before the read and any write.
- New steps module binding `an upstream that keeps no request` (reusing requests_write_steps.upstream_keeps_none) and `no file lines.md`; one import line in test_work_queue.py.

## Red / green
- Red: `python3 -m pytest -q --work-item w148` -> 1 failed; stderr held a traceback, `FileNotFoundError: ... 'lines.md'`, so the Then "no Traceback" assertion failed. Expected: no check existed.
- Green: same command -> 155 passed, 1 skipped. Also tests/scenarios/test_work_queue.py and test_requests.py: 13 passed.
- Suite record at start: 810 passed, 1 failed (this scenario) plus the expected-failing list in the brief.

## Tests changed under an allowance
none

## Open questions
- Wording of the refusal for a --lines path that is a directory (it is refused with the same "does not exist" text).
- A lines file that exists but is unreadable (PermissionError) still escapes as a traceback.
- Missing lines file with neither --source nor --thread: origin refusal wins, as before.
- Defects D4 to D7 of the research notes are left for other work-items.

The plan contained no code.

## Size
`tools size --limit 300` printed nothing.

## Result
Someone running `work request` with a missing lines file now gets `work: the file lines.md does not exist`, exit 1, nothing written. Commit: fd180a0.

Files changed: scripts/workqueue_request.py, tests/scenarios/work_queue_request_steps.py, tests/scenarios/test_work_queue.py.
