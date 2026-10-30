# w238 research notes (supervision r188, r189)

No `tools map` exists: `tests-of` and `untested` are unavailable, so every test list below is `by search`.

## 1. Why each scenario is red today

Command run: `python3 -m pytest -q --work-item w238` (run). 183 ran: 180 passed, 1 skipped, 2 failed.

- r188, `features/supervision.feature:1168` (capability redraft). Fails at its first Given, line 1171: `StepDefinitionNotFoundError`, "i1's capability-proposal p1, for thing, is awaiting-answer, its adds naming ... and its removes naming thing#r3" (run). No step matches the `adds/changes/removes naming` form with `for thing`. The When/Then never ran. Behind it: `scripts/supervise_change.py:Changes.rewrite_lists` replaces all three lists (read), see part 2.
- r189, `features/supervision.feature:1180` (glossary redraft). Fails at its first Given, line 1184: `StepDefinitionNotFoundError`, "i1's glossary-proposal g1 is awaiting-answer, its adds naming the term ..." (run). `supervision_proposal_steps.py:133` requires a `## Questions` clause, so it does not match. The later steps at lines 1186 ("a round of the kind integrate is started for g1, redrafts the term") and 1189 are also undefined (read: no `redrafts` step exists in `tests/scenarios`). Behind it: `supervise_change.py:Changes.write_proposals` glossary branch (lines 129-138) overwrites `glossary.md` with the change list's terms only (read).
- The Then steps at 1177 and 1189 were not reached, so their status is unknown (run stopped first).

## 2. Old assumptions

Requirements: r188 (integrate keeps unnamed ids of a redrafted capability-proposal), r189 (integrate keeps unnamed terms of a redrafted glossary-proposal). r145 (apply writes the lists from the applied change list) stays as it is.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_change.py:Changes.rewrite_lists (59-72) | replaces adds, changes, removes with the ids the entries give for its capability; unnamed ids dropped | r188: the integrate case must keep unnamed ids; apply (r145) keeps replace, so split the two | tests/scripts/test_supervise_change.py:test_a_round_started_for_one_proposal_merges_its_ids_into_another_held_proposal; apply path: features/supervision.feature:1129 (r145) | by search |
| scripts/supervise_change.py:Changes.write_proposals, own held branch (109-121) | calls rewrite_lists with the round's one entry for the proposal the round was started for | integrate needs a merge here (as merge_lists already does for non-own proposals), not a replace | tests/scripts/test_supervise_change.py:test_a_round_started_for_one_proposal_merges_its_ids_into_another_held_proposal | by search |
| scripts/supervise_change.py:Changes.write_proposals, glossary branch (129-138) | writes glossary.md fresh from the change list's terms; never reads a held glossary-proposal | r189: keep held terms; find the held glossary-proposal by its kind, as proposal_for does for capabilities | features/supervision.feature:1575-1578 (r171, fresh write only, no held proposal): by search | by search |
| scripts/supervise_rounds.py:175 (apply branch calls rewrite_lists) | apply rewrites the proposal's lists from the applied change list | none for r188; must keep replace (r145) | features/supervision.feature:1129-1135 (r145), by search, not run | by search |
| scripts/supervise_rounds.py:206 (integrate calls write_proposals with own=name) | passes the started proposal's name as `own` | the own branch is where r188 applies; the glossary branch ignores `own` | none beyond the unit test above | by search |

No other caller of rewrite_lists, merge_lists or write_proposals in `scripts/` or `tests/` (grep for those names, excluding `.shop/`). `tools refs` on the full names found the callers listed above.

Naming conflict (both readings given, not decided): the code names the glossary-proposal `glossary.md` (supervise_change.py:134); the accepted scenarios' steps name it `g1.md` (features/supervision.feature:1184, supervision_proposal_steps.py:138). A fix that matches by file name would miss `g1.md`. Matching by `kind: glossary-proposal` covers both.

Semantics conflict (both readings given): r188 read literally keeps every unnamed id, so an integrate round cannot drop an id from an awaiting-answer proposal. Reading A: integrate unions (merge_lists style), apply replaces. Reading B: the integrate round's change list is the whole new list and only unnamed ids the scenario names are kept. r188's text supports A. The accepted scenario (1168-1177) matches A.

## 3. Tests the requirements make impossible to keep

- tests/scripts/test_supervise_change.py:test_a_round_started_for_one_proposal_merges_its_ids_into_another_held_proposal (lines 26-41), by search. It asserts `adds: [thing#r5]` on p1, the own proposal, which drops the held `thing#r1`. Under r188 it fails: the held id must stay, giving `adds: [thing#r1, thing#r5]`. Must change.
- Same test, lines 37-40 for p2 (merge path, not own): verified sound, unchanged by r188.
- tests/scripts/test_supervise_change.py:test_a_round_started_for_one_proposal_leaves_another_held_proposals_drafts_path_as_it_was (44-53): merge path, verified sound.
- test_two_entries_naming_one_capability_give_one_proposal_with_both_entries_ids (56-63): fresh write, verified sound.
- features/supervision.feature:1129-1135 (r145, apply replaces): must still pass; it pins the apply replace, so the change must not alter the apply branch. Not run.
- features/supervision.feature:1157-1165 (r148): checks only that one proposal exists; sound.
- features/supervision.feature:1559-1568 (r187, merge into another held proposal): sound, unchanged.
- features/supervision.feature:1575-1578 (r171, glossary fresh write): sound if the fix keeps the no-held-glossary case.
None found beyond the first. Search: integrate-round scenarios and unit tests for own-proposal rewrites (grep for `rewrite`, `redraft`, `own`).

## 4. The file set

Production:
- scripts/supervise_change.py (140 lines): integrate-own branch merges instead of rewrite_lists (keep held ids); glossary branch reads a held glossary-proposal by kind and keeps its terms; rewrite_lists kept for apply. Shown by the read of lines 40-140 and by the grep above.
- scripts/supervise_rounds.py (275 lines): no change expected (apply call 175 keeps replace; integrate call 206 passes own). Listed because it is on the path; edit only if the fix needs the round kind passed to write_proposals.

Tests:
- tests/scripts/test_supervise_change.py (63 lines): change the assertion at line 37 to keep `thing#r1`; add a glossary-keeps-terms unit test.
- tests/scenarios/supervision_integrate_steps.py (252 lines): new steps for the capability Given at 1171 and the glossary Given at 1184 and its redraft at 1186; the Then at 1177 and 1189 need steps too (not confirmed defined; run stopped first). Room 48 lines.
- tests/scenarios/supervision_reintegrate_steps.py (175 lines): the p1 integrate step at line 56 ("the integrate round for p1 ... ") may already serve the redraft at 1174; check before adding. Room 125 lines.

Not changed: features/supervision.feature (scenarios exist), spec/capabilities/supervision.md (r188, r189 exist).

Room under the limit (CLAUDE.md gives 300 lines; `tools size --limit 300` printed nothing, so no file is over):
- scripts/supervise_change.py: 140 lines, room 160
- scripts/supervise_rounds.py: 275 lines, room 25
- scripts/supervise.py: 295 lines, room 5 (on the path through Changes mixin, line 64; not edited)
- tests/scripts/test_supervise_change.py: 63 lines, room 237
- tests/scenarios/supervision_integrate_steps.py: 252 lines, room 48
- tests/scenarios/supervision_reintegrate_steps.py: 175 lines, room 125

Reused: supervise_change.py:Changes.merge_lists (82-92) already keeps held ids; the integrate-own fix can follow it.

Git status: I wrote only notes.md and result.json in the stage directory. The worktree was not touched.
