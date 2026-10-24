# research of w120

Work-item: .shop/work/i23-faster-batches-and-a-clean-model-check/w120.md
Agent: code-scout
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.24.0/scripts
Base: 1ad628182e2dd2eb91d1e0ed6e95ecb34f3bcc63
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w120-1-research
Branch: none (a detached checkout)
Work-item branch: work/w120
Accepted scenarios:
- features/work-queue.feature: answer with a line break in it is refused, and nothing changes
- features/work-queue.feature: an answer of two lines to a work-item not awaiting-answer is refused as more than one line first

Read (paths in your worktree):
- .shop/work/i23-faster-batches-and-a-clean-model-check/w120.md
- spec/capabilities/work-queue.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w120-1-research/.shop/scratch/1-research
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w120-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w120-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
