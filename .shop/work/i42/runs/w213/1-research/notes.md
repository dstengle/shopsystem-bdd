# w213 research: spec-integration#r46

How made: no coverage map (`tools tests-of` answers "no map: make one with tools map"), so every test list below is `by search`. `tools refs` on the module `supervise_rounds` gave 0 references; function uses are `read`.

## 1. Why each scenario is red today

Scenario: "a round of the kind apply gives in its result each answer of the capability-proposal that the drafts it applied do not hold" (features/spec-integration.feature:28, @r46).

Command (run): `python3 -m pytest -q --work-item w213`
Result (run): 1 failed, 176 passed, 1 skipped. The failure is `StepDefinitionNotFoundError` on the first Given, `a capability-proposal whose answers are that the customer sees the status of an order and that the customer is told when an order ships` (feature line 30). The run also selected other capabilities' @r46 scenarios (176 passed): `--work-item` matches the tag `r46` in every feature, not only spec-integration's (run).

Steps with no definition (read, by search of tests/): the Given at line 31 "drafts that hold a line that the customer sees the status of an order"; line 32 "no line of those drafts holds that the customer is told when an order ships"; line 33 "work run starts a round of the kind apply on that capability-proposal with those drafts"; line 34 "the round applies those drafts"; line 35 "the round's result gives the answer that the customer is told when an order ships"; line 36 "the round's result does not give the answer that the customer sees the status of an order".

Missing in step definitions: tests/scenarios/spec_integration_steps.py (160 lines) defines only integrate-round steps; tests/scenarios/test_spec_integration.py binds the feature. No apply-round Given/When exists for spec-integration.

Missing in code: the apply branch of `Rounds.run_round` (scripts/supervise_rounds.py:159-192) reads only `changes`, `questions` and `nothing_applied`; nothing writes or reads a per-answer list in an apply result. The apply contract (agents/initiative-round.md:34-36) names only `changes` and the whole-round `nothing_applied`.

## 2. Old assumptions

Old form: an apply round's result gives its output as `changes` (applied drafts), or as one `nothing_applied` sentence when it applies nothing at all. r46 adds that the result gives each unheld answer, also when the round applies some drafts. Search: `nothing_applied|gives_nothing|applied_nothing|round of the kind apply`, read of the functions named.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_rounds.py:gives_nothing (25-29) | true only for a string `nothing_applied`, no questions, no changes | a result with the unheld-answer list and applied drafts is not "nothing": it is not read as nothing, and the list has no reader | by search: supervision_reintegrate_steps.py:33 (r140/r147 scenarios) | read, search |
| scripts/supervise_rounds.py:Rounds.applied_nothing (75-86) | judges the latest apply round by gives_nothing | a partial unheld list is invisible here; r140 covers whole-round only | by search: supervision.feature r140 scenarios, supervision_reintegrate_steps.py | read |
| scripts/supervise_rounds.py:Rounds.route (66-68) | an awaiting-answer proposal whose last apply gave nothing goes to integrate | unclear whether a partial list sends it back (see questions in part 4) | by search: supervision_reintegrate_steps.py | read |
| scripts/supervise_rounds.py:Rounds.run_round apply branch (159-178) | applied from `changes`; no questions and nothing applied asks "which capabilities' lines did it apply?" (r131) | a result with only the new list and no `changes` would get that question; the list must count as output | none | read |
| scripts/supervise_rounds.py:run_round (173-176) | `gives_nothing` keeps the round and commits | whether a partial list also passes here: a reading question | by search: supervision.feature r147 | read |
| scripts/supervise_brief.py:74-75 (apply brief, CHANGE_LIST) | names only the `changes` output of an apply | the brief must name the new field | none | read |
| agents/initiative-round.md:34-36 (apply contract) | `changes`, or `nothing_applied` when the answers give nothing held | the contract must name the per-answer list, also for a partial apply | none (prompt file) | read |
| README.md:170-171 | says an apply that applies nothing is redrafted | stale once a partial unheld list is read; to be kept true | none (doc) | read |
| spec/capabilities/supervision.md r140, r147 | whole-round apply only | no supervision line covers a partial unheld list (gap; a gate question) | by search: supervision.feature @r140, @r147 | read |

Unchanged inputs: supervise_brief.py `answer_lines` (146-156) already gives the apply round each answer beside its question (the r46 comparison's input). supervise_change.py `entries` (16-35) reads `changes` only.

## 3. Tests the requirement makes impossible to keep

None found that the requirement breaks. Searched by text (no map):
- tests/scenarios/supervision_reintegrate_steps.py:30-33 (apply plan with `nothing_applied`) keeps passing if `gives_nothing` and its field are unchanged. Sound (read).
- features/supervision.feature r140 (1059-1100) and r147 (1133-1148) Givens: each plans a whole-round `nothing_applied`; they keep passing if the field stays. Read of Givens only; the Thens were not read.
- Apply plans with `changes` only (tests/scenarios/supervision_rounds_steps.py:28, :111; supervision_session_faults_steps.py:110; supervision_formulate_steps.py:24, :38): unaffected unless the new field is required of every apply.
- features/supervision.feature:1385 "the integrate round for i1 gives DONE with no change list": an integrate round, not an apply; unaffected.

## 4. The file set

Production and prompt files the work-item must change:
- scripts/supervise_rounds.py: apply branch reads the per-answer list, keeps it as the round's output (r46), gives it no question; 267 lines, room 33.
- scripts/supervise_brief.py: the apply brief's CHANGE_LIST names the new field (lines 74-75); 203 lines, room 97.
- agents/initiative-round.md: apply contract names the field for a partial and a whole apply (lines 34-36); markdown, no line limit.
- tests/scenarios/spec_integration_steps.py: define the six steps in part 1; 160 lines, room 140.
- README.md: lines 170-171, if the behaviour is named there; doc.

Path modules, unchanged unless the field is read there:
- scripts/supervise_worker.py: 256 lines, room 44; keeps result.json (line 201), normalises `questions` (211-213).
- scripts/supervise_change.py: 126 lines, room 174; `entries` reads `changes` only.
- scripts/supervise_outputs.py: 73 lines, room 227; the r131 question wording.
- scripts/supervise_rounds.py and supervise_brief.py are the two to watch: room is 33 and 97.

Questions the gate must settle (both readings, no choice made):
- Q-a: name of the field. Reading A: a new list, e.g. `answers_not_held`, beside `changes`. Reading B: fold into `nothing_applied` as a list. Recommended: A, since r147 defines `nothing_applied` as a sentence for the whole-round case.
- Q-b: a partial apply with unheld answers. Reading 1: approve and formulate as now, the list kept in the result only. Reading 2: send the proposal back to integrate, as r140 does for a whole round, or ask the unheld answers as questions. The feature's Thens do not say which.
- Q-c: the supervision capability has no line for the partial case (r140/r147 cover whole rounds only): a supervision line may be needed through the gate.
- Q-d: `--work-item` selects by tag `r46` across all capabilities (176 others ran), not only spec-integration's; whether that is intended.
