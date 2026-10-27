## Budget

- scripts/workqueue_request.py (only file touched)

## What changed
- `gate`: in a repository with `## Upstreams`, `--source` alone is an internal request and is allowed; `--source` with `--thread`/`--raised-for` is still refused (r30); neither source, thread nor raised-for is refused (r31).
- New `_refuse_upstream_part`: a request is to an upstream when its asker is this repository's id and it names no `source`; used by `outcome`, `ask`, `resolve` (r34), naming the upstream. Internal requests (asker the repo itself, with source) are written as either side.

## Red/green
No scenario covers either fix (features cannot be edited); the work-item's rulings name them. No red run was possible. Plan contained no code (none for this narrowed work).
Suite record at start: 989 passed, 0 failed (expected failures listed in brief are w212's transport scenarios).
Final: `python3 -m pytest -q --work-item w211` -> 165 passed, 1 skipped; test_requests.py + test_supervision.py -> 15 passed.
tools size: nothing over 300.

## Tests changed under an allowance
none

## Open questions
- `reply` by the upstream on a request from another asker (finding 2, last part) is not refused: with no transport there is no other path for an answer; left unchosen. `turn` side check likewise not added.
- Findings 3-7 (Minor) deferred as ruled.
- No scenario row for the new refusals of `ask` and `resolve`, nor for an internal request in a repository with upstreams; needs a formulation.

Commit: 7b3f8f29
