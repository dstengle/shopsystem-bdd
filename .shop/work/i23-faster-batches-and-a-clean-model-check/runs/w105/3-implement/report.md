## Budget
- scripts/workqueue_answer.py
- tests/scenarios/work_queue_answer_steps.py

## Changed
- `answer` refuses any of the seven line breaks (LF VT FF CR NEL LS PS) as its first check, before find/status/log; message "the answer has a line break in it; an answer is one line".
- One parsed When step "...an answer of two lines broken by {kind}" in work_queue_answer_steps.py. It writes a log.jsonl line for w1 when the Given left none (ready item), because the shared "are as they were" Then step reads the log; this is setup in my own step.

## Red / green
- Red: `python3 -m pytest -q --work-item w105`: 6 failed (VT, FF, NEL, LS, PS, and the not-awaiting-answer one). Step written first; failure at "work exits with an error" `assert done.returncode != 0` (returncode=0, stdout 'w1 ready'). Expected: answer accepted those breaks.
- After the code, the not-awaiting-answer scenario still failed with FileNotFoundError on log.jsonl (setup, fixed in the step as above).
- Green final: `--work-item w105`: 145 passed, 1 skipped; tests/scenarios/test_work_queue.py: 9 passed.
- Suite at start (brief's Suite record): 671 passed, 11 failed at 1b13869; the failures included the 7 line-break tests of this work-item and others unrelated to it.

## Size
`tools size --limit 300` printed nothing.

## Tests changed under an allowance
none

## Open questions
- Trailing line break at the end of an answer: refused; no scenario says to strip it.
- U+001C–U+001E accepted, yet supervise.py `held` splits on them.
- CR LF as one break, empty answer: no scenario.
- `work add` titles still accept VT, FF, NEL, LS, PS (not r15).

The plan contained no code. Commit: 579290a.
Files changed: scripts/workqueue_answer.py, tests/scenarios/work_queue_answer_steps.py.
