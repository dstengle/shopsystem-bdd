# integrate of i32

Initiative: .shop/work/i32/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q9
Accepted lines of the request:
- 1. **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item, `work run` shall transition the work-item to `ready` for an answer that asks for a change and to `done` for one that accepts the work-item as it is.
- 2. **When** a branch review ends, the branch reviewer shall give in its result's questions only the findings it triages fix now.
- 3. **When** work-queue r26 and r27 change what decision 0063 decides for a reviewer's question, the spec shall hold a decision that supersedes the reviewer's row of decision 0063.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r99
Drafts path: /tmp/work-run-i32-_8yggjjo/i32-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: d3d3839d7347d73cc5e3d51f1761ba13875a4ae2
Worktree: /tmp/work-run-i32-_8yggjjo/i32-1-integrate
Branch: round/i32-1-integrate

Read (paths in your worktree):
- .shop/work/i32/initiative.md

Run directory: /tmp/work-run-i32-_8yggjjo/i32-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i32-_8yggjjo/i32-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i32-_8yggjjo/i32-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
