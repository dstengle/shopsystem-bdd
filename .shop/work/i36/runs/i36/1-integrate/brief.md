# integrate of i36

Initiative: .shop/work/i36/initiative.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: integrate
Request: q13
Accepted lines of the request:
- 1. **When** `work run` writes the brief of a round of the kind `formulate`, `work run` shall tell the round that a round that has formulated every line with one reading and gives each other line as a question has done its work, with the outcome `DONE`.
- 2. **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question with the outcome `PARTIAL`, `work run` shall write each question its result gives under the proposal's `## Questions`.
- 3. **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question with the outcome `PARTIAL`, `work run` shall transition the proposal to `awaiting-answer`.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r99
Drafts path: /home/vscode/shopsystem-bdd/.shop/worktrees/i36-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: 977e30e08f113241f73181f29ad1b2acf7fc5b26
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/i36-1-integrate
Branch: round/i36-1-integrate

Read (paths in your worktree):
- .shop/work/i36/initiative.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/i36-1-integrate/.shop/scratch/1-integrate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/i36-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/i36-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
