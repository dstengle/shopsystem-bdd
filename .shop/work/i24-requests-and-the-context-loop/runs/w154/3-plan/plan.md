# Plan of w154: a round that ends other than DONE keeps its node's status, makes no transition and stops `work run`

From the researcher's notes (`runs/w154/1-research/notes.md`), the earlier plan (`runs/w154/2-plan/plan.md`, which asked one question), the work-item's `## Answers` (the ruling of 2026-10-25), the capability `supervision` and `features/supervision.feature` lines 1049-1074. This plan takes the earlier plan, settles its question by the ruling, and adds nothing else.

## 1. What goes green

- **supervision#r86**, scenario "when a round `work run` started for a capability-proposal ends at its turn limit, the proposal keeps its status". It is red today only because steps are missing. The Given "the gate round's session ends at its turn limit, its result giving the question … on p1" does not exist. The Then "p1 is drafted" does not exist either: the only status Then matches `awaiting-answer` (test_supervision.py:129), and the stand-in's round plan can only give DONE. The behaviour is already right. In probe a-turn, `work run` exited 1, p1 stayed drafted, and the message named the gate round and its turn limit.
- **supervision#r87**, scenario "when a round `work run` started for a capability-proposal gives an outcome other than DONE, no transition is made from it". It is red for three missing or mismatched steps:
  - the Given "the apply round gives BLOCKED, asking …" is missing;
  - the Then "a round of the kind apply was started for p1" does not match the existing step, which requires ", given the answers …";
  - the Then "log.jsonl gives no transition made after the apply round had ended" is missing.

  There is also a code gap (D2). A BLOCKED apply moves p1 to approved, and the formulate round then moves it on to formulated.
- **supervision#r88**, scenario "when a round `work run` started for a capability-proposal leaves no result it can read, `work run` exits with an error naming the round and how it ended". It is red for two missing steps: the Given "the apply round ends, and the formulate round's session ends with no error and before its turn limit, having written no result file", and the Then "`work run` names the formulate round of p1 and that it left no result it can read". The stand-in also cannot give apply and formulate different plans: both are `initiative-round` sessions, and the stand-in keys its plan by agent. The code is already right here. In probe c-formulate, `work run` exited 1, p1 stayed approved, and the message said "the formulate round of p1 … faulted … its round wrote no result file".
- Retires: none. The work-item has no `## Retires` section.

## 2. Where the change lands

- `scripts/supervise_rounds.py`: in `Rounds.round`, read the result's `status`. Any status but DONE keeps the node's status and calls no `move`. That means no transition, and, for a gate round, nothing written under `## Questions` (ruling, D-f). The round then goes through the existing fault path `keep_round`: it commits the stage directory and the log lines, pushes, and keeps the round branch. Last, it raises a Refused that names the round, its stage directory and the outcome it gave. The raise is what stops `Rounds.rounds` from starting the same due round again, forever.
- `tests/scripts/stub_claude.py`: the stand-in's plan can also be keyed by round kind, read from the brief's `# <kind> of <name>` heading. A plan keyed by kind takes precedence over one keyed by agent, and plans keyed by agent keep working. The file has 258 lines, which leaves 42 lines of room.
- `tests/scenarios/supervision_rounds_steps.py`:
  - three Givens: a gate round at its turn limit with a question; an apply round giving BLOCKED with a question; an apply round that ends, then a formulate round with no result file;
  - the Then "a round of the kind apply was started for p1" without the answers clause, either as a step of its own or by making the answers clause optional in the existing regex;
  - the Then "log.jsonl gives no transition made after the apply round had ended";
  - the Then naming the formulate round of p1 and its missing result.
- `tests/scenarios/test_supervision.py`: the Then "p1 is drafted". The implementer either makes the existing `is awaiting-answer` Then take any status or adds a sibling step. The file has 250 lines, so if the step does not fit within the limit it goes in `supervision_rounds_steps.py` instead.

The file set is the researcher's set, unchanged. The notes checked `supervise.py`, `supervise_worker.py`, `supervise_faults.py`, `work`, `workqueue.py` and the feature file and found that none of them needs a change.

## 3. Decisions

- **D-a. A non-DONE round goes through the fault path's commit and push (`keep_round`), never through `move`.** This rests on supervision#r87: there is no transition, and `move` commits a transition. It also rests on supervision#r46 and supervision#r38: the stage directory and the log lines must not be left uncommitted, or the next `work run` refuses, and each commit is pushed. The round branch is kept, as it is for a faulted round.
- **D-b. A non-DONE round raises and ends the run with an error that names the round, its stage directory and its outcome (for example, that it gave the outcome BLOCKED).** This rests on supervision#r88. The raise also stops `Rounds.rounds` from starting the round again. It also means a BLOCKED apply never reaches the formulate round, which supervision#r87 requires ("no transition … of any other node").
- **D-c. An integrate round that gives a non-DONE outcome, or faults, leaves the initiative `started`.** `started` is written when the round begins (supervision#r84). Putting the initiative back to `proposed` would itself be a transition from the round, which supervision#r87 forbids. So the status supervision#r86 keeps is the one the node holds when the round ends.
- **D-d. The r88 message stays as it is ("its round wrote no result file; its session ended as …"), and the step matches it.** The step checks that the message names the formulate round of p1 and gives the message's no-result wording. This rests on supervision#r88, which requires the round and how it ended, not particular words. The other faulted rounds already give the same message.
- **D-e. Keying the stand-in's plan by round kind is test-only.** It changes nothing that `work run` does. It rests on design-decision/worker-results-are-files: the stand-in gives each round its result file.
- **D-f. A gate round whose outcome is not DONE writes nothing on the proposal.** Its questions stay only in its committed `result.json`, and `work run` exits with an error that names the round and its outcome. This was taken by the ruling in w154's `## Answers` (2026-10-25, reading B): "ends" in supervision#r85 means ends with DONE, as supervision#r69's "ends" does under supervision#r87. So the gate branch of `Rounds.round` writes questions only on the DONE path, as it does today through `move`.
- **Out of scope: whether `work run <initiative>` exits with an error while a proposal is `awaiting-answer` (the researcher's D3).** That falls under supervision#r81 and supervision#r32, which this work-item does not accept, and no decision here rests on it. It is left as it is.

## 4. Tests the decisions break

None. I verified this from the notes. No test gives a round an outcome other than DONE: searching `tests/` for "BLOCKED" or "faulted" finds nothing. Every round plan in the tests gives DONE (`supervision_rounds_steps.py`, `supervision_delegation_steps.py`). The scenarios for r68-r71, r80, r83 and r85 still transition once a DONE round ends. D-f keeps r85's write on the DONE path, so the r85 scenario is unaffected.

Specific decisions leave these tests passing:
- `started_with_round`, the r84 scenario, still passes under D-c, because nothing rolls `started` back.
- The existing round plans keyed by agent still work under D-e, because a plan keyed by agent remains the fallback.
- `test_agents.py:43` is not affected.

## 5. Open cases

- `work run` started with no initiative runs initiatives side by side. When one initiative's round raises, does that stop the other initiatives' sessions, or only its own? The scenarios are silent. The existing fault path's behaviour applies, and the implementer names what it is.
- A gate agent that gives its gate with the outcome `QUESTION` rather than DONE. Under D-f and D-b this ends the run every time, as the ruling foresaw. The implementer names what the gate agent gives today.
- What the error message says for a readable non-DONE result: whether it lists the result's questions (for example "Is the old reader kept?") or names only the outcome.
- `Rounds.due` sends an `awaiting-answer` proposal that has no questions and no answers to apply, because 0 >= 0. That is not part of this work; the implementer names it if a scenario reaches it.
