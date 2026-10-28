# integrate of i58

Initiative: .shop/work/i58/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q32
Accepted lines of the request:
- 1. **When** the person approves drafted lines at a gate that a session keeps, `work` shall write a capability-proposal for each capability the drafts change, with the requirement ids it adds, changes and removes.
- 2. **When** the drafts that the person approves at a gate a session keeps change the glossary, `work` shall write a glossary-proposal with the terms the drafts add, change and remove.
- 3. **When** `work` writes a proposal from a gate that a session kept, `work` shall write the proposal as `approved` and log each of its moves, naming the gate and the commit that applied its drafts.
- 4. **When** `work` writes the first proposal of a `proposed` initiative from a gate that a session kept, `work` shall move the initiative to `started`.
- 5. **When** a session keeps the gate of an initiative, `integrating-a-proposal` shall hand the approved drafts to `work run` through `work`, writing no proposal file by hand.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r46, spec-consistency#r28, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, requests#r47, requests#r48, supervision#r177, supervision#r178, supervision#r179, supervision#r180, supervision#r173, supervision#r174, supervision#r175, supervision#r176, supervision#r181, supervision#r182, work-queue#r40, work-queue#r41
Drafts path: /tmp/work-run-i58-7e2r578b/i58-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Base: ff10524ccd60ee2fedd13a4601e0fd5049868de1
Worktree: /tmp/work-run-i58-7e2r578b/i58-1-integrate
Branch: round/i58-1-integrate

Read (paths in your worktree):
- .shop/work/i58/initiative.md

Run directory: /tmp/work-run-i58-7e2r578b/i58-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i58-7e2r578b/i58-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i58-7e2r578b/i58-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
