# gate of work-queue

Capability-proposal: .shop/work/i25/work-queue.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i25-fu_s7dlu/work-queue-1-gate
Branch: round/work-queue-1-gate

Read (paths in your worktree):
- .shop/work/i25/work-queue.md

Run directory: /tmp/work-run-i25-fu_s7dlu/work-queue-1-gate/.shop/scratch/1-gate
Result file: /tmp/work-run-i25-fu_s7dlu/work-queue-1-gate/.shop/scratch/1-gate/result.json

You start in your worktree, /tmp/work-run-i25-fu_s7dlu/work-queue-1-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
