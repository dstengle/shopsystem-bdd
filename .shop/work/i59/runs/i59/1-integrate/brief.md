# integrate of i59

Initiative: .shop/work/i59/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q25
Accepted lines of the request:
- 1. The plugin's commands, `work`, `measure`, `features`, `model`, `tools` and `migrate`, shall give their output as one JSON object on stdout by default.
- 2. **When** a command of the plugin refuses, finds a fault, finds a check failing or has a question for the person, the command shall exit 0 and give what it found and why in its JSON output.
- 3. **If** a command of the plugin crashes on an error it does not handle, then the command shall exit 1.
- 4. The plugin's agents shall return their output as structured JSON.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3@0.29, supervision#r5@0.29, supervision#r16@0.29, supervision#r71@0.29, supervision#r77@0.29, supervision#r80@0.29, supervision#r92@0.29, supervision#r93@0.29, work-queue#r3@0.29, work-queue#r11@0.29, work-queue#r16@0.29, work-queue#r17@0.29, work-queue#r18@0.29, requests#r1@0.29, requests#r3@0.29, supervision#r99@0.29, supervision#r104@0.29, supervision#r112@0.29, supervision#r113@0.29, supervision#r114@0.29, review#r9@0.29, supervision#r125@0.29, supervision#r126@0.29, supervision#r127@0.29, design-model-check#r120@0.29, design-model-check#r121@0.29, requests#r26@0.29, requests#r27@0.29, requests#r35@0.29, requests#r36@0.29, requests#r37@0.29, requests#r38@0.29, spec-integration#r17@0.29, work-queue#r33@0.29, supervision#r137@0.29, supervision#r138@0.29, supervision#r139@0.29, supervision#r140@0.29, requests#r46@0.29, spec-integration#r47@0.29, spec-integration#r48@0.29, spec-integration#r49@0.29, spec-integration#r50@0.29, spec-integration#r51@0.29, spec-integration#r52@0.29, spec-integration#r53@0.29, requests#r47@0.29, requests#r48@0.29, supervision#r177@0.29, supervision#r178@0.29, supervision#r179@0.29, supervision#r174@0.29, supervision#r175@0.29, supervision#r176@0.29, supervision#r181@0.29, supervision#r182@0.29, work-queue#r40@0.29, work-queue#r41@0.29, spec-integration#r57@0.29, supervision#r187@0.29, work-queue#r48@0.29, work-queue#r49@0.29, requests#r50@0.29, requests#r51@0.29, requests#r52@0.29, requests#r53@0.29, requests#r54@0.29, requests#r55@0.29, requests#r56@0.29, requests#r57@0.29, requests#r58@0.29, supervision#r184@0.29, supervision#r185@0.29, supervision#r186@0.29, work-queue#r47@0.29, requests#r49@0.29, supervision#r183@0.29, work-queue#r46@0.29, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35@0.29, migration-tools#r36@0.29, spec-integration#r56@0.29, work-queue#r42@0.29, work-queue#r43@0.29, work-queue#r44@0.29, work-queue#r45@0.29
Drafts path: /tmp/work-run-i59-hfzhnxml/i59-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Base: 3be48327e94e2ec17ea63d9334f33dd184b148e0
Worktree: /tmp/work-run-i59-hfzhnxml/i59-1-integrate
Branch: round/i59-1-integrate

Read (paths in your worktree):
- .shop/work/i59/initiative.md

Run directory: /tmp/work-run-i59-hfzhnxml/i59-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i59-hfzhnxml/i59-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i59-hfzhnxml/i59-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
