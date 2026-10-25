# integrate of i31

Initiative: .shop/work/i31/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q8
Accepted lines of the request:
- 1. **When** a transition that `work run` makes leaves a node of an initiative able to make another transition, `work run` shall take the node through that transition before it ends.
- 2. **If** a round that `work run` started for one capability-proposal ends with an outcome other than `DONE`, **then** `work run` shall take the initiative's other nodes through their transitions before it exits with an error.
- 3. **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall write the question under the proposal's `## Questions` and transition the proposal to `awaiting-answer`.
- 4. **When** a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r99, supervision#r105, supervision#r106, supervision#r107, supervision#r108, formulation#r23, supervision#r109, supervision#r110
Drafts path: /tmp/work-run-i31-na42kb62/i31-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: 9839b05ad9aad4b8f205963f9f056745069a2206
Worktree: /tmp/work-run-i31-na42kb62/i31-1-integrate
Branch: round/i31-1-integrate

Read (paths in your worktree):
- .shop/work/i31/initiative.md

Run directory: /tmp/work-run-i31-na42kb62/i31-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i31-na42kb62/i31-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i31-na42kb62/i31-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
