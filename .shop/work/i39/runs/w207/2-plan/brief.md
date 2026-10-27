# plan of w207

Work-item: .shop/work/i39/w207.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w207-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w207
Questions the researcher gave, for you to settle or ask:
- The accepted scenarios already pass. Does w207 fix branch review 3's findings (D1, D2, D3), which are not scenarios, or only r34-r39? Its findings file also lists fix-now finding 2 in scripts/supervise_change.py, which r34-r39 do not cover.
- D2: must work list --json carry the waiting initiative (r39 applies to list in any form), or is the JSON of r35 only the statuses (r35 read literally)?
- Retiring work status (decision 0072) conflicts with live requests r13 (work show prints requests), requests r14 (work status prints observations) and migration-tools r32 (the SessionStart hook gives work status). Are these to be replaced before the retirement lands?
- The live r7 scenario at features/work-queue.feature:268 uses the no-target work show; removing that branch needs that scenario rewritten. Which?

Read (paths in your worktree):
- .shop/work/i39/w207.md
- spec/capabilities/work-queue.md
- .shop/work/i39/runs/w207/1-research

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w207-2-plan/.shop/scratch/2-plan
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w207-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w207-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
