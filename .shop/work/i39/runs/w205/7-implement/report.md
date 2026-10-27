## Budget
scripts/workqueue_list.py (1 file).

## Changed
`work_item` in scripts/workqueue_list.py refuses, naming the target and its kind, when the file it resolves has a `kind` other than work-item (review F1; the answer of 2026-10-27). This also uses `Refused`, so F5's F401 goes. Commit bf231ddc. The earlier commit (a033c460/bc517d85) already held the work.

## Runs
- Suite record at start: 962 passed, 14 failed (requests scenarios, restored on main by hand; not w205's) at 1508cd06.
- No scenario describes the refusal, so there was no red to run; the change is the ruled fix. Not probed by a test (no feature line to bind; .feature files are not mine).
- Final: `python3 -m pytest -q --work-item w205` → 151 passed, 1 skipped, 56 subtests passed.
- `tools size --limit 300`: printed nothing.

## Tests changed under an allowance
none

## Open questions
F2 (malformed raised.jsonl), F3 (`--json` carries no waiting), F4 (`{state}` ignored) left as the review's observations; no scenario covers them.

## Plan
The plan contained no code; none was pasted.

## Concerns
The refusal of `work show q1` is covered by no scenario.
