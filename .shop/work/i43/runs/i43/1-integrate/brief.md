# integrate of i43

Initiative: .shop/work/i43/initiative.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.1/scripts
Kind: integrate
Request: q23
Accepted lines of the request:
- 1. **When** `work run` starts a branch review, `work run` shall first run, at the initiative branch's head, the whole suite, each work-item's scenarios, each check a work-item names, `tools check`, `tools size`, `features deprecated` and `features bindings`, and give the branch reviewer each one's command, exit code and output, naming the commit they ran at.
- 2. **When** `work run` starts a branch review, `work run` shall give the branch reviewer the commits from the initiative's base to the branch's head, each with the work-item it belongs to or none, and the change of that range less `.shop/`.
- 3. **When** `work run` starts a branch review, `work run` shall give the branch reviewer the files to read: the capabilities the work-items are under, the design-decisions those capabilities rest on, and each work-item's plan, implementer's report and review findings.
- 4. The branch reviewer shall run nothing: it reads what `work run` gives it and the repository's files, and writes its findings and its result.
- 5. **Where** the branch reviewer finds a behaviour that only a run would show, the branch reviewer shall give it as a finding with the test that would show it, marked not run, in place of a reproduction.
- 6. **Where** the system reviewed has a dry-run mode and a real mode of one operation, the branch reviewer shall verify from the suite run `work run` gave it that the randomized test that they agree ran, and how many cases it tried.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r80, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r112, supervision#r113, supervision#r114, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140
Drafts path: /home/vscode/shopsystem-bdd/.shop/worktrees/i43-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: ebbf1beaaa1fb5e4e3d29ffde673a5999a2cbd22
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/i43-1-integrate
Branch: round/i43-1-integrate

Read (paths in your worktree):
- .shop/work/i43/initiative.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/i43-1-integrate/.shop/scratch/1-integrate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/i43-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/i43-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
