# integrate of i41

Initiative: .shop/work/i41/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Kind: integrate
Request: q19
Accepted lines of the request:
- 1. **When** a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
- 2. **When** `work run` starts a round of the kind `integrate` for a capability-proposal that has answers, `work run` shall give the round the capability-proposal's questions and answers and the initiative's ledger, with the accepted lines of the request the initiative fulfils.
- 3. **When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall set the capability-proposal `drafted`, its earlier drafts kept in their round's directory.
- 4. **When** `work run` starts a round of the kind `integrate` for a capability-proposal, `work run` shall keep the proposal's status until the round ends.
- 5. **When** a round of the kind `apply` that `work run` started for a capability-proposal ends having applied its drafts, `work run` shall transition the proposal to `approved`.
- 6. **When** a round of the kind `apply` that `work run` started for a capability-proposal ends having applied its drafts, `work run` shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied.
- 7. **When** a round of the kind `apply` that `work run` started for a capability-proposal ends having applied its drafts, `work run` shall start a round of the kind `formulate` for the proposal.
- 8. **When** a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall take that as the round's output.
- 9. **When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall write no second capability-proposal for that proposal's capability.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, requests#r1, requests#r3, supervision#r99, supervision#r112, supervision#r113, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, work-queue#r33, supervision#r137, supervision#r138, supervision#r139
Drafts path: /home/vscode/shopsystem-bdd/.shop/worktrees/i41-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: c2cbb99c64349b57b8c56ef45808f0c7537b3861
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/i41-1-integrate
Branch: round/i41-1-integrate

Read (paths in your worktree):
- .shop/work/i41/initiative.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/i41-1-integrate/.shop/scratch/1-integrate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/i41-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/i41-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
