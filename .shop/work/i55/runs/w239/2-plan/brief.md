# plan of w239

Work-item: .shop/work/i55/w239.md
Agent: bdd-planner
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts
Base: c53a7c25e23bac68cae83b147c9dd66a2e6c6227
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w239-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w239
Questions the researcher gave, for you to settle or ask:
- Does the retirement of r14 (w239 Retires) remove observations from `work status` (reading A, assumed in the notes: uncited moves to list and status loses its observation lines and JSON key) or keep them (reading B: list gains them, status unchanged, only the r14 scenario dropped)?
- Should `work list --json` carry an `observations` key? r64 says 'print' (text); no test constrains it.

Read (paths in your worktree):
- .shop/work/i55/w239.md
- spec/capabilities/requests.md
- .shop/work/i55/runs/w239/1-research

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w239-2-plan/.shop/scratch/2-plan
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w239-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w239-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
