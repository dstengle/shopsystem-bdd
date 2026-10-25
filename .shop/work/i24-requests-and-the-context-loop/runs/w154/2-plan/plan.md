# Plan of w154: a round that ends other than DONE keeps its node's status, makes no transition and stops `work run`

From the researcher's notes (`runs/w154/1-research/notes.md`), the capability `supervision` and `features/supervision.feature` lines 1049-1074.

## 1. What goes green

- **supervision#r86**: "when a round `work run` started for a capability-proposal ends at its turn limit, the proposal keeps its status". Red today because steps are missing: the Given "the gate round's session ends at its turn limit, its result giving the question … on p1" and the Then "p1 is drafted". The only status Then there is matches `awaiting-answer`, and the stub's round plan can only be DONE. The behaviour itself is already right: probe a-turn gave exit 1 with p1 still drafted, and the message names the round and its turn limit.
- **supervision#r87**: "when a round `work run` started for a capability-proposal gives an outcome other than DONE, no transition is made from it". Red today because the Given "the apply round gives BLOCKED, asking …" is missing, the Then "a round of the kind apply was started for p1" does not match the existing step (that step needs ", given the answers …"), and the Then "log.jsonl gives no transition made after the apply round had ended" is missing. There is also a code gap (D2): a BLOCKED apply moves p1 to approved, then the formulate round moves it to formulated.
- **supervision#r88**: "when a round `work run` started for a capability-proposal leaves no result it can read, `work run` exits with an error naming the round and how it ended". Red today because two steps are missing: the Given "the apply round ends, and the formulate round's session ends with no error and before its turn limit, having written no result file" and the Then "`work run` names the formulate round of p1 and that it left no result it can read". The stub cannot give apply and formulate different plans: both are `initiative-round` sessions, and the stub keys its plan by agent. The code already does the right thing: probe c-formulate gave exit 1 with p1 still approved, and the message says "the formulate round of p1 … faulted … its round wrote no result file".
- Retires: none. The work-item has no `## Retires` section.

## 2. Where the change lands

- `scripts/supervise_rounds.py`: in `Rounds.round`, read the result's `status`. Any status but DONE keeps the node's status and calls no `move` (so no transition and no `## Questions` write; see Q1). It goes through the existing fault path `keep_round`: commit the stage directory and log lines, push, keep the round branch. It then raises a Refused that names the round, its stage directory and the outcome it gave. Raising is what keeps `Rounds.rounds` from starting the same due round again, forever.
- `tests/scripts/stub_claude.py`: the stand-in's plan can also be keyed by round kind, read from the brief's `# <kind> of <name>` heading. A plan keyed by kind wins over one keyed by agent, and plans keyed by agent keep working.
- `tests/scenarios/supervision_rounds_steps.py`: the three Givens: a gate at its turn limit with a question, an apply giving BLOCKED with a question, and an apply that ends followed by a formulate with no result file. Also the Then "a round of the kind apply was started for p1" without the answers clause (a step of its own, or the existing regex with the answers clause made optional), the Then "log.jsonl gives no transition made after the apply round had ended", and the Then naming the formulate round and its missing result.
- `tests/scenarios/test_supervision.py`: the Then "p1 is drafted". The existing `is awaiting-answer` Then is made to take any status, or a sibling step is added, whichever the implementer finds fits. The file is at 250 lines, so if the step does not fit there it goes in `supervision_rounds_steps.py`.

No file is added or removed beyond the researcher's set. The notes checked `supervise.py`, `supervise_worker.py`, `supervise_faults.py`, `work`, `workqueue.py` and the feature file, and none of them needs a change.

## 3. Decisions

- **D-a. A non-DONE round goes through the fault path's commit and push (`keep_round`), not through `move`.** This rests on supervision#r87: no transition, and `move` commits a transition. It also rests on supervision#r46 and r38: the stage directory and log lines must not be left uncommitted, or the next `work run` refuses, and every commit is pushed. The round branch is kept, as for a faulted round.
- **D-b. A non-DONE round raises and ends the run with an error, naming the round, its stage directory and its outcome (for example "gave the outcome BLOCKED").** This rests on supervision#r88. It also stops `Rounds.rounds` from starting the round again, and it means a BLOCKED apply never reaches the formulate round, which supervision#r87 requires ("no transition … of any other node").
- **D-c. An integrate round that gives a non-DONE outcome or faults leaves the initiative `started` (researcher's question 2).** `started` was written when the round began (supervision#r84). Putting it back to `proposed` would itself be a transition from the round, which supervision#r87 forbids. The status that supervision#r86 keeps is therefore the one the node holds when the round ends.
- **D-d. The r88 message stays as it is ("its round wrote no result file; its session ended as …"), and the step matches the formulate round of p1 and the message's no-result wording (researcher's question 4).** This rests on supervision#r88, which asks for the round and how it ended, not for particular words. The message is shared with the other faulted rounds that already give it.
- **D-e. The stub's plan by round kind is test-only.** It changes nothing `work run` does. It rests on design-decision/worker-results-are-files: the stand-in gives each round its result file.
- **Out of scope (researcher's question 3, D3).** Whether `work run <initiative>` exits with an error while a proposal is `awaiting-answer` is a matter for supervision#r81 and r32. This work-item does not accept them, and no decision here rests on it. It is left as it is.
- **Not taken: whether a non-DONE gate round writes its questions (researcher's question 1).** This is a question to the person; see the result's `questions`. Section 2 is written for reading B (nothing written). Under reading A, the gate branch of `Rounds.round` still writes the result's questions under `## Questions`, without `move`, before `keep_round` commits.

## 4. Tests the decisions break

None. I checked this against the notes: no test gives a round an outcome other than DONE (a search of `tests/` for "BLOCKED" or "faulted" finds nothing), and every round plan in the tests is DONE (`supervision_rounds_steps.py`, `supervision_delegation_steps.py`). The scenarios for r68-r71, r80, r83 and r85 still transition after a DONE round ends.

Two tests are unaffected by specific decisions. `started_with_round`, the r84 scenario, still passes under D-c because nothing rolls `started` back. The existing round plans keyed by agent still work under D-e because a plan keyed by agent stays the fallback. `test_agents.py:43` is also unaffected.

## 5. Open cases

- With `work run` started with no initiative, where initiatives run side by side: does a round's raise also stop the sessions of the other initiatives, or only its own? The scenarios are silent. The existing fault path's behaviour applies, and the implementer names which it is.
- A gate round that gives `QUESTION` together with its questions. The spec-integration gate may give its gate under that outcome, not under DONE. Under D-b it ends the run. The implementer names what the gate agent gives today.
- What the r88 message says for a readable non-DONE result: whether it lists the result's questions (for example "Is the old reader kept?") or names only the outcome.
- `Rounds.due` sends an `awaiting-answer` proposal that has no questions and no answers to apply (0 >= 0). That is not part of this work; the implementer names it if a scenario reaches it.
