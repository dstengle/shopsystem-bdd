## Budget
scripts/work, scripts/workqueue_request.py, CLAUDE.md, tests/scenarios/test_requests.py, tests/scenarios/requests_write_steps.py (new; keeps requests_steps.py small)

## Changed
- `work request` (title, --from, --lines, repeatable --source, --thread) and `workqueue_request.request`: refuses no origin (r3), refuses first line failing `model_parse.ears` naming "line N" (r2), writes q<n>.md open/upstream turn, commits it (as the other request commands do), prints q<n>.
- New steps module for r1-r5 Givens/Whens/Thens; CLAUDE.md row updated.
- At start, outcome/turn/resolve already existed (w128); r4/r5 needed only steps.

## Red/green
Start: `pytest -q -n 0 --work-item w126` -> 10 failed (undefined steps / no `request` command), expected: no steps, no command.
Final: same command -> 152 passed, 1 skipped. test_requests.py + test_work_queue.py: 10 passed.
Suite record at start: 10 failed (listed in brief) at b1c11fe.
size: no file over 300.

## Tests changed under an allowance
none
## Open questions
Both --source and --thread; both faults at once (origin checked first); empty/blank lines file; newline in title/values; unreadable lines file; missing spec/index.md (refused by context_path); first failing line only named.
## Plan code
Plan contained no code.
## Outside the file set
requests_write_steps.py (new test module, within the plan's allowance to split steps).
