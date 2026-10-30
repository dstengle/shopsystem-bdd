# Report w238: HAND-BACK on r189

## Budget

scripts/supervise_change.py, tests/scripts/test_supervise_change.py, tests/scenarios/supervision_reintegrate_steps.py (3 files).

## Suite at start

1084 passed, 0 failed (with the listed expected failures).

## Changed

- `Changes.redraft_lists` (new) in supervise_change.py: the own capability-proposal of an integrate round keeps the held ids the change list does not name; a named id sits in the list the change list gives (r188). Apply still uses `rewrite_lists`.
- Steps in supervision_reintegrate_steps.py for r188 and r189 (Givens, redraft rounds, Thens). The p1 Questions/Answers step now takes `[pg]1`.

## Red and green

- r188 red: `python3 -m pytest -q --work-item w238` gave `AssertionError ... adds: [thing#r5] ... removes: []` (p1 lost thing#r4, thing#r2 and thing#r3), as expected from `rewrite_lists`.
- r188 green after the change: the scenario and tests/scripts/test_supervise_change.py pass.
- r189: red now, but not for a reason the plan names (below).

## Stop: HAND-BACK, r189

Observed: with all r189 steps defined and no production change, the scenario passed vacuously. I added an assertion that an integrate round for g1 was started, and it failed:
`AssertionError: ([{'event': 'start', 'argv': ['-p', 'Read the brief file .../worktrees/g1-1-apply/.shop/scratch/1-apply/brief.md ...`.
Only an apply round started for g1. `supervise_glossary.ROUTES = {"drafted": ("gate", ...), "awaiting-answer": ("apply", "approved")}  # no further round (r167)`. `supervise_rounds.due` sends only capability-proposals back to integration (`route`/`sent_back`). When I made the apply round give `nothing_applied` for g1, `work run` looped until the 120 s timeout. So no integrate round can be started for a glossary-proposal in the code today. The plan says "Integrate already passes `own`, and that is enough", which is wrong. r189 needs routing code in `supervise_rounds.py` and/or `supervise_glossary.py`: neither is in the file set and the plan names no such work. The decision of when a glossary-proposal is sent back to integration is open.

The glossary branch of `write_proposals` (writing into the held g1 by kind, keeping its unnamed terms) is not written, because it can't be reached by the scenario until routing exists.

Scenarios: r188 green; r189 red (its Then step asserts an integrate round for g1 ran).

The brief's pytest probes: one still-running background pytest (hung) may remain; I had no permission to kill it.

## Tests changed under an allowance

The plan lists `test_a_round_started_for_one_proposal_merges_its_ids_into_another_held_proposal`: its p1 assertion is now `adds: [thing#r1, thing#r5]` as the plan says. Nothing else.

## Open questions

- How a glossary-proposal whose apply round applied nothing returns to integration (routing); r166/r167 say no further round.
- Plan part 5 cases: a change list naming the glossary when a glossary-proposal is held and the round was not started for it; the same id in two lists; unchanged.

## Other

The plan contained no code. Size check: `tools size --limit 300` printed nothing.
Files: scripts/supervise_change.py, tests/scenarios/supervision_reintegrate_steps.py, tests/scripts/test_supervise_change.py.
Commit: 440352d6.
