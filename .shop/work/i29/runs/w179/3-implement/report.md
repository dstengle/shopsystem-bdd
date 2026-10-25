## Budget

- scripts/supervise_worker.py
- tests/scenarios/supervision_given.py

## Changed
- `Workers.keep_named` skips a value whose resolve/is_file raises OSError or ValueError (D1, D2).
- New given in supervision_given.py: implementer's result gets a `remark` field of ~295 chars with spaces.

## Red/green
- `python3 -m pytest -q --work-item w179`: red, `assert 'awaiting-answer' == 'green'` (OSError errno 36 from keep_named in traceback); the given was undefined before my step was added, so the step and fix were red together expected.
- Green: 144 passed, 1 skipped. tests/scenarios/test_supervision.py touched module: passes.
- Suite at start: 868 passed, 7 failed (incl. this scenario); expected failure test_requests empty delegation.
- `tools size --limit 300`: printed nothing.

## Tests changed under an allowance
none

## Open questions
none beyond plan §5 (questions as long string, NUL byte, errno 95, non-string values: covered by D1, unpinned).

Plan contained no code. Someone can now have a worker give prose fields without the worker's end. Commit: f0695846.
Files: scripts/supervise_worker.py, tests/scenarios/supervision_given.py.
