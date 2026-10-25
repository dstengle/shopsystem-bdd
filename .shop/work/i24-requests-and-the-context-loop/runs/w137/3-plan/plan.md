# Plan of w137: apply, then formulate, for an answered capability-proposal

Planned from `runs/w137/2-research/notes.md` (1-research agrees), supervision's Behaviour, decisions 0037, 0038, 0068, and the agent `agents/initiative-round.md`. Three questions are open (end of this plan). The rest of the plan stands under any answer to them.

## 1. What goes green

Each scenario is in `features/supervision.feature` and bound in `tests/scenarios/test_supervision.py`. All four are red at their first Given today with StepDefinitionNotFoundError, because no step writes a capability-proposal with Questions and Answers. Behind the steps, the code is missing too: `Run.items` reads work-items only, so `work run i1` leaves an answered awaiting-answer p1 alone (probe P1: exit 0, nothing started). `workqueue.move` refuses `approved` and `formulated` (P11). No brief or session exists for an `initiative-round` round.

- supervision#r70: "a capability-proposal whose every question has an answer is given to an apply round with its answers".
- supervision#r80: "when the apply round `work run` started for a capability-proposal ends, the proposal is approved".
- supervision#r71: "when the apply round `work run` started for a capability-proposal ends, a formulate round is started for the proposal".
- supervision#r83: "when the formulate round `work run` started for a capability-proposal ends, the proposal is formulated".

This work-item retires no scenarios (it has no `## Retires`).

## 2. Where the change lands

- `scripts/supervise_rounds.py` (new): the rounds of a capability-proposal for `work run`. It reads the initiative's capability-proposals with their status, questions and answers, and decides which round is due. For an awaiting-answer proposal whose every question has an answer, that is apply. Then it moves the proposal to approved and starts formulate, then moves it to formulated. This logic gets its own module because `supervise.py` has 82 lines of room and `workqueue.py` has about 21, and sibling work-items w136 and w146 (gate) build on the same path.
- `scripts/supervise.py`: `Run.run` gives the initiative's proposals their due rounds, one session at a time, inside the same loop that pulls the work-items. `Run.move` and `commit` are used for the proposal's transitions as they are.
- `scripts/workqueue.py`: `move` accepts a capability-proposal's own statuses (`approved` and `formulated` among them). For a work-item it accepts only the work-item lifecycle, as today. `items` is unchanged.
- `scripts/supervise_brief.py`: the brief of an apply round and of a formulate round. It names the proposal's file, the kind, the stage directory and `Result file:`, and keeps the lines every brief carries (r17, r25, r44). The apply brief gives each answer beside its question, reusing `answer_lines`.
- `scripts/supervise_worker.py`: the `initiative-round` agent and the round stages (`apply`, `formulate`) in `TOOLS`, `MAX_TURNS` and `session`, so a round runs through `Workers.worker`.
- `tests/scenarios/supervision_proposal_steps.py` (new): the Given that writes p1 with Questions and Answers; "every round ends" (and the variant with "every worker gives DONE"); and the Thens: a round of the kind apply was started for p1 given the answers; the transition to approved was made once the apply round had ended; formulate was started after apply ended; the transition to formulated was made once formulate had ended. The Thens read the order of lines in `log.jsonl` and the round's brief.
- `tests/scenarios/supervision_world.py`: a proposal file writer next to `item_text`, and the stand-in's reply for an `initiative-round` session.
- `tests/scenarios/test_supervision.py`: imports the new step module and nothing else.
- `tests/scripts/stub_claude.py`: answers an `initiative-round` session with a result file. This change is needed only if its existing reply path does not already cover that agent.
- `CLAUDE.md`: the `scripts/supervise*.py` row also names `supervise_rounds.py` (the capability-proposal's rounds). The rule there is that a new concern gets a module and a row.

The researcher's set also listed the following. They are kept out, as on the path but unchanged by these four requirements:
- `scripts/model_work.py`: D1, `awaiting-answer` for a proposal. That status is r69's (w136).
- `scripts/workqueue_answer.py`: D3, an answer on a proposal returns it to `drafted`. That belongs to work-queue r24 (w140).
- `scripts/supervise_pool.py`: rounds sharing the pool is r66 (w134).
- `scripts/work`, `scripts/supervise_faults.py`, `scripts/supervise_merge.py`, `scripts/supervise_review.py`, `scripts/workqueue_status.py`, `tests/scenarios/supervision_given.py`: read only.

## 3. Decisions

1. **r70 is read only on an `awaiting-answer` proposal.** A `drafted` proposal goes to gate (r68). An `approved` one goes to formulate (r71). Read on any other status, r70 would start apply again after r80, and the run would never end. Rests on supervision#r70, #r80, #r71, #r68.
2. **When a question "has an answer".** The n-th bullet of `## Answers` answers the n-th of `## Questions` (supervision's Implementation). A proposal with fewer answers than questions gets no round: probes P2 and P3 behave the same after the change. Rests on supervision#r70.
3. **A round runs as a worker.** Each apply and formulate round is a fresh `claude -p` session of `initiative-round` started through `Workers.worker`. So the steps the notes (part 5) say a separate path would skip all hold for a round as well:
   - the push verification (r35);
   - the start and end lines in `log.jsonl` (r8);
   - the checkout check (r28);
   - `session.json` (r62);
   - the r45 checks on how the session ended;
   - `keep_named` (r15).

   Its stage directory is `runs/p1/<k>-apply/` or `runs/p1/<k>-formulate/`, and its brief carries a `Result file:` line. Rests on design-decision/worker-results-are-files, design-decision/a-script-supervises-delivery, supervision#r8 and #r35, and supervision's Implementation (rounds are `initiative-round` sessions).
4. **What counts as "ends" in r80, r71 and r83.** The round's session ends with a result file `work run` can read, whatever outcome it gives. The trigger in those three lines is "ends", where r3 says "gives the outcome DONE". A session with no readable result, or one that r45 counts as cut short, is a failed stage (0038). It makes no transition and starts no next round. What then becomes of the proposal is question 3. Rests on supervision#r80, #r71, #r83, design-decision/worker-results-are-files.
5. **Apply and formulate run in one `work run`.** p1 goes awaiting-answer, then apply, then approved, then formulate, then formulated. The order in `log.jsonl` is: apply end, then the move to approved, then formulate start, then formulate end, then the move to formulated. Rests on supervision#r80, #r71, #r83 and #r1's "until no transition can be made".
6. **Each proposal transition is committed and pushed, through `Run.move` and `Run.commit`.** The commit holds p1's file, its stage directories and `log.jsonl`, with the message `work: p1 <before> -> <after>`. Without the commit, the next worker's checkout check (r28) would find p1's file changed. Rests on supervision#r7 (by its form), #r38, #r28.
7. **`workqueue.move` checks the target status against the lifecycle of the node's kind.** A capability-proposal takes its design-model statuses: drafted, awaiting-answer, approved, formulated, merged, withdrawn. The work-item lifecycle and its refusals stay as they are. `workqueue.items` keeps yielding work-items only, so `work show` still prints nothing about p1. Rests on supervision#r80, #r83.
8. **Round tools.** A round gets the tools of `initiative-round`'s definition with no bare Write or Edit (r13). Its Write and Edit are scoped to the paths its job writes, and Bash follows r14. Its turn limit is the implementer's to give and to name in the report. Rests on supervision#r13, #r14, #r30.

## 4. Tests the decisions break

None. I checked the notes' part 4 (by search; there is no map) against each decision:
- `tests/scripts/test_work_items.py` `test_a_move_to_a_status_outside_the_lifecycle_is_refused`: `finished` is still refused under decision 7.
- `tests/scenarios/test_work_queue.py`, the `move` step and the `nothing_about` check behind "it prints nothing about p1": these stay true because `items` is unchanged (decision 7).
- `tests/scenarios/test_supervision.py` `one_commit_per_move`: it counts w1's moves only, so p1's commits do not change its count.
- The model tests on proposal statuses are untouched, because `model_work.py` is outside the set.
- Every other proposal scenario of supervision has undefined steps today.

## 5. Open cases

These are left for the implementer to name in the report, not to choose. Each one marked with a question below waits on that answer.
- `work run`'s output and exit when the initiative holds only a proposal, now formulated, and no work-item. r9 speaks of work-items only.
- An apply or formulate result that gives questions or an outcome other than DONE. Under decision 4 it still makes the transition. Where its questions go is not said by any of the four lines.
- A proposal that is awaiting-answer with no `## Questions` (probe P4): question 2.
- A round's session that faults: question 3.
- What becomes of the commits an apply or formulate round makes in its worktree (the agent commits `spec/` and `features/`): question 1.
- Drafts of earlier rounds live in the git-ignored `.shop/scratch/drafts/`, so a round's worktree does not have them. That is the business of the round's brief and agent (spec-integration, formulation; w143 to w145), not of these four lines.
- D3: after `work answer` on a proposal, the proposal is `drafted`, so a gate would start again instead of apply. That belongs to work-queue r24 (w140). These scenarios start from awaiting-answer with answers written.

## Questions

1. **Where a round's commits go.** The apply round commits `spec/` and the formulate round commits `features/` (agents/initiative-round.md), in the worktree `work run` gives it. No line says what becomes of those commits.
   - Reading A: `work run` merges the round's branch into the initiative branch when the round ends, before the proposal's transition. The person sees the changed `spec/` and `features/` on the initiative branch, with p1 approved, then formulated.
   - Reading B: the round's branch is kept, unmerged, as r26 keeps a work-item branch. The person sees p1 approved and formulated, `spec/` and `features/` unchanged on the initiative branch, and the round's commits on a kept branch.
2. **An awaiting-answer proposal with no question at all.** This can happen when a gate's result gives none (r85, r69).
   - Reading A: "every question has an answer" holds, so apply starts given no answers. The person sees p1 approved, then formulated, in the same run.
   - Reading B: no round starts. The person sees p1 stay awaiting-answer, and `work run` exits as it does on an awaiting-answer node.
3. **A round whose session ends in an error, at its turn limit, or without a readable result.**
   - Reading A: the proposal is moved to `failed`, its fault written under its `## Faults`, as r45 does for a work-item. The person sees p1 failed and `work run` exits with an error naming p1 and its fault.
   - Reading B: the proposal keeps its status, and `work run` exits with an error naming p1's round and its fault. The person sees p1 still awaiting-answer (or approved), and the round is started again by the next `work run`.
