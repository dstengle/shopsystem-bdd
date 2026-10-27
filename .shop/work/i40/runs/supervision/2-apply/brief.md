# apply of supervision

Capability-proposal: .shop/work/i40/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Drafts path: .shop/work/i40/runs/i40/1-integrate/drafts/round-1/
Base: 96d2b80b65bc675406b72a3628ab6dcb98abd383
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply
Branch: round/supervision-2-apply
Answers the person gave, each with the question it answers:
- Question: The status of supervision's capability-proposal while the new `integrate` round runs is not given by the drafted lines. Lines concerned: [r137] When a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal. [r139] When a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall set the capability-proposal `drafted`, its earlier drafts kept in their round's directory. Readings: (a, recommended) the status is kept until the round ends, which r139 then sets: add 'When `work run` starts a round of the kind `integrate` for a capability-proposal, `work run` shall keep the proposal's status until the round ends.' (b) the proposal is set `drafted` at once, and r139 moves to the start of the round.
  Answer: 2026-10-27: Reading (a), recommended: add 'When `work run` starts a round of the kind `integrate` for a capability-proposal, `work run` shall keep the proposal's status until the round ends.' (answered by the coordinator under the person's delegation of 2026-10-27).

Read (paths in your worktree):
- .shop/work/i40/supervision.md
- .shop/work/i40/runs/supervision/1-gate
- .shop/work/i40/runs/i40/1-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply/.shop/scratch/2-apply
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
