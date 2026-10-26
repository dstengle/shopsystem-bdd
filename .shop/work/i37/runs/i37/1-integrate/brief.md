# integrate of i37

Initiative: .shop/work/i37/initiative.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: integrate
Request: q15
Accepted lines of the request:
- 1. **When** the upstream ends its turn on a request and `work` sets the request to `accepted`, `work` shall keep the request's turn the upstream's.
- 2. **When** `work` sets a request to `delivered`, `work` shall pass the request's turn to its asker.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r99, supervision#r125, supervision#r126, supervision#r127
Drafts path: /home/vscode/shopsystem-bdd/.shop/worktrees/i37-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: 94be81b4c7efa16e4b751858da00db485be242d1
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/i37-1-integrate
Branch: round/i37-1-integrate

Read (paths in your worktree):
- .shop/work/i37/initiative.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/i37-1-integrate/.shop/scratch/1-integrate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/i37-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/i37-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
