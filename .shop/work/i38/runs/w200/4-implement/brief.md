# implement of w200

Work-item: .shop/work/i38/w200.md
Agent: bdd-implementer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Base: 50a40103b15d1b9455b9d609ddb1a96cf799a11d
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w200
Branch: work/w200
Work-item branch: work/w200
Suite record: Suite: 945 passed, 0 failed at cab55fa6 in 27 s
Answers the person gave, each with the question it answers:
- Question: Decision 4 of the plan: a feature-formulator must add an r131 outline row for a formulate round whose result gives no question and no scenario for the requirements its proposal adds or changes (features/supervision.feature:918-923 has no such row). Then the formulate check can be coded red-green.
  Answer: 2026-10-26: Done: features/supervision.feature's r131 outline now has a formulate round row on capability-proposal p1 (columns node and setup added; the step reads 'every other session gives DONE'); the work-item-only outline is deprecated and listed in this work-item's Retires. Make the formulate row green red-green, then retire the deprecated outline (q16's delegation).

Read (paths in your worktree):
- .shop/work/i38/w200.md
- spec/capabilities/supervision.md
- .shop/work/i38/runs/w200/1-research
- .shop/work/i38/runs/w200/2-plan
- .shop/work/i38/runs/w200/3-implement

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w200/.shop/scratch/4-implement
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w200/.shop/scratch/4-implement/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w200: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
