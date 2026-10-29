# integrate of requests

Initiative: .shop/work/i60/requests.md
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
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r9, supervision#r16, supervision#r32, supervision#r71, supervision#r77, supervision#r80, supervision#r92, supervision#r93, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, work-queue#r23, requests#r1, requests#r3, requests#r13, requests#r14, supervision#r99, supervision#r104, supervision#r105, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r34, requests#r35, requests#r36, requests#r37, requests#r38, requests#r39, requests#r41, requests#r43, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, supervision#r149, requests#r46, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, requests#r47, requests#r48, supervision#r162, supervision#r163, supervision#r177, supervision#r178, supervision#r179, supervision#r174, supervision#r175, supervision#r176, supervision#r181, supervision#r182, work-queue#r34, work-queue#r35, work-queue#r40, work-queue#r41, spec-integration#r57, work-queue#r48, work-queue#r49, requests#r49, supervision#r183, work-queue#r46, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35, migration-tools#r36, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45, batch-measurement#r68, batch-measurement#r69, batch-measurement#r70, batch-measurement#r71, batch-measurement#r72, batch-measurement#r73, batch-measurement#r74, delivery#r23, design-model-check#r125, design-model-check#r126, design-model-check#r127, design-model-check#r128, design-model-check#r129, design-model-check#r130, design-model-check#r131, design-model-check#r132, design-model-check#r133, design-model-check#r134, design-model-check#r135, design-model-check#r136, design-model-check#r137, design-model-check#r138, design-model-check#r139, feature-file-tools#r63, feature-file-tools#r64, feature-file-tools#r65, feature-file-tools#r66, feature-file-tools#r67, feature-file-tools#r68, feature-file-tools#r69, feature-file-tools#r70, feature-file-tools#r71, feature-file-tools#r72, feature-file-tools#r73, migration-tools#r37, migration-tools#r38, migration-tools#r39, migration-tools#r40, migration-tools#r41, migration-tools#r42, migration-tools#r43, migration-tools#r44, migration-tools#r45, role-boundaries#r8, supervision#r188, supervision#r189, supervision#r190, supervision#r191, supervision#r192, supervision#r193, supervision#r194, supervision#r195, supervision#r196, supervision#r197, supervision#r198, supervision#r199, supervision#r200, supervision#r201, supervision#r202, supervision#r203, supervision#r204, supervision#r205, supervision#r206, supervision#r207, supervision#r208, work-queue#r50, work-queue#r51, work-queue#r52, work-queue#r53, work-queue#r54, work-queue#r55, work-queue#r56, work-queue#r57, work-queue#r58
Drafts path: /tmp/work-run-i60-wzn42g_j/requests-25-integrate/.shop/scratch/25-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Ledger: .shop/work/i60/ledger.md
Earlier drafts path (read only): .shop/work/i60/runs/requests/19-integrate/drafts/round-1/
Where an answer below asks for lines the request's accepted lines do not, draft those lines under the capabilities the answer names, each quoting the answer it comes from.
Base: ae85edd3a2ce3488f4d930ac5814845eea5e6178
Worktree: /tmp/work-run-i60-wzn42g_j/requests-25-integrate
Branch: round/requests-25-integrate
Answers the person gave, each with the question it answers:
- Question: requests#r60 (added): "**When** `work delegate` writes a delegation in a request, `work` shall commit the request." On which branch is the request committed? Reading A (recommended): "**When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch." Reading B: r60 stays as drafted.
  Answer: 2026-10-29: Reading A, as the person delegated (2026-10-29: answer every question with its recommended reading): r60 becomes "**When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch." by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: Whose part is the delegation, and may either side run `work delegate` (concerns r59: "**When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has.", and r4)? Reading A: only the asker's side: "**If** a side other than the request's asker runs `work delegate`, **then** `work delegate` shall refuse, naming the side that writes the delegation, and change nothing." (r4 then names `work delegate`.) Reading B: either side, no line.
  Answer: 2026-10-29: Reading B: either side may run work delegate, no line; a delegation is the person handing over decisions, mostly the upstream's gate questions (answered by the person, 2026-10-29)
- Question: Does `work delegate` keep to turns as r16 does (concerns r59)? Reading A: "**If** `work delegate` is run in the other side's turn, **then** `work delegate` shall refuse, because it is the other side's turn, and change nothing." Reading B (recommended, since a delegation comes from the person at any moment): "**When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is."
  Answer: 2026-10-29: Reading B: When `work delegate` is run, `work` shall write the delegation whichever side's turn it is (the delegation comes from the person at any moment, so it does not keep to turns as r16 does). by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: Does `work delegate` change a request's status or turn (concerns r59 and r60)? Reading A (recommended): "**When** `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn." Reading B: no line.
  Answer: 2026-10-29: Reading A, as the person's delegation directs (2026-10-28 'I take recommendations'; 2026-10-29 answer every question with its recommended reading): 'When `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn.' by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: requests#r62 (added): "**If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing." It names `withdrawn`, a status this spec does not yet name. Reading A (recommended): keep as drafted. Reading B: drop it until it exists: "...`delivered` or `refused`...".
  Answer: 2026-10-29: Reading A, as recommended and under the person's delegation of 2026-10-29: keep r62 as drafted, naming delivered, refused or withdrawn. by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: requests#r63 (added): "**When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date." Its narrator is a session; requests' narrator is a context taking in or raising a request. Reading A (recommended): stay in requests. Reading B: move to role-boundaries.
  Answer: 2026-10-29: Reading A: r63 stays in requests, as the person's delegation of 2026-10-28/29 says to take the recommended reading. by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: Do r16 and r55 reach `work delegate`? Lines concerned: [r70] "**When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is." (added) and the person's answer that either side may run `work delegate`; r16 ("a command other than `work resolve` ... in the other side's turn ... refuse") and r55 (a side writing the other side's part is refused when the asker is not the upstream itself). Reading A (recommended): the delegation belongs to neither side's part, so r16 and r55 do not reach `work delegate`; no line changes. Reading B: r16 and r55 are retired and redrafted with "other than `work resolve` and `work delegate`".
  Answer: 2026-10-29: Reading A: the delegation belongs to neither side's part, so r16 and r55 do not reach `work delegate`; no line changes (the person, 2026-10-29: answer every question with its recommended reading). by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: requests#r69: "**When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date." Reading 1: the session puts the date into the text it gives `work delegate`, so the request holds the person's words followed by the date. Reading 2: the request holds the person's words alone, word for word, and the date is written beside it, apart from the delegation.
  Answer: 2026-10-29: r69: reading 1, the session puts the date into the text it gives work delegate, as every delegation is written now (The person, <date>: "<words>") (answered by the person, 2026-10-29)

Read (paths in your worktree):
- .shop/work/i60/requests.md
- .shop/work/i60/runs/requests/1-gate
- .shop/work/i60/runs/requests/10-answer
- .shop/work/i60/runs/requests/11-answer
- .shop/work/i60/runs/requests/12-answer
- .shop/work/i60/runs/requests/13-answer
- .shop/work/i60/runs/requests/14-answer
- .shop/work/i60/runs/requests/15-answer
- .shop/work/i60/runs/requests/16-answer
- .shop/work/i60/runs/requests/17-answer
- .shop/work/i60/runs/requests/18-apply
- .shop/work/i60/runs/requests/19-integrate
- .shop/work/i60/runs/requests/2-answer
- .shop/work/i60/runs/requests/20-gate
- .shop/work/i60/runs/requests/21-answer
- .shop/work/i60/runs/requests/22-apply
- .shop/work/i60/runs/requests/23-formulate
- .shop/work/i60/runs/requests/24-formulate
- .shop/work/i60/runs/requests/3-answer
- .shop/work/i60/runs/requests/4-answer
- .shop/work/i60/runs/requests/5-answer
- .shop/work/i60/runs/requests/6-answer
- .shop/work/i60/runs/requests/7-answer
- .shop/work/i60/runs/requests/8-answer
- .shop/work/i60/runs/requests/9-answer
- .shop/work/i60/ledger.md
- .shop/work/i60/runs/requests/19-integrate/drafts/round-1/

Run directory: /tmp/work-run-i60-wzn42g_j/requests-25-integrate/.shop/scratch/25-integrate
Result file: /tmp/work-run-i60-wzn42g_j/requests-25-integrate/.shop/scratch/25-integrate/result.json

You start in your worktree, /tmp/work-run-i60-wzn42g_j/requests-25-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
