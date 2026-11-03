# w242 research: supervision r221

Accepted: supervision#r221@0.29, scenario `features/supervision.feature:2072`. No `tools map` exists, so every tests-of count is by search. `tools refs` misses calls through a module attribute (`supervise_glossary.route` is called at `supervise_rounds.py:59`, refs says 0).

## 1. Why each scenario is red today

Scenario: "an apply round that gives an answer the drafts it applied do not hold for a glossary-proposal is followed by a new integrate round for the glossary-proposal"

Command (run): `python3 -m pytest -q --work-item w242`. Result (run): 1 failed, 181 passed, 1 skipped; the run collected 183 tests, not only this scenario (why unexplained).

Failure (run): `StepDefinitionNotFoundError` on the first Given, `features/supervision.feature:2074`.
- Cause (read): `tests/scenarios/supervision_proposal_steps.py:142-143` takes answers as `"[^,]+?"`; the answer "One line an event, and a ledger is the file of those lines." holds a comma, so the pattern cannot match.
- Later steps, undefined (read, not reached): `supervision_reintegrate_steps.py:30-31` matches the apply Given for `p1` only; `:69-70` the integrate Then for `p1` only.
- Code: `scripts/supervise_rounds.py:58-61` (`due`) and `scripts/supervise_glossary.py:25-30` (`route`) never send a glossary-proposal back to integrate; `supervise_rounds.py:177-180` commits a glossary apply's `nothing_applied` and returns with the status kept, so `due` picks the apply again (inferred from reading, not run).

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_glossary.py:route, ROUTES (:12, :25-30) | awaiting-answer answered goes to apply; `approved` has no route | must check whether the last apply sent it back (r221), as `supervise_rounds.py:68` does for capabilities | none by search, not mapped: features 1839, 1847, 1855, 1864 (glossary apply) | read; refs |
| scripts/supervise_rounds.py:due, glossary loop (:58-61) | calls `supervise_glossary.route` for each glossary-proposal, no `sent_back` | a glossary sent back gets an integrate round first | none by search, not mapped: as above | read; search |
| scripts/supervise_rounds.py:run_round apply, gives_nothing (:177-180) | commits and returns, status kept (awaiting-answer) | with ROUTES, `due` re-issues apply: a loop; r221 needs integrate | none: no scenario has a glossary apply give `nothing_applied` | read; search of features |
| scripts/supervise_rounds.py:run_round apply, move (:174, :203) | glossary apply with `unheld_answers` moves to `approved`; unheld answers ignored | r221 covers unheld answers too: move to approved, then integrate via a sent-back check | none by search | read |
| scripts/supervise_outputs.py:sent_back (:47-56) | one name-free test of apply and formulate results; called only from `supervise_rounds.py:86` | reusable for a glossary-proposal's runs directory as is | none by search, not mapped | read; refs (1 ref in production) |
| scripts/supervise_change.py:write_proposals, glossary part (:129-139) | writes fixed `glossary.md` with the change list's terms; never the named proposal | an integrate round for g1 must redraft g1 (r189, scenario `features/supervision.feature:1183` expects g1 to keep its terms); here it leaves g1 stale and adds a second glossary-proposal | by search: features 1183 (r189), 1574 (r171) | read |
| scripts/supervise_brief.py:83-86 (apply brief) | gives UNHELD_ANSWERS to every apply, glossary included | the glossary apply's `unheld_answers` must be read | by search: none for glossary | read |
| scripts/supervise_glossary.py:withheld (:33-42) | withholds terms of non-approved glossary-proposals | unchanged; g1 awaiting-answer keeps its terms withheld | by search: features 1847-1855 | read |

## 3. Tests the requirements make impossible to keep

None found. Checked by search, not by map:
- `features/supervision.feature` lines with "applies nothing" (1068-1567) all use `p1` (capability); no glossary apply gives `nothing_applied` or `unheld_answers` in a scenario.
- The glossary apply scenarios (1839, 1847, 1855, 1864) give DONE with changes or answers and reach approved or the apply round; the route change leaves them as they are (read of their text).
- Scenario 1183 (r189) passes today because write_proposals never touches g1.md; a fix that rewrites g1 in place must keep its Then true (g1's adds, changes, removes).

## 4. The file set

Edited (must change):
- `scripts/supervise_glossary.py` (91 lines; room 209): `route` checks `sent_back` for an awaiting-answer or approved glossary-proposal and returns integrate, drafted; `approved` gets a route. Read of `supervise_glossary.py` and refs.
- `scripts/supervise_rounds.py` (275; room 25): `due` and the apply branch (:174-203) send a glossary back to integrate and stop the apply loop (:177-180). Read.
- `scripts/supervise_change.py` (140; room 160): `write_proposals` glossary part, see the two readings below. Read.
- `tests/scenarios/supervision_proposal_steps.py` (213; room 87): line 142-143 answers pattern accepts a comma inside quotes. Read of the regex against features 2074.
- `tests/scenarios/supervision_reintegrate_steps.py` (175; room 125): apply Given (:30-31) and integrate Then (:69-70) take `[pg]1`. Read.

Read, on the change's path, not edited (line count, room under 300):
- `scripts/supervise_outputs.py` (103; 197): `sent_back`, reused; not changed.
- `scripts/supervise.py` (295; room 5): `Run` mixes in Rounds and Changes; no addition fits.
- `scripts/workqueue.py` (294; room 6): `move` accepts drafted, approved for proposals (:155); not changed.
- `scripts/supervise_brief.py` (216; 84): UNHELD_ANSWERS reaches glossary applies; not changed.
- `scripts/supervise_worker.py` (259; 41): round outputs; not changed.
- `tests/scenarios/supervision_integrate_steps.py` (252; 48): glossary integrate steps; not changed.
- `tools size --limit 300`: no tracked Python file over 300 (run).

Two readings of an integrate round started for a glossary-proposal g1 (the conflict, not decided here):
- Reading A: the round rewrites g1.md in place, keeping the terms its change list does not name (r189, scenario 1183). Changes `write_proposals` to write `own` (the named proposal) and merge lists as `rewrite_lists` does for capabilities.
- Reading B: the round writes glossary.md beside g1.md, as today; then g1 and glossary.md are both drafted and both gated, and g1's lists stay stale.
