# Plan of w213: spec-integration#r46

## 1. What goes green

- **spec-integration#r46**: scenario "a round of the kind apply gives in its result each answer of the capability-proposal that the drafts it applied do not hold" (features/spec-integration.feature:27-36).
  Red today (notes part 1, run): `StepDefinitionNotFoundError` on its first Given; none of its seven steps has a definition in tests/scenarios/spec_integration_steps.py, which holds only the integrate-round steps of r44 and r45. Behind the steps, nothing tells an apply round to give its unheld answers: the apply brief (supervise_brief.py, the apply branch around line 74) names only the change list, and the apply contract in agents/initiative-round.md (lines 34-36) names only `changes` and the whole-round `nothing_applied`.
- The work-item has no Retires section; no deprecated scenario is retired.

## 2. Where the change lands

- `scripts/supervise_brief.py`: the apply brief gets one more instruction beside the change list: give in the result's new field each answer of the proposal (the answers the brief already lists beside their questions, through `answer_lines`) that the drafts applied do not hold, and say that the field is given also when some drafts are applied. Best kept as a module constant beside `CHANGE_LIST` and `ANSWER_LINES`, appended in the apply branch.
- `agents/initiative-round.md`: the `apply` paragraph names the field: after applying, compare each answer with the applied drafts and give each unheld answer in it, both on a partial apply (beside `changes`) and on a whole-round `nothing_applied`.
- `tests/scenarios/spec_integration_steps.py`: the seven steps of the scenario (three Givens, one When, three Thens), in the r44/r45 style: a stand-in apply round planned in the stub's plan, `work run i1` run as `run_integrate` runs it, the Thens reading the apply round's brief and the result `work run` kept in the apply stage directory. If the file nears 300 lines (it has 160), the new steps go to a new `tests/scenarios/spec_integration_apply_steps.py`, bound from tests/scenarios/test_spec_integration.py like the existing module; then that test file joins the set.
- `README.md`: the bullet at lines 170-173 ("Answers that ask for what the drafts do not hold are redrafted") also names spec-integration r46: an apply round gives in its result each answer its applied drafts do not hold.

Removed from the researcher's set, and why (decisions 2 and 3 below): `scripts/supervise_rounds.py`, `scripts/supervise_worker.py`, `scripts/supervise_change.py`, `scripts/supervise_outputs.py`. `work run` already keeps the round's whole result.json in the stage directory (supervise_worker.py line 201, notes), so the field reaches the kept result with no reader in code; `gives_nothing`, `applied_nothing`, `route` and the r131 question are left as they are.

## 3. Decisions

1. **The field is a new list `unheld_answers`, beside `changes`**, each entry an answer's text as the proposal's `## Answers` holds it; an empty list (or no field) when every answer is held. `nothing_applied` stays the whole-round sentence it is. Rests on spec-integration#r46 (each unheld answer, in the result) and supervision#r147 (`nothing_applied` is the whole-round output, read by `gives_nothing` as a string). The researcher's Q-a reading A; the field name is internal to the round's result and changes nothing the person at the gate sees beyond what r46 asks.
2. **`work run` gives the field no reader in this work**: a partial apply with unheld answers is approved and goes to formulate as today; a whole-round apply giving `nothing_applied` with `unheld_answers` beside it is still read by `gives_nothing` as nothing applied (the extra field does not count against it), so r140's route to integrate is unchanged. Rests on spec-integration#r46 (its subject is `initiative-round`, and it asks only that the result gives the answers) and supervision#r140/#r147 (they cover only the round that applies nothing). What `work run` should do with a partial list is not asked by any line; it is a supervision line for a later proposal (the researcher's Q-b, Q-c), not this work's choice, and leaving today's behaviour changes nothing the narrator observes.
3. **The apply round's output stays its change list** (or `nothing_applied`): a result giving only `unheld_answers`, with neither `changes`, `nothing_applied` nor questions, still gets the r131 question. Rests on supervision#r132 (an apply round's output is its change list) and #r147.
4. **The scenario's Thens read two things**, as the r44/r45 Thens do: the apply round's brief names the answer of shipping and asks for the unheld answers in `unheld_answers` (what `work run` told the round), and the result `work run` kept in the apply stage directory gives the shipping answer in `unheld_answers` and not the order-status answer. "The round applies those drafts" is read from the proposal's lists rewritten from the stand-in's `changes` (r114) and the proposal's status after the run (approved or formulated), not from `spec/`, since the round is a stand-in. Rests on spec-integration#r46 and the stand-in practice of tests/scenarios/spec_integration_steps.py's docstring.

## 4. Tests the decisions break

None. Verified by search of tests/ and scripts/ (no coverage map): no test asserts the apply brief's text ("change list of what you applied" occurs only in supervise_brief.py); the only planned `nothing_applied` (supervision_reintegrate_steps.py:33, r140/r147 scenarios) is read by `gives_nothing`, which decision 2 leaves unchanged; the apply plans giving only `changes` (supervision_rounds_steps.py:28 and :111, supervision_session_faults_steps.py:110, supervision_formulate_steps.py:24 and :38) are unaffected since `work run` neither requires nor reads the new field (decision 3).

## 5. Open cases

- The Givens' setting: an initiative i1 with a capability-proposal awaiting-answer whose `## Questions`/`## Answers` hold the two answers, its kept drafts path written as the body sentence "The drafts of this proposal are in ..." (r108) with one draft holding the order-status line and none the shipping line; the implementer names how much of supervision_rounds_steps.py's proposal setup to reuse.
- Whether the brief instruction is given only when the proposal has answers, or on every apply brief.
- How the round compares an answer with the drafts (wording, a paraphrased line): the contract's wording, for the implementer to name; the stand-in does not exercise it.
- A partial apply whose unheld answers `work run` might send back to integrate or ask as questions: no line says; left to a later supervision proposal (decision 2).
- `--work-item w213` selects every feature's `@r46` (176 other scenarios ran, notes part 1): outside this work; the implementer runs the scenario by its feature too.
