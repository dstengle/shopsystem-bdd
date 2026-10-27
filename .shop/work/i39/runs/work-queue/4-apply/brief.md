# apply of work-queue

Capability-proposal: .shop/work/i39/work-queue.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Drafts path: .shop/work/i39/runs/i39/1-integrate/drafts/round-1/
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-4-apply
Branch: round/work-queue-4-apply
Answers the person gave, each with the question it answers:
- Question: Approve the added work-queue line [r33] (new, under spec/capabilities/work-queue.md): "**While** a request that an initiative raised into an upstream is not `delivered`, `work status` shall print the initiative as waiting on that request." It pairs with supervision r136, which holds back work-items for the capability-proposal while the request is not delivered. Readings: (A) approve the line as drafted [recommended]; (B) drop it, so `work status` says nothing about such a wait; (C) reword it, in which case give the wording.
  Answer: 2026-10-27: r33: Reading (C), reworded to name the consolidated list action that replaces work status. Also folded in: work show and work status are consolidated into one action listing all work with its status and one showing the detail of an individual item.

Read (paths in your worktree):
- .shop/work/i39/work-queue.md
- .shop/work/i39/runs/work-queue/1-gate
- .shop/work/i39/runs/work-queue/2-apply
- .shop/work/i39/runs/work-queue/3-apply
- .shop/work/i39/runs/i39/1-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-4-apply/.shop/scratch/4-apply
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-4-apply/.shop/scratch/4-apply/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-4-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
