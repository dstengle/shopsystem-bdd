# Report of w129

## Budget
- scripts/workqueue.py
- scripts/work
- scripts/workqueue_status.py
- tests/scenarios/test_requests.py
- tests/scenarios/requests_show_steps.py (new)

## Changed
- `workqueue.requests()` reads `.shop/work/requests/q*.md` (name, status, turn, source), natural order.
- `work show` prints `q<n> <status> <turn>` after the work-items; `--json` gains a `requests` key.
- `workqueue_status.uncited()` reads observations with dates; `work status` with no initiative prints
  `observation <id> <date>` lines after the initiative blocks; `--json` gains `observations`. `open_text` (the hook) passes
  `report=False` so the hook text is unchanged (plan D3).
- New `tests/scenarios/requests_show_steps.py`, bound in `test_requests.py`.

## Red and green
- Red: `python3 -m pytest -q -n 0 --work-item w129` → 2 failed (test_requests show and status), on the Then lines (the output held
  no request line / only the `initiative i1 started` block), after the steps were written; before them, undefined steps.
- Green: same command → 144 passed, 1 skipped. Also `--whole-suite` on test_work_queue, test_migration_tools, test_requests:
  132 passed, 13 xfailed, 23 xpassed, none failed.
- Suite at start (brief): 731 passed, 2 failed (the two w129 scenarios among 60+ already red).
- `tools size --limit 300`: prints nothing.

## Tests changed under an allowance
none

## Open questions
- Order of observation lines (file order used, unpinned); missing requests dir / observations file (empty part);
  request with unclosed frontmatter (skipped); observation with no `date:` (prints `None`); request with no status/turn (prints `None`).

## Plan code
The plan contained no code.

## Outside the file set
none

## Now possible
`work show` lists requests with status and turn; `work status` lists observations nothing cites.

Commit: d39f691
Concerns: none.
