# plan of w95

Work-item: .shop/work/i22-rulings-round-trips-query-output/w95.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w95-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w95
Questions the researcher gave with its DONE, for you to settle or ask:
- Accepted deprecated outline row 'no test in the map executed the function unused' (features/analysis-tools.feature L124-136, tagged @r11 @deprecated) asserts exit 1 and passes today; r11 (and scenario L138) require exit 0. Plan must choose: retire that row, or keep it and drop r11's exit 0. Both readings are in notes.md part 7.
- The work run's PYTEST_ADDOPTS (--work-item w95) makes any scenario that runs tools map fail in its temp project; confirm the worker's environment for scenario runs.

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w95.md
- spec/capabilities/analysis-tools.md
- .shop/work/i22-rulings-round-trips-query-output/runs/w95/1-research

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w95-2-plan/.shop/scratch/2-plan
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w95-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w95-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
