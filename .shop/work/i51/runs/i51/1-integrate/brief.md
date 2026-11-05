# integrate of i51

Initiative: .shop/work/i51/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q37
Accepted lines of the request:
- 1. **When** a question of an initiative mentions the glossary, `work run` shall leave the question for the person, giving it to no session under a delegation.
- 2. **Where** the request an initiative fulfils gives a delegation, `work run` shall give each question of the initiative that does not mention the glossary to a session of its own, given the delegation, the files that one question names and nothing else, which answers the question if the delegation covers it and leaves it for the person otherwise.
- 3. **When** a round or a worker writes a question on the definition of a term or on a proposed term, the round or the worker shall name the glossary in the question.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3@0.29, supervision#r5@0.29, supervision#r16@0.29, supervision#r71@0.29, supervision#r77@0.29, supervision#r80@0.29, supervision#r92@0.29, work-queue#r3@0.29, work-queue#r11@0.29, work-queue#r16@0.29, work-queue#r17@0.29, work-queue#r18@0.29, requests#r1@0.29, requests#r3@0.29, supervision#r99@0.29, supervision#r104@0.29, supervision#r112@0.29, supervision#r113@0.29, supervision#r114@0.29, review#r9@0.29, supervision#r125@0.29, supervision#r126@0.29, supervision#r127@0.29, design-model-check#r120@0.29, design-model-check#r121@0.29, requests#r26@0.29, requests#r27@0.29, requests#r35@0.29, requests#r36@0.29, requests#r37@0.29, requests#r38@0.29, spec-integration#r17@0.29, work-queue#r33@0.29, supervision#r137@0.29, supervision#r138@0.29, supervision#r139@0.29, supervision#r140@0.29, requests#r46@0.29, spec-consistency#r28@0.29, spec-integration#r47@0.29, spec-integration#r48@0.29, spec-integration#r49@0.29, spec-integration#r50@0.29, spec-integration#r51@0.29, spec-integration#r52@0.29, spec-integration#r53@0.29, supervision#r173@0.29
Drafts path: /tmp/work-run-i51-du7riv0z/i51-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Base: 3c43389a5a12ce6f84d8556d2d86945c5fd901aa
Worktree: /tmp/work-run-i51-du7riv0z/i51-1-integrate
Branch: round/i51-1-integrate

Read (paths in your worktree):
- .shop/work/i51/initiative.md

Run directory: /tmp/work-run-i51-du7riv0z/i51-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i51-du7riv0z/i51-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i51-du7riv0z/i51-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
