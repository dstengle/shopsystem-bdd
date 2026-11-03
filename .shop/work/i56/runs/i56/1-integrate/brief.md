# integrate of i56

Initiative: .shop/work/i56/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q27
Accepted lines of the request:
- 1. **When** `work request` is given a title and a reason and no lines, `work request` shall keep the request with its reason and no lines.
- 2. **When** `work run` takes in a request that has a reason and no lines, `work run` shall start a round that drafts its lines from its reason and gives them to the person as a question.
- 3. **While** a request has no lines, `work start` shall start no initiative for it.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3@0.29, supervision#r5@0.29, supervision#r16@0.29, supervision#r71@0.29, supervision#r77@0.29, supervision#r80@0.29, supervision#r92@0.29, work-queue#r3@0.29, work-queue#r11@0.29, work-queue#r16@0.29, work-queue#r17@0.29, work-queue#r18@0.29, requests#r1@0.29, requests#r3@0.29, supervision#r99@0.29, supervision#r104@0.29, supervision#r112@0.29, supervision#r113@0.29, supervision#r114@0.29, review#r9@0.29, supervision#r125@0.29, supervision#r126@0.29, supervision#r127@0.29, design-model-check#r120@0.29, design-model-check#r121@0.29, requests#r26@0.29, requests#r27@0.29, requests#r35@0.29, requests#r36@0.29, requests#r37@0.29, requests#r38@0.29, spec-integration#r17@0.29, work-queue#r33@0.29, supervision#r137@0.29, supervision#r138@0.29, supervision#r139@0.29, supervision#r140@0.29, requests#r46@0.29, spec-consistency#r28@0.29, spec-integration#r47@0.29, spec-integration#r48@0.29, spec-integration#r49@0.29, spec-integration#r50@0.29, spec-integration#r51@0.29, spec-integration#r52@0.29, spec-integration#r53@0.29, requests#r47@0.29, requests#r48@0.29, supervision#r177@0.29, supervision#r178@0.29, supervision#r179@0.29, supervision#r180@0.29, supervision#r173@0.29, supervision#r174@0.29, supervision#r175@0.29, supervision#r176@0.29, supervision#r181@0.29, supervision#r182@0.29, work-queue#r40@0.29, work-queue#r41@0.29, spec-integration#r57@0.29, spec-integration#r56@0.29, work-queue#r42@0.29, work-queue#r43@0.29, work-queue#r44@0.29, work-queue#r45@0.29
Drafts path: /tmp/work-run-i56-6m908axm/i56-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Base: e98fc9bc6920b3c087107007edae5053502f0dcc
Worktree: /tmp/work-run-i56-6m908axm/i56-1-integrate
Branch: round/i56-1-integrate

Read (paths in your worktree):
- .shop/work/i56/initiative.md

Run directory: /tmp/work-run-i56-6m908axm/i56-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i56-6m908axm/i56-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i56-6m908axm/i56-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
