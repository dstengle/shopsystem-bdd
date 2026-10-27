# w205 report

## Budget
scripts/work, scripts/workqueue_list.py (new), CLAUDE.md, tests/scenarios/work_queue_list_steps.py (new), tests/scenarios/test_work_queue.py, tests/scenarios/work_queue_status_steps.py, tests/scenarios/work_queue_withdraw_steps.py (added: the `it gives` step had to be narrowed, see below). 7 files.

## Outside the file set
tests/scenarios/work_queue_withdraw_steps.py: its `it gives {triples}` parse matched every `it gives ...` line, so it was ambiguous with the new r35/r38 steps. It is now a regex requiring `<name> in <initiative> with <status>`; its meaning for r11 is unchanged.

## What changed
- `work list [--json]` and `work show [target] [--json]` (scripts/work, scripts/workqueue_list.py). No-target `show` keeps today's output (D1); `status` untouched (D2).
- `show <initiative>` reuses `workqueue_status.status`; `show <work-item>` uses `workqueue.find` and prints status and open questions.
- r39: `list` reads `.shop/work/<initiative>/raised.jsonl` only (reading A); an entry whose last status is not `delivered` prints `initiative i1 waiting on q1 (in ctx-up, accepted)`.
- Steps: new work_queue_list_steps.py; `with_state` widened (work-item/work-items, question clause); `open_with_proposal` takes any state.
- CLAUDE.md: module-map row for workqueue_list.py.

## Red and green
- Red: `python3 -m pytest -q --work-item w205 -n0`: 7 failed (undefined Givens/Thens for list and show; argparse exit 2 "unrecognized arguments: w1", "invalid choice: 'list'"), expected as the plan's section 1.
- Green: same command: 151 passed, 1 skipped, 0 failed (this includes the 7 w205 scenarios). Touched modules test_work_queue.py, test_requests.py, test_migration_tools.py: 7 passed (the work-item filter is active in this environment).
- Suite at the start: 955 passed, 21 failed at 5d1c2c55 (the w205 scenarios and requests tests among them). I did not run the whole suite.
- `tools size --limit 300`: printed nothing; no file over.

## Tests changed under an allowance
none (step definitions were respelled/widened: work_queue_status_steps.py `with_state` and `open_with_proposal`, work_queue_withdraw_steps.py `gives`; no test asserts changed).

## Open questions
- Nothing writes raised.jsonl or updates its status; a malformed line in it raises a traceback (unchosen).
- Whether `list --json` carries the waiting of r39 (not carried).
- Request with no turn / work-item with no status print as `None`; `list` on an empty queue; `show q1`; name that is both initiative and work-item id (initiative wins); detached HEAD in `show <initiative>`; order of lines in `list`.

## Plan
The plan contained no code.

## Now possible
`work list`, `work list --json`, `work show <initiative|work-item> [--json]`, and the waiting line. Commit: bc517d85.
