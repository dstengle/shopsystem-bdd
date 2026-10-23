# research of w99

Work-item: .shop/work/i22-rulings-round-trips-query-output/w99.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-aawfn3s_/w99-1-research
Branch: none (a detached checkout)
Work-item branch: work/w99
Accepted scenarios:
- features/migration-tools.feature: `migrate <command>` on a .shop/plugin-version that holds no version exits with an error, naming what it holds
- features/migration-tools.feature: a session starting in a repository whose .shop/plugin-version holds no version is told to tell the person

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w99.md
- spec/capabilities/migration-tools.md

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-aawfn3s_/w99-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-aawfn3s_/w99-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-aawfn3s_/w99-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
