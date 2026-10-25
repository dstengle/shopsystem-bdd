# answer

Agent: delegation-answerer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: none
Worktree: /tmp/work-run-i33-9vstbbh_/supervision-6-answer
Branch: none (a detached checkout)
Question: Q5 (supervision r121, "whatever its status"). Added line: [r121] **When** a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever its status. (a, recommended) The status of the review's result (its outcome, e.g. `DONE` or `PARTIAL`): r121 as drafted. (b) The review's verdict: "[r121] **When** a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever verdict the review gives." Related, optional: a branch reviewer's session that ends in error, at its turn limit or with no readable result; (a, recommended) add nothing; (b) add "[r122] **If** a branch reviewer's session ends in an error or at its turn limit or leaves no result `work run` can read, then `work run` shall take the review as not read."
Delegation: The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading.

Read (paths in your worktree):
Run directory: /tmp/work-run-i33-9vstbbh_/supervision-6-answer/.shop/scratch/6-answer
Result file: /tmp/work-run-i33-9vstbbh_/supervision-6-answer/.shop/scratch/6-answer/result.json

You start in your worktree, /tmp/work-run-i33-9vstbbh_/supervision-6-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
