# integrate of i42

Initiative: .shop/work/i42/initiative.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.1/scripts
Kind: integrate
Request: q22
Accepted lines of the request:
- 1. **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
- 2. **When** a round of the kind `apply` ends, `initiative-round` shall give in its result each answer of the capability-proposal that the drafts it applied do not hold.
- 3. **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3@0.29, supervision#r5@0.29, supervision#r16@0.29, supervision#r71@0.29, supervision#r80@0.29, work-queue#r3@0.29, work-queue#r11@0.29, work-queue#r16@0.29, work-queue#r17@0.29, work-queue#r18@0.29, requests#r1@0.29, requests#r3@0.29, supervision#r99@0.29, supervision#r112@0.29, supervision#r113@0.29, supervision#r114@0.29, supervision#r125@0.29, supervision#r126@0.29, supervision#r127@0.29, design-model-check#r120@0.29, design-model-check#r121@0.29, requests#r26@0.29, requests#r27@0.29, requests#r35@0.29, requests#r36@0.29, requests#r37@0.29, requests#r38@0.29, work-queue#r33@0.29, supervision#r137@0.29, supervision#r138@0.29, supervision#r139@0.29
Drafts path: /home/vscode/shopsystem-bdd/.shop/worktrees/i42-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: 8f90ad3e6acd9159e1317a8c264050c0e646a842
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/i42-1-integrate
Branch: round/i42-1-integrate

Read (paths in your worktree):
- .shop/work/i42/initiative.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/i42-1-integrate/.shop/scratch/1-integrate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/i42-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/i42-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
