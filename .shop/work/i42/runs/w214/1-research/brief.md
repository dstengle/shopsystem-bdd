# research of w214

Work-item: .shop/work/i42/w214.md
Agent: code-scout
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.1/scripts
Base: 8f90ad3e6acd9159e1317a8c264050c0e646a842
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w214-1-research
Branch: none (a detached checkout)
Work-item branch: work/w214
Accepted scenarios:
- features/supervision.feature: an apply round that gives an answer the drafts it applied do not hold is followed by a new integrate round for the proposal
- features/supervision.feature: an apply round that gives an answer the drafts it applied do not hold is followed by no formulate round for the proposal before the new integrate round's drafts are applied
- features/supervision.feature: a formulate round that formulates nothing because the proposal's answers change lines not in spec/ is followed by a new integrate round for the proposal
- features/supervision.feature: a formulate round that formulates nothing because the proposal's answers change lines not in spec/ leaves the proposal's status as it was
- features/supervision.feature: a formulate round that formulates nothing because the proposal's answers change lines not in spec/ has given its output

Read (paths in your worktree):
- .shop/work/i42/w214.md
- spec/capabilities/supervision.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w214-1-research/.shop/scratch/1-research
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w214-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w214-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
