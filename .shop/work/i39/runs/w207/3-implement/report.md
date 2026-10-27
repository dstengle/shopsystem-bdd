## Budget

- scripts/supervise_change.py
- tests/scripts/test_supervise_change.py
- scripts/workqueue_status.py
- scripts/workqueue_list.py
- tests/scripts/test_workqueue_list.py

## Changed
- supervise_change.py: on the merge path (held.stem != own) the held proposal's drafts sentence is left alone (finding 2).
- workqueue_status.py: `ledger` reads through `workqueue.read` (refusal naming the file when not UTF-8) (D1).
- workqueue_list.py: a work-item file with no kind is refused as "has no kind" (D3).
- Tests: 1 new in test_supervise_change.py, 2 new in test_workqueue_list.py.

## Red and green
Red: `python3 -m pytest -q -n 0 tests/scripts/test_supervise_change.py tests/scripts/test_workqueue_list.py` -> 3 failed, 4 passed (drafts path repointed to drafts/; ledger Traceback; "w1 is a None, not a work-item"). Expected: the fixes were not written.
Green: same command -> 7 passed. `--work-item w207` -> 157 passed, 1 skipped, 56 subtests passed.
Suite record at start: 965 passed, 0 failed at 2b50f401 (expected failures listed in the brief).
The seven accepted scenarios passed before any change (the plan says so). This is a findings fix, so the brief's "fix those and nothing else" applied rather than the red-green hand-back.

## Tests changed under an allowance
none

## Open questions
- Finding 2: p2's apply round still reads p2's own drafts, so merged ids may be dropped on apply (q20 line).
- D1: `show <initiative> --json` for an undecodable ledger takes the same code path and refusal; not separately tested.
- D3: a kind that is present but empty is not distinguished from a wrong kind.
- Finding 1 unchanged (already ruled).

The plan contained no code. `tools size --limit 300` printed nothing.
Commit: b8dab1b2. Files: the five in Budget.
