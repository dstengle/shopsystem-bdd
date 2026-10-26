# gate of requests

Capability-proposal: .shop/work/i37/requests.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: requests#r23, requests#r24
Changes: requests#r7
Removes: none
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i37/runs/i37/1-integrate/drafts/round-1/
Base: 94be81b4c7efa16e4b751858da00db485be242d1
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/requests-1-gate
Branch: round/requests-1-gate

Read (paths in your worktree):
- .shop/work/i37/requests.md
- .shop/work/i37/runs/i37/1-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/requests-1-gate/.shop/scratch/1-gate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/requests-1-gate/.shop/scratch/1-gate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/requests-1-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
