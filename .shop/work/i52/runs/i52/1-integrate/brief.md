# integrate of i52

Initiative: .shop/work/i52/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q38
Accepted lines of the request:
- 1. **When** a round of the kind `integrate` gives terms for an initiative that already has a glossary-proposal, `work run` shall add them to that glossary-proposal, keeping its status, questions and answers.
- 2. **When** a question of an initiative is left for the person, `work run` shall start no further session under the delegation for that initiative's questions until the person has answered.
- 3. **When** `work withdraw` leaves every work-item of an initiative green or withdrawn, `work` shall leave the initiative's status for `work run` to set once its kept branch review lists nothing to fix now.
- 4. **When** `work` sets an initiative's status, `work` shall log the move in the initiative's log.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3@0.29, supervision#r5@0.29, supervision#r16@0.29, supervision#r71@0.29, supervision#r77@0.29, supervision#r80@0.29, supervision#r92@0.29, work-queue#r3@0.29, work-queue#r11@0.29, work-queue#r16@0.29, work-queue#r17@0.29, work-queue#r18@0.29, requests#r1@0.29, requests#r3@0.29, supervision#r99@0.29, supervision#r104@0.29, supervision#r112@0.29, supervision#r113@0.29, supervision#r114@0.29, review#r9@0.29, supervision#r125@0.29, supervision#r126@0.29, supervision#r127@0.29, design-model-check#r120@0.29, design-model-check#r121@0.29, requests#r26@0.29, requests#r27@0.29, requests#r35@0.29, requests#r36@0.29, requests#r37@0.29, requests#r38@0.29, spec-integration#r17@0.29, work-queue#r33@0.29, supervision#r137@0.29, supervision#r138@0.29, supervision#r139@0.29, supervision#r140@0.29, requests#r46@0.29, spec-consistency#r28@0.29, spec-integration#r47@0.29, spec-integration#r48@0.29, spec-integration#r49@0.29, spec-integration#r50@0.29, spec-integration#r51@0.29, spec-integration#r52@0.29, spec-integration#r53@0.29, requests#r47@0.29, requests#r48@0.29, supervision#r177@0.29, supervision#r178@0.29, supervision#r179@0.29, supervision#r180@0.29, supervision#r173@0.29, supervision#r174@0.29, supervision#r175@0.29, supervision#r176@0.29
Drafts path: /tmp/work-run-i52-dg4tc5em/i52-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Base: 51bb24048825d03cf1e81728d51046a41b4c2ce0
Worktree: /tmp/work-run-i52-dg4tc5em/i52-1-integrate
Branch: round/i52-1-integrate

Read (paths in your worktree):
- .shop/work/i52/initiative.md

Run directory: /tmp/work-run-i52-dg4tc5em/i52-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i52-dg4tc5em/i52-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i52-dg4tc5em/i52-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
