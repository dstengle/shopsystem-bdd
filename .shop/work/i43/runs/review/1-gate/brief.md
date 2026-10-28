# gate of review

Capability-proposal: .shop/work/i43/review.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.1/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: review#r32, review#r33, review#r34
Changes: none
Removes: review#r9
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i43/runs/i43/1-integrate/drafts/round-1/
Base: ebbf1beaaa1fb5e4e3d29ffde673a5999a2cbd22
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/review-1-gate
Branch: round/review-1-gate

Read (paths in your worktree):
- .shop/work/i43/review.md
- .shop/work/i43/runs/i43/1-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/review-1-gate/.shop/scratch/1-gate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/review-1-gate/.shop/scratch/1-gate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/review-1-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
