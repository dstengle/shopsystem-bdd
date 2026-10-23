# research of w91

Work-item: .shop/work/i22-rulings-round-trips-query-output/w91.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w91-1-research
Branch: none (a detached checkout)
Work-item branch: work/w91
Accepted scenarios:
- features/work-queue.feature: `work <command>` commits the change it makes to a work-item on the current branch (deprecated)
- features/work-queue.feature: `work <command>` commits the change it makes to a work-item on the current branch
- features/work-queue.feature: answer on an awaiting-answer work-item writes the answer with the date under the work-item's Answers
- features/work-queue.feature: answer on an awaiting-answer work-item transitions it to the status the asking stage started from

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w91.md
- spec/capabilities/work-queue.md

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w91-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w91-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w91-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
