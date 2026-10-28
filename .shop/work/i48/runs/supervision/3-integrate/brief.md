# integrate of supervision

Initiative: .shop/work/i48/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q34
Accepted lines of the request:
- 1. **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids and terms of the proposal that the round's change list does not name.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, supervision#r93, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r46, spec-consistency#r28, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, requests#r47, requests#r48, supervision#r177, supervision#r178, supervision#r174, supervision#r175, supervision#r176, supervision#r181, supervision#r182, work-queue#r40, work-queue#r41, spec-integration#r57, supervision#r187, work-queue#r48, work-queue#r49, requests#r50, requests#r51, requests#r52, requests#r53, requests#r54, requests#r55, requests#r56, requests#r57, requests#r58, supervision#r184, supervision#r185, supervision#r186, work-queue#r47, requests#r49, supervision#r183, work-queue#r46, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35, migration-tools#r36, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45
Drafts path: /tmp/work-run-i48-89bbkiac/supervision-3-integrate/.shop/scratch/3-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Ledger: .shop/work/i48/ledger.md
Earlier drafts path (read only): .shop/work/i48/runs/i48/1-integrate/drafts/round-1/
Where an answer below asks for lines the request's accepted lines do not, draft those lines under the capabilities the answer names, each quoting the answer it comes from.
Base: 6cf63096ec9edd7f549d3452dfc0408f53453906
Worktree: /tmp/work-run-i48-89bbkiac/supervision-3-integrate
Branch: round/supervision-3-integrate
Answers the person gave, each with the question it answers:
- Question: r179, "terms of the proposal": a capability-proposal lists requirement ids, and terms are listed by a glossary-proposal. Line: [r179] **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids and terms of the proposal that the round's change list does not name. Reading A: split it into r179 (requirement ids of the capability-proposal) and r180 "**When** a round of the kind `integrate` redrafts some of the terms of a glossary-proposal it was started for, `work run` shall keep the terms of the glossary-proposal that the round's change list does not name." Reading B: drop "terms", so r179 reads "...shall keep the requirement ids of the capability-proposal that the round's change list does not name." Reading C: keep the line as drafted. Recommended: A.
  Answer: 2026-10-28: r179's terms: reading A, split into r179 (a capability-proposal's requirement ids) and r180 (a glossary-proposal's terms) (answered by the person, 2026-10-28)
- Question: r179, what "keep" means for the ids. Line: [r179] **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids and terms of the proposal that the round's change list does not name. Reading A: the ids stay in the `adds`, `changes` and `removes` that `work run` writes for the proposal (r159, r145), with the line as drafted. Reading B: the apply round is also given the earlier round's drafts of the lines not named, so the line reads "...`work run` shall give the round of the kind `apply` the kept drafts of the earlier round for each line the redraft's change list does not name." Recommended: A.
  Answer: 2026-10-28: r179's keep: reading A, the ids stay in the adds, changes and removes work run writes for the proposal (answered by the person, 2026-10-28)
- Question: r179, which redraft the line covers. Line: [r179] **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids and terms of the proposal that the round's change list does not name. Reading A: any round of the kind `integrate` started for a capability-proposal (r141, r150, r149) that redrafts a subset of its lines, as drafted. Reading B: only a redraft from answers (r142, r148). Recommended: A.
  Answer: 2026-10-28: r179's redrafts: reading A, any integrate round started for a capability-proposal that redrafts a subset of its lines (answered by the person, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i48/supervision.md
- .shop/work/i48/runs/supervision/1-gate
- .shop/work/i48/runs/supervision/2-apply
- .shop/work/i48/ledger.md
- .shop/work/i48/runs/i48/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i48-89bbkiac/supervision-3-integrate/.shop/scratch/3-integrate
Result file: /tmp/work-run-i48-89bbkiac/supervision-3-integrate/.shop/scratch/3-integrate/result.json

You start in your worktree, /tmp/work-run-i48-89bbkiac/supervision-3-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
