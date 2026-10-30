## Budget
- scripts/workqueue_list.py
- tests/scripts/test_work_show_request.py (new; outside the fileset, a unit test of the unsettled-line case the finding asks for)

## Outside the file set
tests/scripts/test_work_show_request.py (new test file).

## Changed
`request_parts` in scripts/workqueue_list.py prints every line, a line with no outcome as `unsettled`. New unit test tests/scripts/test_work_show_request.py.

## Runs
- Red: `python3 -m pytest -q tests/scripts/test_work_show_request.py` failed: line 2 missing from output (expected: old code skipped lines without outcome).
- Green: same test passes; `python3 -m pytest -q --work-item w232`: 184 passed, 1 skipped.
- Suite record at start: 1087 passed, 0 failed (with listed expected failures).
- `tools size --limit 300`: no output.

## Tests changed under an allowance
none
## Open questions
none
Plan contained no code pasted. Commit d32ec491.
