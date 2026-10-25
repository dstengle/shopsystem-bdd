# Plan of w152: work run moves a proposal to awaiting-answer when its gate round ends

## 1. What goes green

- **supervision#r69**: scenario "when the gate round `work run` started for a capability-proposal ends, the proposal is awaiting-answer" (`features/supervision.feature:857`).
  Red today (notes part 1): it stops at its second Given, `the gate round gives the question "Is a title given twice one book or two?" on p1, and every round ends`, with StepDefinitionNotFoundError. No module binds that wording. The nearest binding, `gate_result` in `tests/scenarios/supervision_rounds_steps.py`, binds "the gate round's result gives the question …", which is a different wording, and its `gate_question` needs four quoted strings (question, two readings, the mark). The code behind the Then already works. The research probe ran `supervise_rounds.round` with the scenario's own question. `move` then took p1 to awaiting-answer and wrote the question under `## Questions`, with one gate round started.
- The work-item has no Retires section, so it retires no deprecated scenario.

## 2. Where the change lands

- `tests/scenarios/supervision_rounds_steps.py` (123 lines): one new Given binding for the wording "the gate round gives the question "<q>" on p1, and every round ends". It sets the stand-in's `initiative-round` plan entry to a DONE result whose `questions` list holds that one quoted question as given, with no readings and no mark. It sits next to `gate_result` and `every_round_ends`. The file stays far under 300 lines.

Removed from the researcher's set, each for the reason in part 3:
- `features/supervision.feature`: it is spec-owned, and the accepted scenario is not reworded (decision P1).
- `scripts/model_work.py`, `scripts/supervise.py`, `scripts/supervise_rounds.py`: the defects D1 to D4 are outside `accepts: [supervision#r69]`, and r69 does not need them (decisions P2 to P5).

No production file changes. The research probe shows the r69 code path already working.

## 3. Decisions

- **P1. The step is bound, not reworded.** The new binding matches the accepted feature line exactly, and the feature file stays as it is. The scenario is the accepted wording of supervision#r69, and the planner may change only plan.md and the result. The new wording ("the gate round gives …") and r85's wording ("the gate round's result gives …") match different text, so the two bindings cannot both match one step. Rests on supervision#r69 as accepted.
- **P2. The bare question goes into the plan unchanged.** The question is not passed through `gate_question`, because the scenario gives no readings. Rests on supervision#r69, whose scenario only asserts p1's status. The question text matters to r85's scenario, which keeps its own binding.
- **P3. D1 is not taken here.** D1: a gate that gives zero questions runs apply and formulate with no answer. This is r70 read vacuously, plus a round's non-DONE outcome. Both are already raised by the open question of the sibling w146 (awaiting-answer). r69's scenario gives one question. Rests on supervision#r70 and w146's open question, not on r69.
- **P4. D2 and D4 are not taken here.** D2: `work run i1` with only a proposal awaiting-answer exits 0 and prints nothing. D4: a PARTIAL gate result is taken as the gate. Both change what the narrator sees (the exit, the printed status, a fault). Neither belongs to supervision#r69. D2 is settled, if at all, by supervision#r32 and r81/r82, and D4 by r5/r45 and w146's question. The plan names them in part 5 for whoever owns those lines and does not choose a reading.
- **P5. D3 is not taken here.** D3: `model check` reports a proposal's `awaiting-answer` status as invalid, from STATUSES in `scripts/model_work.py`. The finding belongs to the design model's command, not to supervision, and r69's scenario does not run `model check`. It is left as a finding (part 5).

## 4. Tests the decisions break

None. Checked against notes part 4: a search of `tests/` for `awaiting-answer` and `capability-proposal` found no test asserting that a proposal is never awaiting-answer, or that the gate round leaves a proposal drafted. The only file that changes is the step module, and it gains one binding. That binding's wording differs from `gate_result` ("the gate round's result gives") and from `every_round_ends` (an exact string), so no existing step is shadowed or rebound. The r85 scenario (feature line 1014) keeps `gate_result` unchanged.

## 5. Open cases

- What r69's scenario does not test, and the implementer should name in their report without fixing:
  - a gate result with zero questions (D1; see w146);
  - a PARTIAL gate result with questions (D4);
  - a gate question given as an object, written as JSON text (notes part 3);
  - a failure between `workqueue.move` and the `## Questions` write in `supervise.move`, which leaves awaiting-answer with no questions (notes part 5).
- `work run i1`'s exit and printout when the only node waiting is a proposal (D2). The scenario asserts neither.
- `model check` rejecting `awaiting-answer` for a capability-proposal (D3, `scripts/model_work.py` STATUSES). Raise it as a finding for the design model's capability.
