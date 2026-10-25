# Plan of w137: apply, then formulate, for an answered capability-proposal

Planned from `runs/w137/2-research/notes.md` (1-research agrees with it), from supervision's Behaviour and Implementation, and from the earlier plan `runs/w137/3-plan/plan.md`. This plan keeps the earlier plan and settles its three questions with the answers recorded in w137's `## Answers` (2026-10-25, the coordinator under the person's delegation): Q1 reading A, Q2 reading A, Q3 reading B.

## 1. What goes green

Each scenario is in `features/supervision.feature` and bound in `tests/scenarios/test_supervision.py`. All four fail today at their first Given with StepDefinitionNotFoundError, because no step writes a capability-proposal with Questions and Answers (notes, part 1). The code behind the steps is missing too:
- `Run.items` reads work-items only, so `work run i1` leaves an answered awaiting-answer p1 alone (probe P1: exit 0, nothing started).
- `workqueue.move` refuses `approved` and `formulated` (P11).
- No brief or session exists for an `initiative-round` round.

The four requirements and their scenarios:
- supervision#r70, "a capability-proposal whose every question has an answer is given to an apply round with its answers" (feature line 866).
- supervision#r80, "when the apply round `work run` started for a capability-proposal ends, the proposal is approved" (line 874).
- supervision#r71, "when the apply round `work run` started for a capability-proposal ends, a formulate round is started for the proposal" (line 882).
- supervision#r83, "when the formulate round `work run` started for a capability-proposal ends, the proposal is formulated" (line 996).

There are no scenarios to retire: w137 has no `## Retires`.

## 2. Where the change lands

- `scripts/supervise_rounds.py` (new): a capability-proposal's rounds for `work run`. It covers:
  - reading the initiative's proposals, with their status, questions and answers;
  - choosing the round that is due;
  - starting apply, merging its branch, moving to approved, then the same for formulate and formulated;
  - a faulted round, which ends the run with an error and leaves the proposal unchanged.

  It is a module of its own because `supervise.py` has 82 lines of room and `workqueue.py` about 21. The sibling work-items on the gate path build on the same module.
- `scripts/supervise.py`: `Run.run` gives each proposal its due rounds, one session at a time, inside the loop that pulls work-items. It turns a round's fault into the error exit. The proposal's transitions use `Run.move` and `Run.commit` as they are.
- `scripts/workqueue.py`: `move` checks the target status against the lifecycle of the node's kind. A capability-proposal gets its own statuses, among them `approved` and `formulated`. `items` does not change.
- `scripts/supervise_brief.py`: the brief of an apply round and of a formulate round. It names the proposal's file, the round's kind, the stage directory and `Result file:`, and keeps the lines every brief carries. The apply brief puts each answer beside its question, reusing `answer_lines`.
- `scripts/supervise_worker.py`:
  - the `initiative-round` agent, and the `apply` and `formulate` stages in `TOOLS`, `MAX_TURNS` and `session`;
  - a round's worktree on a round branch from the initiative branch's head (decision 9);
  - for a round, a fault is handed back to the caller. A work-item's fault still moves the work-item to `failed` (decision 10).
- `scripts/supervise_merge.py`: merges a round's branch into the initiative branch, then deletes the branch (decision 9). Added to the earlier plan's set by the Q1 answer. Its work-item merge, with its scenario and suite checks, stays as it is.
- `scripts/supervise_faults.py`: a round's fault (cut short, no result file, or a result that is not JSON) is reported without moving the proposal or writing under its `## Faults` (decision 10). Added by the Q3 answer. It changes only if the fault path cannot be kept from moving the node without it.
- `tests/scenarios/supervision_proposal_steps.py` (new):
  - the Given that writes p1 with its Questions and Answers;
  - "every round ends", and the variant "every round ends and every worker gives DONE";
  - the Thens, which read `log.jsonl`'s order and the apply round's brief: apply started for p1 with the answers; the move to approved after apply ended; formulate started after apply ended; the move to formulated after formulate ended.
- `tests/scenarios/supervision_world.py`: a writer of proposal files next to `item_text`, and the stand-in's reply for an `initiative-round` session.
- `tests/scenarios/test_supervision.py`: imports the new step module and nothing else.
- `tests/scripts/stub_claude.py`: answers an `initiative-round` session with a result file. It changes only if its reply path does not already cover that agent.
- `CLAUDE.md`: the `scripts/supervise*.py` row also names `supervise_rounds.py`, because a new concern gets a module and a row.

Kept out, as in the earlier plan:
- `scripts/model_work.py` (D1, the `awaiting-answer` status, r69/w136).
- `scripts/workqueue_answer.py` (D3, work-queue r24/w140).
- `scripts/supervise_pool.py` (r66/w134).
- Read only: `scripts/work`, `scripts/supervise_review.py`, `scripts/workqueue_status.py`, `tests/scenarios/supervision_given.py`.

## 3. Decisions

1. **r70 applies only to an `awaiting-answer` proposal.** A `drafted` proposal goes to its gate (r68), and an `approved` one goes to formulate (r71). If r70 were read on other statuses it would start apply again after r80, and the run would never end. Rests on supervision#r70, #r80, #r71 and #r68.
2. **When "every question has an answer".** The n-th bullet of `## Answers` answers the n-th bullet of `## Questions` (supervision's Implementation).
   - A proposal with fewer answers than questions gets no round. Probes P2 and P3 behave as they do today.
   - A proposal with no question at all has every question answered, so its apply round starts with no answers given (probe P4 changes: apply runs, then approved, formulate, formulated).

   Rests on supervision#r70 and the answer to Q2 (reading A).
3. **A round runs as a worker.** Each apply and formulate round is a fresh `claude -p` session of `initiative-round`, started through `Workers.worker`. So it gets everything the notes' part 5 lists:
   - the push check (r35);
   - the start and end lines (r8);
   - the checkout check (r28);
   - `session.json` (r62);
   - the r45 checks of how the session ended;
   - `keep_named` (r15).

   Its stage directory is `runs/p1/<k>-apply/` or `runs/p1/<k>-formulate/`, and its brief carries `Result file:`. Rests on design-decision/worker-results-are-files, design-decision/a-script-supervises-delivery, supervision#r8 and #r35, and the Implementation line on r70 and r71.
4. **What "ends" means in r80, r71 and r83.** A round ends when its session leaves a result file `work run` can read, whatever outcome the file gives. These lines say "ends", where r3 says "gives the outcome DONE". A session r45 counts as cut short, or one with no readable result, is a fault (decision 10): no merge, no transition, no next round. Rests on supervision#r80, #r71, #r83 and design-decision/worker-results-are-files.
5. **Apply and formulate run in one `work run`.** The order in `log.jsonl` is: apply start, apply end, the merge of apply's branch, the move to approved, formulate start, formulate end, the merge, the move to formulated. Rests on supervision#r80, #r71, #r83 and r1's "until no transition can be made".
6. **Each proposal transition is committed and pushed through `Run.move` and `Run.commit`.** The commit holds p1's file, its stage directories and `log.jsonl`, with the message `work: p1 <before> -> <after>`. Rests on supervision#r38 and #r28, and the Implementation's commit message.
7. **`workqueue.move` checks the status against the node's kind.** A capability-proposal takes drafted, awaiting-answer, approved, formulated, merged and withdrawn. The work-item lifecycle and its refusals do not change. `items` still yields work-items only, so `work show` still prints nothing about p1. Rests on supervision#r80 and #r83.
8. **Round tools.** A round gets the tools of `initiative-round`'s definition, with no bare Write or Edit (r13). Write and Edit are scoped to the paths its job writes, and Bash is as r14 gives it. The implementer sets the turn limit and names it in the report. Rests on supervision#r13, #r14 and #r30.
9. **A round's commits reach the initiative branch.** The round works on a branch of its own, made from the initiative branch's head. When the round ends (decision 4), `work run` merges that branch into the initiative branch and deletes it, before the proposal's transition. This merge has no scenario or suite check, because r4 is about an implementer's `DONE`. Rests on the answer to Q1 (reading A), with r18's deletion of a merged branch by analogy.
10. **A round that faults leaves the proposal as it was.** A round faults when its session ends in an error or at its turn limit, exits with an error, or leaves no JSON result. Then:
    - p1 keeps its status: no move to `failed`, nothing under its `## Faults`, no merge;
    - `work run` exits 1, with an error naming p1's round (its kind and stage directory) and the fault;
    - the stage directory and its start and end lines are kept as for any worker;
    - the next `work run` starts the round again in a new `<k>`.

    Rests on the answer to Q3 (reading B) and design-decision/exits-are-successful-or-errors.

## 4. Tests the decisions break

None. Each decision was checked against the notes' part 4 (there is no map, so tests were found by search):
- `tests/scripts/test_work_items.py`, `test_a_move_to_a_status_outside_the_lifecycle_is_refused`: `finished` is still refused under decision 7.
- `tests/scenarios/test_work_queue.py`, the `move` step and the `nothing_about` check ("it prints nothing about p1"): still true, because `items` does not change (decision 7).
- `tests/scenarios/test_supervision.py`, `one_commit_per_move`: it counts w1's moves only. The merge commits of decision 9 happen only in scenarios with a proposal.
- Work-item fault scenarios (r45, r34): decision 10 changes only what happens to a round. A work-item's fault still moves it to `failed`.
- Work-item merge scenarios (r4, r18, r61): decision 9 adds a merge of a round's branch and leaves the work-item merge alone.
- The model tests on proposal statuses are untouched, because `model_work.py` is outside the set. Every other supervision scenario with a proposal has undefined steps today.

## 5. Open cases

For the implementer to name in the report, not to choose:
- `work run`'s output and exit when the initiative holds only a proposal, now formulated, and no work-item. r9 speaks of work-items only.
- An apply or formulate result that gives questions, or an outcome other than DONE. Under decision 4 the transition still happens, and none of the four lines says where those questions go.
- A merge of a round's branch that conflicts with the initiative branch (decision 9). No line says what follows.
- A round branch left behind by a faulted round (decision 10), when the next `work run` starts the same round again.
- Drafts of earlier rounds live in the git-ignored `.shop/scratch/drafts/`, so a round's worktree does not have them. That belongs to the round's brief and agent (w143 to w145).
- D3: after `work answer` a proposal is `drafted`, so its gate would start again instead of apply. That is work-queue r24 (w140). These scenarios start from awaiting-answer with the answers already written.
