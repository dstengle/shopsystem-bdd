## Budget
scripts/supervise_glossary.py, tests/scenarios/supervision_done_steps.py, tests/scenarios/supervision_proposal_steps.py

## Changed
- glossary_only_done skips ledger.md (finding 1, r161).
- The r161 Given now writes .shop/work/i1/ledger.md.
- Removed the unused `# noqa: E731` (finding 4).

## Runs
- Red: after the Given got a ledger, `pytest -n0 --work-item w225` failed the r161 glossary-only done scenario (the code read ledger.md as a non-glossary proposal). 1 failed, 188 passed.
- Green: `pytest -q --work-item w225`: 189 passed, 1 skipped.
- Suite at start: 1070 passed, 0 failed (expected failures: w212's parked scenarios).
- `tools size --limit 300`: prints nothing.

## Tests changed under an allowance
supervision_done_steps.py `started_glossary_only` (setup only: added a ledger.md write). supervision_proposal_steps.py `glossary_drafted` (comment only).

## Open questions
none (findings 2 and 3 are observations, not touched)

The plan contained no code to paste. Commit: 8322c119.
