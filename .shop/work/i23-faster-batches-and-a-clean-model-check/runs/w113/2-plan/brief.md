# plan of w113

Work-item: .shop/work/i23-faster-batches-and-a-clean-model-check/w113.md
Agent: bdd-planner
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.24.0/scripts
Base: 1ad628182e2dd2eb91d1e0ed6e95ecb34f3bcc63
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w113-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w113
Questions the researcher gave with its DONE, for you to settle or ask:
- FS, GS, RS (U+001C-U+001E) are not in r15's list, but str.splitlines splits on them: refuse them too, or only the seven listed?
- Does work add's LF/CR-only check on title and fields (scripts/workqueue.py add) come into scope?

Read (paths in your worktree):
- .shop/work/i23-faster-batches-and-a-clean-model-check/w113.md
- spec/capabilities/work-queue.md
- .shop/work/i23-faster-batches-and-a-clean-model-check/runs/w113/1-research

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w113-2-plan/.shop/scratch/2-plan
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w113-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w113-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
