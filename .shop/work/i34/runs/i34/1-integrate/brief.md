# integrate of i34

Initiative: .shop/work/i34/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q11
Accepted lines of the request:
- 1. **When** `work run` checks a work-item against the whole suite, `work run` shall count as expected to fail each scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r99
Drafts path: /tmp/work-run-i34-_okpayqm/i34-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: c7f6d2f71b0d2438e60d21651997f4e47262a3a7
Worktree: /tmp/work-run-i34-_okpayqm/i34-1-integrate
Branch: round/i34-1-integrate

Read (paths in your worktree):
- .shop/work/i34/initiative.md

Run directory: /tmp/work-run-i34-_okpayqm/i34-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i34-_okpayqm/i34-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i34-_okpayqm/i34-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
