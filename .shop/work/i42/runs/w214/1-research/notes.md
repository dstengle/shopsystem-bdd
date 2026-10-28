# research of w214 (supervision r149, r150, r151, r152, r153)

Tools: plugin scripts present. No coverage map: `tools tests-of` and `untested` answer "no map", so every test list below is `by search`. `tools refs` used for names.

## 1. Why each scenario is red today

Command (run once): `python3 -m pytest -q --work-item w214 -p no:cacheprovider`
Result (run): 4 failed, 177 passed, 1 skipped, 56 subtests passed.

- r150 "an apply round that gives an answer ... is followed by a new integrate round" (features 1070): PASSED (run). Its fixture is `nothing_applied`; code path `applied_nothing` works for it.
- r149 "a formulate round that formulates nothing ... is followed by a new integrate round" (features 1503): run: `StepDefinitionNotFoundError` on Given "the formulate round for p1 formulates nothing, giving that p1's answers change lines not in spec/" (features 1508). Read: no step in tests/scenarios/supervision_formulate_steps.py takes it. The Then "a round of the kind integrate was started for p1 after the formulate round had ended" is undefined (grep: only the "after the apply round" form exists, supervision_reintegrate_steps.py:69). Code: `Rounds.route` (scripts/supervise_rounds.py:62-73) sends an answered formulate question back to `formulate` (log move from approved), never to integrate.
- r152 "... leaves the proposal's status as it was" (features 1513): run: undefined Given (features 1518). Read: Thens at features 1521-1522 undefined (grep). Code: `Rounds.run_round` formulate branch (supervise_rounds.py:179-195) moves the proposal to `formulated` (`after` from AFTER, line 193/195) when no question is given.
- r153 "... has given its output" (features 1524): run: undefined Given (features 1529, with ", and no scenario"). Read: Then at features 1532 undefined (grep finds only the apply form, supervision_reintegrate_steps.py:127). Code: the formulate branch (supervise_rounds.py:179-185) asks `supervise_outputs.unformulated` scenarios as a question. The fixture's default `adds` is `thing#r1` with no features/thing.feature (supervision_rounds_steps.py:30-33), so this question is written today.
- r151 "... followed by no formulate round ... before the new integrate round's drafts are applied" (features 1080): run: the Givens and `work run` ran; failed at Then "no round of the kind formulate was started for p1" (features 1090), undefined. Read: no code change expected for the flow (apply nothing -> integrate -> drafted -> gate -> awaiting-answer); the gap is the step. Only the step is missing (read, not run to the end).

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_rounds.py:Rounds.route (62-73) | awaiting-answer proposal whose last move came from approved goes to `formulate` | r149/r152: an answered formulate question whose round formulated nothing must go to `integrate`, status kept | by search: r116 scenario (features 1051), r140/r150 (supervision_reintegrate_steps) | refs (route called from due, supervise_rounds.py:59) and read |
| scripts/supervise_rounds.py:Rounds.due (44-60) | calls route for each awaiting-answer proposal with all answers | unchanged logic; new route result feeds it | by search: every supervision scenario that answers a proposal | read |
| scripts/supervise_rounds.py:Rounds.applied_nothing (75-86) | latest stage is `-apply` and its result gives nothing_applied | r149 needs the formulate counterpart; r150 (new wording: "gives an answer the drafts do not hold") is wider than "applies nothing" | by search: r140, r147, r150, r151 (supervision_reintegrate_steps.py) | refs: 1 reference (supervise_rounds.py:67) |
| scripts/supervise_rounds.py:gives_nothing (25-29) | reads `nothing_applied` with no question and no changes | apply-only; does not read `unheld_answers` that agents/initiative-round.md:36 asks beside `changes` | by search: r147/r150 scenarios | refs: 2 references (lines 84, 173) |
| scripts/supervise_rounds.py:Rounds.run_round formulate branch (179-185) and move (193-195) | no question: asks missing scenarios, else moves to `formulated` | r153: no question for a nothing-formulated result; r152: no move | by search: r83 (features 1495), r131/r132 (supervision_outputs_steps.py, supervision_rounds_steps.py:114-118) | read |
| scripts/supervise_rounds.py:Rounds.run_round apply branch (173-176) | nothing_applied: commit `before` to `before`, return | the model for the formulate case (r152) | by search: r147/r150 | read |
| scripts/supervise_outputs.py:unformulated (52-68), question (71-73) | ids lacking a scenario; the question text | unchanged; must not run for a nothing-formulated result (r153) | by search: r131/r132 tests | read |
| scripts/supervise_brief.py:Briefs.brief (35-80) | the formulate round's brief: generic lines, no formulate-only line (grep `formulate` in the file: none) | the round must be told the new field (agent contract) | none | grep, read 35-80 |
| agents/initiative-round.md, `formulate` (lines 39-40) | reply and coverage; no field for lines outside spec/ | the round must give that field when its answers change lines not in spec/ | none (agent prompt; tests stub the worker) | read |

Note: the field name for "formulates nothing because answers change lines not in spec/" is in no spec, agent or brief. Reading A: mirror `nothing_applied` (a sentence, no changes, no questions). Reading B: a list of the lines the answers change, read by `work run`. Both stand; the plan must pick one.

## 3. Tests the requirements make impossible to keep

Searched by search (no map). No existing test is broken by these requirements as they stand:
- r116 and r83 scenarios (formulate round with a question, or with none and scenarios present): still valid; the new field is absent there.
- r131/r132 (formulate output missing is asked): still valid when the field is absent; they break only if the field is given, which no current test does.
- r147, r150 (apply applies nothing -> integrate; supervision_reintegrate_steps.py): still valid.
- spec_integration_apply_steps.py:35, 72-78 (`unheld_answers` in brief and kept result): asserts only the brief and the kept result; still valid under r150.
- features/supervision.feature:1059-1069, the `@r140 @deprecated` scenario: asserts what r150 asserts (passes today). It is retired by this work-item's Retires; removing it is the change, not a broken test.
No test asserts that an apply round with unheld answers beside changes stays out of integrate: none found.

## 4. The file set

Production:
- scripts/supervise_rounds.py (267 lines, room 33): route sends a nothing-formulated answered proposal to integrate (r149); applied_nothing/gives_nothing read the formulate field and unheld answers (r150 wording, see question); formulate branch returns with no move and no question (r152, r153). Found: read, refs.
- scripts/supervise_brief.py (207 lines, room 93): formulate brief asks for the new field. Found: grep, read.
- agents/initiative-round.md (66 lines; not Python, no limit): formulate section gives the field's contract. Found: read.
Tests:
- tests/scenarios/supervision_formulate_steps.py (83 lines, room 217): Givens "the formulate round for p1 formulates nothing, giving that p1's answers change lines not in spec/" and the ", and no scenario" variant (setting `round:formulate` with the field). Found: read.
- tests/scenarios/supervision_reintegrate_steps.py (138 lines, room 162): Thens for r149 (integrate after formulate ended), r152 (awaiting-answer when formulate ended; no transition between formulate start and integrate start), r153 (no question naming formulate output missing), r151 (no formulate round started for p1). Found: run failures, read.
- features/supervision.feature: remove the `@r140 @deprecated` scenario, lines 1059-1069, as the Retires names it. Found: read.
Not changed, on the path (read or wc only):
- scripts/supervise.py (293 lines, room 7): `Run` mixes in `Rounds`; no edit planned.
- scripts/supervise_outputs.py (73, room 227): unchanged.
- scripts/supervise_change.py (126, room 174): write_proposals rewrites p1 on integrate; whether it clears Questions/Answers was not read.
- scripts/supervise_worker.py (256, room 44), scripts/supervise_faults.py (190, room 110): not read; on the worker path.
- tests/scenarios/test_supervision.py (267, room 33): the pytest-bdd binding; not read.
- tests/scenarios/supervision_rounds_steps.py (273, room 27): helpers `rounds`, `position`; no edit planned.
Size limit: `tools size --limit 300` printed nothing (no tracked Python file over 300 today; read).

Questions for the plan (both readings):
1. The field for "formulates nothing because answers change lines not in spec/": (A) a sentence field like `nothing_applied`; (B) a list of the lines changed. No spec or agent names it.
2. r150 wording ("gives an answer the drafts it applied do not hold") vs. code (`nothing_applied` only): (A) cover `unheld_answers` beside `changes` too (agent contract line 36); (B) keep the nothing-applied case only, as the accepted scenario tests.
