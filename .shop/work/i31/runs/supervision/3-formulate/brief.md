# formulate of supervision

Capability-proposal: .shop/work/i31/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: formulate
Base: 9839b05ad9aad4b8f205963f9f056745069a2206
Worktree: /tmp/work-run-i31-zd_jnr4z/supervision-3-formulate
Branch: round/supervision-3-formulate
Answers the person gave, each with the question it answers:
- Question: Q1 (supervision r112, r113 against r86, r87, r88): what outcome does a `formulate` round that gives a question give? Lines: [r112] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall write the question under the proposal's `## Questions`. [r113] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall transition the proposal to `awaiting-answer`. [r83] changed. now: **When** a round of the kind `formulate` that `work run` started for a capability-proposal ends without giving a question, `work run` shall transition the proposal to `formulated`. was: the same without "without giving a question". Readings: (a, recommended) `DONE` with questions, as a researcher's may (r16): r86-r88 stand as they are. (b) `QUESTION`: r86-r88 then forbid r113's transition, and each changes to begin "**If** a round of any kind ... other than a round of the kind `formulate` that gives a question, gives an outcome other than `DONE`, ..." with its response unchanged.
  Answer: 2026-10-25: Q1: (a), DONE with questions; r86-r88 stand (the coordinator under the person's delegation 2026-10-25)
- Question: Q2 (supervision r70): when the questions a `formulate` round gave are answered, which round does `work run` start? (r70 is in spec/ and not among this round's lines; it says an `apply` round.) Readings: (a) an `apply` round, as r70 says today: no change. (b, recommended) a `formulate` round: add [r116] "**When** every question that a round of the kind `formulate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `formulate` for the proposal, given the answers." and change r70 to "**When** every question that a round of the kind `gate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers."
  Answer: 2026-10-25: Q2: (b), a formulate round given the answers: add r116 and change r70 as given (the coordinator under the person's delegation 2026-10-25)
- Question: Q3 (supervision r115): only a capability-proposal's round ending with an outcome other than `DONE`, or every ending r86-r88 name? Line: [r115] **If** a round that `work run` started for one capability-proposal ends with an outcome other than `DONE`, **then** `work run` shall take the initiative's other nodes through their transitions before it exits with an error. Readings: (a, recommended) as the request gives it: r115 as drafted. (b) every such ending: r115 becomes "**If** a round of any kind that `work run` started for a capability-proposal or an initiative gives an outcome other than `DONE`, ends in an error or at its turn limit, or leaves no result `work run` can read, then `work run` shall take the initiative's other nodes through their transitions before it exits with an error."
  Answer: 2026-10-25: Q3: (b), every such ending, as given (the coordinator under the person's delegation 2026-10-25)
- Question: Q4 (supervision r112): a `formulate` round may give several questions (formulation r3). Does `work run` write each? Line: [r112] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall write the question under the proposal's `## Questions`. Readings: (a, recommended) yes: r112 becomes "**When** a round of the kind `formulate` that `work run` started for a capability-proposal gives questions, `work run` shall write each question its result gives under the proposal's `## Questions`." (b) r112 as drafted, in the request's words. (Also drafted, no question: [r111] **When** a transition that `work run` makes leaves a node of an initiative able to make another transition, `work run` shall take the node through that transition before it ends. and [r114] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied.)
  Answer: 2026-10-25: Q4: (a), write each question its result gives (the coordinator under the person's delegation 2026-10-25)

Read (paths in your worktree):
- .shop/work/i31/supervision.md
- .shop/work/i31/runs/supervision/1-gate
- .shop/work/i31/runs/supervision/2-apply

Run directory: /tmp/work-run-i31-zd_jnr4z/supervision-3-formulate/.shop/scratch/3-formulate
Result file: /tmp/work-run-i31-zd_jnr4z/supervision-3-formulate/.shop/scratch/3-formulate/result.json

You start in your worktree, /tmp/work-run-i31-zd_jnr4z/supervision-3-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
