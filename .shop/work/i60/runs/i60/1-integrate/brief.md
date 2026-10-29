# integrate of i60

Initiative: .shop/work/i60/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q39
Accepted lines of the request:
- 1. **When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has, and commit the request.
- 2. **If** the delegation given to `work delegate` is empty, **then** `work delegate` shall refuse, because the delegation is empty, and change nothing.
- 3. **If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing.
- 4. **When** the person gives a session a delegation for a request outside `work request`, the session shall write it in the request with `work delegate` in the same reply, in the person's words and with the date.
- 5. **When** `work run` reads the delegation of an initiative's request, `work run` shall read the delegation the request has at that moment, given before or after the initiative started.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, supervision#r93, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r46, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, requests#r47, requests#r48, supervision#r162, supervision#r163, supervision#r177, supervision#r178, supervision#r179, supervision#r174, supervision#r175, supervision#r176, supervision#r181, supervision#r182, work-queue#r40, work-queue#r41, spec-integration#r57, supervision#r187, work-queue#r48, work-queue#r49, requests#r50, requests#r51, requests#r52, requests#r53, requests#r54, requests#r55, requests#r56, requests#r57, requests#r58, supervision#r184, supervision#r185, supervision#r186, work-queue#r47, requests#r49, supervision#r183, work-queue#r46, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35, migration-tools#r36, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45, batch-measurement#r68, batch-measurement#r69, batch-measurement#r70, batch-measurement#r71, batch-measurement#r72, batch-measurement#r73, batch-measurement#r74, delivery#r23, design-model-check#r125, design-model-check#r126, design-model-check#r127, design-model-check#r128, design-model-check#r129, design-model-check#r130, design-model-check#r131, design-model-check#r132, design-model-check#r133, design-model-check#r134, design-model-check#r135, design-model-check#r136, design-model-check#r137, design-model-check#r138, design-model-check#r139, feature-file-tools#r63, feature-file-tools#r64, feature-file-tools#r65, feature-file-tools#r66, feature-file-tools#r67, feature-file-tools#r68, feature-file-tools#r69, feature-file-tools#r70, feature-file-tools#r71, feature-file-tools#r72, feature-file-tools#r73, migration-tools#r37, migration-tools#r38, migration-tools#r39, migration-tools#r40, migration-tools#r41, migration-tools#r42, migration-tools#r43, migration-tools#r44, migration-tools#r45, role-boundaries#r8, supervision#r188, supervision#r189, supervision#r190, supervision#r191, supervision#r192, supervision#r193, supervision#r194, supervision#r195, supervision#r196, supervision#r197, supervision#r198, supervision#r199, supervision#r200, supervision#r201, supervision#r202, supervision#r203, supervision#r204, supervision#r205, supervision#r206, supervision#r207, supervision#r208, work-queue#r50, work-queue#r51, work-queue#r52, work-queue#r53, work-queue#r54, work-queue#r55, work-queue#r56, work-queue#r57, work-queue#r58
Drafts path: /tmp/work-run-i60-_83tsys1/i60-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Base: ae85edd3a2ce3488f4d930ac5814845eea5e6178
Worktree: /tmp/work-run-i60-_83tsys1/i60-1-integrate
Branch: round/i60-1-integrate

Read (paths in your worktree):
- .shop/work/i60/initiative.md

Run directory: /tmp/work-run-i60-_83tsys1/i60-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i60-_83tsys1/i60-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i60-_83tsys1/i60-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
