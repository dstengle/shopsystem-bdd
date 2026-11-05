# gate of supervision

Capability-proposal: .shop/work/i38/supervision.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: supervision#r128@0.29, supervision#r129@0.29, supervision#r130@0.29, supervision#r131@0.29, supervision#r132@0.29, supervision#r133@0.29
Changes: supervision#r4@0.29, supervision#r31@0.29, supervision#r45@0.29, supervision#r61@0.29, supervision#r86@0.29, supervision#r87@0.29, supervision#r88@0.29, supervision#r89@0.29, supervision#r90@0.29, supervision#r115@0.29
Removes: supervision#r3@0.29, supervision#r5@0.29, supervision#r16@0.29, supervision#r112@0.29, supervision#r113@0.29
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i38/runs/i38/1-integrate/drafts/round-1/
Base: 50a40103b15d1b9455b9d609ddb1a96cf799a11d
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-1-gate
Branch: round/supervision-1-gate

Read (paths in your worktree):
- .shop/work/i38/supervision.md
- .shop/work/i38/runs/i38/1-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-1-gate/.shop/scratch/1-gate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-1-gate/.shop/scratch/1-gate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-1-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
