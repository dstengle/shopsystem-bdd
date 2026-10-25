# w187 report

## Budget
scripts/supervise_change.py, scripts/supervise_rounds.py, tests/scenarios/supervision_all_steps.py, tests/scripts/test_supervise_change.py (new), CLAUDE.md.

## Changed
- F4: `write_proposals` writes one proposal per capability, merging adds/changes/removes of every entry that names it, in order first named, duplicates within a list dropped.
- F11: stand-in `linger` 1 -> 3 (a margin); overlap assertion unchanged. No failure could be captured, so no lock change (plan decision 1, third branch). I did not run loaded repeat runs (no loop command allowed); the cause stays unknown.
- F2: ruff fixes at the two lines (re.MULTILINE, zip strict=False).
- Shape: `supervise_rounds.py` docstring and CLAUDE.md row name the integrate round (r91, r96) and r95's lock.

## Red/green
- Red: `python3 -m pytest -q -n0 tests/scripts/test_supervise_change.py` -> `assert 3 == 2` (one file per entry, the second overwrote the first). Expected: r92 says one proposal per capability.
- Green: same test passed; `python3 -m pytest -q -p work_items --work-item w187` -> 153 passed, 1 skipped, 56 subtests passed.
- Suite at start: 873 passed, 0 failed at 1b5a84f7 (with the expected list in the brief).
- `tools size --limit 300`: printed nothing.

## Tests changed under an allowance
none (the r95 steps' linger is a stand-in setting; assertions unchanged)

## Open questions
- Duplicate id across entries of one capability: dropped within a list; the same id under adds in one entry and changes in another is kept in both.
- Entry with only a capability gives a proposal with three empty lists.
- F11's true cause unknown (lock overlap not ruled out, none observed).
- `started` with an unreadable request gives no integrate round and no error.
- D4 (`work run i1` exits 0 with no work-item and a proposal awaiting answer) left as is, for the person.

The plan contained no code. Outside the file set: none.
