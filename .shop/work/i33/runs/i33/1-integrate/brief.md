# integrate of i33

Initiative: .shop/work/i33/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q10
Accepted lines of the request:
- 1. **If** every work-item of an initiative is `withdrawn`, **then** `work` shall leave the initiative's status as it is.
- 2. **If** `work add` is given an initiative that is `done` or `abandoned`, **then** `work add` shall refuse, naming the initiative's status, and change nothing.
- 3. **When** the delegation-answerer answers a reviewer's question on a work-item, the delegation-answerer shall give in its result whether its answer asks for a change or accepts the work-item as it is.
- 4. **When** a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever its status.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r99
Drafts path: /tmp/work-run-i33-2zhew41f/i33-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: 1caef88132eda3084c4ef5d18d7c8deeeccaf483
Worktree: /tmp/work-run-i33-2zhew41f/i33-1-integrate
Branch: round/i33-1-integrate

Read (paths in your worktree):
- .shop/work/i33/initiative.md

Run directory: /tmp/work-run-i33-2zhew41f/i33-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i33-2zhew41f/i33-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i33-2zhew41f/i33-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
