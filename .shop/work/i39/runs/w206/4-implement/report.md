## Budget
- scripts/workqueue_list.py
- tests/scripts/test_workqueue_list.py (new)
- scripts/supervise_change.py
- scripts/supervise_rounds.py
- tests/scripts/test_supervise_change.py

## Changes
- `work list --json` drops `turn` from requests (D-a).
- `work list` refuses an unreadable `raised.jsonl` line, naming file and line (D-b).
- `write_proposals(found, stage_dir, own)`: the proposal the round was started for is rewritten as before; another held proposal gets the round's ids merged (union, appended after its own) into adds/changes/removes; its status is untouched, drafts sentence replaced (D-e, D-f). `supervise_rounds.py` passes `name`.

## Runs
- Red: `python3 -m pytest -q -n 0 tests/scripts/test_workqueue_list.py tests/scripts/test_supervise_change.py` gave 3 failed (turn present in JSON; traceback on malformed line; write_proposals takes no `own`), 1 passed. Expected: the behaviours were absent.
- Green: same command, 4 passed. `--work-item w206`: 154 passed, 1 skipped. Supervision integrate/draft/proposal scenarios (`--whole-suite -k`): 84 passed, 1 xfailed.
- Suite at start (brief's record): 962 passed, 0 failed at 694a5f8e, with the listed expected failures.
- Size check: `tools size --limit 300` printed nothing.

## Tests changed under an allowance
none

## Open questions
- Blank line in raised.jsonl skipped (unchanged); a well-formed line lacking only `initiative` is accepted (unchanged).
- An id the round lists in a different field than the other proposal holds it in: both kept, unchosen.
- B023 lambda in supervise_change left as it was.

The plan contained no code. Commit: e4e61321.
