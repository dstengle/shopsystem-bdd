# formulate of supervision

Capability-proposal: .shop/work/i32/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: formulate
Base: d3d3839d7347d73cc5e3d51f1761ba13875a4ae2
Worktree: /tmp/work-run-i32-_6c6pt8f/supervision-4-formulate
Branch: round/supervision-4-formulate
Answers the person gave, each with the question it answers:
- Question: Decision: supervision#r118 and supervision#r119, with decision 0069 (supersedes 0063's row for a reviewer's question; by the person's delegation of 2026-10-25 via q9). Lines in full (both new): - [supervision#r118] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that asks for a change, `work run` shall transition the work-item to `ready`. - [supervision#r119] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that accepts the work-item as it is, `work run` shall transition the work-item to `done`. Readings: (a, recommended) Approve both as drafted. An answer that says neither stays covered by work-queue r28, which already refuses it. (b) Approve both and add [supervision#r120]: **If** a session started under a delegation answers a reviewer's question without saying whether it asks for a change or accepts the work-item as it is, **then** `work run` shall leave the question unanswered for the person. (c) Do not approve; say what to change.
  Answer: 2026-10-25: Reading (a): approve supervision#r118 and supervision#r119 as drafted, with decision 0069. This follows the person's delegation of 2026-10-25 to answer every question with its recommended reading. by: work run, under the delegation "The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading."

Read (paths in your worktree):
- .shop/work/i32/supervision.md
- .shop/work/i32/runs/supervision/1-gate
- .shop/work/i32/runs/supervision/2-answer
- .shop/work/i32/runs/supervision/3-apply

Run directory: /tmp/work-run-i32-_6c6pt8f/supervision-4-formulate/.shop/scratch/4-formulate
Result file: /tmp/work-run-i32-_6c6pt8f/supervision-4-formulate/.shop/scratch/4-formulate/result.json

You start in your worktree, /tmp/work-run-i32-_6c6pt8f/supervision-4-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
