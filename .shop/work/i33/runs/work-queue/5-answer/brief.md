# answer

Agent: delegation-answerer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: none
Worktree: /tmp/work-run-i33-9vstbbh_/work-queue-5-answer
Branch: none (a detached checkout)
Question: r121, "whatever its status". Line: [r121] When a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever its status. Readings: (a, recommended) the status of the review's result (its outcome, e.g. `DONE` or `PARTIAL`): r121 as drafted; (b) the review's verdict: "[r121] When a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever verdict the review gives."
Delegation: The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading.

Read (paths in your worktree):
Run directory: /tmp/work-run-i33-9vstbbh_/work-queue-5-answer/.shop/scratch/5-answer
Result file: /tmp/work-run-i33-9vstbbh_/work-queue-5-answer/.shop/scratch/5-answer/result.json

You start in your worktree, /tmp/work-run-i33-9vstbbh_/work-queue-5-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
