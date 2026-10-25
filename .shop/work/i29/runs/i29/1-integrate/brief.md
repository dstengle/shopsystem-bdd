# integrate of i29

Initiative: .shop/work/i29/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q5
Accepted lines of the request:
- 1. **When** `work run` finds an initiative that is not `done`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now and whose every raised request is `delivered`, `work run` shall set the initiative to `done`.
- 2. **When** `work run` has written an initiative's measurement and its analysis, `work run` shall commit them on the initiative branch.
- 3. **If** a change list that `work run` reads names a capability that `spec/capabilities/` does not have, **then** `work run` shall write no capability-proposal for it and exit with an error naming the capability.
- 4. **When** `work run` starts a round of the kind `gate` or `apply` for a capability-proposal, `work run` shall give the round the path of the kept drafts of the integrate round that wrote the proposal.
- 5. **If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing.
Ids drafted elsewhere (number added lines above each on the same capability): work-queue#r26, work-queue#r27, supervision#r99
Drafts path: /tmp/work-run-i29-wjhtu4f_/i29-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: 4640ef08c740b5867638a4ae1f92e94d586c297c
Worktree: /tmp/work-run-i29-wjhtu4f_/i29-1-integrate
Branch: round/i29-1-integrate

Read (paths in your worktree):
- .shop/work/i29/initiative.md

Run directory: /tmp/work-run-i29-wjhtu4f_/i29-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i29-wjhtu4f_/i29-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i29-wjhtu4f_/i29-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
