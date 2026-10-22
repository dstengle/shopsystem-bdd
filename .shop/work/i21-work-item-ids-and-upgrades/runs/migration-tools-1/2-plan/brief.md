# plan of migration-tools-1

Work-item: .shop/work/i21-work-item-ids-and-upgrades/migration-tools-1.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 202c029c9774c00364b3bace8b0e99b529425e70
Worktree: /tmp/work-run-i21-work-item-ids-and-upgrades-gexbowe1/migration-tools-1-2-plan
Branch: none (a detached checkout)
Work-item branch: work/migration-tools-1
Questions the researcher gave with its DONE, for you to settle or ask:
- Q1: r18 and r22 need a pending 0.24.0 step on a 0.23.1 repository, but .claude-plugin/plugin.json says 0.23.1. Bump the plugin to 0.24.0 in this work-item, or keep 0.23.1 (then no step is pending)? Both readings are in notes.md part 7/Questions.
- Q2: The coordinator note asks for delivering-an-initiative to say `work add <initiative> <title>`; not an accepted requirement, and work add currently takes <name> and writes name-based ids (defect D1). Left to the planner.

Read (paths in your worktree):
- .shop/work/i21-work-item-ids-and-upgrades/migration-tools-1.md
- spec/capabilities/migration-tools.md
- .shop/work/i21-work-item-ids-and-upgrades/runs/migration-tools-1/1-research

Run directory: /tmp/work-run-i21-work-item-ids-and-upgrades-gexbowe1/migration-tools-1-2-plan/.shop/scratch/2-plan
Result file: /tmp/work-run-i21-work-item-ids-and-upgrades-gexbowe1/migration-tools-1-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /tmp/work-run-i21-work-item-ids-and-upgrades-gexbowe1/migration-tools-1-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
