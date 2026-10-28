# plan of w225

Work-item: .shop/work/i46/w225.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 134745663cfa0a109b8564370c2464ef9ee9a7d5
Worktree: /tmp/work-run-i46-3cyz6a2g/w225-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w225
Questions the researcher gave, for you to settle or ask:
- Conflict (spec-integration r55 vs supervision r165/r166): supervise_glossary.withheld withholds the terms of every glossary-proposal not approved, including g1 while its own apply round runs, so g1's apply cannot add its terms. Reading A: withhold excludes the proposal being applied (r165/r166 hold). Reading B: keep withholding for all, and r166 cannot hold. Which reading does the person choose?

Read (paths in your worktree):
- .shop/work/i46/w225.md
- spec/capabilities/supervision.md
- .shop/work/i46/runs/w225/1-research

Run directory: /tmp/work-run-i46-3cyz6a2g/w225-2-plan/.shop/scratch/2-plan
Result file: /tmp/work-run-i46-3cyz6a2g/w225-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /tmp/work-run-i46-3cyz6a2g/w225-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
