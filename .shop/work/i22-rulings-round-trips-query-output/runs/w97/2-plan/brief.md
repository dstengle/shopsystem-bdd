# plan of w97

Work-item: .shop/work/i22-rulings-round-trips-query-output/w97.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w97-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w97
Questions the researcher gave with its DONE, for you to settle or ask:
- Should 'one above the highest work-item' count only w<n>.md-named files (current) or every work-item's id? With fix-login.md holding id w7, the current code gives w2; the id reading gives w8.
- Should a plain note named w2.md (or a non-UTF-8 .md note) beside work-items block work add? Current code refuses both (D1, D2).

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w97.md
- spec/capabilities/design-model-check.md
- .shop/work/i22-rulings-round-trips-query-output/runs/w97/1-research

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w97-2-plan/.shop/scratch/2-plan
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w97-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w97-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
