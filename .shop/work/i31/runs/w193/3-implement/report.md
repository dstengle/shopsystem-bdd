## Budget

- scripts/supervise_brief.py
- agents/initiative-round.md
- tests/scenarios/supervision_formulate_steps.py

## Changed

- r114 Then (`lists_written`) also asserts p1's apply brief asks for the change list in the result's `changes`.
- `supervise_brief.py`: shared `CHANGE_LIST` wording; the apply brief now carries it.
- `agents/initiative-round.md`: the `apply` kind gives the applied change list in `changes`.

## Red / green

- Red: `python3 -m pytest -q --work-item w193` -> 1 failed (the r114 scenario), 154 passed. Expected: the apply brief did not ask for `changes`.
- Green (final): same command -> 155 passed, 1 skipped, 56 subtests passed. `tests/scenarios/test_supervision.py`: 11 passed.
- Suite record at start: 902 passed, 7 failed at 32ce42d3 (failures in test_supervision.py kept-branch-review and done cases, not in w193's scenarios; not run by me).

## Tests changed under an allowance

none (the r114 Then was strengthened, which the plan's Decision 2 allows; nothing weakened)

## Open questions

- A DONE apply round with no `changes` stays a silent no-op; no line settles it.
- An apply list with no entry for the proposal's `argues` empties all lists (F2).
- Wording chosen: the apply text says the list covers every capability the round applied; `rewrite_lists` keeps only the `argues` entry.
- Proposal stays awaiting-answer while `work run` exits 0 (D3); awaiting-answer with no question goes to apply (D4).

The plan contained no code.

## Size

`tools size --limit 300` printed nothing.

## Outcome

`work run` now asks the real apply round for its change list, so r114 holds beyond the stand-in. Commit f92c4536. Files: the three above. No concerns.
