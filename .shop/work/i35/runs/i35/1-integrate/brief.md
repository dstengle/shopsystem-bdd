# integrate of i35

Initiative: .shop/work/i35/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q12
Accepted lines of the request:
- 1. **When** `work run` drafts a work-item, `work run` shall list under its `## Retires` each `@deprecated` scenario whose `Deprecated for:` names a scenario of a requirement the work-item accepts.
- 2. **When** every work-item of an initiative is `green` or `withdrawn`, `work run` shall draft one work-item that retires each `@deprecated` scenario whose replacement's work-item is `green`.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r99
Drafts path: /tmp/work-run-i35-5vwjz_3l/i35-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: 3fbe46ea079ea23096e2dc093be6b24d1799fbd7
Worktree: /tmp/work-run-i35-5vwjz_3l/i35-1-integrate
Branch: round/i35-1-integrate

Read (paths in your worktree):
- .shop/work/i35/initiative.md

Run directory: /tmp/work-run-i35-5vwjz_3l/i35-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i35-5vwjz_3l/i35-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i35-5vwjz_3l/i35-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
