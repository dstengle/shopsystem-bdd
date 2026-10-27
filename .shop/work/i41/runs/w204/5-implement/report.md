## Budget
scripts/supervise_rounds.py (1 file)

# Report: fix of finding F1 only

Changed `Rounds.applied_nothing` in scripts/supervise_rounds.py: trailing `-integrate` stage directories of the proposal are skipped before looking at the latest stage, so a faulted or change-list-less integrate round leaves the proposal routed to integrate again.

Red/green: no new scenario covers the retry (no .feature edits allowed; the reviewer's suggested scenario needs a formulation first). Not red-run by a scenario; existing scenarios stay green.
Suite record at start: 955 passed, 0 failed (with the listed expected failures).
Final run: `python3 -m pytest -q --work-item w204` → 153 passed, 1 skipped; tests/scenarios/test_supervision.py → 9 passed.
Size: `tools size --limit 300` printed nothing.

## Tests changed under an allowance
none

## Open questions
The retry has no scenario; a line/scenario for it (r86/r140) is for formulation. F2-F5 not part of this fix.

The plan contained no code to paste.
Commit: d6667395. File changed: scripts/supervise_rounds.py.
