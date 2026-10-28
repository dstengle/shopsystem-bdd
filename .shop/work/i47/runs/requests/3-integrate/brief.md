# integrate of requests

Initiative: .shop/work/i47/requests.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q33
Accepted lines of the request:
- 1. **While** no work-item accepts a requirement that a scenario names, the whole-suite run of a work-item's branch shall count a failure of that scenario as expected.
- 2. **When** a work-item's researcher gives an empty file set and no question, `work run` shall take the empty file set as the researcher's output.
- 3. **When** `work turn` passes a request's turn with every line's outcome `withdrawn`, `work` shall set the request's status to `withdrawn`.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, supervision#r93, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r46, spec-consistency#r28, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, supervision#r179, supervision#r174, supervision#r175, supervision#r176, supervision#r181, supervision#r182, work-queue#r40, work-queue#r41, spec-integration#r57, supervision#r187, work-queue#r48, work-queue#r49, requests#r50, requests#r51, requests#r52, requests#r53, requests#r54, requests#r55, requests#r56, requests#r57, requests#r58, supervision#r184, supervision#r185, supervision#r186, work-queue#r47, requests#r49, supervision#r183, work-queue#r46, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35, migration-tools#r36, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45
Drafts path: /tmp/work-run-i47-ee1m2t30/requests-3-integrate/.shop/scratch/3-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Ledger: .shop/work/i47/ledger.md
Earlier drafts path (read only): .shop/work/i47/runs/i47/1-integrate/drafts/round-1/
Where an answer below asks for lines the request's accepted lines do not, draft those lines under the capabilities the answer names, each quoting the answer it comes from.
Base: edcfb0c266fb1d7417f5244a620bf7053adf08f7
Worktree: /tmp/work-run-i47-ee1m2t30/requests-3-integrate
Branch: round/requests-3-integrate
Answers the person gave, each with the question it answers:
- Question: requests, r48 against r18: line 3 of q33 says 'passes a request's turn' without saying which side. When the asker passes the turn to the upstream with every line withdrawn, r18 sets awaiting-upstream and r48 sets withdrawn. Lines: [r47] When the upstream ends its turn on a request that is not delivered whose every line has the line outcome refused or withdrawn and at least one line refused, work shall set the request's status to refused (replaces r9, retired). [r48] When work turn passes a request's turn with every line's line outcome withdrawn, work shall set the request's status to withdrawn. Reading A (recommended): r48 holds for either side; change r18 to '[r18] When work turn passes a request's turn to its upstream with a line whose line outcome is not withdrawn, work shall set the request's status to awaiting-upstream.' and keep r48 as drafted. Reading B: r48 holds only for the upstream's turn: '[r48] When work turn passes a request's turn to its asker with every line's line outcome withdrawn, work shall set the request's status to withdrawn.' and r18 stays.
  Answer: 2026-10-28: Q1, r48 against r18: reading A, r48 holds for either side and r18 changes to name a line whose outcome is not withdrawn (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: requests, r48 and delivered: r9 and r47 apply only to a request that is not delivered; line 3 does not say whether r48 does. Line: [r48] When work turn passes a request's turn with every line's line outcome withdrawn, work shall set the request's status to withdrawn. Reading A (recommended): yes: '[r48] When work turn passes the turn of a request that is not delivered with every line's line outcome withdrawn, work shall set the request's status to withdrawn.' Reading B: no: r48 as drafted.
  Answer: 2026-10-28: Q2, r48 and delivered: reading A, r48 holds only for a request that is not delivered (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: requests, r48 and the turn: r7 still passes the turn of a request r48 sets withdrawn to the other side; line 3 does not say where the turn goes. Line: [r48] as above. Reading A: the turn stays with the side that ran work turn: add '[r49] When work sets a request's status to withdrawn, work shall keep the request's turn with the side that ran work turn.', and r7 gets the same exception it makes for accepted. Reading B (recommended): nothing changes.
  Answer: 2026-10-28: Q3, r48 and the turn: reading B, nothing changes (answered by the coordinator under the person's delegation, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i47/requests.md
- .shop/work/i47/runs/requests/1-gate
- .shop/work/i47/runs/requests/2-apply
- .shop/work/i47/ledger.md
- .shop/work/i47/runs/i47/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i47-ee1m2t30/requests-3-integrate/.shop/scratch/3-integrate
Result file: /tmp/work-run-i47-ee1m2t30/requests-3-integrate/.shop/scratch/3-integrate/result.json

You start in your worktree, /tmp/work-run-i47-ee1m2t30/requests-3-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
