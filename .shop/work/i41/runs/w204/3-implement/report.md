# Report of w204 (implement)

## Budget

Touched (11): scripts/supervise_rounds.py, scripts/supervise_change.py, scripts/supervise_brief.py, scripts/supervise.py, agents/initiative-round.md, features/supervision.feature (`features retire` only), tests/scenarios/supervision_formulate_steps.py, tests/scenarios/supervision_rounds_steps.py, tests/scenarios/supervision_reintegrate_steps.py (new), tests/scenarios/test_supervision.py.

## Outside the file set

`scripts/supervise.py`: `move` gained an `also=()` parameter passed to `commit`, so the proposal's move to drafted is one commit with its rewritten file (D5). `supervision_rounds_steps.py`: one step regex widened (`, for thing,`). The plan's other test files (given, proposal, integrate, outputs steps) were not needed: the new steps are in the new module `supervision_reintegrate_steps.py` (CLAUDE.md's map covers `tests/scenarios/` as a module a concern).

## What changed

- Apply result field `nothing_applied` (D1): with no questions and no change list, `run_round` commits the round with no transition and no question (r147); `route` sends an awaiting-answer proposal whose latest stage directory is such an apply to `integrate`/`drafted` (r140).
- Integrate round for a proposal keeps its status while it runs (`before = agrees`, no start of the initiative) and ends in `move(..., drafted)` with the rewritten proposal in one commit (r142, r143).
- `write_proposals` rewrites in place a proposal of the initiative that argues the named capability (lists and drafts sentence), writing no second file (r142, r148).
- Proposal integrate brief: request and accepted lines from `initiative.md`, `Ledger:` line and Read entry, the proposal's questions and answers, and `Earlier drafts path (read only):` (r141).
- agents/initiative-round.md: the two bullets saying how to give `nothing_applied` and how to redraft.
- Retired with `features retire`: the r80, r114, r71 deprecated scenarios.

## Red and green

- Red (before code): r144, r145, r146 failed with StepDefinitionNotFoundError on the apply Given; after widening the Given regex they pass (the behaviour existed). r140, r141, r143, r142, r147 failed on their Then lines (e.g. r147: `AssertionError: - Is a title ... - The apply round of p1 gave no change list; which capabilities' lines did it apply?`; r140: no integrate start in the log; r141: `work: there is no request  under .shop/work/requests`).
- r148 passed vacuously on its first run (no route yet, so nothing wrote a second proposal); it went red on its Then once r140's route existed (`AssertionError: (['thing.md', 'p1.md'], '')`) and green with the in-place rewrite. Noted rather than a hand-back, since its Then does fail on the Then line once the route is there.
- Final: `python3 -m pytest -q --work-item w204` all pass (nine accepted scenarios); `tests/scenarios/test_supervision.py --work-item w204 --whole-suite`: 261 passed, 1 xfailed; `tests/scripts` 143 passed.
- Suite at start (brief): 948 passed, 10 failed at be28c607 (the failing list included this work-item's scenarios).

## Tests changed under an allowance

none (a step regex widened in supervision_rounds_steps.py `answered_proposal`: setup only, adds an optional ", for thing," alternative).

## Open questions

- An apply result giving `nothing_applied` together with questions or a change list: treated as an ordinary apply (the field is ignored), not chosen by any scenario.
- After a redraft, the new gate's questions are added under the kept `## Questions` and earlier answers still count toward `due`; whether apply can start before the person answers the new gate is not covered.
- A redraft whose change list names another capability that already has a proposal: rewritten in place likewise; r148 speaks only of p1's.
- A second apply that applies nothing after a redraft loops back to integrate.
- The stand-in's integrate for p1 under "every other round ends" gives no change list (r96 error); the scenarios hold either way.

The plan contained no code.

## Size check

`tools size --limit 300` printed nothing: no file over.

## Commit

d076baa8 supervision: an apply round that applies nothing sends its proposal back to integration (r140-r148)
