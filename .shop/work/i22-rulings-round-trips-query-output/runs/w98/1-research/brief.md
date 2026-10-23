# research of w98

Work-item: .shop/work/i22-rulings-round-trips-query-output/w98.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w98-1-research
Branch: none (a detached checkout)
Work-item branch: work/w98
Accepted scenarios:
- features/analysis-tools.feature: `tools check` runs each tool under its own heading and fails when any finds something
- features/analysis-tools.feature: `tools check` with --base examines the changed Python files that remain, in place of the paths given
- features/analysis-tools.feature: `tools check` with no file to examine does not fail for ruff and vulture
- features/analysis-tools.feature: `tools check` without import contracts does not run import-linter

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w98.md
- spec/capabilities/analysis-tools.md

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w98-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w98-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w98-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
