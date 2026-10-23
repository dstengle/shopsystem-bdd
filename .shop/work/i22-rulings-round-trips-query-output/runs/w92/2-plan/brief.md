# plan of w92

Work-item: .shop/work/i22-rulings-round-trips-query-output/w92.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w92-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w92
Questions the researcher gave with its DONE, for you to settle or ask:
- Q1: w91.md says the awaiting-ruling to awaiting-answer rename in work run is w91's, and w92 builds on it; w91 is at awaiting-ruling with that question open. Reading A: w91 renames now (w92's rows go green early, the deprecated rows go red). Reading B: w92 renames (workqueue STATUSES, supervise.py, supervise_merge.py change in w92). The accepted scenarios need STATUSES to list awaiting-answer either way.
- Q2: 10 accepted deprecated rows assert awaiting-ruling or ## Rulings and w92 has no Retires section. Reading A: retire them. Reading B: keep them as accepted, so they fail after the rename.
- Q3: D1: the scenarios inherit SHOPSYSTEM_WORK_RUN_WORKER from a worker's pytest, so work run refuses (21 of 25 fail in a worker session). Should the scenarios' env drop it (test_supervision.py:40), or should workers not set it?
- Q4: batch-measurement r41 and its awaiting-answer scenario are not accepted by w92; measure_build.py:76 counts the new name. In w92 or another work-item?
- Q5: exit 3 for awaiting-answer (spec Implementation) is untested; every scenario asserts only a nonzero exit. Should w92 assert 3?

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w92.md
- spec/capabilities/supervision.md
- .shop/work/i22-rulings-round-trips-query-output/runs/w92/1-research

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w92-2-plan/.shop/scratch/2-plan
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w92-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w92-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
