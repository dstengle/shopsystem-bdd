# research of w95

Work-item: .shop/work/i22-rulings-round-trips-query-output/w95.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w95-1-research
Branch: none (a detached checkout)
Work-item branch: work/w95
Accepted scenarios:
- features/analysis-tools.feature: tests-of fails when nothing executed the target or the function does not exist (deprecated)
- features/analysis-tools.feature: tests-of says that no test of the map executed the target and exits successfully
- features/analysis-tools.feature: tests-of with --json prints the tests, their count and the map's commit as one JSON object
- features/analysis-tools.feature: untested with --json prints the functions, their count and the map's commit as one JSON object
- features/analysis-tools.feature: refs with --json prints the references and the summary as one JSON object
- features/analysis-tools.feature: map with --json prints the map's commit and its test count as one JSON object
- features/analysis-tools.feature: tests-of fails when the file has no function by the name given

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w95.md
- spec/capabilities/analysis-tools.md

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w95-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w95-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w95-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
