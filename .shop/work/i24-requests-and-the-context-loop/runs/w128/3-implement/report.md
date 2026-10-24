# Report of w128

## Budget
scripts/work, scripts/workqueue_request.py (new), CLAUDE.md, tests/scenarios/test_requests.py (new), tests/scenarios/requests_steps.py (new), tests/scenarios/work_queue_git_steps.py

## Changed
- New `scripts/workqueue_request.py`: `outcome`, `turn`, `resolve`, each committed through `workqueue.committed`. Request form per plan D2 (`## Lines`, `## Outcomes`, `## Resolution`, entries `<n>. <text>`). `resolve` is `work resolve <request> --line N REQ VERSION` and is refused on a request that is not accepted.
- `scripts/work`: subcommands `outcome`, `turn`, `resolve`. CLAUDE.md: module-map row.
- Tests: `test_requests.py`, `requests_steps.py` (Givens, When, Thens); `work_queue_git_steps.py`: `new_commit_holds` maps a request id to its path, new Then "nothing work keeps for {request} differs...".
- The Given initialises a git repo (the `repo` fixture is not one, and the commands commit).

## Red and green
- Red: `python3 -m pytest -q -n 0 tests/scenarios/test_requests.py -k "..."`: 5 failed. Cause: `work: error: argument cmd: invalid choice: 'outcome'` (and turn/resolve); no command existed.
- Green: `python3 -m pytest -q --work-item w128`: 147 passed, 1 skipped. `tests/scripts`: 141 passed.
- Suite at start: 731 passed, 0 failed (listed failing items are "expected" ones of the brief's record).
- Could not run `tests/scenarios/test_work_queue.py` alone: the `--work-item w128` filter is applied in this session even without the flag (`SystemExit: w128 accepts none of the scenarios it collected`). I changed `new_commit_holds` (plain paths still resolve as before), so `work run`'s suite run is the check.

## Tests changed under an allowance
none (new_commit_holds respelled with a path mapping; assertions unchanged).

## Open questions
Per plan section 5: resolve with a non-accepted line or missing lines; duplicate line numbers; outcome out of range or unknown word; malformed requirement/version; commit messages (`work <cmd>: <request>`); a log for requests; turn with every line withdrawn (becomes refused); turn from the asker only flips the turn. A request id that does not exist is refused (needed to avoid a traceback).

## Other
The plan contained no code. `tools size --limit 300`: nothing printed. Defects D1/D2 of the research notes (withdraw takes a request; model check on requests dir) not fixed, as planned. Merge risk with w126/w127: shared module and step names.

Commit: 15b3801 work outcome, turn and resolve: a request changed and committed (requests r8-r12)
