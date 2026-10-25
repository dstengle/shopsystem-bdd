## Coverage

| id | line | scenario |
|---|---|---|
| r111 | "**When** a transition that `work run` makes leaves a node of an initiative able to make another transition, `work run` shall take the node through that transition before it ends." | an initiative that a work-item's transition leaves able to be done is set done before `work run` ends |
| r116 | "**When** every question that a round of the kind `formulate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `formulate` for the proposal, given the answers." | a capability-proposal whose every question from its formulate round has an answer is given to a formulate round with the answers |
| r70 (changed) | "**When** every question that a round of the kind `gate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers." | none: returned as a question (below). The existing @r70 scenario is not rewritten. |
| r114 | "**When** a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied." | when the apply round `work run` started for a capability-proposal ends, the proposal's adds, changes and removes are written from the change list the round applied |
| r83 (changed) | "**When** a round of the kind `formulate` that `work run` started for a capability-proposal ends without giving a question, `work run` shall transition the proposal to `formulated`." | when the formulate round `work run` started for a capability-proposal ends without giving a question, the proposal is formulated (replaces the existing @r83 scenario) |
| r112 | "**When** a round of the kind `formulate` that `work run` started for a capability-proposal gives questions, `work run` shall write each question its result gives under the proposal's `## Questions`." | when the formulate round `work run` started for a capability-proposal gives questions, each is written under the proposal's ## Questions |
| r113 | "**When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall transition the proposal to `awaiting-answer`." | when the formulate round `work run` started for a capability-proposal gives a question, the proposal is awaiting-answer |
| r115 | "**If** a round of any kind that `work run` started for a capability-proposal or an initiative gives an outcome other than `DONE`, ends in an error or at its turn limit, or leaves no result `work run` can read, then `work run` shall take the initiative's other nodes through their transitions before it exits with an error." | Scenario Outline: when the gate round of a capability-proposal <ending>, the initiative's other nodes are taken through their transitions before `work run` exits with an error (one row for each of: gives BLOCKED, ends in an error, ends at its turn limit, leaves no result file) |

Every other line was left out of this round, as instructed.

## Questions

- r70: "**When** every question that a round of the kind `gate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers."
  - Question 1: the gate round gave no question, so r117 had `work run` write one question asking for approval.
    - Reading A: the approval question r117 writes counts as one of the gate's questions, so the apply round waits until the person answers it.
    - Reading B: the gate round gave no question, so r70's condition is met as soon as the gate round ends, and the apply round starts without the approval being answered.
  - Question 2: every gate question has an answer, and the proposal is back in `awaiting-answer` (or its answers are in) because a formulate round asked questions (r112, r113, r116).
    - Reading A: r70 holds only when the last gate question gets its answer, so only r116's formulate round starts.
    - Reading B: r70 holds whenever every gate question has an answer, so an apply round starts again too, alongside or ahead of r116's formulate round.

## Cases no line mentions

- A formulate round that gives the outcome `QUESTION` (not `DONE`) together with its questions. r112 and r113 say to write the questions and move the proposal to `awaiting-answer`, but r86 and r87 say to keep its status and make no transition. No scenario uses a non-DONE outcome for r112 or r113.
- No line says what status a proposal has while the formulate round from r116 runs. It is still `awaiting-answer`, so r113's move "to `awaiting-answer`" goes from `awaiting-answer` to itself. That is why the r113 scenario takes the r71 path, starting from `approved`.
- An apply round that ends without a change list, or whose change list names a capability other than the proposal's (r114).
- A formulate round that asks a question already under the proposal's `## Questions` (r112).
- r116 read literally also covers a formulate round that gave no question: "every question has an answer" is then true by default. That would start another formulate round on a `formulated` proposal, and with r111 it could loop. No scenario was written for it.
- r111 when the next transition is one `work run` cannot finish in this delivery, for example because of a worker limit or another initiative's round (r95) holding it.

## Drafts

- /tmp/work-run-i31-zd_jnr4z/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-2/supervision.feature
- /tmp/work-run-i31-zd_jnr4z/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-2/supervision.reply.md
