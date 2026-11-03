# integrate of supervision

Initiative: .shop/work/i48/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q34
Accepted lines of the request:
- 1. **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids and terms of the proposal that the round's change list does not name.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3@0.29, supervision#r5@0.29, supervision#r16@0.29, supervision#r71@0.29, supervision#r77@0.29, supervision#r80@0.29, supervision#r92@0.29, supervision#r93@0.29, work-queue#r3@0.29, work-queue#r11@0.29, work-queue#r16@0.29, work-queue#r17@0.29, work-queue#r18@0.29, requests#r1@0.29, requests#r3@0.29, supervision#r99@0.29, supervision#r104@0.29, supervision#r112@0.29, supervision#r113@0.29, supervision#r114@0.29, review#r9@0.29, supervision#r125@0.29, supervision#r126@0.29, supervision#r127@0.29, design-model-check#r120@0.29, design-model-check#r121@0.29, requests#r26@0.29, requests#r27@0.29, requests#r35@0.29, requests#r36@0.29, requests#r37@0.29, requests#r38@0.29, spec-integration#r17@0.29, work-queue#r33@0.29, supervision#r137@0.29, supervision#r138@0.29, supervision#r139@0.29, supervision#r140@0.29, requests#r46@0.29, spec-consistency#r28@0.29, spec-integration#r47@0.29, spec-integration#r48@0.29, spec-integration#r49@0.29, spec-integration#r50@0.29, spec-integration#r51@0.29, spec-integration#r52@0.29, spec-integration#r53@0.29, requests#r47@0.29, requests#r48@0.29, supervision#r177@0.29, supervision#r178@0.29, supervision#r174@0.29, supervision#r175@0.29, supervision#r176@0.29, supervision#r181@0.29, supervision#r182@0.29, work-queue#r40@0.29, work-queue#r41@0.29, spec-integration#r57@0.29, supervision#r187@0.29, work-queue#r48@0.29, work-queue#r49@0.29, requests#r50@0.29, requests#r51@0.29, requests#r52@0.29, requests#r53@0.29, requests#r54@0.29, requests#r55@0.29, requests#r56@0.29, requests#r57@0.29, requests#r58@0.29, supervision#r184@0.29, supervision#r185@0.29, supervision#r186@0.29, work-queue#r47@0.29, requests#r49@0.29, supervision#r183@0.29, work-queue#r46@0.29, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35@0.29, migration-tools#r36@0.29, spec-integration#r56@0.29, work-queue#r42@0.29, work-queue#r43@0.29, work-queue#r44@0.29, work-queue#r45@0.29
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
