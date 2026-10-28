# integrate of supervision

Initiative: .shop/work/i47/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q33
Accepted lines of the request:
- 1. **While** no work-item accepts a requirement that a scenario names, the whole-suite run of a work-item's branch shall count a failure of that scenario as expected.
- 2. **When** a work-item's researcher gives an empty file set and no question, `work run` shall take the empty file set as the researcher's output.
- 3. **When** `work turn` passes a request's turn with every line's outcome `withdrawn`, `work` shall set the request's status to `withdrawn`.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, supervision#r93, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r46, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, supervision#r179, supervision#r174, supervision#r175, supervision#r176, supervision#r181, supervision#r182, work-queue#r40, work-queue#r41, spec-integration#r57, supervision#r187, work-queue#r48, work-queue#r49, requests#r50, requests#r51, requests#r52, requests#r53, requests#r54, requests#r55, requests#r56, requests#r57, requests#r58, supervision#r184, supervision#r185, supervision#r186, work-queue#r47, requests#r49, supervision#r183, work-queue#r46, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35, migration-tools#r36, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45
Drafts path: /tmp/work-run-i47-ee1m2t30/supervision-3-integrate/.shop/scratch/3-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Ledger: .shop/work/i47/ledger.md
Earlier drafts path (read only): .shop/work/i47/runs/i47/1-integrate/drafts/round-1/
Where an answer below asks for lines the request's accepted lines do not, draft those lines under the capabilities the answer names, each quoting the answer it comes from.
Base: edcfb0c266fb1d7417f5244a620bf7053adf08f7
Worktree: /tmp/work-run-i47-ee1m2t30/supervision-3-integrate
Branch: round/supervision-3-integrate
Answers the person gave, each with the question it answers:
- Question: supervision, r177 against r4. Lines: added [r177] **While** no work-item accepts a requirement that a scenario names, `work run` shall count a failure of that scenario in the whole-suite run of a work-item's branch as expected. r4 merges a work-item branch only if the whole suite passes "but for the failing scenarios r43 counts as expected"; as drafted, a failure r177 counts as expected still blocks the merge. Reading A (recommended): r177 lets the merge through: change r4 to "[r4] **When** an implementer's session ends with a result that gives no question, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 and r177 count as expected." Reading B: r4 stays.
  Answer: 2026-10-28: Q1, r177 against r4: reading A, r4 changes (retired, new id) so a failure r177 counts as expected does not block the merge (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: supervision, Implementation note for r177. Line: added [r177] (as above). The existing note "r122: the checks are the whole-suite runs of r24 and r43" names the runs; r177 says only "the whole-suite run of a work-item's branch". Reading A (recommended): r177 covers both runs: add the Implementation line "r177: the whole-suite runs are those of r24 and r43; `--whole-suite` marks each such scenario as xfail." Reading B: only r43's run before a merge: "r177: the whole-suite run is r43's, before a merge."
  Answer: 2026-10-28: Q2, the Implementation note for r177: reading A, r177 covers the whole-suite runs of r24 and r43 (answered by the coordinator under the person's delegation, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i47/supervision.md
- .shop/work/i47/runs/supervision/1-gate
- .shop/work/i47/runs/supervision/2-apply
- .shop/work/i47/ledger.md
- .shop/work/i47/runs/i47/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i47-ee1m2t30/supervision-3-integrate/.shop/scratch/3-integrate
Result file: /tmp/work-run-i47-ee1m2t30/supervision-3-integrate/.shop/scratch/3-integrate/result.json

You start in your worktree, /tmp/work-run-i47-ee1m2t30/supervision-3-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
