# integrate of supervision

Initiative: .shop/work/i62/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q41
Accepted lines of the request:
- 2. **If** a scenario's run fails for a reason that a rerun of that scenario alone does not repeat, **then** `work run` shall run that scenario again once before it refuses the merge, and give both runs in its question when the second also fails.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r9, supervision#r16, supervision#r28, supervision#r32, supervision#r71, supervision#r77, supervision#r80, supervision#r92, supervision#r93, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, work-queue#r23, requests#r1, requests#r3, requests#r13, requests#r14, supervision#r99, supervision#r104, supervision#r105, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r34, requests#r35, requests#r36, requests#r37, requests#r38, requests#r39, requests#r41, requests#r43, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, supervision#r149, requests#r46, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, requests#r47, requests#r48, supervision#r162, supervision#r163, supervision#r177, supervision#r178, supervision#r179, supervision#r174, supervision#r175, supervision#r176, supervision#r181, supervision#r182, work-queue#r34, work-queue#r35, work-queue#r40, work-queue#r41, spec-integration#r57, work-queue#r48, work-queue#r49, requests#r49, supervision#r183, work-queue#r46, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35, migration-tools#r36, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45, batch-measurement#r68, batch-measurement#r69, batch-measurement#r70, batch-measurement#r71, batch-measurement#r72, batch-measurement#r73, batch-measurement#r74, delivery#r23, design-model-check#r125, design-model-check#r126, design-model-check#r127, design-model-check#r128, design-model-check#r129, design-model-check#r130, design-model-check#r131, design-model-check#r132, design-model-check#r133, design-model-check#r134, design-model-check#r135, design-model-check#r136, design-model-check#r137, design-model-check#r138, design-model-check#r139, feature-file-tools#r63, feature-file-tools#r64, feature-file-tools#r65, feature-file-tools#r66, feature-file-tools#r67, feature-file-tools#r68, feature-file-tools#r69, feature-file-tools#r70, feature-file-tools#r71, feature-file-tools#r72, feature-file-tools#r73, migration-tools#r37, migration-tools#r38, migration-tools#r39, migration-tools#r40, migration-tools#r41, migration-tools#r42, migration-tools#r43, migration-tools#r44, migration-tools#r45, role-boundaries#r8, supervision#r190, supervision#r191, supervision#r192, supervision#r193, supervision#r194, supervision#r195, supervision#r196, supervision#r197, supervision#r198, supervision#r199, supervision#r200, supervision#r201, supervision#r202, supervision#r203, supervision#r204, supervision#r205, supervision#r206, supervision#r207, supervision#r208, work-queue#r50, work-queue#r51, work-queue#r52, work-queue#r53, work-queue#r54, work-queue#r55, work-queue#r56, work-queue#r57, work-queue#r58, requests#r60, requests#r61, requests#r62, requests#r63, supervision#r221
Drafts path: /tmp/work-run-i62-kgtleaid/supervision-11-integrate/.shop/scratch/11-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Ledger: .shop/work/i62/ledger.md
Earlier drafts path (read only): .shop/work/i62/runs/i62/1-integrate/drafts/round-2/
Where an answer below asks for lines the request's accepted lines do not, draft those lines under the capabilities the answer names, each quoting the answer it comes from.
Base: 955ad466c30a8e870af65b406cdd4b241699f24e
Worktree: /tmp/work-run-i62-kgtleaid/supervision-11-integrate
Branch: round/supervision-11-integrate
Answers the person gave, each with the question it answers:
- Question: r213, "its question". Line (added): [r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item. Readings: (a, recommended, as drafted) the question r131 writes under the work-item's `## Questions`; (b) a question of its own: "[r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall write under the work-item's `## Questions` a question that gives both runs of the scenario and transition the work-item to `awaiting-answer`."
  Answer: 2026-10-30: Reading (a), as recommended and drafted: `work run` gives both runs of the scenario in the question r131 writes under the work-item's `## Questions`, per the person's delegation of 2026-10-28 and 2026-10-29 (answer every question with its recommended reading). by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: r213, what "both runs" give. Line (added): [r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item. Readings: (a, recommended, as drafted) both runs, without saying what each gives; (b) each run with its command, how it ended and its output: "... give both runs of the scenario, each with its command, how it ended and its output, in the question r131 writes for the work-item."
  Answer: 2026-11-02: Reading (a), as recommended and drafted, on each open question: (2) both runs, without saying what each gives; (3) no line for a passing second run; (4) every failure that would refuse the merge gets one more run; (5) the second run is of that scenario by itself; (6) scenarios only, in both runs r4 makes. The ids r212 and r213 are already taken in spec/capabilities/supervision.md (it now goes to r218): the two lines take the next free ids, r219 and r220, the references between them renumbered to match (the person, 2026-11-02).
- Question: After a passing second run. Lines (added): r212 and r213 (q41 does not say the merge goes ahead). Readings: (a, recommended, as drafted) add no line; (b) add a line: "[r214] **When** the second run of a scenario that r212 makes passes, `work run` shall take the scenario as passing for r4's merge."
  Answer: 2026-11-02: (3) After a passing second run: reading (a), add no line (the person, 2026-11-02).
- Question: r212's condition. Line (added): [r212] **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge. Readings: (a, recommended, as drafted) every failure that would refuse the merge gets one more run; the rerun is how `work run` finds whether it repeats; (b) only failures `work run` can tell in advance are not the work-item's (q41 gives no list): "[r212] **If** a scenario fails in a run that `work run` makes before a merge, for a reason that `work run` takes as not caused by the work-item, **then** `work run` shall run that scenario again once, alone, before it refuses the merge."
  Answer: 2026-11-02: (4) r212's condition: reading (a), every failure that would refuse the merge gets one more run (the person, 2026-11-02).
- Question: r212, "alone". Line (added): r212 as in the previous question. Readings: (a, recommended, as drafted) the second run is of that scenario by itself; (b) the same run is made again: "[r212] **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall make that run again once before it refuses the merge."
  Answer: 2026-11-02: (5) r212, alone: reading (a), the second run is of that scenario by itself (the person, 2026-11-02).
- Question: r212, reach. Line (added): r212 as above. Readings: (a, recommended, as drafted) scenarios only, in both runs r4 makes; (b) a failing non-scenario test of the suite gets a second run too: "[r212] **If** a scenario or test fails in a run ..."
  Answer: 2026-11-02: (6) r212, reach: reading (a), scenarios only, in both runs r4 makes (the person, 2026-11-02).
- Question: r219: Reading 1: the merge is refused whatever the second run gives; reading 2: refused only if the second run also fails, and a passing second run lets the merge go ahead.
  Answer: 2026-11-02: r219: reading 2. The merge is refused only if the second run also fails; a passing second run lets the merge go ahead. This replaces my earlier answer (3), 'add no line for a passing second run': r219 is to say so itself, or a further line beside it (the person, 2026-11-02).

Read (paths in your worktree):
- .shop/work/i62/supervision.md
- .shop/work/i62/runs/supervision/1-gate
- .shop/work/i62/runs/supervision/10-formulate
- .shop/work/i62/runs/supervision/2-answer
- .shop/work/i62/runs/supervision/3-answer
- .shop/work/i62/runs/supervision/4-answer
- .shop/work/i62/runs/supervision/5-answer
- .shop/work/i62/runs/supervision/6-answer
- .shop/work/i62/runs/supervision/7-answer
- .shop/work/i62/runs/supervision/8-apply
- .shop/work/i62/runs/supervision/9-formulate
- .shop/work/i62/ledger.md
- .shop/work/i62/runs/i62/1-integrate/drafts/round-2/

Run directory: /tmp/work-run-i62-kgtleaid/supervision-11-integrate/.shop/scratch/11-integrate
Result file: /tmp/work-run-i62-kgtleaid/supervision-11-integrate/.shop/scratch/11-integrate/result.json

You start in your worktree, /tmp/work-run-i62-kgtleaid/supervision-11-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
