# plan of size-check

Work-item: .shop/work/i15-size-limit/size-check.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 2ea9b66fb6b40f0918de085a0ef8a4be38ac5130
Worktree: /tmp/work-run-i15-size-limit-l6t3hnm6/size-check-2-plan
Branch: none (a detached checkout)
Questions the researcher gave with its DONE, for you to settle or ask:
- CLAUDE.md does not exist in the checkout or its git history, yet the work-item's file set and the agent prompts assume it states a size limit. Should the plan create CLAUDE.md with the module map and the limit, or leave the r52 default of 300 as the only limit?
- r50-r52 do not say what `tools size` does in a non-Python project, outside git, with a tracked file deleted in the working tree, or with --limit 0, a negative or a non-number. Which should the plan pick?

Read (paths in your worktree):
- .shop/work/i15-size-limit/size-check.md
- spec/capabilities/analysis-tools.md
- .shop/work/i15-size-limit/runs/size-check/1-research

Run directory: /tmp/work-run-i15-size-limit-l6t3hnm6/size-check-2-plan/.shop/scratch/2-plan
Result file: /tmp/work-run-i15-size-limit-l6t3hnm6/size-check-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /tmp/work-run-i15-size-limit-l6t3hnm6/size-check-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write your notes, plan, report or findings in the run directory and, last, the result file: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings).
