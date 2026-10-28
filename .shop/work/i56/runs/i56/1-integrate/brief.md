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
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r46, spec-consistency#r28, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, requests#r47, requests#r48, supervision#r177, supervision#r178, supervision#r179, supervision#r180, supervision#r173, supervision#r174, supervision#r175, supervision#r176, supervision#r181, supervision#r182, work-queue#r40, work-queue#r41, spec-integration#r57, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45
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
