# research of w94

Work-item: .shop/work/i22-rulings-round-trips-query-output/w94.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w94-1-research
Branch: none (a detached checkout)
Work-item branch: work/w94
Accepted scenarios:
- features/batch-measurement.feature: each work-item is given with its transitions, its awaiting-ruling and failed counts and the commits its merge brought in (deprecated)
- features/batch-measurement.feature: each work-item is given with its transitions, its awaiting-answer and failed counts and the commits its merge brought in
- features/batch-measurement.feature: the totals are over the stages' sessions, an unended stage included, and span the first transition to the last (deprecated)
- features/batch-measurement.feature: the totals are over the stages' sessions, an unended stage included, and span the first transition to the last
- features/batch-measurement.feature: each stage is given with its session's round trips
- features/batch-measurement.feature: a stage whose session has no transcript to be found is given without its round trips
- features/batch-measurement.feature: show prints each stage's round trips beside its turns
- features/batch-measurement.feature: show prints the stages of a measurement that gives no round trips without them

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w94.md
- spec/capabilities/batch-measurement.md

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w94-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w94-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w94-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
